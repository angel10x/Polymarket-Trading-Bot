"""
Core data models for prediction market exchanges.

Unified types for markets, events, order books, orders, positions, and balances.
"""

from datetime import datetime
from typing import Any, Literal, NotRequired, TypedDict

# ---------------------------------------------------------------------------
# Core Data Models
# ---------------------------------------------------------------------------


class MarketOutcome(TypedDict, total=False):
    """Single outcome within a prediction market (price, label, metadata)."""
    outcome_id: str
    market_id: str
    label: str
    price: float
    price_change_24h: float
    metadata: dict[str, Any]


class UnifiedMarket(TypedDict, total=False):
    """Normalized market representation shared across exchanges."""
    market_id: str
    title: str
    description: str
    slug: str
    outcomes: list[MarketOutcome]
    resolution_date: datetime | float
    volume_24h: float
    volume: float
    liquidity: float
    open_interest: float
    url: str
    image: str
    category: str
    tags: list[str]
    tick_size: float
    yes: MarketOutcome
    no: MarketOutcome
    up: MarketOutcome
    down: MarketOutcome


class UnifiedEvent(TypedDict, total=False):
    """Normalized event / tournament containing one or more markets."""
    id: str
    title: str
    description: str
    slug: str
    markets: list[UnifiedMarket]
    url: str
    image: str
    category: str
    tags: list[str]


CandleInterval = Literal["1m", "5m", "15m", "1h", "6h", "1d"]


class PriceCandle(TypedDict, total=False):
    """OHLCV candle for price history over a fixed interval."""
    timestamp: int | float
    open: float
    high: float
    low: float
    close: float
    volume: float


class OrderLevel(TypedDict):
    """Single level in an order book (price / size)."""
    price: float
    size: float


class OrderBook(TypedDict):
    """Aggregated bid/ask levels for a market at a point in time."""
    bids: list[OrderLevel]
    asks: list[OrderLevel]
    timestamp: NotRequired[int | float]


class Trade(TypedDict, total=False):
    """Executed trade on an exchange (not necessarily user-specific)."""
    id: str
    timestamp: int | float
    price: float
    amount: float
    side: Literal["buy", "sell", "unknown"]


class UserTrade(Trade, total=False):
    """User-specific trade data, extending a generic trade with order info."""
    order_id: str


# ---------------------------------------------------------------------------
# Trading Data Models
# ---------------------------------------------------------------------------


class Order(TypedDict, total=False):
    """Standardized order object used for creating and tracking orders."""
    id: str
    market_id: str
    outcome_id: str
    side: Literal["buy", "sell"]
    type: Literal["market", "limit"]
    price: float
    amount: float
    status: Literal["pending", "open", "filled", "cancelled", "rejected"]
    filled: float
    remaining: float
    timestamp: int | float
    fee: float


class Position(TypedDict, total=False):
    """Open or closed position in a particular market outcome."""
    market_id: str
    outcome_id: str
    outcome_label: str
    size: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float


class Balance(TypedDict):
    """Wallet or account balance for a single currency or token."""
    currency: str
    total: float
    available: float
    locked: float


class CreateOrderParams(TypedDict, total=False):
    """Parameters required to create an order on any supported exchange."""
    market_id: str
    outcome_id: str
    side: Literal["buy", "sell"]
    type: Literal["market", "limit"]
    amount: float
    price: float
    fee: int | float
    tick_size: str | int | float
    neg_risk: bool
