# RTDS Crypto Prices

<Note>Polymarket provides a Typescript client for interacting with this streaming service. [Download and view it's documentation here](https://github.com/Polymarket/real-time-data-client)</Note>

## Overview

The crypto prices subscription provides real-time updates for cryptocurrency price data from two different sources:

* **Binance Source** (`crypto_prices`): Real-time price data from Binance exchange
* **Chainlink Source** (`crypto_prices_chainlink`): Price data from Chainlink oracle networks

Both streams deliver current market prices for various cryptocurrency trading pairs, but use different symbol formats and subscription structures.

## Binance Source (`crypto_prices`)

### Subscription Details

* **Topic**: `crypto_prices`
* **Type**: `update`
* **Authentication**: Not required
* **Filters**: Optional (specific symbols can be filtered)
* **Symbol Format**: Lowercase concatenated pairs (e.g., `solusdt`, `btcusdt`)

### Subscription Message

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "crypto_prices",
      "type": "update"
    }
  ]
}
```

### With Symbol Filter

To subscribe to specific cryptocurrency symbols, include a filters parameter:

```json  theme={null}
{
  "action": "subscribe", 
  "subscriptions": [
    {
      "topic": "crypto_prices",
      "type": "update",
      "filters": "solusdt,btcusdt,ethusdt"
    }
  ]
}
```

## Chainlink Source (`crypto_prices_chainlink`)

### Subscription Details

* **Topic**: `crypto_prices_chainlink`
* **Type**: `*` (all types)
* **Authentication**: Not required
* **Filters**: Optional (JSON object with symbol specification)
* **Symbol Format**: Slash-separated pairs (e.g., `eth/usd`, `btc/usd`)

### Subscription Message

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "crypto_prices_chainlink",
      "type": "*",
      "filters": ""
    }
  ]
}
```

### With Symbol Filter

To subscribe to specific cryptocurrency symbols, include a JSON filters parameter:

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "crypto_prices_chainlink",
      "type": "*",
      "filters": "{\"symbol\":\"eth/usd\"}"
    }
  ]
}
```

## Message Format

### Binance Source Message Format

When subscribed to Binance crypto prices (`crypto_prices`), you'll receive messages with the following structure:

```json  theme={null}
{
  "topic": "crypto_prices",
  "type": "update", 
  "timestamp": 1753314064237,
  "payload": {
    "symbol": "solusdt",
    "timestamp": 1753314064213,
    "value": 189.55
  }
}
```

### Chainlink Source Message Format

When subscribed to Chainlink crypto prices (`crypto_prices_chainlink`), you'll receive messages with the following structure:

```json  theme={null}
{
  "topic": "crypto_prices_chainlink",
  "type": "update", 
  "timestamp": 1753314064237,
  "payload": {
    "symbol": "eth/usd",
    "timestamp": 1753314064213,
    "value": 3456.78
  }
}
```

## Payload Fields

| Field       | Type   | Description                                                                                                                                                |
| ----------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `symbol`    | string | Trading pair symbol<br />**Binance**: lowercase concatenated (e.g., "solusdt", "btcusdt")<br />**Chainlink**: slash-separated (e.g., "eth/usd", "btc/usd") |
| `timestamp` | number | Price timestamp in Unix milliseconds                                                                                                                       |
| `value`     | number | Current price value in the quote currency                                                                                                                  |

## Example Messages

### Binance Source Examples

#### Solana Price Update (Binance)

```json  theme={null}
{
  "topic": "crypto_prices",
  "type": "update",
  "timestamp": 1753314064237,
  "payload": {
    "symbol": "solusdt", 
    "timestamp": 1753314064213,
    "value": 189.55
  }
}
```

#### Bitcoin Price Update (Binance)

```json  theme={null}
{
  "topic": "crypto_prices",
  "type": "update", 
  "timestamp": 1753314088421,
  "payload": {
    "symbol": "btcusdt",
    "timestamp": 1753314088395,
    "value": 67234.50
  }
}
```

### Chainlink Source Examples

#### Ethereum Price Update (Chainlink)

```json  theme={null}
{
  "topic": "crypto_prices_chainlink",
  "type": "update",
  "timestamp": 1753314064237,
  "payload": {
    "symbol": "eth/usd", 
    "timestamp": 1753314064213,
    "value": 3456.78
  }
}
```

#### Bitcoin Price Update (Chainlink)

```json  theme={null}
{
  "topic": "crypto_prices_chainlink",
  "type": "update", 
  "timestamp": 1753314088421,
  "payload": {
    "symbol": "btc/usd",
    "timestamp": 1753314088395,
    "value": 67234.50
  }
}
```

## Supported Symbols

### Binance Source Symbols

The Binance source supports various cryptocurrency trading pairs using lowercase concatenated format:

* `btcusdt` - Bitcoin to USDT
* `ethusdt` - Ethereum to USDT
* `solusdt` - Solana to USDT
* `xrpusdt` - XRP to USDT

### Chainlink Source Symbols

The Chainlink source supports cryptocurrency trading pairs using slash-separated format:

* `btc/usd` - Bitcoin to USD
* `eth/usd` - Ethereum to USD
* `sol/usd` - Solana to USD
* `xrp/usd` - XRP to USD

## Notes

### General

* Price updates are sent as market prices change
* The timestamp in the payload represents when the price was recorded
* The outer timestamp represents when the message was sent via WebSocket
* No authentication is required for crypto price data


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt