from enum import Enum

Collateral = "Collateral"


class Token(Enum):
    A = "TokenA"
    B = "TokenB"

    def complement(self):
        return Token.B if self == Token.A else Token.A
