"""Fetch positions from Polymarket and detect changes between snapshots."""

import logging
from typing import Any, Optional

import requests

from polymarket_copy_trader.constants import (
    POLYMARKET_DATA_API_BASE_URL,
    POSITION_SIZE_EPSILON,
)

logger = logging.getLogger(__name__)


def fetch_positions_for_wallet(wallet_address: str) -> Optional[list[dict[str, Any]]]:
    """
    Fetch current positions for a wallet from Polymarket data API.

    Args:
        wallet_address: Ethereum wallet address to query.

    Returns:
        List of position dicts, or None on error.
    """
    url = f"{POLYMARKET_DATA_API_BASE_URL}/positions"
    params = {"user": wallet_address}
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.warning("Failed to fetch positions for %s: %s", wallet_address[:10], e)
        return None


def _position_by_asset(positions: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Build a map of asset id -> position for fast lookup."""
    return {p["asset"]: p for p in positions}


def _build_new_buy_order(asset_id: str, position: dict[str, Any]) -> dict[str, Any]:
    """Build a change record for a newly opened position (buy)."""
    return {
        "asset": asset_id,
        "type": "BUY",
        "size": position["size"],
        "price": position["avgPrice"],
        "title": position.get("title"),
        "outcome": position.get("outcome"),
        "conditionId": position.get("conditionId"),
        "slug": position.get("slug"),
    }


def _build_full_sell_order(asset_id: str, position: dict[str, Any]) -> dict[str, Any]:
    """Build a change record for a fully closed position (sell)."""
    return {
        "asset": asset_id,
        "type": "SELL",
        "size": position["size"],
        "price": None,
        "title": position.get("title"),
        "outcome": position.get("outcome"),
        "conditionId": position.get("conditionId"),
        "slug": position.get("slug"),
    }


def _build_partial_change_order(
    asset_id: str,
    previous_position: dict[str, Any],
    current_position: dict[str, Any],
    size_delta: float,
) -> dict[str, Any]:
    """Build a change record for a position size increase or decrease."""
    base = {
        "asset": asset_id,
        "title": current_position.get("title"),
        "outcome": current_position.get("outcome"),
        "conditionId": current_position.get("conditionId"),
        "slug": current_position.get("slug"),
    }
    if size_delta > 0:
        cost_current = float(current_position["size"]) * float(
            current_position["avgPrice"]
        )
        cost_previous = float(previous_position["size"]) * float(
            previous_position["avgPrice"]
        )
        exec_price = (cost_current - cost_previous) / size_delta
        base["type"] = "BUY"
        base["size"] = size_delta
        base["price"] = exec_price
    else:
        size_sold = -size_delta
        pnl_previous = float(previous_position.get("realizedPnl", 0))
        pnl_current = float(current_position.get("realizedPnl", 0))
        exec_price = float(previous_position["avgPrice"]) + (
            (pnl_current - pnl_previous) / size_sold
        )
        base["type"] = "SELL"
        base["size"] = size_sold
        base["price"] = exec_price
    return base


def detect_position_changes(
    previous_positions: list[dict[str, Any]],
    current_positions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Compare two position snapshots and return a list of inferred order changes.

    Detects: new positions (buy), closed positions (sell), and size changes (buy/sell).

    Args:
        previous_positions: Positions at time T.
        current_positions: Positions at time T+1.

    Returns:
        List of change dicts with keys: asset, type (BUY/SELL), size, price, slug, etc.
    """
    previous_by_asset = _position_by_asset(previous_positions)
    current_by_asset = _position_by_asset(current_positions)
    all_asset_ids = set(previous_by_asset) | set(current_by_asset)
    changes: list[dict[str, Any]] = []

    for asset_id in all_asset_ids:
        prev_position = previous_by_asset.get(asset_id)
        curr_position = current_by_asset.get(asset_id)

        if prev_position is None and curr_position is not None:
            changes.append(_build_new_buy_order(asset_id, curr_position))
            continue

        if prev_position is not None and curr_position is None:
            changes.append(_build_full_sell_order(asset_id, prev_position))
            continue

        if prev_position is None or curr_position is None:
            continue

        size_delta = float(curr_position["size"]) - float(prev_position["size"])
        if abs(size_delta) < POSITION_SIZE_EPSILON:
            continue

        changes.append(
            _build_partial_change_order(
                asset_id, prev_position, curr_position, size_delta
            )
        )

    return changes
