from web3 import Web3


class CTHelpers:
    P = 21888242871839275222246405745257275088696311157297823662689037894645226208583

    @classmethod
    def get_token_id(
        cls, condition_id: str, collateral_address: str, token_index: int
    ) -> int:
        index_set = 1 << token_index
        collection_id = cls.get_collection_id(condition_id, index_set)
        return cls.get_position_id(collateral_address, collection_id)

    @classmethod
    def get_collection_id(cls, condition_id: str, index_set: int) -> str:
        assert isinstance(condition_id, str)
        assert isinstance(index_set, int)

        x1 = cls.get_x1(condition_id, index_set)
        # check the parity of the first msb
        odd = (x1 >> 255) == 1
        a = x1 % cls.P

        while True:
            a += 1
            yy = pow(a, 3, cls.P) + 3 % cls.P
            # check if yy is a square mod P
            # https://en.wikipedia.org/wiki/Euler%27s_criterion
            if pow(yy, cls.P - 1 >> 1, cls.P) == 1:
                break

        if odd:
            # set the second msb
            a += 1 << 254

        # pad to 64 hex chars + '0x'
        return "{0:#0{1}x}".format(a, 66)

    @staticmethod
    def get_x1(condition_id: str, index_set: int):
        return int.from_bytes(
            Web3.keccak(
                bytes.fromhex(condition_id[2:])
                + index_set.to_bytes(32, byteorder="big")
            ),
            byteorder="big",
        )

    @staticmethod
    def get_position_id(collateral_address: str, collection_id: str) -> int:
        assert isinstance(collateral_address, str)
        assert isinstance(collection_id, str)

        return int.from_bytes(
            Web3.keccak(
                bytes.fromhex(collateral_address[2:]) + bytes.fromhex(collection_id[2:])
            ),
            byteorder="big",
        )
