# Methods Overview

> CLOB client methods require different levels of authentication. This reference is organized by what credentials you need to call each method. 

<CardGroup cols={2}>
  <Card title="Public Methods" icon="globe" href="/developers/CLOB/clients/methods-public">
    Access market data, orderbooks, and prices.
  </Card>

  <Card title="L1 Methods" icon="key" href="/developers/CLOB/clients/methods-l1">
    Private key authentication to create or derive API keys (L2 headers).
  </Card>

  <Card title="L2 Methods" icon="lock" href="/developers/CLOB/clients/methods-l2">
    Manage and close orders. Creating orders requires signer.
  </Card>

  <Card title="Builder Program Methods" icon="hammer" href="/developers/CLOB/clients/methods-builder">
    Builder-specific operations for those in the Builders Program.
  </Card>
</CardGroup>

***

## Client Initialization by Use Case

<Tabs>
  <Tab title="Get Market Data">
    <CodeGroup>
      ```typescript TypeScript theme={null}
      // No signer or credentials needed
      const client = new ClobClient(
        "https://clob.polymarket.com", 
        137
      );

      // All public methods available
      const markets = await client.getMarkets();
      const book = await client.getOrderBook(tokenId);
      const price = await client.getPrice(tokenId, "BUY");
      ```

      ```python Python theme={null}
      # No signer or credentials needed
      client = new ClobClient(
          host="https://clob.polymarket.com", 
          chain_id=137
      )

      # All public methods available
      markets = client.get_markets()
      book = client.get_order_book()
      price = client.get_price()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Generate User API Credentials">
    <CodeGroup>
      ```typescript TypeScript theme={null}
      // Create client with signer
      const client = new ClobClient(
        "https://clob.polymarket.com", 
        137, 
        signer
      );

      // All public and L1 methods available
      const newCreds = createApiKey();
      const derivedCreds = deriveApiKey();
      const creds = createOrDeriveApiKey();
      ```

      ```python Python theme={null}
      # Create client with signer
      client = new ClobClient(
          host="https://clob.polymarket.com", 
          chain_id=137
          key="private_key"
        )

      # All public and L1 methods available
      new_creds = client.create_api_key()
      derived_creds = client.derive_api_key()
      creds = client.create_or_derive_api_key()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Create and Post Order">
    <CodeGroup>
      ```typescript TypeScript theme={null}
      // Create client with signer and creds
      const client = new ClobClient(
        "https://clob.polymarket.com", 
        137, 
        signer,
        creds,
        2, // Indicates Gnosis Safe proxy
        funder // Safe wallet address holding funds
      );

      // All public, L1, and L2 methods available
      const order = await client.createOrder({ /* ... */ });
      const result = await client.postOrder(order);
      const trades = await client.getTrades();
      ```

      ```python Python theme={null}
      # Create client with signer and creds
      const client = new ClobClient(
          host="https://clob.polymarket.com",
          chain_id=137,
          key="private_key",
          creds=creds,
          signature_type=2, // Indicates Gnosis Safe proxy
          funder="funder_address" // Safe wallet address holding funds
      )

      # All public, L1, and L2 methods available
      order = client.create_order({ /* ... */ })
      result = client.post_order(order)
      trades = client.get_trades()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Get Builders Orders">
    <CodeGroup>
      ```typescript TypeScript theme={null}
      // Create client with builder's authentication headers
      import { BuilderConfig, BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";

      const builderCreds: BuilderApiKeyCreds = {
        key: process.env.POLY_BUILDER_API_KEY!,
        secret: process.env.POLY_BUILDER_SECRET!,
        passphrase: process.env.POLY_BUILDER_PASSPHRASE!
      };

      const builderConfig: BuilderConfig = {
        localBuilderCreds: builderCreds
      };

      const client = new ClobClient(
        "https://clob.polymarket.com", 
        137, 
        signer,
        creds, // User's API credentials
        2,
        funder,
        undefined,
        false,
        builderConfig // Builder's API credentials
      );

      // You can call all methods including builder methods
      const builderTrades = await client.getBuilderTrades();
      ```

      ```python Python theme={null}
      # Create client with builder's authentication headers
      from py_clob_client.client import ClobClient
      from py_clob_client.clob_types import ApiCreds
      from py_builder_signing_sdk.config import BuilderConfig, BuilderApiKeyCreds

      builder_creds = BuilderApiKeyCreds(
          key="POLY_BUILDER_API_KEY",
          secret="POLY_BUILDER_SECRET,
          passphrase="POLY_BUILDER_PASSPHRASE"
      )

      builder_config = BuilderConfig(
          local_builder_creds=builder_creds
      )

      client = ClobClient(
          host="https://clob.polymarket.com",
          chain_id=137,
          key="private_key",
          creds=creds, # User's API credentials
          signature_type=2,
          funder=funder_address,
          builder_config=builder_config # Builder's API credentials
      )

      # You can call all methods including builder methods
      builder_trades = client.get_builder_trades()
      ```
    </CodeGroup>

    Learn more about the Builders Program and Relay Client here
  </Tab>
</Tabs>

***

## Resources

<CardGroup cols={2}>
  <Card title="TypeScript Client" icon="github" href="https://github.com/Polymarket/clob-client">
    Open source TypeScript client on GitHub
  </Card>

  <Card title="Python Client" icon="github" href="https://github.com/Polymarket/py-clob-client">
    Open source Python client for GitHub
  </Card>

  <Card title="TypeScript Examples" icon="code" href="https://github.com/Polymarket/clob-client/tree/main/examples">
    TypeScript client method examples
  </Card>

  <Card title="Python Examples" icon="python" href="https://github.com/Polymarket/py-clob-client/tree/main/examples">
    Python client method examples
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