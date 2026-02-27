"""Copy-trade execution via Polymarket (pmxt)."""

import logging
import threading
from typing import Any

import pmxt

from polymarket_copy_trader.config import get_env_credentials, validate_credentials_for_trading
from polymarket_copy_trader.constants import DEFAULT_ORDER_FEE_BPS, SIGNATURE_TYPE

logger = logging.getLogger(__name__)


class CopyTrader:
    """
    Executes copy trades on Polymarket based on detected position changes.
    Thread-safe for parallel execution; caches market_id by slug to reduce latency.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        self._copy_percentage = float(config.get("copy_percentage", 1.0))
        self._trading_enabled = bool(config.get("trading_enabled", False))
        self._client: pmxt.Polymarket | None = None
        self._lock = threading.Lock()
        self._market_id_cache: dict[str, str] = {}
        self._connect()

    def _connect(self) -> None:
        """Initialize Polymarket client using credentials from environment."""
        private_key, proxy_address = get_env_credentials()
        if not validate_credentials_for_trading(private_key, proxy_address):
            logger.warning(
                "POLYMARKET_PRIVATE_KEY or POLYMARKET_PROXY_ADDRESS missing; trading will fail."
            )
        logger.info("Connecting to Polymarket...")
        self._client = pmxt.Polymarket(
            private_key=private_key,
            proxy_address=proxy_address,
            signature_type=SIGNATURE_TYPE,
        )
        logger.info("Connected to Polymarket.")

    def _get_market_id(self, slug: str | None) -> str | None:
        """Resolve slug to market_id, using cache when possible."""
        if not slug or not self._client:
            return None
        with self._lock:
            if slug in self._market_id_cache:
                return self._market_id_cache[slug]
        markets = self._client.fetch_markets(slug=slug)
        if not markets:
            return None
        market_id = markets[0].market_id
        with self._lock:
            self._market_id_cache[slug] = market_id
        return market_id

    def execute_trade(self, change: dict[str, Any], market_id: str | None = None) -> Any | None:
        """
        Execute a single copy trade from a detected position change.

        Args:
            change: Dict with asset, type (BUY/SELL), size, slug, etc.
            market_id: If provided, skip fetch_markets (use when batching to reduce latency).

        Returns:
            Order object from pmxt on success, None otherwise.
        """
        if self._client is None:
            logger.error("Polymarket client not initialized.")
            return None

        try:
            side = change["type"].lower()
            asset_id = change["asset"]
            original_size = float(change["size"])
            slug = change.get("slug")

            our_size = round(original_size * self._copy_percentage / 100, 2)
            if our_size <= 0:
                logger.debug("Skipping trade: calculated size %s is too small.", our_size)
                return None

            if market_id is None:
                market_id = self._get_market_id(slug)
            if not market_id:
                logger.warning("Market not found for slug: %s", slug)
                return None

            logger.info("Copying %s for %s: %s shares", side, slug, our_size)

            if not self._trading_enabled:
                logger.info("Trading disabled in config (dry run).")
                return None

            with self._lock:
                try:
                    order = self._client.create_order(
                        market_id=market_id,
                        outcome_id=asset_id,
                        side=side,
                        type="market",
                        amount=our_size,
                        fee=DEFAULT_ORDER_FEE_BPS,
                    )
                except Exception as e:
                    msg = str(e).lower()
                    if "not enough balance" in msg or "insufficient" in msg:
                        logger.error(
                            "Order failed: not enough balance. Reduce size or fund your account. (%s)",
                            e,
                        )
                    elif "trading restricted" in msg or "available regions" in msg:
                        logger.error(
                            "Order failed: trading restricted in your region. (%s)",
                            e,
                        )
                    else:
                        logger.exception("Order failed: %s", e)
                    return None
            logger.info("Order placed successfully. Order ID: %s", order.id)
            return order

        except Exception as e:
            logger.exception("Failed to execute copy trade: %s", e)
            return None
