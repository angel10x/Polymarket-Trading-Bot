# 策略开发指南

本指南面向第一次在本项目上开发策略的用户，力求一步一步、可直接上手。

## 1) 心智模型

项目分三层：

1. 数据层：`MarketManager` + `MarketWebSocket`
2. 逻辑层：你的策略类（信号、风控、状态）
3. 执行层：`TradingBot`（下单、撤单、仓位管理）

`BaseStrategy` 已经帮你接好数据和主循环，你只需要实现三个方法并决定何时交易。

## 2) 可复用的核心组件

- `strategies/base.py`
  - `BaseStrategy`：WebSocket 初始化、循环与刷新、订单同步。
  - `StrategyConfig`：风险与节奏配置。
- `lib/market_manager.py`
  - 15 分钟市场发现与自动切换。
  - 订单簿缓存、mid 价、买卖差价。
- `lib/price_tracker.py`
  - 价格历史、闪崩检测等工具。
- `lib/position_manager.py`
  - 持仓、TP/SL、PnL 统计。
- `src/bot.py`
  - 下单/撤单/查询接口与 gasless 支持。

## 3) 最小环境配置

交易所需环境变量：

```bash
export POLY_PRIVATE_KEY=0x你的私钥
export POLY_SAFE_ADDRESS=0x你的Safe地址
```

可选（Builder gasless）：

```bash
export POLY_BUILDER_API_KEY=...
export POLY_BUILDER_API_SECRET=...
export POLY_BUILDER_API_PASSPHRASE=...
```

先验证 WebSocket 是否正常：

```bash
python apps/orderbook_tui.py --coin ETH
```

能看到实时订单簿就说明数据通了。

## 4) 最小策略模板

创建 `strategies/my_strategy.py`：

```python
from dataclasses import dataclass
from typing import Dict

from strategies.base import BaseStrategy, StrategyConfig
from src.websocket_client import OrderbookSnapshot


@dataclass
class MyStrategyConfig(StrategyConfig):
    entry_price: float = 0.45
    side: str = "up"


class MyStrategy(BaseStrategy):
    async def on_book_update(self, snapshot: OrderbookSnapshot) -> None:
        # 可选：每次订单簿更新触发
        pass

    async def on_tick(self, prices: Dict[str, float]) -> None:
        side = self.config.side
        price = prices.get(side, 0.0)
        if price <= 0:
            return

        if self.positions.can_open_position and price <= self.config.entry_price:
            await self.execute_buy(side, price)

    def render_status(self, prices: Dict[str, float]) -> None:
        up = prices.get("up", 0.0)
        down = prices.get("down", 0.0)
        print(f"up={up:.4f} down={down:.4f} positions={self.positions.position_count}")
```

## 5) 运行脚本

创建 `apps/run_my_strategy.py`：

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
        raise RuntimeError("POLY_PRIVATE_KEY 未设置")
    bot = TradingBot(config=config, private_key=private_key)
    strategy = MyStrategy(bot=bot, config=MyStrategyConfig())
    await strategy.run()


if __name__ == "__main__":
    asyncio.run(main())
```

提示：内置策略的运行脚本在这里：

```bash
python apps/run_flash_crash.py --coin ETH
```

## 6) 策略生命周期

`BaseStrategy.run()` 会执行：

1. `start()`：连接 WebSocket 并等待首批数据
2. 每个 tick：
   - 读取当前价格
   - 调用 `on_tick(prices)`
   - 检查 TP/SL 并自动平仓
   - 刷新显示
3. `stop()`：退出清理

## 7) 下单方式

方式一：使用封装好的快捷方法：

- `await self.execute_buy(side, price)`
- `await self.execute_sell(position, price)`

方式二：直接调用 bot：

```python
await self.bot.place_order(token_id, price, size, side="BUY")
```

若使用方式二，记得同步更新 `PositionManager`。

## 8) 风控建议

建议在配置里设置：

- `max_positions`：最大持仓数
- `take_profit`：止盈
- `stop_loss`：止损

示例：

```python
MyStrategyConfig(
    max_positions=1,
    take_profit=0.10,
    stop_loss=0.05,
)
```

## 9) 常见坑

- **异步阻塞**：不要在 `on_tick` 里直接做阻塞 IO。
- **token_id 混淆**：使用 `self.token_ids["up"]` / `self.token_ids["down"]`。
- **仓位计算**：`execute_buy()` 用 `config.size`（USDC）/ `price` 计算份额。
- **刚启动没数据**：价格可能是 0，逻辑里要防御。

## 10) 测试建议

可以单测信号逻辑，mock 下单：

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

## 11) 排查清单

- 先跑 `python apps/orderbook_tui.py --coin ETH` 看数据是否正常
- 打印 `prices` 确认 tick 是否有更新
- 检查 Safe 地址与环境变量

---

建议从 `strategies/flash_crash.py` 复制改起，是最省力的方式。
