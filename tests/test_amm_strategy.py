from re import M
from unittest import TestCase
import uuid

from poly_market_maker.market import Market
from poly_market_maker.token import Token, Collateral
from poly_market_maker.strategies.amm_strategy import AMMStrategy
from poly_market_maker.order import Order, Side


class OrderBook:
    def __init__(self):
        self.orders = []
        self.orders_being_placed = []
        self.orders_being_cancelled = []
        self.balances = {Token.A: 100, Token.B: 200, Collateral: 1000}


class OrderBookManager:
    def __init__(self):
        self.order_book = OrderBook()

    def get_order_book(self):
        return self.order_book

    def place_orders(self, orders):
        for order in orders:
            self.order_book.orders_being_placed += [
                Order(
                    size=order.size,
                    price=order.price,
                    token=order.token,
                    side=order.side,
                    id=str(uuid.uuid4()),
                )
            ]

    def cancel_orders(self, orders):
        self.order_book.orders_being_cancelled = orders

    def cancel_all_orders(self):
        self.order_book.orders_being_cancelled = [
            order for order in self.order_book.orders
        ]

    def update_orders(self):
        self.order_book.orders = list(
            set(self.order_book.orders)
            .union(set(self.order_book.orders_being_placed))
            .difference(set(self.order_book.orders_being_cancelled))
        )
        self.order_book.orders_being_placed = []
        self.order_book.orders_being_cancelled = []


class TestAMMStrategy(TestCase):
    usdc_address = "0x2E8DCfE708D44ae2e406a1c02DFE2Fa13012f961"
    condition_id = "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af"
    market = Market(condition_id, usdc_address)
    config = {
        "p_min": 0.05,
        "p_max": 0.95,
        "delta": 0.01,
        "spread": 0.01,
        "depth": 0.10,
        "max_collateral": 200.0,
    }
    strategy = AMMStrategy(config)

    # def test_synchronize(self):
    #     price_feed = PriceFeed(0.6, 0.4, self.market)
    #     order_book_manager = OrderBookManager()
    #     strategy = AMMStrategy(self.market, self.config)

    #     strategy.synchronize()
    #     order_book = order_book_manager.get_order_book()

    #     len_orders_being_placed = len(order_book.orders_being_placed)
    #     self.assertTrue(len_orders_being_placed > 0)
    #     self.assertTrue(len(order_book.orders_being_cancelled) == 0)

    def test_get_orders_to_cancel(self):
        order_book_manager = OrderBookManager()
        strategy = AMMStrategy(self.config)

        target_prices = {Token.A: 0.6, Token.B: 0.4}
        (orders_to_cancel, _) = strategy.get_orders(
            order_book_manager.get_order_book(), target_prices
        )

        self.assertEqual(orders_to_cancel, [])

        orders_placed = 10
        order_book_manager.place_orders(
            orders_placed * [Order(token=Token.A, price=0.1, size=15, side=Side.BUY)]
        )
        order_book_manager.update_orders()

        (orders_to_cancel, _) = strategy.get_orders(
            order_book_manager.get_order_book(), target_prices
        )

        self.assertEqual(len(orders_to_cancel), orders_placed)
