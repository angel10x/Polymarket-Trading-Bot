# L2 Methods

> These methods require user API credentials (L2 headers). Use these for placing trades and managing user's positions.

***

## Client Initialization

L2 methods require the client to initialize with the signer, signatureType, user API credentials, and funder.

<Tabs>
  <Tab title="TypeScript">
    ```typescript  theme={null}
    import { ClobClient } from "@polymarket/clob-client";
    import { Wallet } from "ethers";

    const signer = new Wallet(process.env.PRIVATE_KEY)

    const apiCreds = {
      apiKey: process.env.API_KEY,
      secret: process.env.SECRET,
      passphrase: process.env.PASSPHRASE,
    };

    const client = new ClobClient(
      "https://clob.polymarket.com",
      137,
      signer,
      apiCreds,
      2, // Deployed Safe proxy wallet
      process.env.FUNDER_ADDRESS // Address of deployed Safe proxy wallet
    );

    // Ready to send authenticated requests to the CLOB API!
    const order = await client.postOrder(signedOrder);
    ```
  </Tab>

  <Tab title="Python">
    ```python  theme={null}
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import ApiCreds
    import os

    api_creds = ApiCreds(
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("SECRET"),
        api_passphrase=os.getenv("PASSPHRASE")
    )

    client = ClobClient(
        host="https://clob.polymarket.com",
        chain_id=137,
        key=os.getenv("PRIVATE_KEY"),
        creds=api_creds,
        signature_type=2, # Deployed Safe proxy wallet
        funder=os.getenv("FUNDER_ADDRESS") # Address of deployed Safe proxy wallet
    )

    # Ready to send authenticated requests to the CLOB API!
    order = await client.post_order(signed_order)
    ```
  </Tab>
</Tabs>

***

## Order Creation and Management

***

### createAndPostOrder()

A convenience method that creates, prompts signature, and posts an order in a single call.
Use when you want to buy/sell at a specific price and can wait.

```typescript Signature theme={null}
async createAndPostOrder(
  userOrder: UserOrder,
  options?: Partial<CreateOrderOptions>,
  orderType?: OrderType.GTC | OrderType.GTD, // Defaults to GTC
): Promise<OrderResponse>
```

```typescript Params theme={null}
interface UserOrder {
  tokenID: string;
  price: number;
  size: number;
  side: Side;
  feeRateBps?: number;
  nonce?: number;
  expiration?: number;
  taker?: string;
}

type CreateOrderOptions = {
  tickSize: TickSize;
  negRisk?: boolean;
}

type TickSize = "0.1" | "0.01" | "0.001" | "0.0001";
```

```typescript Response theme={null}
interface OrderResponse {
  success: boolean;
  errorMsg: string;
  orderID: string;
  transactionsHashes: string[];
  status: string;
  takingAmount: string;
  makingAmount: string;
}
```

***

### createAndPostMarketOrder()

A convenience method that creates, prompts signature, and posts an order in a single call.
Use when you want to buy/sell right now at whatever the market price is.

```typescript Signature theme={null}
async createAndPostMarketOrder(
  userMarketOrder: UserMarketOrder,
  options?: Partial<CreateOrderOptions>,
  orderType?: OrderType.FOK | OrderType.FAK, // Defaults to FOK
): Promise<OrderResponse>
```

```typescript Params theme={null}
interface UserMarketOrder {
  tokenID: string;
  amount: number;
  side: Side;
  price?: number;
  feeRateBps?: number;
  nonce?: number;
  taker?: string;
  orderType?: OrderType.FOK | OrderType.FAK;
}

type CreateOrderOptions = {
  tickSize: TickSize;
  negRisk?: boolean;
}

type TickSize = "0.1" | "0.01" | "0.001" | "0.0001";
```

```typescript Response theme={null}
interface OrderResponse {
  success: boolean;
  errorMsg: string;
  orderID: string;
  transactionsHashes: string[];
  status: string;
  takingAmount: string;
  makingAmount: string;
}
```

***

### postOrder()

Posts a pre-signed and created order to the CLOB.

```typescript Signature theme={null}
async postOrder(
  order: SignedOrder,
  orderType?: OrderType, // Defaults to GTC
): Promise<OrderResponse>
```

```typescript Params theme={null}
order: SignedOrder  // Pre-signed order from createOrder() or createMarketOrder()
orderType?: OrderType  // Optional, defaults to GTC
```

```typescript Response theme={null}
interface OrderResponse {
  success: boolean;
  errorMsg: string;
  orderID: string;
  transactionsHashes: string[];
  status: string;
  takingAmount: string;
  makingAmount: string;
}
```

***

### postOrders()

Posts up to 15 pre-signed and created orders in a single batch.

```typescript  theme={null}
async postOrders(
  args: PostOrdersArgs[],
): Promise<OrderResponse[]>
```

```typescript Params theme={null}
interface PostOrdersArgs {
  order: SignedOrder;
  orderType: OrderType;
}
```

```typescript Response theme={null}
OrderResponse[]  // Array of OrderResponse objects

interface OrderResponse {
  success: boolean;
  errorMsg: string;
  orderID: string;
  transactionsHashes: string[];
  status: string;
  takingAmount: string;
  makingAmount: string;
}
```

***

### cancelOrder()

Cancels a single open order.

```typescript Signature theme={null}
async cancelOrder(orderID: string): Promise<CancelOrdersResponse>
```

```typescript Response theme={null}
interface CancelOrdersResponse {
  canceled: string[];
  not_canceled: Record<string, any>;
}
```

***

### cancelOrders()

Cancels multiple orders in a single batch.

```typescript Signature theme={null}
async cancelOrders(orderIDs: string[]): Promise<CancelOrdersResponse>
```

```typescript Params theme={null}
orderIDs: string[];
```

```typescript Response theme={null}
interface CancelOrdersResponse {
  canceled: string[];
  not_canceled: Record<string, any>;
}
```

***

### cancelAll()

Cancels all open orders.

```typescript Signature theme={null}
async cancelAll(): Promise<CancelResponse>
```

```typescript Response theme={null}
interface CancelOrdersResponse {
  canceled: string[];
  not_canceled: Record<string, any>;
}
```

***

### cancelMarketOrders()

Cancels all open orders for a specific market.

```typescript Signature theme={null}
async cancelMarketOrders(
  payload: OrderMarketCancelParams
): Promise<CancelOrdersResponse>
```

```typescript Parameters theme={null}
interface OrderMarketCancelParams {
  market?: string;
  asset_id?: string;
}
```

```typescript Response theme={null}
interface CancelOrdersResponse {
  canceled: string[];
  not_canceled: Record<string, any>;
}
```

***

## Order and Trade Queries

***

### getOrder()

Get details for a specific order.

```typescript Signature theme={null}
async getOrder(orderID: string): Promise<OpenOrder>
```

```typescript Response theme={null}
interface OpenOrder {
  id: string;
  status: string;
  owner: string;
  maker_address: string;
  market: string;
  asset_id: string;
  side: string;
  original_size: string;
  size_matched: string;
  price: string;
  associate_trades: string[];
  outcome: string;
  created_at: number;
  expiration: string;
  order_type: string;
}
```

***

### getOpenOrders()

Get all your open orders.

```typescript Signature theme={null}
async getOpenOrders(
  params?: OpenOrderParams,
  only_first_page?: boolean,
): Promise<OpenOrdersResponse>
```

```typescript Params theme={null}
interface OpenOrderParams {
  id?: string; // Order ID
  market?: string; // Market condition ID
  asset_id?: string; // Token ID
}

only_first_page?: boolean  // Defaults to false
```

```typescript Response theme={null}
type OpenOrdersResponse = OpenOrder[];

interface OpenOrder {
  id: string;
  status: string;
  owner: string;
  maker_address: string;
  market: string;
  asset_id: string;
  side: string;
  original_size: string;
  size_matched: string;
  price: string;
  associate_trades: string[];
  outcome: string;
  created_at: number;
  expiration: string;
  order_type: string;
}
```

***

### getTrades()

Get your trade history (filled orders).

```typescript Signature theme={null}
async getTrades(
  params?: TradeParams,
  only_first_page?: boolean,
): Promise<Trade[]>
```

```typescript Params theme={null}
interface TradeParams {
  id?: string;
  maker_address?: string;
  market?: string;
  asset_id?: string;
  before?: string;
  after?: string;
}

only_first_page?: boolean  // Defaults to false
```

```typescript Response theme={null}
interface Trade {
  id: string;
  taker_order_id: string;
  market: string;
  asset_id: string;
  side: Side;
  size: string;
  fee_rate_bps: string;
  price: string;
  status: string;
  match_time: string;
  last_update: string;
  outcome: string;
  bucket_index: number;
  owner: string;
  maker_address: string;
  maker_orders: MakerOrder[];
  transaction_hash: string;
  trader_side: "TAKER" | "MAKER";
}

interface MakerOrder {
  order_id: string;
  owner: string;
  maker_address: string;
  matched_amount: string;
  price: string;
  fee_rate_bps: string;
  asset_id: string;
  outcome: string;
  side: Side;
}
```

***

### getTradesPaginated()

Get trade history with pagination for large result sets.

```typescript Signature theme={null}
async getTradesPaginated(
  params?: TradeParams,
): Promise<TradesPaginatedResponse>
```

```typescript Params theme={null}
interface TradeParams {
  id?: string;
  maker_address?: string;
  market?: string;
  asset_id?: string;
  before?: string;
  after?: string;
}
```

```typescript Response theme={null}
interface TradesPaginatedResponse {
  trades: Trade[];
  limit: number;
  count: number;
}
```

***

## Balance and Allowances

***

### getBalanceAllowance()

Get your balance and allowance for specific tokens.

```typescript Signature theme={null}
async getBalanceAllowance(
  params?: BalanceAllowanceParams
): Promise<BalanceAllowanceResponse>
```

```typescript Params theme={null}
interface BalanceAllowanceParams {
  asset_type: AssetType;
  token_id?: string;
}

enum AssetType {
  COLLATERAL = "COLLATERAL",
  CONDITIONAL = "CONDITIONAL",
}
```

```typescript Response theme={null}
interface BalanceAllowanceResponse {
  balance: string;
  allowance: string;
}
```

***

### updateBalanceAllowance()

Updates the cached balance and allowance for specific tokens.

```typescript Signature theme={null}
async updateBalanceAllowance(
  params?: BalanceAllowanceParams
): Promise<void>
```

```typescript Params theme={null}
interface BalanceAllowanceParams {
  asset_type: AssetType;
  token_id?: string;
}

enum AssetType {
  COLLATERAL = "COLLATERAL",
  CONDITIONAL = "CONDITIONAL",
}
```

***

## API Key Management (L2)

### getApiKeys()

Get all API keys associated with your account.

```typescript Signature theme={null}
async getApiKeys(): Promise<ApiKeysResponse>
```

```typescript Response theme={null}
interface ApiKeysResponse {
  apiKeys: ApiKeyCreds[];
}

interface ApiKeyCreds {
  key: string;
  secret: string;
  passphrase: string;
}
```

***

### deleteApiKey()

Deletes (revokes) the currently authenticated API key.

**TypeScript Signature:**

```typescript  theme={null}
async deleteApiKey(): Promise<any>
```

***

## Notifications

***

### getNotifications()

Retrieves all event notifications for the L2 authenticated user.
Records are removed automatically after 48 hours or if manually removed via dropNotifications().

```typescript Signature theme={null}
public async getNotifications(): Promise<Notification[]>
```

```typescript Response theme={null}
interface Notification {
    id: number;           // Unique notification ID
    owner: string;        // User's L2 credential apiKey or empty string for global notifications
    payload: any;         // Type-specific payload data
    timestamp?: number;   // Unix timestamp
    type: number;         // Notification type (see type mapping below)
}
```

**Notification Type Mapping**

| Name               | Value | Description                              |
| ------------------ | ----- | ---------------------------------------- |
| Order Cancellation | 1     | User's order was canceled                |
| Order Fill         | 2     | User's order was filled (maker or taker) |
| Market Resolved    | 4     | Market was resolved                      |

***

### dropNotifications()

Mark notifications as read/dismissed.

```typescript Signature theme={null}
public async dropNotifications(params?: DropNotificationParams): Promise<void>
```

```typescript Params theme={null}
interface DropNotificationParams {
    ids: string[];  // Array of notification IDs to mark as read
}
```

***

## See Also

<CardGroup cols={2}>
  <Card title="Understand CLOB Authentication" icon="shield" href="/developers/CLOB/authentication">
    Deep dive into L1 and L2 authentication
  </Card>

  <Card title="Public Methods" icon="globe" href="/developers/CLOB/clients/methods-l2">
    Access market data, orderbooks, and prices.
  </Card>

  <Card title="L1 Methods" icon="lock" href="/developers/CLOB/clients/methods-l2">
    Private key authentication to create or derive API keys (L2 headers)
  </Card>

  <Card title="Web Socket API" icon="hammer" href="/developers/CLOB/websocket/wss-overview">
    Real-time market data streaming
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt