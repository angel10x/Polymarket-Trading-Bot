"""Configuration loading and environment validation."""

import json
import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from polymarket_copy_trader.constants import (
    CONFIG_FILENAME,
    DEFAULT_RATE_LIMIT_CALLS,
    POLL_INTERVAL_SECONDS,
)

load_dotenv()

logger = logging.getLogger(__name__)


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """
    Load application config from a JSON file.

    Args:
        config_path: Path to config file. Defaults to CONFIG_FILENAME in cwd.

    Returns:
        Config dict with keys: wallets_to_track, copy_percentage, rate_limit, trading_enabled.

    Raises:
        FileNotFoundError: If config file does not exist.
        json.JSONDecodeError: If config is invalid JSON.
    """
    path = Path(config_path or CONFIG_FILENAME)
    if not path.is_absolute():
        path = Path.cwd() / path

    with path.open(encoding="utf-8") as f:
        raw = json.load(f)

    return {
        "wallets_to_track": raw.get("wallets_to_track", []),
        "copy_percentage": float(raw.get("copy_percentage", 1.0)),
        "rate_limit": int(raw.get("rate_limit", DEFAULT_RATE_LIMIT_CALLS)),
        "trading_enabled": bool(raw.get("trading_enabled", False)),
        "poll_interval": float(raw.get("poll_interval", POLL_INTERVAL_SECONDS)),
    }


def get_env_credentials() -> tuple[str | None, str | None]:
    """
    Read Polymarket credentials from environment.

    Returns:
        (private_key, proxy_address). Either may be None if not set.
    """
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    proxy_address = os.getenv("POLYMARKET_PROXY_ADDRESS")
    return private_key, proxy_address


def validate_credentials_for_trading(
    private_key: str | None, proxy_address: str | None
) -> bool:
    """Return True if both credentials are non-empty (trading can be attempted)."""
    return bool(
        private_key and private_key.strip() and proxy_address and proxy_address.strip()
    )


def save_config(config: dict[str, Any], config_path: str | Path | None = None) -> None:
    """
    Save application config to a JSON file.

    Args:
        config: Config dict (wallets_to_track, copy_percentage, rate_limit,
            trading_enabled, poll_interval).
        config_path: Path to config file. Defaults to CONFIG_FILENAME in cwd.
    """
    path = Path(config_path or CONFIG_FILENAME)
    if not path.is_absolute():
        path = Path.cwd() / path

    payload = {
        "wallets_to_track": config.get("wallets_to_track", []),
        "copy_percentage": config.get("copy_percentage", 1.0),
        "rate_limit": config.get("rate_limit", DEFAULT_RATE_LIMIT_CALLS),
        "trading_enabled": config.get("trading_enabled", False),
        "poll_interval": config.get("poll_interval", POLL_INTERVAL_SECONDS),
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
