# Polymarket Changelog

> Welcome to the Polymarket Changelog. Here you will find any important changes to Polymarket, including but not limited to CLOB, API, UI and Mobile Applications.

<Update label="Sept 24, 2025" description="Polymarket Real-Time Data Socket (RTDS) official release">
  * **Crypto Price Feeds**: Access real-time cryptocurrency prices from two sources (Binance & Chainlink)
  * **Comment Streaming**: Real-time updates for comment events including new comments, replies, and reactions
  * **Dynamic Subscriptions**: Add, remove, and modify subscriptions without reconnecting
  * **TypeScript Client**: Official TypeScript client available at [real-time-data-client](https://github.com/Polymarket/real-time-data-client)
    For complete documentation, see [RTDS Overview](/developers/RTDS/RTDS-overview).
</Update>

<Update label="September 15, 2025" description="WSS price_change event update">
  * There has been a significant change to the structure of the price change message. This update will be applied at 11PM UTC September 15, 2025. We apologize for the short notice
    * Please see the [migration guide](/developers/CLOB/websocket/market-channel-migration-guide) for details.
</Update>

<Update label="August 26, 2025" description="Updated /trades and /activity endpoints">
  * Reduced maximum values for query parameters on Data-API /trades and /activity:
    * `limit`: 500
    * `offset`: 1,000
</Update>

<Update label="August 21, 2025" description="Batch Orders Increase">
  * The batch orders limit has been increased from from 5 -> 15. Read more about the batch orders functionality [here](/developers/CLOB/orders/create-order-batch).
</Update>

<Update label="July 23, 2025" description="Get Book(s) update">
  * We’re adding new fields to the `get-book` and `get-books` CLOB endpoints to include key market metadata that previously required separate queries.
    * `min_order_size`
      * type: string
      * description: Minimum allowed order size.
    * `neg_risk`
      * type: boolean
      * description: Boolean indicating whether the market is neg\_risk.
    * `tick_size`
      * type: string
      * description: Minimum allowed order size.
</Update>

<Update label="June 3, 2025" description="New Batch Orders Endpoint">
  * We’re excited to roll out a highly requested feature: **order batching**. With this new endpoint, users can now submit up to five trades in a single request. To help you get started, we’ve included sample code demonstrating how to use it. Please see [Place Multiple Orders (Batching)](/developers/CLOB/orders/create-order-batch) for more details.
</Update>

<Update label="June 3, 2025" description="Change to /data/trades">
  * We're adding a new `side` field to the `MakerOrder` portion of the trade object. This field will indicate whether the maker order is a `buy` or `sell`, helping to clarify trade events where the maker side was previously ambiguous. For more details, refer to the MakerOrder object on the [Get Trades](/developers/CLOB/trades/trades) page.
</Update>

<Update label="May 28, 2025" description="Websocket Changes">
  * The 100 token subscription limit has been removed for the Markets channel. You can now subscribe to as many token IDs as needed for your use case.
  * New Subscribe Field `initial_dump`
    * Optional field to indicate whether you want to receive the initial order book state when subscribing to a token or list of tokens.
    * `default: true`
</Update>

<Update label="May 28, 2025" description="New FAK Order Type">
  We’re excited to introduce a new order type soon to be available to all users: Fill and Kill (FAK). FAK orders behave similarly to the well-known Fill or Kil(FOK) orders, but with a key difference:

  * FAK will fill as many shares as possible immediately at your specified price, and any remaining unfilled portion will be canceled.
  * Unlike FOK, which requires the entire order to fill instantly or be canceled, FAK is more flexible and aims to capture partial fills if possible.
</Update>

<Update label="May 15, 2025" description="Increased API Rate Limits">
  All API users will enjoy increased rate limits for the CLOB endpoints.

  * CLOB - /books (website) (300req - 10s / Throttle requests over the maximum configured rate)
  * CLOB - /books (50 req - 10s / Throttle requests over the maximum configured rate)
  * CLOB - /price (100req - 10s / Throttle requests over the maximum configured rate)
  * CLOB markets/0x (50req / 10s - Throttle requests over the maximum configured rate)
  * CLOB POST /order - 500 every 10s (50/s) - (BURST) - Throttle requests over the maximum configured rateed
  * CLOB POST /order - 3000 every 10 minutes (5/s) - Throttle requests over the maximum configured rate
  * CLOB DELETE /order - 500 every 10s (50/s) - (BURST) - Throttle requests over the maximum configured rate
  * DELETE /order - 3000 every 10 minutes (5/s) - Throttle requests over the maximum configured rate
</Update>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt