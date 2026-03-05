import logging
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, wait

from poly_market_maker.order import Order, Side


class OrderBook:
    """Represents the current snapshot of the order book.

    Attributes:
        -orders: Current list of active orders.
        -balances: Current balances state.
        -orders_being_placed: `True` if at least one order is currently being placed. `False` otherwise.
        -orders_being_cancelled: `True` if at least one orders is currently being cancelled. `False` otherwise.
    """

    def __init__(
        self,
        orders: list[Order],
        balances: dict,
        orders_being_placed: bool,
        orders_being_cancelled: bool,
    ):
        assert isinstance(orders_being_placed, bool)
        assert isinstance(orders_being_cancelled, bool)

        self.orders = orders
        self.balances = balances
        self.orders_being_placed = orders_being_placed
        self.orders_being_cancelled = orders_being_cancelled


class OrderBookManager:
    """Tracks state of the order book without constantly querying it.

    Attributes:
        refresh_frequency: Frequency (in seconds) of how often background order book (and balances)
            refresh takes place.
    """

    def __init__(self, refresh_frequency: int, max_workers: int = 5):
        self.logger = logging.getLogger(self.__class__.__name__)

        assert isinstance(refresh_frequency, int)
        assert isinstance(max_workers, int)

        self.refresh_frequency = refresh_frequency
        self.get_orders_function = None
        self.get_balances_function = None
        self.place_order_function = None
        self.cancel_order_function = None
        self.cancel_all_orders_function = None
        self.on_update_function = None

        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._lock = threading.Lock()
        self._state = None
        self._refresh_count = 0
        self._currently_placing_orders = 0
        self._orders_placed = list()
        self._order_ids_cancelling = set()
        self._order_ids_cancelled = set()

    def get_orders_with(self, get_orders_function: Callable[[], list[Order]]):
        """
        Configures the function used to fetch active keeper orders.
        """
        assert callable(get_orders_function)

        self.get_orders_function = get_orders_function

    def get_balances_with(self, get_balances_function: Callable):
        """
        Configures the (optional) function used to fetch current keeper balances.
        Args:
            get_balances_function: The function which will be periodically called by the order book manager
                in order to get current keeper balances. This is optional, is not configured balances
                will not be fetched.
        """
        assert callable(get_balances_function)

        self.get_balances_function = get_balances_function

    def place_orders_with(self, place_order_function: Callable):
        """
        Configures the function used to place orders.
        Args:
            place_order_function: The function which will be called in order to place new orders.
        """
        assert callable(place_order_function)

        self.place_order_function = place_order_function

    def cancel_orders_with(self, cancel_order_function: Callable):
        """
        Configures the function used to cancel orders.
        Args:
            cancel_order_function: The function which will be called in order to cancel orders.
        """
        assert callable(cancel_order_function)

        self.cancel_order_function = cancel_order_function

    def cancel_all_orders_with(self, cancel_all_orders_function: Callable):
        """
        Configures the function used to cancel all keeper orders.
        Args:
            cancel_all_orders_function: The function which will be called in order to cancel orders.
        """
        assert callable(cancel_all_orders_function)

        self.cancel_all_orders_function = cancel_all_orders_function

    def on_update(self, on_update_function: Callable):
        assert callable(on_update_function)

        self.on_update_function = on_update_function

    def start(self):
        """Start the background refresh of active keeper orders."""
        threading.Thread(target=self._thread_refresh_order_book, daemon=True).start()

    def get_order_book(self) -> OrderBook:
        """
        Returns the current snapshot of the active keeper orders and balances.
        """
        while self._state is None:
            self.logger.info("Waiting for the order book to become available...")
            time.sleep(0.5)

        with self._lock:
            self.logger.debug("Getting the order book...")
            if self._state.get("orders") is not None:
                self.logger.debug(
                    f"Orders retrieved last time: {[order.id for order in self._state['orders']]}"
                )
            self.logger.debug(
                f"Orders placed since then: {[order.id for order in self._orders_placed]}"
            )
            self.logger.debug(
                f"Orders cancelled since then: {[order_id for order_id in self._order_ids_cancelled]}"
            )
            self.logger.debug(
                f"Orders being cancelled: {[order_id for order_id in self._order_ids_cancelling]}"
            )
            self.logger.debug(
                f"Orders being placed: {self._currently_placing_orders} order(s)"
            )

            orders = []

            # Add orders which have been placed if they exist
            if self._state.get("orders") is not None:
                orders = list(self._state["orders"])
                for order in self._orders_placed:
                    if order.id not in list(map(lambda order: order.id, orders)):
                        orders.append(order)

                # Remove orders being cancelled and already cancelled.
                orders = list(
                    filter(
                        lambda order: order.id not in self._order_ids_cancelling
                        and order.id not in self._order_ids_cancelled,
                        orders,
                    )
                )

                self.logger.debug(
                    f"Open keeper orders: {[order.id for order in orders]}"
                )

        return OrderBook(
            orders=orders,
            balances=self._state["balances"],
            orders_being_placed=self._currently_placing_orders > 0,
            orders_being_cancelled=len(self._order_ids_cancelling) > 0,
        )

    def place_order(self, place_order_function: Callable[[Order], Order], order: Order):
        """Places new order. Order placement will happen in a background thread.

        Args:
            place_order_function: Function used to place the order.
        """
        assert callable(place_order_function)

        with self._lock:
            self._currently_placing_orders += 1

        self._report_order_book_updated()

        result = self._executor.submit(
            self._thread_place_order(place_order_function, order)
        )
        wait([result])

    def place_orders(self, orders: list[Order]):
        """Places new orders. Order placement will happen in a background thread.

        Args:
            new_orders: List of new orders to place.
        """
        assert isinstance(orders, list)
        assert callable(self.place_order_function)

        with self._lock:
            self._currently_placing_orders += len(orders)

        self._report_order_book_updated()

        results = [
            self._executor.submit(
                self._thread_place_order(self.place_order_function, order)
            )
            for order in orders
        ]
        wait(results)

    def cancel_orders(self, orders: list[Order]):
        """
        Cancels existing orders. Order cancellation will happen in a background thread.

        Args:
            orders: List of orders to cancel.
        """
        self.logger.info("Cancelling orders...")
        assert isinstance(orders, list)
        assert callable(self.cancel_order_function)

        with self._lock:
            for order in orders:
                self._order_ids_cancelling.add(order.id)

        self._report_order_book_updated()

        results = [
            self._executor.submit(
                self._thread_cancel_order(self.cancel_order_function, order)
            )
            for order in orders
        ]
        wait(results)

    def cancel_all_orders(self):
        """
        Cancels all existing orders
        """
        while True:
            orders = self.get_order_book().orders
            if len(orders) == 0:
                self.logger.info("No open orders on order book.")
                break
            order_ids = [order.id for order in orders]
            with self._lock:
                for order_id in order_ids:
                    self._order_ids_cancelling.add(order_id)

            self.logger.info(f"Cancelling {len(order_ids)} open orders...")

            # Cancel all orders
            result = self._executor.submit(
                self._thread_cancel_all_orders(self.cancel_all_orders_function, orders)
            )
            wait([result])
            self.wait_for_stable_order_book()
            time.sleep(2)

        # Wait for the background thread to refresh the order book twice, so we are 99.9% sure
        # that there are no orders left in the backend.
        #
        # The reason we wait twice for the order book refresh is that the first refresh might have
        # started still while the orders were still being cancelled. By waiting twice we are sure that the
        # second refresh has started after the whole order cancellation process was already finished.
        self.logger.info(
            "No open orders. Waiting for the order book to refresh twice just to be sure..."
        )
        self.wait_for_order_book_refresh()
        self.wait_for_order_book_refresh()

        orders = self.get_order_book().orders
        if len(orders) > 0:
            # TODO: not repeating the cancel_all since it could lead to an infinite recursion
            # self.logger.info(f"There are still {len(orders)} open orders! Repeating the cancel_all_orders function!")
            # return self.cancel_all_orders()
            self.logger.info(f"There are still {len(orders)} open keeper orders!")
            return

        self.logger.info("All orders successfully cancelled!")

    def wait_for_order_cancellation(self):
        """Wait until no background order cancellation takes place."""
        while len(self._order_ids_cancelling) > 0:
            time.sleep(0.1)

    def wait_for_order_book_refresh(self):
        """Wait until at least one background order book refresh happens since now."""
        with self._lock:
            old_counter = self._refresh_count

        while True:
            with self._lock:
                new_counter = self._refresh_count

            if new_counter > old_counter:
                break

            time.sleep(0.1)

    def wait_for_stable_order_book(self):
        """Wait until no background order placement nor cancellation takes place."""
        while True:
            order_book = self.get_order_book()
            if (
                not order_book.orders_being_cancelled
                and not order_book.orders_being_placed
            ):
                break
            time.sleep(0.1)

    def _report_order_book_updated(self):
        if self.on_update_function is not None:
            self.on_update_function()

    def _run_get_orders(self):
        try:
            orders = self.get_orders_function()
            return orders
        except Exception as e:
            self.logger.error(f"Exception fetching orderbook! Error: {e}")
            return None

    def _run_get_balances(self):
        try:
            balances = (
                self.get_balances_function()
                if self.get_balances_function is not None
                else None
            )
            self.logger.debug(f"Balances: {balances}")
            return balances
        except Exception as e:
            self.logger.error(f"Exception fetching onchain balances! Error: {e}")
            return None

    def _thread_refresh_order_book(self):
        while True:
            try:
                with self._lock:
                    orders_already_cancelled_before = set(self._order_ids_cancelled)
                    orders_already_placed_before = set(self._orders_placed)

                # get orders
                orders = self._run_get_orders()

                # get balances
                balances = self._run_get_balances()

                with self._lock:
                    self._order_ids_cancelled = (
                        self._order_ids_cancelled - orders_already_cancelled_before
                    )
                    for order in orders_already_placed_before:
                        self._orders_placed.remove(order)

                    if self._state is None:
                        self.logger.info("Order book became available")

                    # Issue: RPC endpoints are sometimes unreliable and fetching the onchain balances for the keeper sometimes
                    # fails. This kills the whole refresh orderbook process which is clearly undesirable.
                    # Fix should be to ensure the process doesn't fail if any specific internal function fails
                    if self._state is None:
                        self._state = {}

                    if orders is not None:
                        # If either the orderbook or balance check fails, the state stays as it was before the refresh
                        self._state["orders"] = orders
                    if balances is not None:
                        self._state["balances"] = balances
                    # self._state = {'orders': orders, 'balances': balances}
                    self._refresh_count += 1

                self._report_order_book_updated()

                self.logger.debug(
                    f"Fetched the order book"
                    f" (orders: {[order.id for order in orders]}, "
                    f" buys: {len([order for order in orders if order.side == Side.BUY])}, "
                    f" sells: {len([order for order in orders if order.side == Side.SELL])})"
                )
            except ValueError as e:
                self.logger.error(f"Failed to fetch the order book or balances ({e})!")

            time.sleep(self.refresh_frequency)

    def _thread_place_order(
        self, place_order_function: Callable[[Order], Order], order: Order
    ):
        assert callable(place_order_function)

        def func():
            try:
                new_order = place_order_function(order)

                if new_order is not None:
                    with self._lock:
                        self._orders_placed.append(new_order)
            except BaseException as exception:
                self.logger.exception(exception)
            finally:
                with self._lock:
                    self._currently_placing_orders -= 1
                self._report_order_book_updated()

        return func

    def _thread_cancel_order(
        self, cancel_order_function: Callable[[Order], None], order: Order
    ):
        assert callable(cancel_order_function)

        def func():
            order_id = order.id
            try:
                if cancel_order_function(order):
                    with self._lock:
                        self._order_ids_cancelled.add(order_id)
                        self._order_ids_cancelling.remove(order_id)
            except BaseException as e:
                self.logger.exception(f"Failed to cancel {order_id}")
                self.logger.exception(f"Exception: {e}")
            finally:
                with self._lock:
                    try:
                        self._order_ids_cancelling.remove(order_id)
                    except KeyError:
                        pass
                self._report_order_book_updated()

        return func

    def _thread_cancel_all_orders(
        self,
        cancel_all_orders_function: Callable[[list[Order]], bool],
        orders: list[Order],
    ):
        assert callable(cancel_all_orders_function)

        def func():
            order_ids = [order.id for order in orders]
            try:
                if cancel_all_orders_function(orders):
                    with self._lock:
                        for order_id in order_ids:
                            self._order_ids_cancelled.add(order_id)
                            self._order_ids_cancelling.remove(order_id)
            except BaseException:
                self.logger.exception("Failed to cancel all")
            finally:
                with self._lock:
                    for order_id in order_ids:
                        try:
                            self._order_ids_cancelling.remove(order_id)
                        except KeyError:
                            pass
                self._report_order_book_updated()

        return func
