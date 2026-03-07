# Quickstart

> Initialize the CLOB and place your first order.

## Installation

<CodeGroup>
  ```bash TypeScript theme={null}
  npm install @polymarket/clob-client ethers
  ```

  ```bash Python theme={null}
  pip install py-clob-client
  ```
</CodeGroup>

***

## Quick Start

### 1. Setup Client

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { ClobClient } from "@polymarket/clob-client";
  import { Wallet } from "ethers"; // v5.8.0

  const HOST = "https://clob.polymarket.com";
  const CHAIN_ID = 137; // Polygon mainnet
  const signer = new Wallet(process.env.PRIVATE_KEY);

  // Create or derive user API credentials
  const tempClient = new ClobClient(HOST, CHAIN_ID, signer);
  const apiCreds = await tempClient.createOrDeriveApiKey();

  // See 'Signature Types' note below
  const signatureType = 0;

  // Initialize trading client
  const client = new ClobClient(
    HOST, 
    CHAIN_ID, 
    signer, 
    apiCreds, 
    signatureType
  );
  ```

  ```python Python theme={null}
  from py_clob_client.client import ClobClient
  import os

  host = "https://clob.polymarket.com"
  chain_id = 137 # Polygon mainnet
  private_key = os.getenv("PRIVATE_KEY")

  # Create or derive user API credentials
  temp_client = ClobClient(host, key=private_key, chain_id=chain_id)
  api_creds = await temp_client.create_or_derive_api_key()

  # See 'Signature Types' note below
  signature_type = 0

  # Initialize trading client
  client = ClobClient(
      host,
      key=private_key,
      chain_id=chain_id,
      creds=api_creds,
      signature_type=signature_type
  )
  ```
</CodeGroup>

<Note>
  This quick start sets your EOA as the trading account. You'll need to fund this
  wallet to trade and pay for gas on transactions. Gas-less transactions are only
  available by deploying a proxy wallet and using Polymarket's Polygon relayer
  infrastructure.
</Note>

<Accordion title="Signature Types">
  | Wallet Type  | ID  | When to Use                                            |
  | ------------ | --- | ------------------------------------------------------ |
  | EOA          | `0` | Standard Ethereum wallet (MetaMask)                    |
  | Custom Proxy | `1` | Specific to Magic Link users from Polymarket only      |
  | Gnosis Safe  | `2` | Injected providers (Metamask, Rabby, embedded wallets) |
</Accordion>

***

### 2. Place an Order

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { Side } from "@polymarket/clob-client";

  // Place a limit order in one step
  const response = await client.createAndPostOrder({
    tokenID: "YOUR_TOKEN_ID", // Get from Gamma API
    price: 0.65, // Price per share
    size: 10, // Number of shares
    side: Side.BUY, // or SELL
  });

  console.log(`Order placed! ID: ${response.orderID}`);
  ```

  ```python Python theme={null}
  from py_clob_client.clob_types import OrderArgs
  from py_clob_client.order_builder.constants import BUY

  # Place a limit order in one step
  response = await client.create_and_post_order(
      OrderArgs(
          token_id="YOUR_TOKEN_ID",  # Get from Gamma API
          price=0.65,                # Price per share
          size=10,                   # Number of shares
          side=BUY,                  # or SELL
      )
  )

  print(f"Order placed! ID: {response['orderID']}")
  ```
</CodeGroup>

***

### 3. Check Your Orders

<CodeGroup>
  ```typescript TypeScript theme={null}
  // View all open orders
  const openOrders = await client.getOpenOrders();
  console.log(`You have ${openOrders.length} open orders`);

  // View your trade history
  const trades = await client.getTrades();
  console.log(`You've made ${trades.length} trades`);
  ```

  ```python Python theme={null}
  # View all open orders
  open_orders = await client.get_open_orders()
  print(f"You have {len(open_orders)} open orders")

  # View your trade history
  trades = await client.get_trades()
  print(f"You've made {len(trades)} trades")
  ```
</CodeGroup>

***

## Complete Example

<CodeGroup>
  ```typescript TypeScript theme={null}
  import { ClobClient, Side } from "@polymarket/clob-client";
  import { Wallet } from "ethers";

  async function trade() {
    const HOST = "https://clob.polymarket.com";
    const CHAIN_ID = 137; // Polygon mainnet
    const signer = new Wallet(process.env.PRIVATE_KEY);

    const tempClient = new ClobClient(HOST, CHAIN_ID, signer);
    const apiCreds = await tempClient.createOrDeriveApiKey();

    const signatureType = 0;

    const client = new ClobClient(
      HOST,
      CHAIN_ID,
      signer,
      apiCreds,
      signatureType
    );

    const response = await client.createAndPostOrder({
      tokenID: "YOUR_TOKEN_ID",
      price: 0.65,
      size: 10,
      side: Side.BUY,
    });

    console.log(`Order placed! ID: ${response.orderID}`);
  }

  trade();
  ```

  ```python Python theme={null}
  from py_clob_client.client import ClobClient
  from py_clob_client.clob_types import OrderArgs
  from py_clob_client.order_builder.constants import BUY
  import asyncio
  import os

  async def trade():
      host = "https://clob.polymarket.com"
      chain_id = 137 # Polygon mainnet
      private_key = os.getenv("PRIVATE_KEY")

      temp_client = ClobClient(host, key=private_key, chain_id=chain_id)
      creds = await temp_client.create_or_derive_api_key()

      signature_type=0

      client = ClobClient(
          host,
          chain_id=chain_id,
          key=private_key,
          creds=creds,
          signature_type=signature_type
      )

      response = await client.create_and_post_order(
          OrderArgs(
              token_id="YOUR_TOKEN_ID",
              price=0.65,
              size=10,
              side=BUY
          )
      )

      print(f"Order placed! ID: {response['orderID']}")

  if __name__ == "__main__":
      asyncio.run(trade())
  ```
</CodeGroup>

***

## Troubleshooting

<AccordionGroup>
  <Accordion title="Error: L2_AUTH_NOT_AVAILABLE">
    You forgot to call `createOrDeriveApiKey()`. Make sure you initialize the client with API credentials:

    ```typescript  theme={null}
    const creds = await clobClient.createOrDeriveApiKey();
    const client = new ClobClient(host, chainId, wallet, creds);
    ```
  </Accordion>

  <Accordion title="Order rejected: insufficient balance">
    Ensure you have:

    * **USDC** in your funder address for BUY orders
    * **Outcome tokens** in your funder address for SELL orders

    Check your balance at [polymarket.com/portfolio](https://polymarket.com/portfolio).
  </Accordion>

  <Accordion title="Order rejected: insufficient allowance">
    You need to approve the Exchange contract to spend your tokens. This is typically done through the Polymarket UI on your first trade. Or use the CTF contract's `setApprovalForAll()` method.
  </Accordion>

  <Accordion title="What's my funder address?">
    Your funder address is the Polymarket proxy wallet where you deposit funds. Find it:

    1. Go to [polymarket.com/settings](https://polymarket.com/settings)
    2. Look for "Wallet Address" or "Profile Address"
    3. This is your `FUNDER_ADDRESS`
  </Accordion>
</AccordionGroup>

***

## Next Steps

<CardGroup cols={1}>
  <Card title="Full Example Implementations" icon="puzzle" href="/developers/builders/builder-demos">
    Complete Next.js examples demonstrating integration of embedded wallets
    (Privy, Magic, Turnkey, wagmi) and the CLOB and Builder Relay clients
  </Card>
</CardGroup>

<CardGroup cols={2}>
  <Card title="Understand CLOB Authentication" icon="shield" href="/developers/CLOB/authentication">
    Deep dive into L1 and L2 authentication
  </Card>

  <Card title="Browse Client Methods" icon="book" href="/developers/CLOB/clients/methods-overview">
    Explore the complete client reference
  </Card>

  <Card title="Find Markets to Trade" icon="chart-line" href="/developers/gamma-markets-api/get-markets">
    Use Gamma API to discover markets
  </Card>

  <Card title="Monitor with WebSocket" icon="signal-stream" href="/developers/CLOB/websocket/wss-overview">
    Get real-time order updates
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt