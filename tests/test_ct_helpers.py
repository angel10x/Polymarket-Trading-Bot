from unittest import TestCase
from web3 import Web3

from poly_market_maker.ct_helpers import CTHelpers


class TestCTHelpers(TestCase):
    P = 21888242871839275222246405745257275088696311157297823662689037894645226208583

    """
    variables taken from a live market
    """

    def test_get_token_id_0(self):
        collateral_address = "0x7D1DC38E60930664F8cBF495dA6556ca091d2F92"
        condition_id = (
            "0xb69563b77dbad5dd82f54dc7ecc4c59fe1c7608e85ba759bf32ca4aebca845f0"
        )
        token_id_0 = 29010198852889164345666134995376491938579607903021308052828733253912957267646
        token_id_1 = 22125780403561061025829053926057155110588171618010034914848187335085907496192

        index_set = 2
        # ensure the odd flag is not set
        a = int.from_bytes(
            Web3.keccak(
                bytes.fromhex(condition_id[2:])
                + index_set.to_bytes(32, byteorder="big")
            ),
            byteorder="big",
        )

        # check the parity of the first msb
        odd = (a >> 255) != 0
        self.assertEqual(odd, False)

        self.assertEqual(
            CTHelpers.get_token_id(condition_id, collateral_address, 0), token_id_0
        )
        self.assertEqual(
            CTHelpers.get_token_id(condition_id, collateral_address, 1), token_id_1
        )

    """
    variables from ct_helpers.sol to ensure that the odd flag is used at least once
    """

    def test_get_token_id_1(self):
        collateral_address = "0x7D1DC38E60930664F8cBF495dA6556ca091d2F92"
        condition_id = (
            "0xda558eddf6eb57760bd5371fb313167f871d823a16e9d66fccb292baf2a117c0"
        )
        token_id_0 = 108051088633899060239124498527429950692254744883563327407154880807410490438693
        token_id_1 = 45163082656174410071592939534766820181648934703824597457997612898109272294349

        index_set = 2

        # ensure the odd flag is set
        a = int.from_bytes(
            Web3.keccak(
                bytes.fromhex(condition_id[2:])
                + index_set.to_bytes(32, byteorder="big")
            ),
            byteorder="big",
        )
        # check the parity of the first msb
        odd = (a >> 255) != 0
        self.assertEqual(odd, True)

        self.assertEqual(
            CTHelpers.get_token_id(condition_id, collateral_address, 0), token_id_0
        )
        self.assertEqual(
            CTHelpers.get_token_id(condition_id, collateral_address, 1), token_id_1
        )
