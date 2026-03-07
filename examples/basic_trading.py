#!/usr/bin/env python3
"""
Basic Trading Examples

Demonstrates common trading operations with the trading bot.

Usage:
    python examples/basic_trading.py
"""

import os
import asyncio
import sys
from pathlib import Path

# Auto-load .env file
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.bot import TradingBot
from src.config import Config


async def main():
    """Run basic trading examples."""
    print("=" * 50)
    print("Basic Trading Examples")
    print("=" * 50)

    # Check credentials
    private_key = os.environ.get("POLY_PRIVATE_KEY")
    if not private_key:
        print("\nError: POLY_PRIVATE_KEY not set in .env file")
        sys.exit(1)

    # Initialize the bot from environment
    config = Config.from_env()
    bot = TradingBot(config=config, private_key=private_key)

    print(f"\nBot initialized with Safe: {bot.config.safe_address}")
    print(f"Gasless mode: {bot.config.use_gasless}")

    # Example 1: Get open orders
    print("\n--- Example 1: Get Open Orders ---")
    orders = await bot.get_open_orders()
    print(f"You have {len(orders)} open orders")

    # Example 2: Get recent trades
    print("\n--- Example 2: Get Recent Trades ---")
    trades = await bot.get_trades(limit=5)
    print(f"Recent trades: {len(trades)}")

    # Example 3: Get market price (using default token from config)
    if bot.config.default_token_id:
        print("\n--- Example 3: Get Market Price ---")
        price = await bot.get_market_price(bot.config.default_token_id)
        print(f"Current price: {price}")

        # Example 4: Get order book
        print("\n--- Example 4: Get Order Book ---")
        orderbook = await bot.get_order_book(bot.config.default_token_id)
        print(f"Order book bids: {len(orderbook.get('bids', []))}")
        print(f"Order book asks: {len(orderbook.get('asks', []))}")

        # Example 5: Place a test order (commented out)
        print("\n--- Example 5: Place an Order ---")
        print("To place an order, uncomment the code below:\n")
        print("""
        result = await bot.place_order(
            token_id=bot.config.default_token_id,
            price=0.50,      # Price per share
            size=1.0,        # Number of shares
            side="BUY"       # or "SELL"
        )
        print(f"Order result: {result.success}, {result.order_id}")
        """)

    # Example 6: Cancel all orders
    print("\n--- Example 6: Cancel All Orders ---")
    print("To cancel all orders, uncomment the code below:\n")
    print("""
    result = await bot.cancel_all_orders()
    print(f"Cancelled: {result.success}, {result.message}")
    """)

    print("\n" + "=" * 50)
    print("Examples complete!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
