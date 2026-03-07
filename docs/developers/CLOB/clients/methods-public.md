# Public Methods

> These methods can be called without a signer or user credentials. Use these for reading market data, prices, and order books.

## Client Initialization

Public methods require the client to initialize with the host URL and Polygon chain ID.

<Tabs>
  <Tab title="TypeScript">
    ```typescript  theme={null}
    import { ClobClient } from "@polymarket/clob-client";

    const client = new ClobClient(
      "https://clob.polymarket.com",
      137
    );

    // Ready to call public methods
    const markets = await client.getMarkets();
    ```
  </Tab>

  <Tab title="Python">
    ```python  theme={null}
    from py_clob_client.client import ClobClient

    client = ClobClient(
        host="https://clob.polymarket.com",
        chain_id=137
    )

    # Ready to call public methods
    markets = await client.get_markets()
    ```
  </Tab>
</Tabs>

***

## Health Check

***

### getOk()

Health check endpoint to verify the CLOB service is operational.

```typescript Signature theme={null}
async getOk(): Promise<any>
```

***

## Markets

***

### getMarket()

Get details for a single market by condition ID.

```typescript Signature theme={null}
async getMarket(conditionId: string): Promise<Market>
```

```typescript Response theme={null}
interface MarketToken {
  outcome: string;
  price: number;
  token_id: string;
  winner: boolean;
}

interface Market {
  accepting_order_timestamp: string | null;
  accepting_orders: boolean;
  active: boolean;
  archived: boolean;
  closed: boolean;
  condition_id: string;
  description: string;
  enable_order_book: boolean;
  end_date_iso: string;
  fpmm: string;
  game_start_time: string;
  icon: string;
  image: string;
  is_50_50_outcome: boolean;
  maker_base_fee: number;
  market_slug: string;
  minimum_order_size: number;
  minimum_tick_size: number;
  neg_risk: boolean;
  neg_risk_market_id: string;
  neg_risk_request_id: string;
  notifications_enabled: boolean;
  question: string;
  question_id: string;
  rewards: {
    max_spread: number;
    min_size: number;
    rates: any | null;
  };
  seconds_delay: number;
  tags: string[];
  taker_base_fee: number;
  tokens: MarketToken[];
}
```

***

### getMarkets()

Get details for multiple markets paginated.

```typescript Signature theme={null}
async getMarkets(): Promise<PaginationPayload>
```

```typescript Response theme={null}
interface PaginationPayload {
  limit: number;
  count: number;
  data: Market[];
}

interface Market {
  accepting_order_timestamp: string | null;
  accepting_orders: boolean;
  active: boolean;
  archived: boolean;
  closed: boolean;
  condition_id: string;
  description: string;
  enable_order_book: boolean;
  end_date_iso: string;
  fpmm: string;
  game_start_time: string;
  icon: string;
  image: string;
  is_50_50_outcome: boolean;
  maker_base_fee: number;
  market_slug: string;
  minimum_order_size: number;
  minimum_tick_size: number;
  neg_risk: boolean;
  neg_risk_market_id: string;
  neg_risk_request_id: string;
  notifications_enabled: boolean;
  question: string;
  question_id: string;
  rewards: {
    max_spread: number;
    min_size: number;
    rates: any | null;
  };
  seconds_delay: number;
  tags: string[];
  taker_base_fee: number;
  tokens: MarketToken[];
}

interface MarketToken {
  outcome: string;
  price: number;
  token_id: string;
  winner: boolean;
}
```

***

### getSimplifiedMarkets()

Get simplified market data paginated for faster loading.

```typescript Signature theme={null}
async getSimplifiedMarkets(): Promise<PaginationPayload>
```

```typescript Response theme={null}
interface PaginationPayload {
  limit: number;
  count: number;
  data: SimplifiedMarket[];
}

interface SimplifiedMarket {
  accepting_orders: boolean;
  active: boolean;
  archived: boolean;
  closed: boolean;
  condition_id: string;
  rewards: {
    rates: any | null;
    min_size: number;
    max_spread: number;
  };
    tokens: SimplifiedToken[];
}

interface SimplifiedToken {
  outcome: string;
  price: number;
  token_id: string;
}
```

***

### getSamplingMarkets()

```typescript Signature theme={null}
async getSamplingMarkets(): Promise<PaginationPayload>
```

```typescript Response theme={null}
interface PaginationPayload {
  limit: number;
  count: number;
  data: Market[];
}

interface Market {
  accepting_order_timestamp: string | null;
  accepting_orders: boolean;
  active: boolean;
  archived: boolean;
  closed: boolean;
  condition_id: string;
  description: string;
  enable_order_book: boolean;
  end_date_iso: string;
  fpmm: string;
  game_start_time: string;
  icon: string;
  image: string;
  is_50_50_outcome: boolean;
  maker_base_fee: number;
  market_slug: string;
  minimum_order_size: number;
  minimum_tick_size: number;
  neg_risk: boolean;
  neg_risk_market_id: string;
  neg_risk_request_id: string;
  notifications_enabled: boolean;
  question: string;
  question_id: string;
  rewards: {
    max_spread: number;
    min_size: number;
    rates: any | null;
  };
  seconds_delay: number;
  tags: string[];
  taker_base_fee: number;
  tokens: MarketToken[];
}

interface MarketToken {
  outcome: string;
  price: number;
  token_id: string;
  winner: boolean;
}
```

***

### getSamplingSimplifiedMarkets()

```typescript Signature theme={null}
async getSamplingSimplifiedMarkets(): Promise<PaginationPayload>
```

```typescript Response theme={null}
interface PaginationPayload {
  limit: number;
  count: number;
  data: SimplifiedMarket[];
}

interface SimplifiedMarket {
  accepting_orders: boolean;
  active: boolean;
  archived: boolean;
  closed: boolean;
  condition_id: string;
  rewards: {
    rates: any | null;
    min_size: number;
    max_spread: number;
  };
    tokens: SimplifiedToken[];
}

interface SimplifiedToken {
  outcome: string;
  price: number;
  token_id: string;
}
```

***

## Order Books and Prices

***

### calculateMarketPrice()

```typescript Signature theme={null}
async calculateMarketPrice(
  tokenID: string,
  side: Side,
  amount: number,
  orderType: OrderType = OrderType.FOK
): Promise<number>
```

```typescript Params theme={null}
enum OrderType {
  GTC = "GTC",  // Good Till Cancelled
  FOK = "FOK",  // Fill or Kill
  GTD = "GTD",  // Good Till Date
  FAK = "FAK",  // Fill and Kill
}

enum Side {
  BUY = "BUY",
  SELL = "SELL",
}
```

```typescript Response theme={null}
number // calculated market price
```

***

### getOrderBook()

Get the order book for a specific token ID.

```typescript Signature theme={null}
async getOrderBook(tokenID: string): Promise<OrderBookSummary>
```

```typescript Response theme={null}
interface OrderBookSummary {
  market: string;
  asset_id: string;
  timestamp: string;
  bids: OrderSummary[];
  asks: OrderSummary[];
  min_order_size: string;
  tick_size: string;
  neg_risk: boolean;
  hash: string;
}

interface OrderSummary {
  price: string;
  size: string;
}
```

***

### getOrderBooks()

Get order books for multiple token IDs.

```typescript Signature theme={null}
async getOrderBooks(params: BookParams[]): Promise<OrderBookSummary[]>
```

```typescript Params theme={null}
interface BookParams {
  token_id: string;
  side: Side;  // Side.BUY or Side.SELL
}
```

```typescript Response theme={null}
OrderBookSummary[]
```

***

### getPrice()

Get the current best price for buying or selling a token ID.

```typescript Signature theme={null}
async getPrice(
  tokenID: string,
  side: "BUY" | "SELL"
): Promise<any>
```

```typescript Response theme={null}
{
  price: string;
}
```

***

### getPrices()

Get the current best prices for multiple token IDs.

```typescript Signature theme={null}
async getPrices(params: BookParams[]): Promise<PricesResponse>
```

```typescript Params theme={null}
interface BookParams {
  token_id: string;
  side: Side;  // Side.BUY or Side.SELL
}
```

```typescript Response theme={null}
interface TokenPrices {
  BUY?: string;
  SELL?: string;
}

type PricesResponse = {
  [tokenId: string]: TokenPrices;
}
```

***

### getMidpoint()

Get the midpoint price (average of best bid and best ask) for a token ID.

```typescript Signature theme={null}
async getMidpoint(tokenID: string): Promise<any>
```

```typescript Response theme={null}
{
  mid: string;
}
```

***

### getMidpoints()

Get the midpoint prices (average of best bid and best ask) for multiple token IDs.

```typescript Signature theme={null}
async getMidpoints(params: BookParams[]): Promise<any>
```

```typescript Params theme={null}
interface BookParams {
  token_id: string;
  side: Side;  // Side is ignored
}
```

```typescript Response theme={null}
{
  [tokenId: string]: string;
}
```

***

### getSpread()

Get the spread (difference between best ask and best bid) for a token ID.

```typescript Signature theme={null}
async getSpread(tokenID: string): Promise<SpreadResponse>
```

```typescript Response theme={null}
interface SpreadResponse {
  spread: string;
}
```

***

### getSpreads()

Get the spreads (difference between best ask and best bid) for multiple token IDs.

```typescript Signature theme={null}
async getSpreads(params: BookParams[]): Promise<SpreadsResponse>
```

```typescript Params theme={null}
interface BookParams {
  token_id: string;
  side: Side;
}
```

```typescript Response theme={null}
type SpreadsResponse = {
  [tokenId: string]: string;
}
```

***

### getPricesHistory()

Get historical price data for a token.

```typescript Signature theme={null}
async getPricesHistory(params: PriceHistoryFilterParams): Promise<MarketPrice[]>
```

```typescript Params theme={null}
interface PriceHistoryFilterParams {
  market: string; // tokenID
  startTs?: number;
  endTs?: number;
  fidelity?: number;
  interval: PriceHistoryInterval;
}

enum PriceHistoryInterval {
  MAX = "max",
  ONE_WEEK = "1w",
  ONE_DAY = "1d",
  SIX_HOURS = "6h",
  ONE_HOUR = "1h",
}
```

```typescript Response theme={null}
interface MarketPrice {
  t: number;  // timestamp
  p: number;  // price
}
```

***

## Trades

***

### getLastTradePrice()

Get the price of the most recent trade for a token.

```typescript Signature theme={null}
async getLastTradePrice(tokenID: string): Promise<LastTradePrice>
```

```typescript Response theme={null}
interface LastTradePrice {
  price: string;
  side: string;
}
```

***

### getLastTradesPrices()

Get the price of the most recent trade for a token.

```typescript Signature theme={null}
async getLastTradesPrices(params: BookParams[]): Promise<LastTradePriceWithToken[]>
```

```typescript Params theme={null}
interface BookParams {
  token_id: string;
  side: Side;
}
```

```typescript Response theme={null}
interface LastTradePriceWithToken {
  price: string;
  side: string;
  token_id: string;
}
```

***

### getMarketTradesEvents

```typescript Signature theme={null}
async getMarketTradesEvents(conditionID: string): Promise<MarketTradeEvent[]>
```

```typescript Response theme={null}
interface MarketTradeEvent {
  event_type: string;
  market: {
    condition_id: string;
    asset_id: string;
    question: string;
    icon: string;
    slug: string;
  };
  user: {
    address: string;
    username: string;
    profile_picture: string;
    optimized_profile_picture: string;
    pseudonym: string;
  };
  side: Side;
  size: string;
  fee_rate_bps: string;
  price: string;
  outcome: string;
  outcome_index: number;
  transaction_hash: string;
  timestamp: string;
}
```

## Market Parameters

***

### getFeeRateBps()

Get the fee rate in basis points for a token.

```typescript Signature theme={null}
async getFeeRateBps(tokenID: string): Promise<number>
```

```typescript Response theme={null}
number
```

***

### getTickSize()

Get the tick size (minimum price increment) for a market.

```typescript Signature theme={null}
async getTickSize(tokenID: string): Promise<TickSize>
```

```typescript Response theme={null}
type TickSize = "0.1" | "0.01" | "0.001" | "0.0001";
```

***

### getNegRisk()

Check if a market uses negative risk (binary complementary tokens).

```typescript Signature theme={null}
async getNegRisk(tokenID: string): Promise<boolean>
```

```typescript Response theme={null}
boolean
```

***

## Time & Server Info

### getServerTime()

Get the current server timestamp.

```typescript Signature theme={null}
async getServerTime(): Promise<number>
```

```typescript Response theme={null}
number // Unix timestamp in seconds
```

***

## See Also

<CardGroup cols={2}>
  <Card title="L1 Methods" icon="key" href="/developers/CLOB/clients/methods-l1">
    Private key authentication to create or derive API keys (L2 headers).
  </Card>

  <Card title="L2 Methods" icon="lock" href="/developers/CLOB/clients/methods-l2">
    Manage and close orders. Creating orders requires signer.
  </Card>

  <Card title="CLOB Rest API Reference" icon="hammer" href="/api-reference/orderbook/get-order-book-summary">
    Complete REST endpoint documentation
  </Card>

  <Card title="Web Socket API" icon="hammer" href="/developers/CLOB/websocket/wss-overview">
    Real-time market data streaming
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt