import logging
import signal
import threading
import time


class AsyncCallback:
    """
    Invokes callback logic in a separate thread
    Forked and modified from pymaker's AsyncCallback: https://github.com/makerdao/pymaker/blob/master/pymaker/util.py#L100
    Attributes:
        callback: The callback function to be invoked in a separate thread.
    """

    def __init__(self, callback):
        self.callback = callback
        self.thread = None

    def trigger(self, on_start=None, on_finish=None) -> bool:
        """Invokes the callback in a separate thread, unless one is already running.

        If callback isn't currently running, invokes it in a separate thread and returns `True`.
        If the previous callback invocation still hasn't finished, doesn't do anything
        and returns `False`.

        Arguments:
            on_start: Optional method to be called before the actual callback. Can be `None`.
            on_finish: Optional method to be called after the actual callback. Can be `None`.

        Returns:
            `True` if callback has been invoked, or if it invocation attempt failed.
            `False` if the previous callback invocation still hasn't finished.
        """
        if self.thread is None or not self.thread.is_alive():

            def thread_target():
                if on_start is not None:
                    on_start()
                self.callback()
                if on_finish is not None:
                    on_finish()

            self.thread = threading.Thread(target=thread_target)

            try:
                self.thread.start()
            except Exception as e:
                self.thread = None

                logging.critical(f"Failed to start the async callback thread ({e})")
            return True
        else:
            return False

    def wait(self):
        """Waits for the currently running callback to finish.

        If the callback isn't running or hasn't even been invoked once, returns instantly.
        """
        if self.thread is not None:
            self.thread.join()


class Lifecycle:
    """
    Keeper lifecycle controller
    Forked and modified from pymaker's Lifecycle: https://github.com/makerdao/pymaker/blob/master/pymaker/lifecycle.py
    Usage:
        with Lifecycle() as lifecycle:
            lifecycle.on_startup(self.some_startup_function)
            lifecycle.every(15, self.do_something_else)
            lifecycle.on_shutdown(self.some_shutdown_function)
    Note: this version will only listen to timers, instead of per block events for simplicity
    """

    def __init__(self, delay=0):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.delay = delay
        self.wait_for_functions = []
        self.startup_function = None
        self.shutdown_function = None
        self.every_timers = []

        self.terminated_internally = False
        self.terminated_externally = False
        self.fatal_termination = False
        self._at_least_one_every = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Initialization phase
        self.logger.info("Initializing keeper lifecycle...")

        # Initial delay
        if self.delay > 0:
            self.logger.info(f"Waiting for {self.delay} seconds of initial delay...")
            time.sleep(self.delay)

        # Initial checks
        if len(self.wait_for_functions) > 0:
            self.logger.info("Waiting for initial checks to pass...")

            for index, (wait_for_function, max_wait) in enumerate(
                self.wait_for_functions, start=1
            ):
                start_time = time.time()
                while True:
                    try:
                        result = wait_for_function()
                    except Exception as e:
                        self.logger.exception(
                            f"Initial check #{index} failed with an exception: '{e}'"
                        )
                        result = False

                    if result:
                        break

                    if time.time() - start_time >= max_wait:
                        self.logger.warning(
                            f"Initial check #{index} took more than {max_wait} seconds to pass, skipping"
                        )
                        break

                    time.sleep(0.1)

        # Startup phase
        if self.startup_function:
            self.logger.info("Executing keeper startup logic...")
            self.startup_function()

        # Bind `on_block`, bind `every`
        # Enter the main loop
        self._start_every_timers()
        self._main_loop()

        # Enter shutdown process
        self.logger.info("Shutting down the keeper")

        # If any every (timer) callback is still running, wait for it to terminate
        if len(self.every_timers) > 0:
            self.logger.info("Waiting for outstanding timers to terminate...")
            for timer in self.every_timers:
                timer[1].wait()

        # Shutdown phase
        if self.shutdown_function:
            self.logger.info("Executing keeper shutdown logic...")
            self.shutdown_function()
            self.logger.info("Shutdown logic finished")
        self.logger.info("Keeper terminated")
        exit(10 if self.fatal_termination else 0)

    def initial_delay(self, initial_delay: int):
        """
        Set the initial delay
        Args:
            initial_delay: Initial delay on keeper startup (in seconds).
        """
        assert isinstance(initial_delay, int)

        self.delay = initial_delay

    def wait_for(self, initial_check, max_wait: int):
        """
        Make the keeper wait for the function to turn true before startup.

        The primary use case is to allow background threads to have a chance to pull necessary
        information like prices, gas prices etc. At the same time we may not want to wait indefinitely
        for that information to become available as the price source may be down etc.

        Args:
            initial_check: Function which will be evaluated and its result compared to True.
            max_wait: Maximum waiting time (in seconds).
        """
        assert callable(initial_check)
        assert isinstance(max_wait, int)

        self.wait_for_functions.append((initial_check, max_wait))

    def on_startup(self, callback):
        """Register the specified callback to be run on keeper startup.

        Args:
            callback: Function to be called on keeper startup.
        """
        assert callable(callback)

        assert self.startup_function is None
        self.startup_function = callback

    def on_shutdown(self, callback):
        """Register the specified callback to be run on keeper shutdown.

        Args:
            callback: Function to be called on keeper shutdown.
        """
        assert callable(callback)

        assert self.shutdown_function is None
        self.shutdown_function = callback

    def terminate(self, message=None):
        if message is not None:
            self.logger.warning(message)

        self.terminated_internally = True

    def every(self, frequency_in_seconds: int, callback):
        """Register the specified callback to be called by a timer.

        Args:
            frequency_in_seconds: Execution frequency (in seconds).
            callback: Function to be called by the timer.
        """
        self.every_timers.append((frequency_in_seconds, AsyncCallback(callback)))

    def _sigint_sigterm_handler(self, sig, frame):
        if self.terminated_externally:
            self.logger.warning(
                "Graceful keeper termination due to SIGINT/SIGTERM already in progress"
            )
        else:
            self.logger.warning(
                "Keeper received SIGINT/SIGTERM signal, will terminate gracefully"
            )
            self.terminated_externally = True

    def _start_thread_safely(self, t: threading.Thread):
        delay = 10

        while True:
            try:
                t.start()
                break
            except Exception as e:
                self.logger.critical(
                    f"Failed to start a thread ({e}), trying again in {delay} seconds"
                )
                time.sleep(delay)

    def _start_every_timers(self):
        for idx, timer in enumerate(self.every_timers, start=1):
            self._start_every_timer(idx, timer[0], timer[1])

        if len(self.every_timers) > 0:
            self.logger.info(f"Started {len(self.every_timers)} timer(s)")

    def _start_every_timer(self, idx: int, frequency_in_seconds: int, callback):
        def setup_timer(delay):
            timer = threading.Timer(delay, func)
            timer.daemon = True

            self._start_thread_safely(timer)

        def func():
            try:
                if (
                    not self.terminated_internally
                    and not self.terminated_externally
                    and not self.fatal_termination
                ):

                    def on_start():
                        self.logger.debug(f"Processing the timer #{idx}")

                    def on_finish():
                        self.logger.debug(f"Finished processing the timer #{idx}")

                    if not callback.trigger(on_start, on_finish):
                        self.logger.debug(
                            f"Ignoring timer #{idx} as previous one is already running"
                        )
                else:
                    self.logger.debug(
                        f"Ignoring timer #{idx} as keeper is already terminating"
                    )
            except:
                setup_timer(frequency_in_seconds)
                raise
            setup_timer(frequency_in_seconds)

        setup_timer(1)
        self._at_least_one_every = True

    def _main_loop(self):
        # terminate gracefully on either SIGINT or SIGTERM
        signal.signal(signal.SIGINT, self._sigint_sigterm_handler)
        signal.signal(signal.SIGTERM, self._sigint_sigterm_handler)

        while self._at_least_one_every:
            time.sleep(1)

            # if the keeper logic asked us to terminate, we do so
            if self.terminated_internally:
                self.logger.warning(
                    "Keeper logic asked for termination, the keeper will terminate"
                )
                break

            # if SIGINT/SIGTERM asked us to terminate, we do so
            if self.terminated_externally:
                self.logger.warning(
                    "The keeper is terminating due do SIGINT/SIGTERM signal received"
                )
                break
