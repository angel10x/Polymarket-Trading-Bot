# Polymarket Bot

<div align="center">

![Rust](https://img.shields.io/badge/python-3.12+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

[English](#polymarket-bot) • [简体中文](README.zh-CN.md)

</div>

Don’t stress the process — focus on the results. 

That’s how I approach trading. What about you? 

I have a feeling you see it the same way, so let’s run it.

## Important notice

This software is a **copy-trading bot** that replicates positions from a chosen wallet on Polymarket. The current release (v1) does not include built-in strategy logic, risk controls, or guarantees of profitability. Outcomes depend on the tracked wallet, your sizing, and market conditions. You can extend or adapt the code to implement your own risk and strategy layers. A newer version exists but is not publicly released; updates and support will continue to be provided over time.

### Contact
- [Discussions](../../discussions)
- [WhatsApp](https://wa.me/16286666724?text=Hello%20there)
- [Telegram](https://t.me/angel_10_x)
- [Discord](https://discord.com/users/1114372741672488990)

## Why python?

I still remember the moment I decided to build my Polymarket bot.

At first, I stood at the familiar crossroads every developer knows too well ' which language should I trust with something that needed to be fast, reliable, and intelligent? TypeScript tempted me with its structured ecosystem and rich tooling. Other languages promised performance or strict type guarantees. But none of them felt like the right companion for the journey I was about to begin.

Because this wasn't just another script.

This was a living system ' a bot that would observe markets, interpret signals, adapt to uncertainty, and act with precision in a space where probabilities shift like tides.

And that is why I chose Python.

Python didn't just offer syntax; it offered *flow*. The code felt like thought translated directly into action. When I began wiring together market data ingestion, event interpretation, and strategy logic, Python allowed me to move at the speed of curiosity. Ideas became prototypes in minutes. Strategies evolved overnight. Refactors felt like gentle edits rather than structural battles.

But the deeper reason was intelligence.

Building a Polymarket bot is not merely about sending transactions, it's about understanding context. Parsing sentiment, modeling probabilities, experimenting with reinforcement signals, and testing hypotheses rapidly. Python's ecosystem placed an entire laboratory at my fingertips: data analysis tools, statistical libraries, async frameworks, and machine learning capabilities that transformed the project from a trading bot into an experimental platform.

TypeScript could orchestrate APIs elegantly.
Python could help me *think*.

There was also a quiet comfort in Python's readability. Weeks later, when strategies became layered and decision paths intertwined, I could still open a file and understand my past self. The code read like notes from a conversation rather than instructions carved in stone. That clarity made iteration fearless.

And iteration is survival in prediction markets.

Python also became the bridge between research and execution. I could simulate strategies, visualize outcomes, tweak assumptions, and immediately embed those insights back into the bot's runtime behavior. The boundary between experimentation and production dissolved.

What surprised me most, though, was the emotional dimension.

Late nights debugging WebSocket streams, watching probabilities flicker, seeing the first autonomous trade execute successfully ' Python made those moments feel collaborative rather than adversarial. The language faded into the background, leaving only the problem space and my curiosity.

The Polymarket bot eventually became more than automation.
It became a narrative of decisions, risks, and evolving understanding.

Choosing Python was not about rejecting TypeScript or other languages. It was about selecting the medium that best matched the nature of the problem ' dynamic, exploratory, data-driven, and adaptive.

In the end, Python didn't just power the bot.

It powered the process of discovery that made the bot possible.


## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment**

   Copy `.env.example` to `.env` and set your Polymarket credentials:

   ```
   POLYMARKET_PRIVATE_KEY=your_private_key
   POLYMARKET_PROXY_ADDRESS=your_proxy_address
   ```

3. **Config**

   Create or edit `config.json` in the project root:

   ```json
   {
       "wallets_to_track": ["0x..."],
       "copy_percentage": 1.0,
       "rate_limit": 25,
       "poll_interval": 0.5,
       "trading_enabled": true
   }
   ```

### Configuration options

| Option              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `wallets_to_track`  | List of wallet addresses to copy.                                          |
| `copy_percentage`   | Size relative to tracked wallet (e.g. `1.0` = 100%, `0.5` = 50%).          |
| `rate_limit`       | Max API requests per 10-second window (default: 25).                        |
| `poll_interval`     | Seconds between position checks (default: 0.5; min 0.3). Lower = faster detection. |
| `trading_enabled`  | If `false`, only logs what would be done (dry run).                         |

## Running

From the project root:

```bash
python main.py
```

Or run as a module:

```bash
python -m polymarket_copy_trader
```

Press `Ctrl+C` to stop.

### Dashboard

Run the web UI to start/stop the bot and view live logs:

```bash
python -m uvicorn dashboard.app:app --reload --host 0.0.0.0 --port 8000
```

Open [http://localhost:8000](http://localhost:8000). The sidebar lists all bots (Copy Trader, Arbitrage, Sports Betting, Market Maker). Only Copy Trader is runnable today; use **Start** / **Stop** and **Config** for it; logs stream in real time. Other bots show "Coming soon."

## License

See [LICENSE](LICENSE).
