# L1 Methods

> These methods require a wallet signer (private key) but do not require user API credentials. Use these for initial setup.

## Client Initialization

L1 methods require the client to initialize with a signer.

<Tabs>
  <Tab title="TypeScript">
    ```typescript  theme={null}
    import { ClobClient } from "@polymarket/clob-client";
    import { Wallet } from "ethers";

    const signer = new Wallet(process.env.PRIVATE_KEY);

    const client = new ClobClient(
      "https://clob.polymarket.com",
      137,
      signer // Signer required for L1 methods
    );

    // Ready to create user API credentials
    const apiKey = await client.createApiKey();
    ```
  </Tab>

  <Tab title="Python">
    ```python  theme={null}
    from py_clob_client.client import ClobClient
    import os

    private_key = os.getenv("PRIVATE_KEY")

    client = ClobClient(
        host="https://clob.polymarket.com",
        chain_id=137,
        key=private_key  # Signer required for L1 methods
    )

    # Ready to create user API credentials
    api_key = await client.create_api_key()
    ```
  </Tab>
</Tabs>

<Warning>
  **Security:** Never commit private keys to version control. Always use environment variables or secure key management systems.
</Warning>

***

## API Key Management

***

### createApiKey()

Creates a new API key (L2 credentials) for the wallet signer. This generates a new set of credentials that can be used for L2 authenticated requests.
Each wallet can only have one active API key at a time. Creating a new key invalidates the previous one.

```typescript Signature theme={null}
async createApiKey(nonce?: number): Promise<ApiKeyCreds>
```

```typescript Params theme={null}
`nonce` (optional): Custom nonce for deterministic key generation. If not provided, a default derivation is used.
```

```typescript Response theme={null}
interface ApiKeyCreds {
  apiKey: string;
  secret: string;
  passphrase: string;
}
```

***

### deriveApiKey()

Derives an existing API key (L2 credentials) using a specific nonce. If you've already created API credentials with a particular nonce, this method will return the same credentials again.

```typescript Signature theme={null}
async deriveApiKey(nonce?: number): Promise<ApiKeyCreds>
```

```typescript Params theme={null}
`nonce` (optional): Custom nonce for deterministic key generation. If not provided, a default derivation is used.
```

```typescript Response theme={null}
interface ApiKeyCreds {
  apiKey: string;
  secret: string;
  passphrase: string;
}
```

***

### createOrDeriveApiKey()

Convenience method that attempts to derive an API key with the default nonce, or creates a new one if it doesn't exist. This is the recommended method for initial setup if you're unsure if credentials already exist.

```typescript Signature theme={null}
async createOrDeriveApiKey(nonce?: number): Promise<ApiKeyCreds>
```

```typescript Params theme={null}
`nonce` (optional): Custom nonce for deterministic key generation. If not provided, a default derivation is used.
```

```typescript Response theme={null}
interface ApiKeyCreds {
  apiKey: string;
  secret: string;
  passphrase: string;
}
```

***

## Order Signing

### createOrder()

Create and sign a limit order locally without posting it to the CLOB.
Use this when you want to sign orders in advance or implement custom order submission logic.
Place order via L2 methods postOrder or postOrders.

```typescript Signature theme={null}
async createOrder(
  userOrder: UserOrder,
  options?: Partial<CreateOrderOptions>
): Promise<SignedOrder>
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

interface CreateOrderOptions {
  tickSize: TickSize;
  negRisk?: boolean;
}
```

```typescript Response theme={null}
interface SignedOrder {
  salt: string;
  maker: string;
  signer: string;
  taker: string;
  tokenId: string;
  makerAmount: string;
  takerAmount: string;
  side: number;  // 0 = BUY, 1 = SELL
  expiration: string;
  nonce: string;
  feeRateBps: string;
  signatureType: number;
  signature: string;
}
```

***

### createMarketOrder()

Create and sign a market order locally without posting it to the CLOB.
Use this when you want to sign orders in advance or implement custom order submission logic.
Place orders via L2 methods postOrder or postOrders.

```typescript Signature theme={null}
async createMarketOrder(
  userMarketOrder: UserMarketOrder,
  options?: Partial<CreateOrderOptions>
): Promise<SignedOrder>
```

```typescript Params theme={null}
interface UserMarketOrder {
  tokenID: string;
  amount: number;  // BUY: dollar amount, SELL: number of shares
  side: Side;
  price?: number;  // Optional price limit
  feeRateBps?: number;
  nonce?: number;
  taker?: string;
  orderType?: OrderType.FOK | OrderType.FAK;
}
```

```typescript Response theme={null}
interface SignedOrder {
  salt: string;
  maker: string;
  signer: string;
  taker: string;
  tokenId: string;
  makerAmount: string;
  takerAmount: string;
  side: number;  // 0 = BUY, 1 = SELL
  expiration: string;
  nonce: string;
  feeRateBps: string;
  signatureType: number;
  signature: string;
}
```

***

## Troubleshooting

<AccordionGroup>
  <Accordion title="Error: INVALID_SIGNATURE">
    Your wallet's private key is incorrect or improperly formatted.

    **Solution:**

    * Verify your private key is a valid hex string (starts with "0x")
    * Ensure you're using the correct key for the intended address
    * Check that the key has proper permissions
  </Accordion>

  <Accordion title="Error: NONCE_ALREADY_USED">
    The nonce you provided has already been used to create an API key.

    **Solution:**

    * Use `deriveApiKey()` with the same nonce to retrieve existing credentials
    * Or use a different nonce with `createApiKey()`
  </Accordion>

  <Accordion title="Error: Invalid Funder Address">
    Your funder address is incorrect or doesn't match your wallet.

    **Solution:** Check your Polymarket profile address at [polymarket.com/settings](https://polymarket.com/settings).

    If it does not exist or user has never logged into Polymarket.com, deploy it first before creating L2 authentication.
  </Accordion>

  <Accordion title="Lost API credentials but have nonce">
    ```typescript  theme={null}
    // Use deriveApiKey with the original nonce
    const recovered = await client.deriveApiKey(originalNonce);
    ```
  </Accordion>

  <Accordion title="Lost both credentials and nonce">
    Unfortunately, there's no way to recover lost API credentials without the nonce. You'll need to create new credentials:

    ```typescript  theme={null}
    // Create fresh credentials with a new nonce
    const newCreds = await client.createApiKey();
    // Save the nonce this time!
    ```
  </Accordion>
</AccordionGroup>

***

## See Also

<CardGroup cols={2}>
  <Card title="Understand CLOB Authentication" icon="shield" href="/developers/CLOB/authentication">
    Deep dive into L1 and L2 authentication
  </Card>

  <Card title="CLOB Quickstart Guide" icon="hammer" href="/developers/CLOB/quickstart">
    Initialize the CLOB quickly and place your first order.
  </Card>

  <Card title="Public Methods" icon="globe" href="/developers/CLOB/clients/methods-l2">
    Access market data, orderbooks, and prices.
  </Card>

  <Card title="L2 Methods" icon="lock" href="/developers/CLOB/clients/methods-l2">
    Manage and close orders. Creating orders requires signer.
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt