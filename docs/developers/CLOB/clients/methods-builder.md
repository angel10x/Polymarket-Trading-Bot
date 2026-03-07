# Builder Methods

> These methods require builder API credentials and are only relevant for Builders Program order attribution.

## Client Initialization

Builder methods require the client to initialize with a separate authentication setup using
builder configs acquired from [Polymarket.com](https://polymarket.com/settings?tab=builder)
and the `@polymarket/builder-signing-sdk` package.

<Tabs>
  <Tab title="Local Builder Credentials">
    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { ClobClient } from "@polymarket/clob-client";
      import { BuilderConfig, BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";

      const builderConfig = new BuilderConfig({
        localBuilderCreds: new BuilderApiKeyCreds({
          key: process.env.BUILDER_API_KEY,
          secret: process.env.BUILDER_SECRET,
          passphrase: process.env.BUILDER_PASS_PHRASE,
        }),
      });

      const clobClient = new ClobClient(
        "https://clob.polymarket.com",
        137,
        signer,
        apiCreds, // The user's API credentials generated from L1 authentication
        signatureType,
        funderAddress,
        undefined,
        false,
        builderConfig
      );
      ```

      ```python Python theme={null}
      from py_clob_client.client import ClobClient
      from py_builder_signing_sdk.config import BuilderConfig, BuilderApiKeyCreds
      import os

      builder_config = BuilderConfig(
          local_builder_creds=BuilderApiKeyCreds(
              key=os.getenv("BUILDER_API_KEY"),
              secret=os.getenv("BUILDER_SECRET"),
              passphrase=os.getenv("BUILDER_PASS_PHRASE"),
          )
      )

      clob_client = ClobClient(
          host="https://clob.polymarket.com",
          chain_id=137,
          key=os.getenv("PRIVATE_KEY"),
          creds=creds, # The user's API credentials generated from L1 authentication
          signature_type=signature_type,
          funder=funder,
          builder_config=builder_config
      )
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Remote Builder Signing">
    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { ClobClient } from "@polymarket/clob-client";
      import { BuilderConfig } from "@polymarket/builder-signing-sdk";

      const builderConfig = new BuilderConfig({
          remoteBuilderConfig: {url: "http://localhost:3000/sign"}
      });

      const clobClient = new ClobClient(
        "https://clob.polymarket.com",
        137,
        signer,
        apiCreds, // The user's API credentials generated from L1 authentication
        signatureType,
        funder,
        undefined,
        false,
        builderConfig
      );
      ```

      ```typescript Python theme={null}
      from py_clob_client.client import ClobClient
      from py_builder_signing_sdk.config import BuilderConfig, RemoteBuilderConfig
      import os

      builder_config = BuilderConfig(
          remote_builder_config=RemoteBuilderConfig(
              url="http://localhost:3000/sign"
          )
      )

      clob_client = ClobClient(
          host="https://clob.polymarket.com",
          chain_id=137,
          key=os.getenv("PRIVATE_KEY"),
          creds=creds, # The user's API credentials generated from L1 authentication
          signature_type=signature_type,
          funder=funder,
          builder_config=builder_config
      )
      ```
    </CodeGroup>
  </Tab>
</Tabs>

<Info>
  [More information on builder signing](/developers/builders/builder-signing-server)
</Info>

***

## Methods

***

### getBuilderTrades()

Retrieves all trades attributed to your builder account.
This method allows builders to track which trades were routed through your platform.

```typescript Signature theme={null}
async getBuilderTrades(
  params?: TradeParams,
): Promise<BuilderTradesPaginatedResponse>
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
interface BuilderTradesPaginatedResponse {
  trades: BuilderTrade[];
  next_cursor: string;
  limit: number;
  count: number;
}

interface BuilderTrade {
  id: string;
  tradeType: string;
  takerOrderHash: string;
  builder: string;
  market: string;
  assetId: string;
  side: string;
  size: string;
  sizeUsdc: string;
  price: string;
  status: string;
  outcome: string;
  outcomeIndex: number;
  owner: string;
  maker: string;
  transactionHash: string;
  matchTime: string;
  bucketIndex: number;
  fee: string;
  feeUsdc: string;
  err_msg?: string | null;
  createdAt: string | null;
  updatedAt: string | null;
}
```

***

### revokeBuilderApiKey()

Revokes the builder API key used to authenticate the current request.
After revocation, the key can no longer be used to make builder-authenticated requests.

```typescript Signature theme={null}
async revokeBuilderApiKey(): Promise<any>
```

***

## See Also

<CardGroup cols={2}>
  <Card title="Builders Program Introduction" icon="hammer" href="/developers/builders/builder-intro">
    Learn the benefits, how to implement, and more.
  </Card>

  <Card title="Implement Builders Signing" icon="key" href="/developers/builders/builder-signing-server">
    Attribute orders to you, and pre-requisite to using the Relayer Client.
  </Card>

  <Card title="Relayer Client" icon="globe" href="/developers/builders/relayer-client">
    The relayer executes other gasless transactions for your users, on your app.
  </Card>

  <Card title="Full Example Implementations" icon="puzzle" href="/developers/builders/builder-demos">
    Complete Next.js examples integrated with embedded wallets (Privy, Magic, Turnkey, wagmi)
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt