"""
Example Trading Strategies and Usage Examples

This package contains example code for the Polymarket Trading Bot.
Start with quickstart.py for the simplest introduction.

Examples:
    quickstart.py       - Simplest possible example (start here!)
    basic_trading.py    - Common trading operations
    strategy_example.py - Custom strategy framework

Quick Start:
    from examples.quickstart import main
    import asyncio
    asyncio.run(main())
"""

from .quickstart import main as run_quickstart
from .basic_trading import main as run_basic_example
from .strategy_example import (
    BaseStrategy,
    MeanReversionStrategy,
    GridTradingStrategy,
    run_example_strategy
)

__all__ = [
    "run_quickstart",
    "run_basic_example",
    "BaseStrategy",
    "MeanReversionStrategy",
    "GridTradingStrategy",
    "run_example_strategy",
]
