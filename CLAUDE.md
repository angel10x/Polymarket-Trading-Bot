# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A beginner-friendly Python trading bot for Polymarket with gasless transactions via Builder Program. Uses EIP-712 signing for orders, encrypted private key storage, and supports both the CLOB API and Relayer API.

## Common Commands

```bash
# Setup (first time)
pip install -r requirements.txt
cp .env.example .env  # Edit with your credentials
source .env

# Run quickstart example
python examples/quickstart.py

# Run full integration test
python scripts/full_test.py

# Run the bot
python scripts/run_bot.py              # Quick demo
python scripts/run_bot.py --interactive # Interactive mode

# Testing
pytest tests/ -v                        # Run all tests (89 tests)
pytest tests/test_utils.py -v           # Test utility functions
pytest tests/test_bot.py -v             # Test bot module
pytest tests/test_crypto.py -v          # Test encryption
pytest tests/test_signer.py -v          # Test EIP-712 signing
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         TradingBot                          │
│                        (bot.py)                             │
│  - High-level trading interface                             │
│  - Async order operations                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
┌─────────────┐ ┌───────────┐ ┌───────────────┐
│ OrderSigner │ │ ClobClient│ │ RelayerClient │
│ (signer.py) │ │(client.py)│ │ (client.py)   │
│             │ │           │ │               │
│ EIP-712     │ │ Order     │ │ Gasless       │
│ signatures  │ │ submission│ │ transactions  │
└──────┬──────┘ └─────┬─────┘ └───────────────┘
       │              │
       ▼              ▼
┌─────────────┐ ┌───────────┐
│ KeyManager  │ │  Config   │
│ (crypto.py) │ │(config.py)│
│             │ │           │
│ PBKDF2 +    │ │ YAML/ENV  │
│ Fernet      │ │ loading   │
└─────────────┘ └───────────┘
```

### Module Responsibilities

| Module | Purpose | Key Classes |
|--------|---------|-------------|
| `bot.py` | Main trading interface | `TradingBot`, `OrderResult` |
| `client.py` | API communication | `ClobClient`, `RelayerClient` |
| `signer.py` | EIP-712 signing | `OrderSigner`, `Order` |
| `crypto.py` | Key encryption | `KeyManager` |
| `config.py` | Configuration | `Config`, `BuilderConfig` |
| `utils.py` | Helper functions | `create_bot_from_env`, `validate_address` |

### Data Flow

1. `TradingBot.place_order()` creates an `Order` dataclass
2. `OrderSigner.sign_order()` produces EIP-712 signature
3. `ClobClient.post_order()` submits to CLOB with Builder HMAC auth headers
4. If gasless enabled, `RelayerClient` handles Safe deployment/approvals

## Key Patterns

- **Async methods**: All trading operations (`place_order`, `cancel_order`, `get_trades`) are async
- **Config precedence**: Environment vars > YAML file > defaults
- **Builder HMAC auth**: Timestamp + method + path + body signed with api_secret
- **Signature type 2**: Gnosis Safe signatures for Polymarket

## Configuration

Config loads from `config.yaml` or environment variables:

```python
# From environment
config = Config.from_env()

# From YAML
config = Config.load("config.yaml")

# With env overrides
config = Config.load_with_env("config.yaml")
```

Key fields:
- `safe_address`: Your Polymarket proxy wallet address
- `builder.api_key/api_secret/api_passphrase`: For gasless trading
- `clob.chain_id`: 137 (Polygon mainnet)

## Testing Notes

- Tests use `pytest` with `pytest-asyncio` for async
- Mock external API calls; never hit real Polymarket APIs in tests
- Test private key: `"0x" + "a" * 64`
- Test safe address: `"0x" + "b" * 40`
- YAML config values starting with `0x` must be quoted to avoid integer parsing

## Dependencies

- `eth-account>=0.13.0`: Uses new `encode_typed_data` API
- `web3>=6.0.0`: Polygon RPC interactions
- `cryptography`: Fernet encryption for private keys
- `pyyaml`: YAML config file support
- `python-dotenv`: .env file loading

## Polymarket API Context

- CLOB API: `https://clob.polymarket.com` - order submission/cancellation
- Relayer API: `https://relayer-v2.polymarket.com` - gasless transactions
- Token IDs are ERC-1155 identifiers for market outcomes
- Prices are 0-1 (probability percentages)
- USDC has 6 decimal places

**Important**: The `docs/` directory contains official Polymarket documentation. When implementing or debugging API features, always reference:
- `docs/developers/CLOB/` - CLOB API endpoints, authentication, orders
- `docs/developers/builders/` - Builder Program, Relayer, gasless transactions
- `docs/api-reference/` - REST API endpoint specifications

## For Beginners

Start with these files in order:
1. `examples/quickstart.py` - Simplest possible example
2. `examples/basic_trading.py` - Common operations
3. `src/bot.py` - Read the TradingBot class
4. `examples/strategy_example.py` - Custom strategy framework
