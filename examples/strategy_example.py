#!/usr/bin/env python3
"""
Strategy Template - Custom Trading Strategies

This file provides a template for building custom trading strategies.
Copy this file and modify the Strategy class for your own strategies.

BaseStrategy provides:
- Order management
- Position tracking
- PnL calculation
- Risk management hooks
- Event callbacks

Example strategies included:
- Mean Reversion: Buy when price drops, sell when it rises
- Grid Trading: Place orders at regular price intervals
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.bot import TradingBot, OrderResult, OrderSide


class StrategyStatus(Enum):
    """Strategy execution status."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"


@dataclass
class Position:
    """Represents a trading position."""
    token_id: str
    side: str  # 'BUY' or 'SELL'
    size: float
    entry_price: float
    entry_time: datetime = field(default_factory=datetime.now)

    @property
    def is_long(self) -> bool:
        return self.side == OrderSide.BUY.value

    @property
    def is_short(self) -> bool:
        return self.side == OrderSide.SELL.value


@dataclass
class OrderInfo:
    """Information about a placed order."""
    order_id: str
    token_id: str
    side: str
    price: float
    size: float
    status: str  # 'pending', 'filled', 'cancelled'
    placed_at: datetime = field(default_factory=datetime.now)


class StrategyEvent:
    """Strategy lifecycle events."""
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.type = event_type
        self.data = data
        self.timestamp = datetime.now()


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.

    To create a custom strategy:
    1. Inherit from BaseStrategy
    2. Implement required methods
    3. Optionally override optional methods

    Example:
        class MyStrategy(BaseStrategy):
            def __init__(self, bot: TradingBot, params: Dict):
                super().__init__(bot, params)
                self.param1 = params.get('param1', 10)

            async def on_tick(self, price_data: Dict):
                # Your strategy logic here
                pass
    """

    def __init__(
        self,
        bot: TradingBot,
        params: Optional[Dict[str, Any]] = None,
        name: str = "BaseStrategy"
    ):
        """
        Initialize strategy.

        Args:
            bot: TradingBot instance
            params: Strategy parameters
            name: Strategy name
        """
        self.bot = bot
        self.params = params or {}
        self.name = name

        # State
        self.status = StrategyStatus.STOPPED
        self.positions: Dict[str, Position] = {}
        self.orders: Dict[str, OrderInfo] = {}

        # Callbacks
        self.on_order_callbacks: List[Callable[[OrderResult], None]] = []
        self.on_tick_callbacks: List[Callable[[Dict], None]] = []
        self.on_error_callbacks: List[Callable[[Exception], None]] = []

        # Settings
        self.check_interval = self.params.get('check_interval', 60)  # seconds
        self.max_positions = self.params.get('max_positions', 3)
        self.stop_loss = self.params.get('stop_loss')  # e.g., 0.1 = 10%
        self.take_profit = self.params.get('take_profit')  # e.g., 0.2 = 20%

    # Required methods to implement

    @abstractmethod
    async def on_tick(self, price_data: Dict[str, Any]) -> None:
        """
        Called periodically with market data.

        Implement your strategy logic here.
        Place orders, close positions, etc.

        Args:
            price_data: Market data dictionary
        """
        pass

    @abstractmethod
    async def on_order_update(self, order: OrderInfo) -> None:
        """
        Called when an order status changes.

        Args:
            order: OrderInfo with updated status
        """
        pass

    # Optional lifecycle methods

    async def initialize(self) -> None:
        """Called when strategy starts."""
        await self.sync_positions()
        await self.sync_orders()
        self.status = StrategyStatus.RUNNING

    async def cleanup(self) -> None:
        """Called when strategy stops."""
        self.status = StrategyStatus.STOPPED

    async def on_error(self, error: Exception) -> None:
        """Called when an error occurs."""
        self.status = StrategyStatus.ERROR
        for callback in self.on_error_callbacks:
            callback(error)

    # Helper methods for subclasses

    async def place_order(
        self,
        token_id: str,
        price: float,
        size: float,
        side: str
    ) -> OrderInfo:
        """Place an order and track it."""
        result = await self.bot.place_order(
            token_id=token_id,
            price=price,
            size=size,
            side=side
        )

        order_info = OrderInfo(
            order_id=result.order_id or f"temp_{int(time.time())}",
            token_id=token_id,
            side=side,
            price=price,
            size=size,
            status='pending'
        )

        if result.success:
            self.orders[order_info.order_id] = order_info
        else:
            order_info.status = 'failed'
            order_info.order_id = f"failed_{int(time.time())}"
            self.orders[order_info.order_id] = order_info

        return order_info

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        result = await self.bot.cancel_order(order_id)

        if order_id in self.orders:
            self.orders[order_id].status = 'cancelled'

        return result.success

    async def cancel_all_orders(self, token_id: Optional[str] = None) -> None:
        """Cancel all pending orders."""
        for order_id, order in list(self.orders.items()):
            if token_id and order.token_id != token_id:
                continue
            if order.status == 'pending':
                await self.cancel_order(order_id)

    async def sync_positions(self) -> None:
        """Sync positions with open orders and trades."""
        # Get open orders
        open_orders = await self.bot.get_open_orders()

        # Get trades
        trades = await self.bot.get_trades(limit=100)

        # This is a simplified sync - extend for production use
        self.positions = {}

    async def sync_orders(self) -> None:
        """Sync order status with exchange."""
        for order_id, order in list(self.orders.items()):
            if order.status != 'pending':
                continue

            order_data = await self.bot.get_order(order_id)
            if order_data:
                new_status = order_data.get('status', order.status)
                order.status = new_status
                await self.on_order_update(order)

    def add_position(self, position: Position) -> None:
        """Add a position."""
        key = f"{position.token_id}_{position.side}"
        self.positions[key] = position

    def close_position(self, token_id: str, side: str) -> Optional[Position]:
        """Close and return a position."""
        key = f"{token_id}_{side}"
        return self.positions.pop(key, None)

    # Callback registration

    def add_on_order_callback(self, callback: Callable[[OrderResult], None]) -> None:
        """Register order callback."""
        self.on_order_callbacks.append(callback)

    def add_on_tick_callback(self, callback: Callable[[Dict], None]) -> None:
        """Register tick callback."""
        self.on_tick_callbacks.append(callback)

    def add_on_error_callback(self, callback: Callable[[Exception], None]) -> None:
        """Register error callback."""
        self.on_error_callbacks.append(callback)

    # Main loop

    async def run(
        self,
        token_ids: List[str],
        duration: Optional[int] = None  # seconds, None = infinite
    ) -> None:
        """
        Run the strategy loop.

        Args:
            token_ids: List of token IDs to monitor
            duration: Run duration in seconds (None = run forever)
        """
        await self.initialize()

        start_time = time.time()

        try:
            while self.status == StrategyStatus.RUNNING:
                # Check duration
                if duration and (time.time() - start_time) > duration:
                    break

                # Get price data for each token
                for token_id in token_ids:
                    try:
                        price_data = await self.bot.get_market_price(token_id)
                        price_data['token_id'] = token_id

                        # Call on_tick
                        await self.on_tick(price_data)

                        # Notify callbacks
                        for callback in self.on_tick_callbacks:
                            callback(price_data)

                    except Exception as e:
                        await self.on_error(e)

                # Wait before next tick
                await asyncio.sleep(self.check_interval)

        finally:
            await self.cleanup()

    def stop(self) -> None:
        """Stop the strategy."""
        self.status = StrategyStatus.STOPPED


class MeanReversionStrategy(BaseStrategy):
    """
    Mean Reversion Strategy

    Buys when price drops below moving average,
    sells when price rises above moving average.

    Parameters:
        window: Moving average window size
        threshold: Price deviation threshold to trigger trade
        size: Order size
    """

    def __init__(
        self,
        bot: TradingBot,
        params: Optional[Dict[str, Any]] = None,
        name: str = "MeanReversion"
    ):
        super().__init__(bot, params or {}, name)

        self.window = self.params.get('window', 10)
        self.threshold = self.params.get('threshold', 0.05)  # 5%
        self.size = self.params.get('size', 1.0)

        # Price history for moving average
        self.price_history: Dict[str, List[float]] = {}

    async def on_tick(self, price_data: Dict[str, Any]) -> None:
        token_id = price_data.get('token_id')
        price = price_data.get('price', 0)

        if not token_id or price <= 0:
            return

        # Initialize history if needed
        if token_id not in self.price_history:
            self.price_history[token_id] = []

        # Add to history
        self.price_history[token_id].append(price)

        # Keep only window size
        if len(self.price_history[token_id]) > self.window:
            self.price_history[token_id] = self.price_history[token_id][-self.window:]

        # Need enough data
        if len(self.price_history[token_id]) < self.window:
            return

        # Calculate moving average
        ma = sum(self.price_history[token_id]) / len(self.price_history[token_id])

        # Calculate deviation
        deviation = (price - ma) / ma

        # Trading logic
        key = f"{token_id}_BUY"

        if deviation < -self.threshold:
            # Price below average - BUY
            if key not in self.positions:
                print(f"[{self.name}] Buying {token_id} at {price}")
                await self.place_order(token_id, price, self.size, "BUY")

        elif deviation > self.threshold:
            # Price above average - SELL
            if key in self.positions:
                print(f"[{self.name}] Selling {token_id} at {price}")
                await self.place_order(token_id, price, self.size, "SELL")

    async def on_order_update(self, order: OrderInfo) -> None:
        # Update position when order fills
        if order.status == 'filled':
            if order.side == 'BUY':
                self.add_position(Position(
                    token_id=order.token_id,
                    side='BUY',
                    size=order.size,
                    entry_price=order.price
                ))
            elif order.side == 'SELL':
                self.close_position(order.token_id, 'BUY')


class GridTradingStrategy(BaseStrategy):
    """
    Grid Trading Strategy

    Places buy orders at grid levels below current price
    and sell orders at grid levels above current price.

    Parameters:
        grid_size: Number of grid levels
        grid_spacing: Distance between grid levels (as %)
        size: Order size per grid level
    """

    def __init__(
        self,
        bot: TradingBot,
        params: Optional[Dict[str, Any]] = None,
        name: str = "GridTrading"
    ):
        super().__init__(bot, params or {}, name)

        self.grid_size = self.params.get('grid_size', 5)
        self.grid_spacing = self.params.get('grid_spacing', 0.02)  # 2%
        self.size = self.params.get('size', 1.0)

        # Track grid levels
        self.grid_levels: Dict[str, List[float]] = {}

    async def on_tick(self, price_data: Dict[str, Any]) -> None:
        token_id = price_data.get('token_id')
        current_price = price_data.get('price', 0)

        if not token_id or current_price <= 0:
            return

        # Initialize grid if needed
        if token_id not in self.grid_levels:
            self.grid_levels[token_id] = self._create_grid(current_price)
            await self._place_grid_orders(token_id, current_price)

    def _create_grid(self, current_price: float) -> List[float]:
        """Create grid price levels."""
        levels = []

        # Buy grid (below current)
        for i in range(self.grid_size):
            price = current_price * (1 - (i + 1) * self.grid_spacing)
            levels.append(price)

        # Sell grid (above current)
        for i in range(self.grid_size):
            price = current_price * (1 + (i + 1) * self.grid_spacing)
            levels.append(price)

        return levels

    async def _place_grid_orders(self, token_id: str, current_price: float) -> None:
        """Place orders at grid levels."""
        for level in self.grid_levels[token_id]:
            if level < current_price:
                side = "BUY"
            else:
                side = "SELL"

            await self.place_order(token_id, level, self.size, side)

    async def on_order_update(self, order: OrderInfo) -> None:
        # When an order fills, check if we should replace the grid
        if order.status == 'filled':
            # In a real strategy, you might rebalance here
            pass


# Example usage
async def run_example_strategy():
    """Example of running a custom strategy."""
    import os
    from dotenv import load_dotenv
    load_dotenv()

    from src.config import Config

    # Get credentials from environment
    private_key = os.environ.get("POLY_PRIVATE_KEY")
    safe_address = os.environ.get("POLY_SAFE_ADDRESS")

    if not private_key or not safe_address:
        print("Error: Set POLY_PRIVATE_KEY and POLY_SAFE_ADDRESS in .env file")
        return

    # Create config and bot
    config = Config.from_env()
    bot = TradingBot(config=config, private_key=private_key)

    # Create strategy with parameters
    strategy_params = {
        'window': 10,
        'threshold': 0.05,
        'size': 1.0,
        'check_interval': 60
    }

    strategy = MeanReversionStrategy(
        bot=bot,
        params=strategy_params
    )

    # Demo: Show strategy info
    print(f"Strategy: {strategy.name}")
    print(f"Parameters: {strategy_params}")
    print(f"Bot initialized: {bot.is_initialized()}")
    print(f"Signer address: {bot.signer.address if bot.signer else 'None'}")
    print()
    print("To run the strategy with a specific token:")
    print("  await strategy.run(['TOKEN_ID'], duration=3600)")


if __name__ == "__main__":
    print("=" * 50)
    print("Strategy Example - Mean Reversion")
    print("=" * 50)
    asyncio.run(run_example_strategy())
