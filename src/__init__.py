"""
Polymarket Trading Bot - A Simple Python Trading Library

A production-ready trading bot for Polymarket with:
- Encrypted private key storage (PBKDF2 + Fernet)
- Gasless transactions via Builder Program
- Modular architecture for easy extension
- Comprehensive testing

Quick Start:
    # Option 1: From environment variables
    from src import create_bot_from_env
    bot = create_bot_from_env()

    # Option 2: Manual configuration
    from src import TradingBot, Config
    config = Config(safe_address="0x...")
    bot = TradingBot(config=config, private_key="0x...")

    # Place an order
    result = await bot.place_order(token_id, price=0.5, size=1.0, side="BUY")

Modules:
    bot.py     - TradingBot class (main interface)
    config.py  - Configuration management
    client.py  - API clients (CLOB, Relayer)
    signer.py  - EIP-712 order signing
    crypto.py  - Private key encryption
    utils.py   - Helper functions
"""

# Core classes
from .bot import TradingBot, OrderResult
from .signer import OrderSigner, Order
from .client import ApiClient, ClobClient, RelayerClient
from .crypto import KeyManager
from .config import Config, BuilderConfig
from .gamma_client import GammaClient
from .websocket_client import MarketWebSocket, OrderbookManager, OrderbookSnapshot

# Utility functions
from .utils import (
    create_bot_from_env,
    validate_address,
    validate_private_key,
    format_price,
    format_usdc,
    truncate_address,
)

__version__ = "1.0.0"
__author__ = "Polymarket Trading Bot Contributors"

__all__ = [
    # Core classes
    "TradingBot",
    "OrderResult",
    "OrderSigner",
    "Order",
    "ApiClient",
    "ClobClient",
    "RelayerClient",
    "KeyManager",
    "Config",
    "BuilderConfig",
    "GammaClient",
    "MarketWebSocket",
    "OrderbookManager",
    "OrderbookSnapshot",
    # Utility functions
    "create_bot_from_env",
    "validate_address",
    "validate_private_key",
    "format_price",
    "format_usdc",
    "truncate_address",
]
