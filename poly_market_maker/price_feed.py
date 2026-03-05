from enum import Enum
import logging

from poly_market_maker.clob_api import ClobApi
from poly_market_maker.market import Market
from poly_market_maker.token import Token


class PriceFeedSource(Enum):
    CLOB = "clob"


class PriceFeed:
    """Market mid price resolvers"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_price(self) -> float:
        raise NotImplemented()


class PriceFeedClob(PriceFeed):
    """Resolves the prices from the clob"""

    def __init__(self, market: Market, clob_api: ClobApi):
        super().__init__()

        assert isinstance(market, Market)
        assert isinstance(clob_api, ClobApi)

        self.market = market
        self.clob_api = clob_api

    def get_price(self, token: Token) -> float:
        token_id = self.market.token_id(token)

        self.logger.debug("Fetching target price using the clob midpoint price...")
        target_price = self.clob_api.get_price(token_id)
        self.logger.debug(f"target_price: {target_price}")
        return target_price
