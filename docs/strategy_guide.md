# Strategy Development Guide

This guide explains how to build a new strategy on top of this repo. It is written for
Python users with basic async knowledge, but it stays practical and step-by-step.

## 1) Mental Model

You have three layers:

1. Data: `MarketManager` + `MarketWebSocket`
2. Logic: your strategy subclass (signals, risk rules)
3. Execution: `TradingBot` (orders, cancel, positions)

The base class already wires data and timing for you. Your job is to implement three
methods and decide when to trade.

## 2) Core Components (What You Can Reuse)

- `strategies/base.py`
  - `BaseStrategy` handles WebSocket setup, ticks, and order refresh.
  - `StrategyConfig` defines default risk and timing settings.
- `lib/market_manager.py`
  - Market discovery and auto-switching for 15m markets.
  - Orderbook caching, mid price, spread, and best bid/ask.
- `lib/price_tracker.py`
  - Rolling price history and flash-crash detection utilities.
- `lib/position_manager.py`
  - Tracks open positions, TP/SL, and PnL stats.
- `src/bot.py`
  - Order placement/cancel APIs and gasless support.

## 3) Minimum Setup

Environment variables (required for live trading):

```bash
export POLY_PRIVATE_KEY=0xYourPrivateKey
export POLY_SAFE_ADDRESS=0xYourSafeAddress
```

Optional (gasless mode):

```bash
export POLY_BUILDER_API_KEY=...
export POLY_BUILDER_API_SECRET=...
export POLY_BUILDER_API_PASSPHRASE=...
```

Quick connectivity check:

```bash
python apps/orderbook_tui.py --coin ETH
```

If you see live orderbooks, the WebSocket side is healthy.

## 4) A Minimal Strategy Template

Create `strategies/my_strategy.py`:

```python
from dataclasses import dataclass
from typing import Dict

from strategies.base import BaseStrategy, StrategyConfig
from src.websocket_client import OrderbookSnapshot


@dataclass
class MyStrategyConfig(StrategyConfig):
    # Add any custom parameters here
    entry_price: float = 0.45
    side: str = "up"


class MyStrategy(BaseStrategy):
    async def on_book_update(self, snapshot: OrderbookSnapshot) -> None:
        # Optional: react to each orderbook update
        pass

    async def on_tick(self, prices: Dict[str, float]) -> None:
        # Simple example: buy once when price <= entry_price
        side = self.config.side
        price = prices.get(side, 0.0)
        if price <= 0:
            return

        if self.positions.can_open_position and price <= self.config.entry_price:
            await self.execute_buy(side, price)

    def render_status(self, prices: Dict[str, float]) -> None:
        # Keep it simple for now; you can build a TUI later
        up = prices.get("up", 0.0)
        down = prices.get("down", 0.0)
        print(f"up={up:.4f} down={down:.4f} positions={self.positions.position_count}")
```

## 5) A Runner Script

Create `apps/run_my_strategy.py`:

```python
import asyncio
import os

from src.bot import TradingBot
from src.config import Config
from strategies.my_strategy import MyStrategy, MyStrategyConfig


async def main():
    config = Config.from_env()
    private_key = os.environ.get("POLY_PRIVATE_KEY")
    if not private_key:
        raise RuntimeError("POLY_PRIVATE_KEY is not set")
    bot = TradingBot(config=config, private_key=private_key)
    strategy = MyStrategy(bot=bot, config=MyStrategyConfig())
    await strategy.run()


if __name__ == "__main__":
    asyncio.run(main())
```

Tip: the repo already includes a runner for the built-in strategy:

```bash
python apps/run_flash_crash.py --coin ETH
```

Note: if you prefer, load the private key directly from env:

```python
import os
private_key = os.environ["POLY_PRIVATE_KEY"]
```

## 6) Strategy Lifecycle

`BaseStrategy.run()` calls:

1. `start()` - connects WebSocket and waits for data
2. Every tick:
   - reads current prices
   - calls `on_tick(prices)`
   - checks exits (`take_profit` / `stop_loss`)
   - updates status UI
3. `stop()` - cleanup on exit

Your main logic lives in `on_tick()` and optionally `on_book_update()`.

## 7) Trading Helpers

You can place orders two ways:

1) Convenience helpers:
- `await self.execute_buy(side, price)`
- `await self.execute_sell(position, price)`

2) Direct bot calls:

```python
await self.bot.place_order(token_id, price, size, side="BUY")
```

If you use direct calls, you should also update `PositionManager` yourself.

## 8) Risk Controls

Recommended defaults in config:

- `max_positions`: limit exposure
- `take_profit`: auto exit when up X dollars
- `stop_loss`: auto exit when down X dollars

Example:

```python
MyStrategyConfig(
    max_positions=1,
    take_profit=0.10,
    stop_loss=0.05,
)
```

## 9) Common Pitfalls

- **Async blocking**: use the existing async API; do not call `requests` directly
  inside `on_tick`.
- **Token ID mixups**: use `self.token_ids["up"]` / `self.token_ids["down"]`.
- **Position sizing**: `execute_buy()` uses `config.size` as USDC size, then
  converts to shares by `size / price`.
- **No data yet**: on startup, prices can be `0`. Guard your logic.

## 10) Testing Tips

Unit test signal logic with small inputs. Mock bot calls:

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_entry_signal(monkeypatch):
    bot = AsyncMock()
    strategy = MyStrategy(bot=bot, config=MyStrategyConfig(entry_price=0.5))
    await strategy.on_tick({"up": 0.45})
    assert bot.place_order.called
```

## 11) Debug Checklist

- Run `python apps/orderbook_tui.py --coin ETH` to confirm data flow.
- Log `prices` in `on_tick()` to ensure you see updates.
- Check your Safe address and environment variables.

---

If you want, you can copy `strategies/flash_crash.py` and start from there.
