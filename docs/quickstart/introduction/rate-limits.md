# API Rate Limits

## How Rate Limiting Works

All rate limits are enforced using Cloudflare's throttling system. When you exceed the maximum configured rate for any endpoint, requests are throttled rather than immediately rejected. This means:

* **Throttling**: Requests over the limit are delayed/queued rather than dropped
* **Burst Allowances**: Some endpoints allow short bursts above the sustained rate
* **Time Windows**: Limits reset based on sliding time windows (e.g., per 10 seconds, per minute)

## General Rate Limits

| Endpoint              | Limit                | Notes                                              |
| --------------------- | -------------------- | -------------------------------------------------- |
| General Rate Limiting | 15000 requests / 10s | Throttle requests over the maximum configured rate |
| "OK" Endpoint         | 100 requests / 10s   | Throttle requests over the maximum configured rate |

## Data API Rate Limits

| Endpoint                     | Limit               | Notes                                              |
| ---------------------------- | ------------------- | -------------------------------------------------- |
| Data API (General)           | 1000 requests / 10s | Throttle requests over the maximum configured rate |
| Data API `/trades`           | 200 requests / 10s  | Throttle requests over the maximum configured rate |
| Data API `/positions`        | 150 requests / 10s  | Throttle requests over the maximum configured rate |
| Data API `/closed-positions` | 150 requests / 10s  | Throttle requests over the maximum configured rate |
| Data API "OK" Endpoint       | 100 requests / 10s  | Throttle requests over the maximum configured rate |

## GAMMA API Rate Limits

| Endpoint                         | Limit               | Notes                                              |
| -------------------------------- | ------------------- | -------------------------------------------------- |
| GAMMA (General)                  | 4000 requests / 10s | Throttle requests over the maximum configured rate |
| GAMMA Get Comments               | 200 requests / 10s  | Throttle requests over the maximum configured rate |
| GAMMA `/events`                  | 300 requests / 10s  | Throttle requests over the maximum configured rate |
| GAMMA `/markets`                 | 300 requests / 10s  | Throttle requests over the maximum configured rate |
| GAMMA `/markets` /events listing | 400 requests / 10s  | Throttle requests over the maximum configured rate |
| GAMMA Tags                       | 200 requests / 10s  | Throttle requests over the maximum configured rate |
| GAMMA Search                     | 300 requests / 10s  | Throttle requests over the maximum configured rate |

## CLOB API Rate Limits

### General CLOB Endpoints

| Endpoint                      | Limit               | Notes                                              |
| ----------------------------- | ------------------- | -------------------------------------------------- |
| CLOB (General)                | 9000 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB GET Balance Allowance    | 200 requests / 10s  | Throttle requests over the maximum configured rate |
| CLOB UPDATE Balance Allowance | 50 requests / 10s   | Throttle requests over the maximum configured rate |

### CLOB Market Data

| Endpoint          | Limit               | Notes                                              |
| ----------------- | ------------------- | -------------------------------------------------- |
| CLOB `/book`      | 1500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/books`     | 500 requests / 10s  | Throttle requests over the maximum configured rate |
| CLOB `/price`     | 1500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/prices`    | 500 requests / 10s  | Throttle requests over the maximum configured rate |
| CLOB `/midprice`  | 1500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/midprices` | 500 requests / 10s  | Throttle requests over the maximum configured rate |

### CLOB Ledger Endpoints

| Endpoint                                                    | Limit              | Notes                                              |
| ----------------------------------------------------------- | ------------------ | -------------------------------------------------- |
| CLOB Ledger (`/trades` `/orders` `/notifications` `/order`) | 900 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Ledger `/data/orders`                                  | 500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Ledger `/data/trades`                                  | 500 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB `/notifications`                                       | 125 requests / 10s | Throttle requests over the maximum configured rate |

### CLOB Markets & Pricing

| Endpoint              | Limit               | Notes                                              |
| --------------------- | ------------------- | -------------------------------------------------- |
| CLOB Price History    | 1000 requests / 10s | Throttle requests over the maximum configured rate |
| CLOB Market Tick Size | 200 requests / 10s  | Throttle requests over the maximum configured rate |

### CLOB Authentication

| Endpoint      | Limit              | Notes                                              |
| ------------- | ------------------ | -------------------------------------------------- |
| CLOB API Keys | 100 requests / 10s | Throttle requests over the maximum configured rate |

### CLOB Trading Endpoints

| Endpoint                            | Limit                              | Notes                                                      |
| ----------------------------------- | ---------------------------------- | ---------------------------------------------------------- |
| CLOB POST `/order`                  | 3500 requests / 10s (500/s)        | BURST - Throttle requests over the maximum configured rate |
| CLOB POST `/order`                  | 36000 requests / 10 minutes (60/s) | Throttle requests over the maximum configured rate         |
| CLOB DELETE `/order`                | 3000 requests / 10s (300/s)        | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/order`                | 30000 requests / 10 minutes (50/s) | Throttle requests over the maximum configured rate         |
| CLOB POST `/orders`                 | 1000 requests / 10s (100/s)        | BURST - Throttle requests over the maximum configured rate |
| CLOB POST `/orders`                 | 15000 requests / 10 minutes (25/s) | Throttle requests over the maximum configured rate         |
| CLOB DELETE `/orders`               | 1000 requests / 10s (100/s)        | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/orders`               | 15000 requests / 10 minutes (25/s) | Throttle requests over the maximum configured rate         |
| CLOB DELETE `/cancel-all`           | 250 requests / 10s (25/s)          | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/cancel-all`           | 6000 requests / 10 minutes (10/s)  | Throttle requests over the maximum configured rate         |
| CLOB DELETE `/cancel-market-orders` | 1000 requests / 10s (100/s)        | BURST - Throttle requests over the maximum configured rate |
| CLOB DELETE `/cancel-market-orders` | 1500 requests / 10 minutes (25/s)  | Throttle requests over the maximum configured rate         |

## Other API Rate Limits

| Endpoint          | Limit                  | Notes                                              |
| ----------------- | ---------------------- | -------------------------------------------------- |
| RELAYER `/submit` | 25 requests / 1 minute | Throttle requests over the maximum configured rate |
| User PNL API      | 200 requests / 10s     | Throttle requests over the maximum configured rate |


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt