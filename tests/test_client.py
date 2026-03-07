"""
Unit tests for client and bot async behavior.
"""

import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client import ClobClient
from src.bot import TradingBot
from src.config import Config


def test_get_trades_passes_limit_and_token(monkeypatch):
    client = ClobClient(host="https://example.com")
    captured = {}

    def fake_request(method, endpoint, data=None, headers=None, params=None):
        captured["method"] = method
        captured["endpoint"] = endpoint
        captured["params"] = params
        return []

    monkeypatch.setattr(client, "_request", fake_request)

    client.get_trades(token_id="token_123", limit=50)

    assert captured["method"] == "GET"
    assert captured["endpoint"] == "/data/trades"
    assert captured["params"] == {"limit": 50, "token_id": "token_123"}


def test_get_trades_passes_limit_only(monkeypatch):
    client = ClobClient(host="https://example.com")
    captured = {}

    def fake_request(method, endpoint, data=None, headers=None, params=None):
        captured["params"] = params
        return []

    monkeypatch.setattr(client, "_request", fake_request)

    client.get_trades(limit=25)

    assert captured["params"] == {"limit": 25}


@pytest.mark.asyncio
async def test_bot_get_market_price_runs_in_thread(monkeypatch):
    config = Config(safe_address="0x" + "b" * 40)
    bot = TradingBot(config=config)

    class DummyClient:
        def get_market_price(self, token_id):
            return {"price": 0.5, "token_id": token_id}

    bot.clob_client = DummyClient()

    calls = {}

    async def fake_to_thread(func, *args, **kwargs):
        calls["func"] = func
        calls["args"] = args
        calls["kwargs"] = kwargs
        return func(*args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", fake_to_thread)

    result = await bot.get_market_price("token_abc")

    assert calls["func"] == bot.clob_client.get_market_price
    assert calls["args"] == ("token_abc",)
    assert calls["kwargs"] == {}
    assert result["price"] == 0.5
