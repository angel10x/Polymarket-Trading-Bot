import enum
import math
import web3
import requests
import logging
import time

from poly_market_maker.metrics import gas_station_latency

DEFAULT_FIXED_GAS_PRICE = 100000000000


class GasStrategy(enum.Enum):
    FIXED = "fixed"
    STATION = "station"
    WEB3 = "web3"


class GasStation:
    def __init__(
        self,
        strat=GasStrategy.STATION,
        w3: web3.Web3 = None,
        url: str = None,
        fixed=DEFAULT_FIXED_GAS_PRICE,
    ):
        self.strat = self._get_gas_strategy(w3, url, strat)
        self.w3 = w3
        self.url = url
        self.fixed = int(fixed) if fixed else DEFAULT_FIXED_GAS_PRICE
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_gas_price(self) -> int:
        """
        Get gas price
        """
        self.logger.info(f"Using gas price strategy: {self.strat.value.upper()}...")
        gas = None
        start_time = time.time()

        try:
            if self.strat == GasStrategy.FIXED:
                gas = self.fixed

            if self.strat == GasStrategy.WEB3:
                rpc_gas_price = self.w3.eth.generate_gas_price()
                gas = rpc_gas_price

            if self.strat == GasStrategy.STATION:
                gas_station_gas_price = self._get_gas_station_gas()
                gas = gas_station_gas_price

            gas_station_latency.labels(strategy=self.strat.value, status="ok").observe(
                (time.time() - start_time)
            )

            self.logger.info(f"Gas: {gas}")
        except Exception as e:
            self.logger.error(
                f"Error fetching gas from gas station, strategy: {self.strat.value.upper()}: {e}"
            )
            gas_station_latency.labels(
                strategy=self.strat.value, status="error"
            ).observe((time.time() - start_time))

        return gas

    def _get_gas_strategy(self, w3, url, user_given_strat):
        # if the user provided a strategy, use that directly
        if user_given_strat:
            return user_given_strat

        if url:
            return GasStrategy.STATION

        if w3:
            return GasStrategy.WEB3

        return GasStrategy.FIXED

    def _get_rpc_gas_price(self):
        try:
            gas = self.w3.eth.generate_gas_price()
            # Round up to avoid transaction underpriced errors
            return math.ceil(gas / (10**9)) * (10**9)
        except:
            self.logger.error(
                f"Error fetching gas from web3, returning configured fixed gas price: {self.fixed}"
            )
            return self.fixed

    def _get_gas_station_gas(self):
        try:
            resp = requests.get(self.url)
            resp_json = resp.json()

            # Always fast
            gas = resp_json.get("fast")
            return math.ceil(gas) * (10**9)
        except:
            self.logger.error(
                f"Error fetching gas from gasstation, returning configured fixed gas price: {self.fixed}"
            )
            return self.fixed
