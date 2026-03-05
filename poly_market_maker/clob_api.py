import logging
import sys
import time
from py_clob_client.client import ClobClient, ApiCreds, OrderArgs, FilterParams
from py_clob_client.exceptions import PolyApiException

from poly_market_maker.utils import randomize_default_price
from poly_market_maker.constants import OK
from poly_market_maker.metrics import clob_requests_latency

DEFAULT_PRICE = 0.5


class ClobApi:
    def __init__(self, host, chain_id, private_key):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.client = self._init_client_L1(
            host=host,
            chain_id=chain_id,
            private_key=private_key,
        )

        try:
            api_creds = self.client.derive_api_key()
            self.logger.debug(f"Api key found: {api_creds.api_key}")
        except PolyApiException:
            self.logger.debug("Api key not found. Creating a new one...")
            api_creds = self.client.create_api_key()
            self.logger.debug(f"Api key created: {api_creds.api_key}.")

        self.client = self._init_client_L2(
            host=host,
            chain_id=chain_id,
            private_key=private_key,
            creds=api_creds,
        )

    def get_address(self):
        return self.client.get_address()

    def get_collateral_address(self):
        return self.client.get_collateral_address()

    def get_conditional_address(self):
        return self.client.get_conditional_address()

    def get_exchange(self, neg_risk = False):
        return self.client.get_exchange_address(neg_risk)

    def get_price(self, token_id: int) -> float:
        """
        Get the current price on the orderbook
        """
        self.logger.debug("Fetching midpoint price from the API...")
        start_time = time.time()
        try:
            resp = self.client.get_midpoint(token_id)
            clob_requests_latency.labels(method="get_midpoint", status="ok").observe(
                (time.time() - start_time)
            )
            if resp.get("mid") is not None:
                return float(resp.get("mid"))
        except Exception as e:
            self.logger.error(f"Error fetching current price from the CLOB API: {e}")
            clob_requests_latency.labels(method="get_midpoint", status="error").observe(
                (time.time() - start_time)
            )

        return self._rand_price()

    def _rand_price(self) -> float:
        price = randomize_default_price(DEFAULT_PRICE)
        self.logger.info(
            f"Could not fetch price from CLOB API, returning random price: {price}"
        )
        return price

    def get_orders(self, condition_id: str):
        """
        Get open keeper orders on the orderbook
        """
        self.logger.debug("Fetching open keeper orders from the API...")
        start_time = time.time()
        try:
            resp = self.client.get_orders(FilterParams(market=condition_id))
            clob_requests_latency.labels(method="get_orders", status="ok").observe(
                (time.time() - start_time)
            )

            return [self._get_order(order) for order in resp]
        except Exception as e:
            self.logger.error(
                f"Error fetching keeper open orders from the CLOB API: {e}"
            )
            clob_requests_latency.labels(method="get_orders", status="error").observe(
                (time.time() - start_time)
            )
        return []

    def place_order(self, price: float, size: float, side: str, token_id: int) -> str:
        """
        Places a new order
        """
        self.logger.info(
            f"Placing a new order: Order[price={price},size={size},side={side},token_id={token_id}]"
        )
        start_time = time.time()
        try:
            resp = self.client.create_and_post_order(
                OrderArgs(price=price, size=size, side=side, token_id=token_id)
            )
            clob_requests_latency.labels(
                method="create_and_post_order", status="ok"
            ).observe((time.time() - start_time))
            order_id = None
            if resp and resp.get("success") and resp.get("orderID"):
                order_id = resp.get("orderID")
                self.logger.info(
                    f"Succesfully placed new order: Order[id={order_id},price={price},size={size},side={side},tokenID={token_id}]!"
                )
                return order_id

            err_msg = resp.get("errorMsg")
            self.logger.error(
                f"Could not place new order! CLOB returned error: {err_msg}"
            )
        except Exception as e:
            self.logger.error(f"Request exception: failed placing new order: {e}")
            clob_requests_latency.labels(
                method="create_and_post_order", status="error"
            ).observe((time.time() - start_time))
        return None

    def cancel_order(self, order_id) -> bool:
        self.logger.info(f"Cancelling order {order_id}...")
        if order_id is None:
            self.logger.debug("Invalid order_id")
            return True

        start_time = time.time()
        try:
            resp = self.client.cancel(order_id)
            clob_requests_latency.labels(method="cancel", status="ok").observe(
                (time.time() - start_time)
            )
            return resp == OK
        except Exception as e:
            self.logger.error(f"Error cancelling order: {order_id}: {e}")
            clob_requests_latency.labels(method="cancel", status="error").observe(
                (time.time() - start_time)
            )
        return False

    def cancel_all_orders(self) -> bool:
        self.logger.info("Cancelling all open keeper orders..")
        start_time = time.time()
        try:
            resp = self.client.cancel_all()
            clob_requests_latency.labels(method="cancel_all", status="ok").observe(
                (time.time() - start_time)
            )
            return resp == OK
        except Exception as e:
            self.logger.error(f"Error cancelling all orders: {e}")
            clob_requests_latency.labels(method="cancel_all", status="error").observe(
                (time.time() - start_time)
            )
        return False

    def _init_client_L1(
        self,
        host,
        chain_id,
        private_key,
    ) -> ClobClient:
        clob_client = ClobClient(host, chain_id, private_key)
        try:
            if clob_client.get_ok() == OK:
                self.logger.info("Connected to CLOB API!")
                self.logger.info(
                    "CLOB Keeper address: {}".format(clob_client.get_address())
                )
                return clob_client
        except:
            self.logger.error("Unable to connect to CLOB API, shutting down!")
            sys.exit(1)

    def _init_client_L2(
        self, host, chain_id, private_key, creds: ApiCreds
    ) -> ClobClient:
        clob_client = ClobClient(host, chain_id, private_key, creds)
        try:
            if clob_client.get_ok() == OK:
                self.logger.info("Connected to CLOB API!")
                self.logger.info(
                    "CLOB Keeper address: {}".format(clob_client.get_address())
                )
                return clob_client
        except:
            self.logger.error("Unable to connect to CLOB API, shutting down!")
            sys.exit(1)

    def _get_order(self, order_dict: dict) -> dict:
        size = float(order_dict.get("original_size")) - float(
            order_dict.get("size_matched")
        )
        price = float(order_dict.get("price"))
        side = order_dict.get("side")
        order_id = order_dict.get("id")
        token_id = int(order_dict.get("asset_id"))

        return {
            "size": size,
            "price": price,
            "side": side,
            "token_id": token_id,
            "id": order_id,
        }
