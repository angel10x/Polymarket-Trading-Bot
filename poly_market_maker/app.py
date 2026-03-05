import logging
import time

from prometheus_client import start_http_server

from poly_market_maker.args import get_args
from poly_market_maker.clob_api import ClobApi
from poly_market_maker.contracts import Contracts
from poly_market_maker.gas import GasStation, GasStrategy
from poly_market_maker.lifecycle import Lifecycle
from poly_market_maker.market import Market
from poly_market_maker.metrics import keeper_balance_amount
from poly_market_maker.order import Order, Side
from poly_market_maker.orderbook import OrderBookManager
from poly_market_maker.price_feed import PriceFeedClob
from poly_market_maker.strategy import StrategyManager
from poly_market_maker.token import Token, Collateral
from poly_market_maker.utils import setup_logging, setup_web3


class App:
    """Market maker keeper on Polymarket CLOB"""

    def __init__(self, args: list):
        setup_logging()
        self.logger = logging.getLogger(__name__)

        args = get_args(args)
        self.sync_interval = args.sync_interval

        # self.min_tick = args.min_tick
        # self.min_size = args.min_size

        # server to expose the metrics.
        self.metrics_server_port = args.metrics_server_port
        start_http_server(self.metrics_server_port)

        self.web3 = setup_web3(args.rpc_url, args.private_key)
        self.address = self.web3.eth.account.from_key(args.private_key).address

        self.clob_api = ClobApi(
            host=args.clob_api_url,
            chain_id=self.web3.eth.chain_id,
            private_key=args.private_key,
        )

        self.gas_station = GasStation(
            strat=GasStrategy(args.gas_strategy),
            w3=self.web3,
            url=args.gas_station_url,
            fixed=args.fixed_gas_price,
        )
        self.contracts = Contracts(self.web3, self.gas_station)

        self.market = Market(
            args.condition_id,
            self.clob_api.get_collateral_address(),
        )

        self.price_feed = PriceFeedClob(self.market, self.clob_api)

        self.order_book_manager = OrderBookManager(
            args.refresh_frequency, max_workers=1
        )
        self.order_book_manager.get_orders_with(self.get_orders)
        self.order_book_manager.get_balances_with(self.get_balances)
        self.order_book_manager.cancel_orders_with(
            lambda order: self.clob_api.cancel_order(order.id)
        )
        self.order_book_manager.place_orders_with(self.place_order)
        self.order_book_manager.cancel_all_orders_with(
            lambda _: self.clob_api.cancel_all_orders()
        )
        self.order_book_manager.start()

        self.strategy_manager = StrategyManager(
            args.strategy,
            args.strategy_config,
            self.price_feed,
            self.order_book_manager,
        )

        # Cache addresses used in get_balances (called at refresh_frequency)
        self._collateral_address: str | None = None
        self._conditional_address: str | None = None

    def main(self):
        """Run the keeper: startup, periodic sync, shutdown on exit."""
        self.logger.debug(self.sync_interval)
        with Lifecycle() as lifecycle:
            lifecycle.on_startup(self.startup)
            lifecycle.every(self.sync_interval, self.synchronize)
            lifecycle.on_shutdown(self.shutdown)

    def startup(self):
        self.logger.info("Running startup callback...")
        self.approve()
        time.sleep(5)  # 5 second initial delay so that bg threads fetch the orderbook
        self.logger.info("Startup complete!")

    def synchronize(self):
        """
        Synchronize the orderbook by cancelling orders out of bands and placing new orders if necessary
        """
        self.logger.debug("Synchronizing orderbook...")
        self.strategy_manager.synchronize()
        self.logger.debug("Synchronized orderbook!")

    def shutdown(self):
        """Shut down the keeper and cancel all orders."""
        self.logger.info("Keeper shutting down...")
        self.order_book_manager.cancel_all_orders()
        self.logger.info("Keeper is shut down!")

    def _balance_addresses(self) -> tuple[str, str]:
        """Cached collateral and conditional token addresses for balance/metrics."""
        if self._collateral_address is None:
            self._collateral_address = self.clob_api.get_collateral_address()
            self._conditional_address = self.clob_api.get_conditional_address()
        return self._collateral_address, self._conditional_address

    def get_balances(self) -> dict:
        """Fetch onchain balances of collateral and conditional tokens for the keeper."""
        self.logger.debug("Getting balances for address: %s", self.address)
        collateral_addr, conditional_addr = self._balance_addresses()
        token_id_a = self.market.token_id(Token.A)
        token_id_b = self.market.token_id(Token.B)

        collateral_balance = self.contracts.token_balance_of(
            collateral_addr, self.address
        )
        token_A_balance = self.contracts.token_balance_of(
            conditional_addr, self.address, token_id_a
        )
        token_B_balance = self.contracts.token_balance_of(
            conditional_addr, self.address, token_id_b
        )
        gas_balance = self.contracts.gas_balance(self.address)

        keeper_balance_amount.labels(
            accountaddress=self.address,
            assetaddress=collateral_addr,
            tokenid="-1",
        ).set(collateral_balance)
        keeper_balance_amount.labels(
            accountaddress=self.address,
            assetaddress=conditional_addr,
            tokenid=token_id_a,
        ).set(token_A_balance)
        keeper_balance_amount.labels(
            accountaddress=self.address,
            assetaddress=conditional_addr,
            tokenid=token_id_b,
        ).set(token_B_balance)
        keeper_balance_amount.labels(
            accountaddress=self.address,
            assetaddress="0x0",
            tokenid="-1",
        ).set(gas_balance)

        return {
            Collateral: collateral_balance,
            Token.A: token_A_balance,
            Token.B: token_B_balance,
        }

    def get_orders(self) -> list[Order]:
        """Fetch active orders from the CLOB for this market."""
        condition_id = self.market.condition_id
        orders = self.clob_api.get_orders(condition_id)
        return [
            Order(
                size=o["size"],
                price=o["price"],
                side=Side(o["side"]),
                token=self.market.token(o["token_id"]),
                id=o["id"],
            )
            for o in orders
        ]

    def place_order(self, new_order: Order) -> Order:
        """Place a single order on the CLOB; returns the same order with id set."""
        order_id = self.clob_api.place_order(
            price=new_order.price,
            size=new_order.size,
            side=new_order.side.value,
            token_id=self.market.token_id(new_order.token),
        )
        return Order(
            price=new_order.price,
            size=new_order.size,
            side=new_order.side,
            id=order_id,
            token=new_order.token,
        )

    def approve(self):
        """Approve the keeper on the collateral and conditional tokens."""
        collateral = self.clob_api.get_collateral_address()
        conditional = self.clob_api.get_conditional_address()
        exchange = self.clob_api.get_exchange()

        self.contracts.max_approve_erc20(collateral, self.address, exchange)
        self.contracts.max_approve_erc1155(conditional, self.address, exchange)
