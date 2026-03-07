"""
Strategies - Trading Strategy Implementations

This package contains trading strategy implementations:

- base: Base class for all strategies
- flash_crash: Flash crash volatility strategy

Usage:
    from strategies.base import BaseStrategy, StrategyConfig
    from strategies.flash_crash import FlashCrashStrategy, FlashCrashConfig
"""

from strategies.base import BaseStrategy, StrategyConfig
from strategies.flash_crash import FlashCrashStrategy, FlashCrashConfig

__all__ = [
    "BaseStrategy",
    "StrategyConfig",
    "FlashCrashStrategy",
    "FlashCrashConfig",
]
