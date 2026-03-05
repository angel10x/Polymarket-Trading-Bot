from unittest import TestCase

from poly_market_maker.order import Side, Order
from poly_market_maker.token import Token

from poly_market_maker.strategies.amm_strategy import OrderType


class TestOrderType(TestCase):
    token = Token.A

    def test_eq(self):
        order_type_1 = OrderType(
            Order(size=0.1, side=Side.BUY, token=self.token, price=0.61)
        )
        order_type_2 = OrderType(
            Order(size=0.3, side=Side.BUY, token=self.token, price=0.61)
        )

        self.assertEqual(order_type_1, order_type_2)

    def test_set_membership(self):
        order_types = [
            OrderType(
                Order(
                    size=0.1,
                    side=Side.BUY,
                    token=self.token,
                    price=float(price),
                )
            )
            for price in range(45, 55, 1)
        ]

        order_type_in = OrderType(
            Order(size=0.3, side=Side.BUY, token=self.token, price=50.0)
        )
        order_type_not_in = OrderType(
            Order(size=0.3, side=Side.BUY, token=self.token, price=100.0)
        )
        self.assertTrue(order_type_in in set(order_types))
        self.assertTrue(order_type_not_in not in set(order_types))

    def test_not_in(self):
        order_types = [
            OrderType(
                Order(
                    size=1.0,
                    side=Side.BUY,
                    token=self.token,
                    price=float(price),
                )
            )
            for price in range(45, 55, 1)
        ]

        order_type = OrderType(
            Order(size=3.0, side=Side.BUY, token=self.token, price=57.0)
        )
        self.assertTrue(order_type not in set(order_types))
