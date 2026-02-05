# Polymarket Copy Trader

A simple bot to track and copy positions on Polymarket. Built with [pmxt](https://github.com/pmxt-dev/pmxt)

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your credentials:
   ```
   POLYMARKET_PRIVATE_KEY=your_private_key
   POLYMARKET_PROXY_ADDRESS=your_proxy_address
   ```
3. Configure `config.json`:
   ```json
   {
       "wallets_to_track": ["0x..."],
       "copy_percentage": 1.0,
       "rate_limit": 25,
       "trading_enabled": true
   }
   ```

## Configuration

- `wallets_to_track`: List of wallet addresses to follow.
- `copy_percentage`: How much to copy relative to their size (e.g., `1.0` = 100%, `0.2` = 20%, `2.0` = 200%).
- `rate_limit`: The maximum number of API requests allowed per 10-second window (default is 25).
- `trading_enabled`: If `false`, the bot will only log what it would do.

## Running

```bash
python src/main.py
```
