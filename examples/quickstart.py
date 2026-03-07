#!/usr/bin/env python3
"""
Quickstart Example - Your First Trade in 5 Minutes

This is the simplest possible example to get started with the trading bot.
Perfect for beginners who want to understand the basics.

Prerequisites:
    1. Install dependencies: pip install -r requirements.txt
    2. Create .env file with your credentials (see .env.example)

Usage:
    python examples/quickstart.py
"""

import os
import sys
import asyncio
from pathlib import Path

# Auto-load .env file
from dotenv import load_dotenv
load_dotenv()

# Add project root to path (so we can import from src/)
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.bot import TradingBot
from src.config import Config


def check_environment():
    """Check if required environment variables are set."""
    private_key = os.environ.get("POLY_PRIVATE_KEY")
    safe_address = os.environ.get("POLY_SAFE_ADDRESS")

    if not private_key:
        print("ERROR: POLY_PRIVATE_KEY environment variable not set!")
        print("")
        print("Set it with:")
        print("  export POLY_PRIVATE_KEY=your_private_key")
        print("")
        print("Or create a .env file and run: source .env")
        return None, None

    if not safe_address:
        print("ERROR: POLY_SAFE_ADDRESS environment variable not set!")
        print("")
        print("Set it with:")
        print("  export POLY_SAFE_ADDRESS=0xYourSafeAddress")
        print("")
        print("Find your Safe address at: polymarket.com/settings")
        return None, None

    return private_key, safe_address


async def main():
    """
    Simple example showing how to:
    1. Initialize the bot
    2. Check open orders
    3. View recent trades
    """
    print("=" * 50)
    print("Polymarket Trading Bot - Quickstart")
    print("=" * 50)
    print()

    # Step 1: Check environment
    print("[Step 1] Checking environment variables...")
    private_key, safe_address = check_environment()
    if not private_key:
        sys.exit(1)
    print(f"  Safe address: {safe_address}")
    print()

    # Step 2: Create configuration
    print("[Step 2] Creating configuration...")
    config = Config.from_env()
    print(f"  Gasless mode: {config.use_gasless}")
    print()

    # Step 3: Initialize the bot
    print("[Step 3] Initializing trading bot...")
    bot = TradingBot(
        config=config,
        private_key=private_key
    )

    if bot.is_initialized():
        print("  Bot initialized successfully!")
        print(f"  Signer address: {bot.signer.address}")
    else:
        print("  ERROR: Bot failed to initialize")
        sys.exit(1)
    print()

    # Step 4: Check open orders
    print("[Step 4] Fetching open orders...")
    try:
        orders = await bot.get_open_orders()
        print(f"  You have {len(orders)} open orders")
        for order in orders[:3]:  # Show first 3
            token = order.get("tokenId", "?")[:16]
            side = order.get("side", "?")
            price = order.get("price", "?")
            size = order.get("size", "?")
            print(f"    - {side} {size} @ {price} (token: {token}...)")
    except Exception as e:
        print(f"  Could not fetch orders: {e}")
    print()

    # Step 5: Check recent trades
    print("[Step 5] Fetching recent trades...")
    try:
        trades = await bot.get_trades(limit=5)
        print(f"  Found {len(trades)} recent trades")
        for trade in trades[:3]:  # Show first 3
            side = trade.get("side", "?")
            price = trade.get("price", "?")
            size = trade.get("size", "?")
            print(f"    - {side} {size} @ {price}")
    except Exception as e:
        print(f"  Could not fetch trades: {e}")
    print()

    # Done!
    print("=" * 50)
    print("Quickstart complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("  1. Place an order:")
    print("     result = await bot.place_order(token_id, 0.5, 1.0, 'BUY')")
    print()
    print("  2. Cancel an order:")
    print("     await bot.cancel_order(order_id)")
    print()
    print("  3. See examples/basic_trading.py for more examples")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
