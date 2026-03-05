import json
from unittest import TestCase

from poly_market_maker.token import Token
from poly_market_maker.order import Order, Side

from poly_market_maker.strategies.bands import Band, Bands

test_bands_config = {
    "bands": [
        {
            "minMargin": 0.02,
            "avgMargin": 0.03,
            "maxMargin": 0.04,
            "minAmount": 10.0,
            "avgAmount": 20.0,
            "maxAmount": 50.0,
        },
        {
            "minMargin": 0.04,
            "avgMargin": 0.05,
            "maxMargin": 0.06,
            "minAmount": 20.0,
            "avgAmount": 30.0,
            "maxAmount": 40.0,
        },
    ]
}


class TestBand(TestCase):
    token = Token.A

    def test_create_band(self):
        test_band = Band(
            *list(
                {
                    "minMargin": 0.01,
                    "avgMargin": 0.02,
                    "maxMargin": 0.03,
                    "minAmount": 20.0,
                    "avgAmount": 30.0,
                    "maxAmount": 40.0,
                }.values()
            )
        )

        self.assertEqual(test_band.min_margin, 0.01)
        self.assertEqual(test_band.avg_margin, 0.02)
        self.assertEqual(test_band.max_margin, 0.03)
        self.assertEqual(test_band.min_amount, 20.0)
        self.assertEqual(test_band.avg_amount, 30.0)
        self.assertEqual(test_band.max_amount, 40.0)

    def test_excessive_orders(self):
        # Given the below buy band with a target_price of 0.5
        # meaning we should have orders at least minMargin away from the target_price
        # and at most maxMargin away from the target_price
        # Band is from {0.495 : 0.40 }
        test_band = Band(
            *list(
                {
                    "minMargin": 0.01,
                    "avgMargin": 0.10,
                    "maxMargin": 0.20,
                    "minAmount": 1.0,
                    "avgAmount": 10.0,
                    "maxAmount": 50.0,
                }.values()
            )
        )
        orders = [
            Order(size=10, price=0.48, side=Side.BUY, token=self.token),
            Order(size=20, price=0.45, side=Side.BUY, token=self.token),
            Order(size=30, price=0.42, side=Side.BUY, token=self.token),
        ]

        # with a target_price of fifty cents
        target_price = 0.50

        # with no orders, nothing gets canceled
        self.assertEqual(
            len(test_band.excessive_orders([], target_price, True, True)), 0
        )

        # Total order size > maxAmount so we need to cancel some orders
        # since there is only 1 band, we cancel orders closest to the target price as those are the most "at risk"
        scheduled_to_be_canceled = test_band.excessive_orders(
            orders, target_price, True, True
        )
        self.assertEqual(len(scheduled_to_be_canceled), 1)
        self.assertEqual(scheduled_to_be_canceled.pop(), orders[0])

        # If there were multiple bands, we'd cancel orders furthest from the target price, as those are least likely to get hit
        scheduled_to_be_canceled = test_band.excessive_orders(
            orders, target_price, False, True
        )
        self.assertEqual(len(scheduled_to_be_canceled), 1)
        self.assertEqual(scheduled_to_be_canceled.pop(), orders[2])

    def test_create_bands(self):
        test_bands = Bands(test_bands_config.get("bands"))
        self.assertIsNotNone(test_bands)
        self.assertEqual(len(test_bands.bands), 2)

    def test_bands_cancellable_orders(self):
        test_bands = Bands(test_bands_config.get("bands"))

        # Initialize buys and sells that fit in both bands
        target_price = 0.50
        orders = [
            Order(size=20, price=0.47, side=Side.BUY, token=self.token),
            Order(size=30, price=0.44, side=Side.BUY, token=self.token),
            Order(size=20, price=0.53, side=Side.SELL, token=self.token),
            Order(size=30, price=0.56, side=Side.SELL, token=self.token),
        ]

        # Expect none to be cancelled
        self.assertEqual(len(test_bands.cancellable_orders(orders, target_price)), 2)

        # Say price moves to 80c
        target_price = 0.80

        # All 4 orders are now cancellable
        self.assertEqual(len(test_bands.cancellable_orders(orders, target_price)), 4)

    def test_bands_new_orders_usdc_only(self):
        test_bands = Bands(test_bands_config.get("bands"))

        # Given the following balances:
        target_price = 0.5
        keeper_usdc_balance = 100.0
        keeper_token_balance = 0.0

        # and the following existing orders:
        existing_orders = [
            Order(size=5, price=0.48, side=Side.BUY, token=self.token),
        ]

        # place new orders
        new_orders = test_bands.new_orders(
            existing_orders,
            keeper_usdc_balance,
            keeper_token_balance,
            target_price,
            self.token,
        )

        new_buys = [o for o in new_orders if o.side == Side.BUY]
        new_sells = [o for o in new_orders if o.side == Side.SELL]

        # no new sells, bc we have no tokens
        self.assertEqual(len(new_sells), 0)

        # new buys in band 1 to bring amount to avgAmount
        self.assertEqual(new_buys[0].size, 15.0)
        self.assertEqual(new_buys[0].price, 0.47)

        # new buys in band 2 to bring amount to avgAmount
        self.assertEqual(new_buys[1].size, 30.0)
        self.assertEqual(new_buys[1].price, 0.45)

    def test_bands_new_orders_token_only(self):
        test_bands = Bands(test_bands_config.get("bands"))

        # Given the following balances:
        target_price = 0.5
        keeper_usdc_balance = 100.0
        keeper_token_balance = 100.0

        # and the following existing orders:
        existing_orders = [
            Order(size=5, price=0.48, side=Side.BUY, token=self.token),
        ]

        # place new orders
        new_orders = test_bands.new_orders(
            existing_orders,
            keeper_usdc_balance,
            keeper_token_balance,
            target_price,
            self.token,
        )

        new_buys = [o for o in new_orders if o.side == Side.BUY]
        new_sells = [o for o in new_orders if o.side == Side.SELL]

        # no new buys, bc we could achieve avgAmount with tokens only
        self.assertEqual(len(new_buys), 0)

        # new sells in band 1 to bring amount to avgAmount
        self.assertEqual(new_sells[0].size, 15.0)
        self.assertEqual(new_sells[0].price, 0.53)

        # new sells in band 2 to bring amount to avgAmount
        self.assertEqual(new_sells[1].size, 30.0)
        self.assertEqual(new_sells[1].price, 0.55)

    def test_bands_new_orders_mixed(self):
        test_bands = Bands(test_bands_config.get("bands"))

        # Given the following balances:
        target_price = 0.5
        keeper_usdc_balance = 30.0
        keeper_token_balance = 30.0

        # and the following existing orders:
        existing_orders = [
            Order(size=5, price=0.48, side=Side.BUY, token=self.token),
        ]

        # place new orders
        new_orders = test_bands.new_orders(
            existing_orders,
            keeper_usdc_balance,
            keeper_token_balance,
            target_price,
            self.token,
        )

        new_buys = [o for o in new_orders if o.side == Side.BUY]
        new_sells = [o for o in new_orders if o.side == Side.SELL]

        # new sells in band 1 to bring amount to avgAmount
        self.assertEqual(new_sells[0].size, 15.0)
        self.assertEqual(new_sells[0].price, 0.53)

        # new sells in band 2 to bring amount to avgAmount
        self.assertEqual(new_sells[1].size, 15.0)
        self.assertEqual(new_sells[1].price, 0.55)

        self.assertEqual(new_buys[0].size, 15.0)
        self.assertEqual(new_buys[0].price, 0.45)

    def test_bands_new_orders_mixed_and_limited(self):
        test_bands = Bands(test_bands_config.get("bands"))

        # Given the following balances:
        target_price = 0.5
        keeper_usdc_balance = 100.0
        keeper_token_balance = 30.0

        # and the following existing orders:
        existing_orders = [
            Order(size=5, price=0.48, side=Side.BUY, token=self.token),
        ]

        # place new orders
        new_orders = test_bands.new_orders(
            existing_orders,
            keeper_usdc_balance,
            keeper_token_balance,
            target_price,
            self.token,
        )

        new_buys = [o for o in new_orders if o.side == Side.BUY]
        new_sells = [o for o in new_orders if o.side == Side.SELL]

        # new sells in band 1 to bring amount to avgAmount
        self.assertEqual(new_sells[0].size, 15.0)
        self.assertEqual(new_sells[0].price, 0.53)

        # new sells in band 2 to use the rest of token balance
        # note that we don't have enough to get to avgAmount
        self.assertEqual(new_sells[1].size, 15.0)
        self.assertEqual(new_sells[1].price, 0.55)

        # we place buy order with size 15 to get to avgAmount = 30
        self.assertEqual(new_buys[0].size, 15.0)
        self.assertEqual(new_buys[0].price, 0.45)

    def test_virtual_bands_orders(self):
        # load bands with margins that are very close together
        # without adjustment all orders would be at same price

        test_bands = Bands(test_bands_config.get("bands"))

        target_price = 0.04

        # confirm adjustments are made to spread orders to neighboring ticks
        virtual_bands = test_bands._calculate_virtual_bands(target_price)

        self.assertEqual(len(virtual_bands), 1)
        self.assertEqual(virtual_bands[0].min_margin, 0.02)
        self.assertEqual(virtual_bands[0].avg_margin, 0.03)
        self.assertEqual(virtual_bands[0].max_margin, 0.04)

    # def test_tight_bands_cancellable_and_new_orders(self):
    #     with open("./tests/tight_bands.json") as fh:
    #         test_bands = Bands.read(json.load(fh))

    #     # Initialize buys and sells that fit in two of 3 adjusted bands on each side
    #     target_price = 0.50
    #     buys = [
    #         Order(size=100, price=0.49, side=Side.BUY),
    #         Order(size=100, price=0.48, side=Side.BUY),
    #     ]
    #     sells = [
    #         Order(size=100, price=0.51, side=Side.SELL),
    #         Order(size=100, price=0.52, side=Side.SELL),
    #     ]

    #     # Expect none to be cancelled
    #     self.assertEqual(
    #         len(test_bands.cancellable_orders(buys, sells, target_price)), 0
    #     )

    #     # Expect two to need to be created
    #     keeper_usdc_balance = 500.0
    #     keeper_yes_balance = 500.0

    #     new_orders = test_bands.new_orders(
    #         buys,
    #         sells,
    #         keeper_usdc_balance,
    #         keeper_yes_balance,
    #         target_price,
    #     )

    #     self.assertEqual(len(new_orders), 2)

    #     self.assertEqual(new_orders[0].price, 0.47)
    #     self.assertEqual(new_orders[0].side, BUY)

    #     self.assertEqual(new_orders[1].price, 0.53)
    #     self.assertEqual(new_orders[1].side, SELL)

    #     # Say price moves to 80c
    #     target_price = 0.80

    #     # All 4 orders are now cancellable
    #     self.assertEqual(
    #         len(test_bands.cancellable_orders(buys, sells, target_price)), 4
    #     )

    #     # Expect six to need to be created
    #     new_orders = test_bands.new_orders(
    #         [],
    #         [],
    #         keeper_usdc_balance,
    #         keeper_yes_balance,
    #         target_price,
    #     )

    #     self.assertEqual(len(new_orders), 6)

    #     self.assertEqual(new_orders[0].price, 0.79)
    #     self.assertEqual(new_orders[0].side, BUY)

    #     self.assertEqual(new_orders[1].price, 0.78)
    #     self.assertEqual(new_orders[1].side, BUY)

    #     self.assertEqual(new_orders[2].price, 0.77)
    #     self.assertEqual(new_orders[2].side, BUY)

    #     self.assertEqual(new_orders[3].price, 0.81)
    #     self.assertEqual(new_orders[3].side, SELL)

    #     self.assertEqual(new_orders[4].price, 0.82)
    #     self.assertEqual(new_orders[4].side, SELL)

    #     self.assertEqual(new_orders[5].price, 0.83)
    #     self.assertEqual(new_orders[5].side, SELL)

    # def test_cant_create_order_over_dollar_or_under_zero(self):
    #     with open("./tests/tight_bands.json") as fh:
    #         test_bands = Bands.read(json.load(fh))

    #     target_price = 1.0
    #     new_asks = test_bands._new_sell_orders([], 500.0, target_price)

    #     # shouldn't be any valid asks because they would all be over 1.0
    #     self.assertEqual(len(new_asks), 0)

    #     target_price = 0.0
    #     new_asks = test_bands._new_buy_orders([], 500.0, target_price)

    #     # shouldn't be any valid bids because they would all be under 0.0
    #     self.assertEqual(len(new_asks), 0)

    # def test_order_size_limit(self):
    #     band = Band(
    #         {
    #             "minMargin": 0.005,
    #             "avgMargin": 0.01,
    #             "maxMargin": 0.02,
    #             "minAmount": 5.0,
    #             "avgAmount": 10.0,
    #             "maxAmount": 15.0,
    #         }
    #     )

    #     test_bands = Bands(bands=[band])

    #     # Given the following balances:
    #     target_price = 0.5
    #     keeper_usdc_balance = 100.0
    #     keeper_yes_balance = 100.0

    #     # and the following existing orders (none):
    #     existing_buys = []
    #     existing_sells = []

    #     # place new orders
    #     new_orders = test_bands.new_orders(
    #         existing_buys,
    #         existing_sells,
    #         keeper_usdc_balance,
    #         keeper_yes_balance,
    #         target_price,
    #     )

    #     self.assertEqual(len(new_orders), 0)

    # def test_loose_bands(self):
    #     buy_bands = [
    #         Band(
    #             {
    #                 "minMargin": 0.03,
    #                 "avgMargin": 0.05,
    #                 "maxMargin": 0.07,
    #                 "minAmount": 30.0,
    #                 "avgAmount": 50.0,
    #                 "maxAmount": 100.0,
    #             }
    #         ),
    #         Band(
    #             {
    #                 "minMargin": 0.07,
    #                 "avgMargin": 0.09,
    #                 "maxMargin": 0.11,
    #                 "minAmount": 50.0,
    #                 "avgAmount": 75.0,
    #                 "maxAmount": 120.0,
    #             }
    #         ),
    #         Band(
    #             {
    #                 "minMargin": 0.11,
    #                 "avgMargin": 0.13,
    #                 "maxMargin": 0.15,
    #                 "minAmount": 75.0,
    #                 "avgAmount": 100.0,
    #                 "maxAmount": 150.0,
    #             }
    #         ),
    #         Band(
    #             {
    #                 "minMargin": 0.15,
    #                 "avgMargin": 0.17,
    #                 "maxMargin": 0.19,
    #                 "minAmount": 100.0,
    #                 "avgAmount": 100.0,
    #                 "maxAmount": 200.0,
    #             }
    #         ),
    #     ]

    #     sell_bands = [
    #         Band(
    #             {
    #                 "minMargin": 0.03,
    #                 "avgMargin": 0.05,
    #                 "maxMargin": 0.07,
    #                 "minAmount": 30.0,
    #                 "avgAmount": 50.0,
    #                 "maxAmount": 100.0,
    #             }
    #         ),
    #         Band(
    #             {
    #                 "minMargin": 0.07,
    #                 "avgMargin": 0.09,
    #                 "maxMargin": 0.11,
    #                 "minAmount": 50.0,
    #                 "avgAmount": 75.0,
    #                 "maxAmount": 120.0,
    #             }
    #         ),
    #         Band(
    #             {
    #                 "minMargin": 0.11,
    #                 "avgMargin": 0.13,
    #                 "maxMargin": 0.15,
    #                 "minAmount": 75.0,
    #                 "avgAmount": 100.0,
    #                 "maxAmount": 150.0,
    #             }
    #         ),
    #         Band(
    #             {
    #                 "minMargin": 0.15,
    #                 "avgMargin": 0.17,
    #                 "maxMargin": 0.19,
    #                 "minAmount": 100.0,
    #                 "avgAmount": 100.0,
    #                 "maxAmount": 200.0,
    #             }
    #         ),
    #     ]

    #     test_bands = Bands(buy_bands, sell_bands)

    #     # Given the following balances:
    #     target_price = 0.6416888120654723
    #     keeper_usdc_balance = 1000.0
    #     keeper_yes_balance = 1000.0

    #     # and the following existing orders (none):
    #     existing_buys = []
    #     existing_sells = []

    #     # place new orders
    #     new_orders = test_bands.new_orders(
    #         existing_buys,
    #         existing_sells,
    #         keeper_usdc_balance,
    #         keeper_yes_balance,
    #         target_price,
    #     )
    #     print(new_orders)

    #     self.assertEqual(len(new_orders), 8)

    #     buys = [o for o in new_orders if o.side == BUY]
    #     sells = [o for o in new_orders if o.side == SELL]

    #     self.assertEqual(
    #         len(test_bands.cancellable_orders(buys, sells, target_price)), 0
    #     )
