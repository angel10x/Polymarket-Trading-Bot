"""
Lib - Reusable Components Library

This package provides reusable components for trading strategies and applications:

- console: Terminal output utilities (colors, formatting)
- market_manager: Market discovery and WebSocket management
- price_tracker: Price history and pattern detection
- position_manager: Position tracking with TP/SL

Usage:
    from lib import MarketManager, PriceTracker, PositionManager
    from lib.console import Colors, print_colored
"""

from lib.console import Colors
from lib.market_manager import MarketManager, MarketInfo
from lib.price_tracker import PriceTracker, PricePoint, FlashCrashEvent
from lib.position_manager import PositionManager, Position

__all__ = [
    "Colors",
    "MarketManager",
    "MarketInfo",
    "PriceTracker",
    "PricePoint",
    "FlashCrashEvent",
    "PositionManager",
    "Position",
]
