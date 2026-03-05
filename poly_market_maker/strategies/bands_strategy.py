from poly_market_maker.token import Token, Collateral
from poly_market_maker.order import Order, Side
from poly_market_maker.orderbook import OrderBook

from poly_market_maker.strategies.bands import Bands
from poly_market_maker.strategies.base_strategy import BaseStrategy


class BandsStrategy(BaseStrategy):
    def __init__(
        self,
        config: dict,
    ):
        assert isinstance(config, dict)

        super().__init__()
        try:
            self.bands = Bands(config.get("bands"))
        except Exception as e:
            self.logger.exception(
                f"Config is invalid ({e}). Treating the config as if it has no bands."
            )

    def get_orders(self, orderbook: OrderBook, target_prices):
        """
        Synchronize the orderbook by cancelling orders out of bands and placing new orders if necessary
        """
        orders_to_place = []
        orders_to_cancel = []

        for token in Token:
            self.logger.debug(f"{token.value} target price: {target_prices[token]}")

        # cancel orders
        for token in Token:
            orders = self._orders_by_corresponding_buy_token(orderbook.orders, token)
            orders_to_cancel += self.bands.cancellable_orders(
                orders, target_prices[token]
            )

        # remaining open orders
        open_orders = list(set(orders) - set(orders_to_cancel))
        balance_locked_by_open_buys = sum(
            order.size * order.price for order in open_orders if order.side == Side.BUY
        )
        self.logger.debug(f"Collateral locked by buys: {balance_locked_by_open_buys}")

        free_collateral_balance = (
            orderbook.balances[Collateral] - balance_locked_by_open_buys
        )
        self.logger.debug(f"Free collateral balance: {free_collateral_balance}")

        # place orders
        for token in Token:
            orders = self._orders_by_corresponding_buy_token(orderbook.orders, token)

            balance_locked_by_open_sells = sum(
                order.size for order in orders if order.side == Side.SELL
            )
            self.logger.debug(
                f"{token.complement().value} locked by sells: {balance_locked_by_open_sells}"
            )

            free_token_balance = (
                orderbook.balances[token.complement()] - balance_locked_by_open_sells
            )
            self.logger.debug(
                f"Free {token.complement().value} balance: {free_token_balance}"
            )

            new_orders = self.bands.new_orders(
                orders,
                free_collateral_balance,
                free_token_balance,
                target_prices[token],
                token,
            )
            free_collateral_balance -= sum(
                order.size * order.price
                for order in new_orders
                if order.side == Side.BUY
            )
            orders_to_place += new_orders

        return (orders_to_cancel, orders_to_place)

    def _orders_by_corresponding_buy_token(self, orders: list[Order], buy_token: Token):
        return list(
            filter(
                lambda order: self._filter_by_corresponding_buy_token(order, buy_token),
                orders,
            )
        )

    def _filter_by_corresponding_buy_token(self, order: Order, buy_token: Token):
        return (order.side == Side.BUY and order.token == buy_token) or (
            order.side == Side.SELL and order.token != buy_token
        )
