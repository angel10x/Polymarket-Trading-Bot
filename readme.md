# 🚀 Polymarket Trading Bot

**A powerful yet beginner‑friendly Python trading bot for Polymarket.**
Built for **crypto traders, quant developers, and prediction market
enthusiasts** who want to automate trading strategies with **real‑time
data, gasless execution, and clean developer APIs**.

Want to learn more or get setup help? Please connect with our techy team on Telegram: @qntrade 🚀

------------------------------------------------------------------------

# ⚡ Why Traders Love This Bot

• **Trade Polymarket programmatically in minutes**\
• **Gasless trading support** (Builder Program ready)\
• **Real‑time orderbook via WebSocket**\
• **Built‑in volatility strategies**\
• **Clean Python API for building custom strategies**\
• **Live terminal orderbook interface**\
• **Secure private‑key encryption**\
• **Fully tested production‑ready architecture**

Whether you're **testing alpha**, **running automated strategies**, or
**learning prediction market trading**, this bot gives you a powerful
foundation.

------------------------------------------------------------------------

# 📦 Features

### ⚡ Simple API

Start trading with only a few lines of Python.

### ⛽ Gasless Transactions

Use Polymarket Builder credentials to trade **without paying gas**.

### 📡 Real-Time WebSocket Data

Receive **live orderbook updates and mid‑price feeds**.

### 📊 15-Minute Markets Support

Automatically discovers **BTC / ETH / SOL / XRP 15‑minute Up/Down
markets**.

### 🧠 Flash Crash Strategy

Pre‑built strategy that detects **sudden probability crashes** and
trades volatility.

### 🖥 Terminal Trading UI

Beautiful real‑time **orderbook visualization inside your terminal**.

### 🔐 Secure Key Storage

Private keys encrypted with:

-   PBKDF2 (480,000 iterations)
-   Fernet symmetric encryption
-   Secure file permissions

### 🧪 Fully Tested

Includes **89 unit tests** covering the trading engine.

------------------------------------------------------------------------

# ⚡ Quick Start (5 Minutes)

## 1️⃣ Clone Repository

``` bash
git clone https://github.com/qntrade/polymarket-trading-bot.git
cd polymarket-trading-bot
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 2️⃣ Configure Credentials

``` bash
export POLY_PRIVATE_KEY=your_metamask_private_key
export POLY_SAFE_ADDRESS=0xYourPolymarketSafeAddress
```

Find your Safe address at:

👉 https://polymarket.com/settings

------------------------------------------------------------------------

## 3️⃣ Run the Bot

``` bash
python examples/quickstart.py
```

Or launch the **Flash Crash trading strategy**:

``` bash
python strategies/flash_crash_strategy.py --coin BTC
```

That's it.

You're now trading Polymarket automatically.

------------------------------------------------------------------------

# 📈 Built‑In Strategy

## Flash Crash Strategy

Detects sudden probability drops and buys the crash.

### Example

``` bash
python strategies/flash_crash_strategy.py --coin BTC
```

### Custom Settings

``` bash
python strategies/flash_crash_strategy.py --coin ETH --drop 0.25 --size 10
```

### Strategy Logic

1.  Discover current 15‑minute market
2.  Monitor prices via WebSocket
3.  Detect sudden price crash
4.  Buy undervalued side
5.  Exit with take‑profit or stop‑loss

Default parameters:

  Parameter          Default
  ------------------ ---------
  Drop Threshold     0.30
  Detection Window   10s
  Trade Size         \$5
  Take Profit        \$0.10
  Stop Loss          \$0.05

------------------------------------------------------------------------

# 🧑‍💻 Developer Friendly API

### Minimal Example

``` python
from src import create_bot_from_env
import asyncio

async def main():
    bot = create_bot_from_env()
    orders = await bot.get_open_orders()
    print(len(orders))

asyncio.run(main())
```

------------------------------------------------------------------------

### Place an Order

``` python
result = await bot.place_order(
    token_id="123...",
    price=0.65,
    size=10,
    side="BUY"
)
```

------------------------------------------------------------------------

# 📡 Real-Time Market Data

``` python
@ws.on_book
async def on_book_update(snapshot):
    print(snapshot.mid_price)
```

Perfect for:

• market‑making bots\
• arbitrage strategies\
• latency‑sensitive trading systems

------------------------------------------------------------------------

# 📊 Terminal Orderbook Viewer

View live orderbook updates directly in terminal:

``` bash
python strategies/orderbook_tui.py --coin BTC --levels 5
```

Great for **manual traders monitoring liquidity**.

------------------------------------------------------------------------

# ⚙️ Configuration

Environment variables:

  Variable                      Description
  ----------------------------- --------------------
  POLY_PRIVATE_KEY              Wallet private key
  POLY_SAFE_ADDRESS             Polymarket Safe
  POLY_BUILDER_API_KEY          Builder API key
  POLY_BUILDER_API_SECRET       Builder secret
  POLY_BUILDER_API_PASSPHRASE   Builder passphrase

------------------------------------------------------------------------

# ⛽ Gasless Trading

To enable **zero‑gas execution**:

1.  Apply to Builder Program
2.  Set credentials

``` bash
export POLY_BUILDER_API_KEY=...
export POLY_BUILDER_API_SECRET=...
export POLY_BUILDER_API_PASSPHRASE=...
```

The bot will automatically switch to **gasless mode**.

------------------------------------------------------------------------

# 🧪 Testing

Run tests:

``` bash
pytest tests/ -v
```

Coverage:

``` bash
pytest --cov=src
```

------------------------------------------------------------------------

# 🔐 Security Best Practices

• Never commit private keys\
• Use a dedicated trading wallet\
• Keep encrypted key files private\
• Rotate API credentials regularly

------------------------------------------------------------------------

# 📜 License

MIT License

------------------------------------------------------------------------

# 🔥 Join the Trader Community

Stay updated with new strategies, bots, and alpha.

👉 Telegram: https://t.me/qntrade

------------------------------------------------------------------------

# ⭐ Support the Project

If you find this useful:

• Star the repository\
• Share with other traders\
• Build your own strategies on top of it

Happy Trading 🚀
