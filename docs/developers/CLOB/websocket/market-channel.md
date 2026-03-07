# Market Channel

Public channel for updates related to market updates (level 2 price data).

**SUBSCRIBE**

`<wss-channel> market`

## Book Message

Emitted When:

* First subscribed to a market
* When there is a trade that affects the book

### Structure

| Name        | Type            | Description                                                                 |
| ----------- | --------------- | --------------------------------------------------------------------------- |
| event\_type | string          | "book"                                                                      |
| asset\_id   | string          | asset ID (token ID)                                                         |
| market      | string          | condition ID of market                                                      |
| timestamp   | string          | unix timestamp the current book generation in milliseconds (1/1,000 second) |
| hash        | string          | hash summary of the orderbook content                                       |
| buys        | OrderSummary\[] | list of type (size, price) aggregate book levels for buys                   |
| sells       | OrderSummary\[] | list of type (size, price) aggregate book levels for sells                  |

Where a `OrderSummary` object is of the form:

| Name  | Type   | Description                        |
| ----- | ------ | ---------------------------------- |
| price | string | size available at that price level |
| size  | string | price of the orderbook level       |

```json Response theme={null}
{
  "event_type": "book",
  "asset_id": "65818619657568813474341868652308942079804919287380422192892211131408793125422",
  "market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
  "bids": [
    { "price": ".48", "size": "30" },
    { "price": ".49", "size": "20" },
    { "price": ".50", "size": "15" }
  ],
  "asks": [
    { "price": ".52", "size": "25" },
    { "price": ".53", "size": "60" },
    { "price": ".54", "size": "10" }
  ],
  "timestamp": "123456789000",
  "hash": "0x0...."
}
```

## price\_change Message

<div style={{backgroundColor: '#fff3cd', border: '1px solid #ffeaa7', borderRadius: '4px', padding: '12px', marginBottom: '16px'}}>
  <strong>⚠️ Breaking Change Notice:</strong> The price\_change message schema will be updated on September 15, 2025 at 11 PM UTC. Please see the [migration guide](/developers/CLOB/websocket/market-channel-migration-guide) for details.
</div>

Emitted When:

* A new order is placed
* An order is cancelled

### Structure

| Name           | Type           | Description                    |
| -------------- | -------------- | ------------------------------ |
| event\_type    | string         | "price\_change"                |
| market         | string         | condition ID of market         |
| price\_changes | PriceChange\[] | array of price change objects  |
| timestamp      | string         | unix timestamp in milliseconds |

Where a `PriceChange` object is of the form:

| Name      | Type   | Description                        |
| --------- | ------ | ---------------------------------- |
| asset\_id | string | asset ID (token ID)                |
| price     | string | price level affected               |
| size      | string | new aggregate size for price level |
| side      | string | "BUY" or "SELL"                    |
| hash      | string | hash of the order                  |
| best\_bid | string | current best bid price             |
| best\_ask | string | current best ask price             |

```json Response theme={null}
{
    "market": "0x5f65177b394277fd294cd75650044e32ba009a95022d88a0c1d565897d72f8f1",
    "price_changes": [
        {
            "asset_id": "71321045679252212594626385532706912750332728571942532289631379312455583992563",
            "price": "0.5",
            "size": "200",
            "side": "BUY",
            "hash": "56621a121a47ed9333273e21c83b660cff37ae50",
            "best_bid": "0.5",
            "best_ask": "1"
        },
        {
            "asset_id": "52114319501245915516055106046884209969926127482827954674443846427813813222426",
            "price": "0.5",
            "size": "200",
            "side": "SELL",
            "hash": "1895759e4df7a796bf4f1c5a5950b748306923e2",
            "best_bid": "0",
            "best_ask": "0.5"
        }
    ],
    "timestamp": "1757908892351",
    "event_type": "price_change"
}
```

## tick\_size\_change Message

Emitted When:

* The minimum tick size of the market changes. This happens when the book's price reaches the limits: price > 0.96 or price \< 0.04

### Structure

| Name            | Type   | Description                |
| --------------- | ------ | -------------------------- |
| event\_type     | string | "price\_change"            |
| asset\_id       | string | asset ID (token ID)        |
| market          | string | condition ID of market     |
| old\_tick\_size | string | previous minimum tick size |
| new\_tick\_size | string | current minimum tick size  |
| side            | string | buy/sell                   |
| timestamp       | string | time of event              |

```json Response theme={null}
{
"event_type": "tick_size_change",
"asset_id": "65818619657568813474341868652308942079804919287380422192892211131408793125422",\
"market": "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
"old_tick_size": "0.01",
"new_tick_size": "0.001",
"timestamp": "100000000"
}
```

## last\_trade\_price Message

Emitted When:

* When a maker and taker order is matched creating a trade event.

```json Response theme={null}
{
"asset_id":"114122071509644379678018727908709560226618148003371446110114509806601493071694",
"event_type":"last_trade_price",
"fee_rate_bps":"0",
"market":"0x6a67b9d828d53862160e470329ffea5246f338ecfffdf2cab45211ec578b0347",
"price":"0.456",
"side":"BUY",
"size":"219.217767",
"timestamp":"1750428146322"
}
```


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt