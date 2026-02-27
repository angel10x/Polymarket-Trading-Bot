"""Main copy-trader loop: poll positions and execute copy trades."""

import logging
import threading
import time
from concurrent.futures import as_completed, ThreadPoolExecutor
from pathlib import Path
from typing import Any

from ratelimit import limits, sleep_and_retry

from polymarket_copy_trader.config import load_config
from polymarket_copy_trader.constants import (
    MIN_POLL_INTERVAL_SECONDS,
    POLL_INTERVAL_SECONDS,
    RATE_LIMIT_PERIOD_SECONDS,
)
from polymarket_copy_trader.events import emit_task, get_ui_queue
from polymarket_copy_trader.market_activity import (
    aggregate_changes_by_market,
    log_market_activity,
    MarketActivityTracker,
)
from polymarket_copy_trader.positions import (
    fetch_positions_for_wallet,
    detect_position_changes,
)
from polymarket_copy_trader.trading import CopyTrader

logger = logging.getLogger(__name__)


def _setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def run(config_path: str | Path | None = None) -> None:
    """
    Load config, initialize state, and run the copy-trader loop until interrupted.

    Args:
        config_path: Optional path to config JSON. Defaults to config.json in cwd.
    """
    run_until_stopped(None, config_path)


def run_until_stopped(
    stop_event: threading.Event | None,
    config_path: str | Path | None = None,
) -> None:
    """
    Run the copy-trader loop until KeyboardInterrupt or stop_event is set.

    Args:
        stop_event: If set, the loop checks it each iteration and exits when set.
        config_path: Optional path to config file. Defaults to config.json in cwd.
    """
    config = load_config(config_path)
    wallets_to_track = config.get("wallets_to_track", [])
    rate_limit_calls = config.get("rate_limit", 25)
    poll_interval = max(
        MIN_POLL_INTERVAL_SECONDS,
        float(config.get("poll_interval", POLL_INTERVAL_SECONDS)),
    )

    if not wallets_to_track:
        logger.error("No wallets to track. Set wallets_to_track in config.")
        return

    copy_trader = CopyTrader(config)

    @sleep_and_retry
    @limits(calls=rate_limit_calls, period=RATE_LIMIT_PERIOD_SECONDS)
    def fetch_positions_ratelimited(wallet_address: str) -> list[dict[str, Any]] | None:
        return fetch_positions_for_wallet(wallet_address)

    logger.info("Initializing state for %d wallet(s)...", len(wallets_to_track))
    wallet_positions: dict[str, list[dict[str, Any]]] = {}
    market_trackers: dict[str, MarketActivityTracker] = {
        w: MarketActivityTracker() for w in wallets_to_track
    }
    for wallet in wallets_to_track:
        positions = fetch_positions_ratelimited(wallet)
        if positions is not None:
            wallet_positions[wallet] = positions
            logger.info(
                "Initialized %s... with %d position(s)",
                wallet[:8],
                len(positions),
            )

    logger.info("Copy trader loop started.")
    try:
        while stop_event is None or not stop_event.is_set():
            for wallet in wallets_to_track:
                if stop_event and stop_event.is_set():
                    break
                try:
                    current_positions = fetch_positions_ratelimited(wallet)
                    if current_positions is None:
                        continue

                    previous_positions = wallet_positions.get(wallet, [])
                    changes = detect_position_changes(
                        previous_positions, current_positions
                    )

                    if changes:
                        for change in changes:
                            logger.info(
                                "Detected %s for %s: %s shares of %s",
                                change["type"],
                                wallet[:8],
                                change["size"],
                                change.get("title"),
                            )
                            if get_ui_queue() is not None:
                                emit_task("his", change)
                        # Per-market summary: how much the copied trader bought/sold in each market
                        by_market = aggregate_changes_by_market(changes)
                        log_market_activity(by_market, wallet[:8])
                        if wallet in market_trackers:
                            market_trackers[wallet].update(changes)
                        # Execute all copy trades in parallel to reduce latency when
                        # the target submitted multiple tx in one block.
                        max_workers = min(len(changes), 8)
                        with ThreadPoolExecutor(max_workers=max_workers) as executor:
                            future_to_change = {
                                executor.submit(copy_trader.execute_trade, c): c
                                for c in changes
                            }
                            for future in as_completed(future_to_change):
                                change = future_to_change[future]
                                result = future.result()
                                if get_ui_queue() is not None:
                                    emit_task("mine", change, result)

                    wallet_positions[wallet] = current_positions

                except Exception as e:
                    logger.exception("Error tracking wallet %s: %s", wallet[:8], e)

            # Wait for poll_interval or until stop_event is set (so Ctrl+C stops quickly)
            if stop_event is not None:
                if stop_event.wait(timeout=poll_interval):
                    break
            else:
                time.sleep(poll_interval)

        logger.info("Copy trader stopped (stop event set).")
    except KeyboardInterrupt:
        logger.info("Copy trader stopped by user.")
    finally:
        for wallet in wallets_to_track:
            if wallet in market_trackers:
                market_trackers[wallet].log_totals(wallet[:8])


def main(config_path: str | Path | None = None) -> None:
    """Entry point: configure logging and run the copy trader."""
    _setup_logging()
    run(config_path=config_path)


if __name__ == "__main__":
    main()
