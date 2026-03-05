from unittest import TestCase

from poly_market_maker.market import Market, Token

usdc_address = "0x2E8DCfE708D44ae2e406a1c02DFE2Fa13012f961"
condition_id = "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af"
token_id_0 = (
    1343197538147866997676250008839231694243646439454152539053893078719042421992
)
token_id_1 = (
    16678291189211314787145083999015737376658799626183230671758641503291735614088
)


class TestMarket(TestCase):
    market = Market(condition_id, usdc_address)

    def test_init_market(self):
        self.assertEqual(self.market.condition_id, condition_id)

        self.assertEqual(self.market.token_id(Token.A), token_id_0)
        self.assertEqual(self.market.token_id(Token.B), token_id_1)

        self.assertEqual(self.market.token(token_id_0), Token.A)
        self.assertEqual(self.market.token(token_id_1), Token.B)

        self.assertRaises(ValueError, self.market.token, 0)
