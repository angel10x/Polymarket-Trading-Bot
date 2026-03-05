from enum import Enum
from py_clob_client.order_builder.constants import BUY, SELL

from poly_market_maker.market import Token


class Side(Enum):
    BUY = BUY
    SELL = SELL

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for side in Side:
                if value.lower() == side.value.lower():
                    return side
        return super()._missing_(value)


class Order:
    def __init__(self, size: float, price: float, side: Side, token: Token, id=None):
        if isinstance(size, int):
            size = float(size)

        assert isinstance(size, float)
        assert isinstance(price, float)
        assert isinstance(side, Side)
        assert isinstance(token, Token)
        if id is not None:
            assert isinstance(id, str)

        self.size = size
        self.price = price
        self.side = side
        self.token = token
        self.id = id

    def __repr__(self):
        return f"Order[id={self.id}, price={self.price}, size={self.size}, side={self.side.value}, token={self.token.value}]"
