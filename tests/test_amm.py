from unittest import TestCase

from poly_market_maker.token import Token
from poly_market_maker.strategies.amm import AMM, AMMConfig


class TestAMM(TestCase):
    token = Token.A
    config = AMMConfig(
        p_min=0.05, p_max=0.95, delta=0.01, depth=0.1, spread=0.05, max_collateral=200.0
    )

    def test_get_buy_orders(self):
        p = 0.5
        amm = AMM(self.token, self.config)

        amm.set_price(p)
        expected_number_of_orders = (
            int(100 * (self.config.depth - self.config.spread)) + 1
        )

        buy_orders = amm.get_buy_orders(1000)
        self.assertEqual(expected_number_of_orders, len(buy_orders))

        sell_orders = amm.get_sell_orders(1000)
        self.assertEqual(expected_number_of_orders, len(sell_orders))

    def test_get_sell_size(self):
        p = 0.5
        size = 1000

        amm = AMM(self.token, self.config)

        sell_size = amm._sell_size(size, p, self.config.p_max, self.config.p_max)
        self.assertEqual(sell_size, size)

    def test_get_buy_size(self):
        p = 0.5
        collateral = 1000

        amm = AMM(self.token, self.config)

        buy_size = amm._buy_size(collateral, p, self.config.p_min, self.config.p_min)
        self.assertLess(buy_size * self.config.p_min, collateral)
        self.assertGreater(buy_size * p, collateral)

    def test_set_price(self):
        p = 0.5

        amm = AMM(self.token, self.config)
        amm.set_price(p)

        (buy_prices, sell_prices) = (amm.buy_prices, amm.sell_prices)
        self.assertEqual(amm.p_l, 0.40)
        self.assertEqual(buy_prices, [0.45, 0.44, 0.43, 0.42, 0.41, 0.40])

        self.assertEqual(amm.p_u, 0.6)
        # self.assertEqual(sell_prices[0], p + self.config.spread)
        # consider converting all internal units to decimal
        self.assertEqual(
            sell_prices,
            [0.55, 0.56, 0.57, 0.58, 0.59, 0.60],
        )
