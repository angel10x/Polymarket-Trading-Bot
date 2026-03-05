from unittest import TestCase

from poly_market_maker.strategy import Strategy


class TestStrategy(TestCase):
    def test_strategy(self):
        strategy = Strategy.AMM
        self.assertEqual(strategy.value, "amm")

        strategy = Strategy("amm")
        self.assertEqual(strategy.value, "amm")

        self.assertRaises(ValueError, Strategy, "x")
