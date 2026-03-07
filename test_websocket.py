#!/usr/bin/env python3
"""
Test WebSocket subscription to Polymarket CLOB market channel.
"""

import json
import asyncio

try:
    import websockets
except ImportError:
    print("Please install websockets: pip install websockets")
    exit(1)

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.gamma_client import GammaClient


async def test_websocket():
    """Test WebSocket connection and subscription."""

    # Get current market
    gamma = GammaClient()
    market_info = gamma.get_market_info("BTC")

    if not market_info:
        print("No active BTC market found")
        return

    print(f"Market: {market_info['question']}")
    print(f"Accepting orders: {market_info['accepting_orders']}")

    token_ids = market_info["token_ids"]
    up_token = token_ids.get("up")
    down_token = token_ids.get("down")

    print(f"Up token: {up_token}")
    print(f"Down token: {down_token}")

    if not up_token or not down_token:
        print("Missing token IDs")
        return

    url = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

    print(f"\nConnecting to {url}...")

    async with websockets.connect(url) as ws:
        print("Connected!")

        # Send subscription
        subscribe_msg = {
            "assets_ids": [up_token, down_token],
            "type": "MARKET"
        }

        msg_json = json.dumps(subscribe_msg)
        print(f"\nSending subscription: {msg_json}")
        await ws.send(msg_json)
        print("Subscription sent!")

        # Wait for messages
        print("\nWaiting for messages (Ctrl+C to stop)...\n")

        msg_count = 0
        try:
            async for message in ws:
                msg_count += 1
                data = json.loads(message)
                event_type = data.get("event_type", "unknown")

                if event_type == "book":
                    asset_id = data.get("asset_id", "")[:20]
                    bids = data.get("bids", [])
                    asks = data.get("asks", [])
                    best_bid = bids[0]["price"] if bids else "N/A"
                    best_ask = asks[0]["price"] if asks else "N/A"
                    print(f"[{msg_count}] BOOK: asset={asset_id}... bid={best_bid} ask={best_ask}")

                elif event_type == "price_change":
                    changes = data.get("price_changes", [])
                    for change in changes:
                        side = change.get("side", "?")
                        price = change.get("price", "?")
                        best_bid = change.get("best_bid", "?")
                        best_ask = change.get("best_ask", "?")
                        print(f"[{msg_count}] PRICE_CHANGE: side={side} price={price} bid={best_bid} ask={best_ask}")

                elif event_type == "last_trade_price":
                    price = data.get("price", "?")
                    side = data.get("side", "?")
                    size = data.get("size", "?")
                    print(f"[{msg_count}] TRADE: side={side} price={price} size={size}")

                else:
                    print(f"[{msg_count}] {event_type}: {str(data)[:100]}")

        except KeyboardInterrupt:
            print(f"\n\nReceived {msg_count} messages total")


if __name__ == "__main__":
    try:
        asyncio.run(test_websocket())
    except KeyboardInterrupt:
        print("\nStopped")
