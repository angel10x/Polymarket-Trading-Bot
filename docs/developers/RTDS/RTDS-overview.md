# Real Time Data Socket

## Overview

The Polymarket Real-Time Data Socket (RTDS) is a WebSocket-based streaming service that provides real-time updates for various Polymarket data streams. The service allows clients to subscribe to multiple data feeds simultaneously and receive live updates as events occur on the platform.

<Note>Polymarket provides a Typescript client for interacting with this streaming service. [Download and view it's documentation here](https://github.com/Polymarket/real-time-data-client)</Note>

### Connection Details

* **WebSocket URL**: `wss://ws-live-data.polymarket.com`
* **Protocol**: WebSocket
* **Data Format**: JSON

### Authentication

The RTDS supports two types of authentication depending on the subscription type:

1. **CLOB Authentication**: Required for certain trading-related subscriptions
   * `key`: API key
   * `secret`: API secret
   * `passphrase`: API passphrase

2. **Gamma Authentication**: Required for user-specific data
   * `address`: User wallet address

### Connection Management

The WebSocket connection supports:

* **Dynamic Subscriptions**: Without disconnecting from the socket users can add, remove and modify topics and filters they are subscribed to.
* **Ping/Pong**: You should send PING messages (every 5 seconds ideally) to maintain connection

## Available Subscription Types

<Note>Although this connection technically supports additional activity and subscription types, they are not fully supported at this time. Users are free to use them but there may be some unexpected behavior.</Note>

The RTDS currently supports the following subscription types:

1. **[Crypto Prices](/developers/RTDS/RTDS-crypto-prices)** - Real-time cryptocurrency price updates
2. **[Comments](/developers/RTDS/RTDS-comments)** - Comment-related events including reactions

## Message Structure

All messages received from the WebSocket follow this structure:

```json  theme={null}
{
  "topic": "string",
  "type": "string", 
  "timestamp": "number",
  "payload": "object"
}
```

* `topic`: The subscription topic (e.g., "crypto\_prices", "comments", "activity")
* `type`: The message type/event (e.g., "update", "reaction\_created", "orders\_matched")
* `timestamp`: Unix timestamp in milliseconds
* `payload`: Event-specific data object

## Subscription Management

### Subscribe to Topics

To subscribe to data streams, send a JSON message with this structure:

```json  theme={null}
{
  "action": "subscribe",
  "subscriptions": [
    {
      "topic": "topic_name",
      "type": "message_type",
      "filters": "optional_filter_string",
      "clob_auth": {
        "key": "api_key",
        "secret": "api_secret", 
        "passphrase": "api_passphrase"
      },
      "gamma_auth": {
        "address": "wallet_address"
      }
    }
  ]
}
```

### Unsubscribe from Topics

To unsubscribe from data streams, send a similar message with `"action": "unsubscribe"`.

## Error Handling

* Connection errors will trigger automatic reconnection attempts
* Invalid subscription messages may result in connection closure
* Authentication failures will prevent successful subscription to protected topics


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt