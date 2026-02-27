"""Tests for position fetching and change detection."""

from polymarket_copy_trader.positions import (
    detect_position_changes,
    _position_by_asset,
)


def test_position_by_asset() -> None:
    """_position_by_asset builds a dict keyed by asset id."""
    positions = [
        {"asset": "a1", "size": 10},
        {"asset": "a2", "size": 20},
    ]
    by_asset = _position_by_asset(positions)
    assert by_asset == {"a1": positions[0], "a2": positions[1]}


def test_detect_new_buy() -> None:
    """New position appears -> one BUY change with full size."""
    previous: list[dict] = []
    current = [
        {
            "asset": "x",
            "size": 5,
            "avgPrice": 0.6,
            "title": "Market X",
            "slug": "x",
            "outcome": None,
            "conditionId": None,
        },
    ]
    changes = detect_position_changes(previous, current)
    assert len(changes) == 1
    assert changes[0]["type"] == "BUY"
    assert changes[0]["asset"] == "x"
    assert changes[0]["size"] == 5


def test_detect_full_sell() -> None:
    """Previous-only position -> one SELL change with previous size."""
    previous = [
        {
            "asset": "y",
            "size": 10,
            "avgPrice": 0.5,
            "title": "Y",
            "slug": "y",
            "outcome": None,
            "conditionId": None,
        },
    ]
    current: list[dict] = []
    changes = detect_position_changes(previous, current)
    assert len(changes) == 1
    assert changes[0]["type"] == "SELL"
    assert changes[0]["size"] == 10


def test_detect_no_change() -> None:
    """Same positions -> no inferred changes."""
    pos = [
        {
            "asset": "z",
            "size": 3,
            "avgPrice": 0.4,
            "title": "Z",
            "slug": "z",
            "outcome": None,
            "conditionId": None,
        }
    ]
    changes = detect_position_changes(pos, pos)
    assert len(changes) == 0
