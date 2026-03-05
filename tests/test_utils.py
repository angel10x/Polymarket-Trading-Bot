from unittest import TestCase

from poly_market_maker.utils import randomize_default_price


class TestUtils(TestCase):
    def test_randomize_default_price(self):
        price = 0.5
        randomized_price = randomize_default_price(price)
        # The randomized price is in the range: {price - 0.1, price + 0.1}
        upper_price_limit = price + 0.1
        lower_price_limit = price - 0.1
        self.assertTrue(lower_price_limit <= randomized_price <= upper_price_limit)
