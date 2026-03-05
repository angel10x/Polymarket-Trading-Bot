from unittest import TestCase

from poly_market_maker.strategies.amm import AMMManager, AMMConfig
from poly_market_maker.order import Side
from poly_market_maker.token import Token, Collateral


class TestAMMManager(TestCase):
    balances = {Token.A: 1000, Token.B: 1000, Collateral: 1000}
    config = AMMConfig(
        p_min=0.05,
        p_max=0.95,
        delta=0.01,
        spread=0.01,
        depth=0.05,
        max_collateral=200.0,
    )

    def test_get_expected_order_prices(self):
        amm_manager = AMMManager(self.config)

        target_prices = {Token.A: 0.4, Token.B: 0.6}
        orders = amm_manager.get_expected_orders(target_prices, self.balances)
        self.assertTrue(len(orders) > 0)

        sell_orders = [order for order in orders if order.side == Side.SELL]
        buy_orders = [order for order in orders if order.side == Side.BUY]

        sell_orders_a = [order for order in sell_orders if order.token == Token.A]
        sell_orders_b = [order for order in sell_orders if order.token == Token.B]
        buy_orders_a = [order for order in buy_orders if order.token == Token.A]
        buy_orders_b = [order for order in buy_orders if order.token == Token.B]

        sell_prices_a = [order.price for order in sell_orders_a]
        self.assertEqual(sell_prices_a, [0.41, 0.42, 0.43, 0.44, 0.45])
        sell_prices_b = [order.price for order in sell_orders_b]
        self.assertEqual(sell_prices_b, [0.61, 0.62, 0.63, 0.64, 0.65])

        buy_prices_a = [order.price for order in buy_orders_a]
        self.assertEqual(buy_prices_a, [0.39, 0.38, 0.37, 0.36, 0.35])
        buy_prices_b = [order.price for order in buy_orders_b]
        self.assertEqual(buy_prices_b, [0.59, 0.58, 0.57, 0.56, 0.55])

    def test_get_expected_order_sizes(self):
        amm_manager = AMMManager(self.config)

        target_prices = {Token.A: 0.5, Token.B: 0.5}
        orders = amm_manager.get_expected_orders(target_prices, self.balances)

        sell_orders = [order for order in orders if order.side == Side.SELL]
        buy_orders = [order for order in orders if order.side == Side.BUY]

        sell_orders_a = [order for order in sell_orders if order.token == Token.A]
        sell_orders_b = [order for order in sell_orders if order.token == Token.B]
        buy_orders_a = [order for order in buy_orders if order.token == Token.A]
        buy_orders_b = [order for order in buy_orders if order.token == Token.B]

        sell_sizes_a = [order.size for order in sell_orders_a]
        for i in range(len(sell_sizes_a) - 1):
            self.assertGreater(sell_sizes_a[i], sell_sizes_a[i + 1])

        self.assertLessEqual(sum(sell_sizes_a), self.balances[Token.A])

        sell_sizes_b = [order.size for order in sell_orders_b]
        for i in range(len(sell_sizes_b) - 1):
            self.assertGreater(sell_sizes_b[i], sell_sizes_b[i + 1])

        self.assertLessEqual(sum(sell_sizes_b), self.balances[Token.B])

        buy_sizes_a = [order.size for order in buy_orders_a]
        print(buy_sizes_a)
        for i in range(len(buy_sizes_a) - 1):
            self.assertLess(buy_sizes_a[i], buy_sizes_a[i + 1])

        net_cost_a = sum(order.price * order.size for order in buy_orders_a)
        net_cost_b = sum(order.price * order.size for order in buy_orders_b)
        self.assertLessEqual(net_cost_a + net_cost_b, self.balances[Collateral])

    # def test_get_expected_orders(self):
    #     amm_manager = AMMManager(self.config)

    #     target_prices = {Token.A: 0.5, Token.B: 0.5}
    #     orders = amm_manager.get_expected_orders(target_prices, self.balances)
