from unittest import TestCase

from poly_market_maker.market import Token


class TestToken(TestCase):
    def test_token(self):
        self.assertEqual(Token.A.value, "TokenA")
        self.assertEqual(Token.B.value, "TokenB")

    def test_complement(self):
        self.assertEqual(Token.A.complement(), Token.B)
        self.assertEqual(Token.B.complement(), Token.A)
