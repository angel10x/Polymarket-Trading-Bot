import itertools
import logging

from poly_market_maker.token import Token
from poly_market_maker.constants import MIN_TICK, MIN_SIZE, MAX_DECIMALS
from poly_market_maker.order import Order, Side


class Band:
    def __init__(
        self,
        min_margin: float,
        avg_margin: float,
        max_margin: float,
        min_amount: float,
        avg_amount: float,
        max_amount: float,
    ):
        self.logger = logging.getLogger(self.__class__.__name__)

        assert isinstance(min_margin, float)
        assert isinstance(avg_margin, float)
        assert isinstance(max_margin, float)
        assert isinstance(min_amount, float)
        assert isinstance(avg_amount, float)
        assert isinstance(max_amount, float)

        self.min_margin = min_margin
        self.avg_margin = avg_margin
        self.max_margin = max_margin
        self.min_amount = min_amount
        self.avg_amount = avg_amount
        self.max_amount = max_amount

        assert self.min_amount >= float(0)
        assert self.avg_amount >= float(0)
        assert self.max_amount >= float(0)
        assert self.min_amount <= self.avg_amount
        assert self.avg_amount <= self.max_amount

        assert self.min_margin <= self.avg_margin
        assert self.avg_margin <= self.max_margin
        assert self.min_margin < self.max_margin

    def excessive_orders(
        self,
        orders: list[Order],
        target_price: float,
        is_first_band: bool,
        is_last_band: bool,
    ) -> list[Order]:
        """Return orders which need to be cancelled to bring the total order amount in the band below maximum."""
        self.logger.debug("Running excessive orders.")
        # Get all orders which are currently present in the band.
        orders_in_band = [
            order for order in orders if self.includes(order, target_price)
        ]
        orders_total_size = sum(order.size for order in orders_in_band)

        # The sorting in which we remove orders depends on which band we are in.
        # * In the first band we start cancelling with orders closest to the target price.
        # * In the last band we start cancelling with orders furthest from the target price.
        # * In remaining cases we remove orders starting from the smallest one.

        def price_sorting(order):
            return abs(order.price - target_price)

        def size_sorting(order):
            return order.size

        if is_first_band:
            sorting = price_sorting
            reverse = True
        elif is_last_band:
            sorting = price_sorting
            reverse = False
        else:
            sorting = size_sorting
            reverse = False

        orders_in_band = sorted(orders_in_band, key=sorting, reverse=reverse)
        orders_for_cancellation = []
        band_amount = sum(order.size for order in orders_in_band)

        while band_amount > self.max_amount:
            order = orders_in_band.pop()
            orders_for_cancellation.append(order)
            band_amount -= order.size

        if len(orders_for_cancellation) > 0:
            self.logger.info(
                f"Band (spread <{self.min_margin}, {self.max_margin}>,"
                f" amount <{self.min_amount}, {self.max_amount}>) has amount {orders_total_size}, scheduling"
                f" {len(orders_for_cancellation)} order(s) for cancellation: {', '.join(map(lambda order: '#' + str(order.id), orders_for_cancellation))}"
            )

        return orders_for_cancellation

    def includes(self, order: Order, target_price: float) -> bool:
        if order.side == Side.BUY:
            price = order.price
        else:
            # round to 6 decimals to avoid floating point issues
            price = round(1 - order.price, MAX_DECIMALS)

        return (price > self.min_price(target_price)) and (
            price <= self.max_price(target_price)
        )

    @staticmethod
    def _apply_margin(price: float, margin: float) -> float:
        return round(price - margin, MAX_DECIMALS)

    def min_price(self, target_price: float) -> float:
        return self._apply_margin(target_price, self.max_margin)

    def buy_price(self, target_price: float) -> float:
        return self._apply_margin(target_price, self.avg_margin)

    def sell_price(self, target_price: float) -> float:
        return self._apply_margin(1 - target_price, -self.avg_margin)

    def max_price(self, target_price: float) -> float:
        return self._apply_margin(target_price, self.min_margin)

    def __repr__(self):
        return f"Band[spread<{self.min_margin}, {self.max_margin}>, amount<{self.min_amount}, {self.max_amount}>]"

    def __str__(self):
        return self.__repr__()


class Bands:
    def __init__(self, bands_from_config: list[dict]):
        self.logger = logging.getLogger(self.__class__.__name__)
        assert isinstance(bands_from_config, list)

        try:
            self.bands = [Band(*list(band.values())) for band in bands_from_config]

        except Exception as e:
            logging.getLogger().exception(
                f"Config is invalid ({e}). Treating the config as if it has no bands."
            )

            self.bands = []

        if self._bands_overlap(self.bands):
            self.logger.error("Bands in the config overlap!")
            raise Exception("Bands in the config overlap!")

    def _calculate_virtual_bands(self, target_price: float) -> list[Band]:
        if target_price <= 0.0:
            return []

        virtual_bands = []
        # increase avg_price if necessary
        # any bands with max_price <= 0 will not be used
        for band in self.bands:
            if band.max_price(target_price) > 0:
                if band.buy_price(target_price) <= 0:
                    band.avg_margin = target_price - MIN_TICK
                virtual_bands.append(band)
        return virtual_bands

    def _excessive_orders(
        self, orders: list[Order], bands: list[Band], target_price: float
    ) -> list[Order]:
        """Return orders which need to be cancelled to bring total amounts within all bands below maximums."""
        assert isinstance(orders, list)
        assert isinstance(bands, list)
        assert isinstance(target_price, float)

        for band in bands:
            for order in band.excessive_orders(
                orders,
                target_price,
                band == bands[0],  # is first
                band == bands[-1],  # is last
            ):
                yield order

    def _outside_any_band_orders(
        self, orders: list[Order], bands: list[Band], target_price: float
    ) -> list[Order]:
        """Return buy or sell orders which need to be cancelled as they do not fall into any buy or sell band."""
        assert isinstance(orders, list)
        assert isinstance(bands, list)
        assert isinstance(target_price, float)

        for order in orders:
            if not any(band.includes(order, target_price) for band in bands):
                self.logger.info(
                    f"Order #{order.id} doesn't belong to any band, scheduling it for cancellation"
                )
                yield order

    def cancellable_orders(self, orders: list, target_price: float) -> list:
        assert isinstance(orders, list)
        assert isinstance(target_price, float)

        if target_price is None:
            self.logger.debug("Cancelling all orders as no price is available.")
            orders_to_cancel = orders

        else:
            orders_to_cancel = list(
                itertools.chain(
                    self._excessive_orders(
                        orders,
                        self._calculate_virtual_bands(target_price),
                        target_price,
                    ),
                    self._outside_any_band_orders(
                        orders,
                        self._calculate_virtual_bands(target_price),
                        target_price,
                    ),
                )
            )

        return orders_to_cancel

    def new_orders(
        self,
        orders: list[Order],
        collateral_balance: float,
        token_balance: float,
        target_price: float,
        buy_token: Token,
    ) -> list[Order]:
        assert isinstance(orders, list)
        assert isinstance(collateral_balance, float)
        assert isinstance(target_price, float)

        sell_token = buy_token.complement()
        new_orders = []
        for band in self._calculate_virtual_bands(target_price):
            band_amount = sum(
                order.size for order in orders if band.includes(order, target_price)
            )

            self.logger.debug(f"{band} has existing amount {band_amount},")

            if band_amount < band.min_amount:
                # sell
                sell_price = band.sell_price(target_price)

                sell_size = round(
                    min(band.avg_amount - band_amount, token_balance),
                    MAX_DECIMALS,
                )
                sell_order = self._new_order(
                    sell_price, sell_size, Side.SELL, sell_token
                )

                if sell_order is not None:
                    band_amount += sell_size
                    token_balance -= sell_size
                    new_orders.append(sell_order)

                if band_amount < band.avg_amount:
                    # buy
                    buy_price = band.buy_price(target_price)
                    buy_size = round(
                        min(
                            band.avg_amount - band_amount,
                            collateral_balance / buy_price,
                        ),
                        MAX_DECIMALS,
                    )
                    buy_order = self._new_order(
                        buy_price, buy_size, Side.BUY, buy_token
                    )

                    if buy_order is not None:
                        band_amount += buy_size
                        collateral_balance -= buy_size * buy_price
                        new_orders.append(buy_order)

        return new_orders

    def _new_order(self, price: float, size: float, side: Side, token: Token) -> Order:
        """
        Return sell orders which need to be placed to bring total amounts within all sell bands above minimums
        """

        if not self._new_order_is_valid(price, size):
            return None

        self.logger.debug(
            f"Creating new {side} order with price {price} and size: {size}"
        )

        return Order(price=price, size=size, side=side, token=token)

    @staticmethod
    def _new_order_is_valid(price, size):
        return (price > float(0)) and (price < float(1.0)) and (size >= MIN_SIZE)

    @staticmethod
    def _bands_overlap(bands: list[Band]):
        def two_bands_overlap(band1: Band, band2: Band):
            return (
                band1.min_margin < band2.max_margin
                and band2.min_margin < band1.max_margin
            )

        for band1 in bands:
            if (
                len(
                    list(
                        filter(
                            lambda band2: two_bands_overlap(band1, band2),
                            bands,
                        )
                    )
                )
                > 1
            ):
                return True
        return False
