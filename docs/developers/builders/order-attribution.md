# Order Attribution

> Learn how to attribute orders to your builder account

## Overview

The [CLOB (Central Limit Order Book)](/developers/CLOB/introduction) is Polymarket's order matching system. Order attribution adds builder authentication headers when placing orders through the CLOB Client, enabling Polymarket to credit trades to your builder account. This allows you to:

* Track volume on the [Builder Leaderboard](https://builders.polymarket.com/)
* Compete for grants based on trading activity
* Monitor performance via the Data API

***

## Builder API Credentials

Each builder receives API credentials from their [Builder Profile](/developers/builders/builder-profile):

| Credential   | Description                          |
| ------------ | ------------------------------------ |
| `key`        | Your builder API key identifier      |
| `secret`     | Secret key for signing requests      |
| `passphrase` | Additional authentication passphrase |

<Warning>
  **Security Notice**: Your Builder API keys must be kept secure. Never expose them in client-side code.
</Warning>

***

## Signing Methods

<Tabs>
  <Tab title="Remote Signing (Recommended)">
    Remote signing keeps your credentials secure on a server you control.

    **How it works:**

    1. User signs an order payload
    2. Payload is sent to your builder signing server
    3. Your server adds builder authentication headers
    4. Complete order is sent to the CLOB

    ### Server Implementation

    Your signing server receives request details and returns the authentication headers. Use the `buildHmacSignature` function from the SDK:

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { 
        buildHmacSignature, 
        BuilderApiKeyCreds 
      } from "@polymarket/builder-signing-sdk";

      const BUILDER_CREDENTIALS: BuilderApiKeyCreds = {
        key: process.env.POLY_BUILDER_API_KEY!,
        secret: process.env.POLY_BUILDER_SECRET!,
        passphrase: process.env.POLY_BUILDER_PASSPHRASE!,
      };

      // POST /sign - receives { method, path, body } from the client SDK
      export async function handleSignRequest(request) {
        const { method, path, body } = await request.json();
        
        const timestamp = Date.now().toString();
        
        const signature = buildHmacSignature(
          BUILDER_CREDENTIALS.secret,
          parseInt(timestamp),
          method,
          path,
          body
        );

        return {
          POLY_BUILDER_SIGNATURE: signature,
          POLY_BUILDER_TIMESTAMP: timestamp,
          POLY_BUILDER_API_KEY: BUILDER_CREDENTIALS.key,
          POLY_BUILDER_PASSPHRASE: BUILDER_CREDENTIALS.passphrase,
        };
      }
      ```

      ```python Python theme={null}
      import os
      import time
      from py_builder_signing_sdk.signing.hmac import build_hmac_signature
      from py_builder_signing_sdk import BuilderApiKeyCreds

      BUILDER_CREDENTIALS = BuilderApiKeyCreds(
          key=os.environ["POLY_BUILDER_API_KEY"],
          secret=os.environ["POLY_BUILDER_SECRET"],
          passphrase=os.environ["POLY_BUILDER_PASSPHRASE"],
      )

      # POST /sign - receives { method, path, body } from the client SDK
      def handle_sign_request(method: str, path: str, body: str):
          timestamp = str(int(time.time()))
          
          signature = build_hmac_signature(
              BUILDER_CREDENTIALS.secret,
              timestamp,
              method,
              path,
              body
          )

          return {
              "POLY_BUILDER_SIGNATURE": signature,
              "POLY_BUILDER_TIMESTAMP": timestamp,
              "POLY_BUILDER_API_KEY": BUILDER_CREDENTIALS.key,
              "POLY_BUILDER_PASSPHRASE": BUILDER_CREDENTIALS.passphrase,
          }
      ```
    </CodeGroup>

    <Warning>
      Never commit credentials to version control. Use environment variables or a secrets manager.
    </Warning>

    ### Client Configuration

    Point your client to your signing server:

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { ClobClient } from "@polymarket/clob-client";
      import { BuilderConfig } from "@polymarket/builder-signing-sdk";

      // Point to your signing server
      const builderConfig = new BuilderConfig({
        remoteBuilderConfig: { 
          url: "https://your-server.com/sign"
        }
      });

      // Or with optional authorization token
      const builderConfigWithAuth = new BuilderConfig({
        remoteBuilderConfig: { 
          url: "https://your-server.com/sign", 
          token: "your-auth-token" 
        }
      });

      const client = new ClobClient(
        "https://clob.polymarket.com",
        137,
        signer, // ethers v5.x EOA signer
        creds, // User's API Credentials
        2, // signatureType for the Safe proxy wallet
        funderAddress, // Safe proxy wallet address
        undefined, 
        false,
        builderConfig
      );

      // Orders automatically use the signing server
      const order = await client.createOrder({
        price: 0.40,
        side: Side.BUY,
        size: 5,
        tokenID: "YOUR_TOKEN_ID"
      });

      const response = await client.postOrder(order);
      ```

      ```python Python theme={null}
      from py_clob_client.client import ClobClient
      from py_builder_signing_sdk import BuilderConfig, RemoteBuilderConfig

      # Point to your signing server
      builder_config = BuilderConfig(
          remote_builder_config=RemoteBuilderConfig(
              url="https://your-server.com/sign"
          )
      )

      # Or with optional authorization token
      builder_config_with_auth = BuilderConfig(
          remote_builder_config=RemoteBuilderConfig(
              url="https://your-server.com/sign",
              token="your-auth-token"
          )
      )

      client = ClobClient(
          host="https://clob.polymarket.com",
          chain_id=137,
          key=private_key,
          creds=creds,  # User's API Credentials
          signature_type=2,  # signatureType for the Safe proxy wallet
          funder=funder_address,  # Safe proxy wallet address
          builder_config=builder_config
      )

      # Orders automatically use the signing server
      order = client.create_order({
          "price": 0.40,
          "side": "BUY",
          "size": 5,
          "token_id": "YOUR_TOKEN_ID"
      })

      response = client.post_order(order)
      ```
    </CodeGroup>

    ### Troubleshooting

    <AccordionGroup>
      <Accordion title="Invalid Signature Errors">
        **Error:** Client receives invalid signature errors

        **Solution:**

        1. Verify the request body is passed correctly as JSON
        2. Check that `path`, `body`, and `method` match what the client sends
        3. Ensure your server and client use the same Builder API credentials
      </Accordion>

      <Accordion title="Missing Credentials">
        **Error:** `Builder credentials not configured` or undefined values

        **Solution:** Ensure your environment variables are set:

        * `POLY_BUILDER_API_KEY`
        * `POLY_BUILDER_SECRET`
        * `POLY_BUILDER_PASSPHRASE`
      </Accordion>
    </AccordionGroup>
  </Tab>

  <Tab title="Local Signing">
    Sign orders locally when you control the entire order placement flow.

    **How it works:**

    1. Your system creates and signs orders on behalf of users
    2. Your system uses Builder API credentials locally to add headers
    3. Complete signed order is sent directly to the CLOB

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { ClobClient } from "@polymarket/clob-client";
      import { BuilderConfig, BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";

      // Configure with local builder credentials
      const builderCreds: BuilderApiKeyCreds = {
        key: process.env.POLY_BUILDER_API_KEY!,
        secret: process.env.POLY_BUILDER_SECRET!,
        passphrase: process.env.POLY_BUILDER_PASSPHRASE!
      };

      const builderConfig = new BuilderConfig({
        localBuilderCreds: builderCreds
      });

      const client = new ClobClient(
        "https://clob.polymarket.com",
        137,
        signer, // ethers v5.x EOA signer
        creds, // User's API Credentials
        2, // signatureType for the Safe proxy wallet
        funderAddress, // Safe proxy wallet address
        undefined, 
        false,
        builderConfig
      );

      // Orders automatically include builder headers
      const order = await client.createOrder({
        price: 0.40,
        side: Side.BUY,
        size: 5,
        tokenID: "YOUR_TOKEN_ID"
      });

      const response = await client.postOrder(order);
      ```

      ```python Python theme={null}
      import os
      from py_clob_client.client import ClobClient
      from py_builder_signing_sdk import BuilderConfig, BuilderApiKeyCreds

      # Configure with local builder credentials
      builder_creds = BuilderApiKeyCreds(
          key=os.environ["POLY_BUILDER_API_KEY"],
          secret=os.environ["POLY_BUILDER_SECRET"],
          passphrase=os.environ["POLY_BUILDER_PASSPHRASE"]
      )

      builder_config = BuilderConfig(
          local_builder_creds=builder_creds
      )

      client = ClobClient(
          host="https://clob.polymarket.com",
          chain_id=137,
          key=private_key,
          creds=creds,  # User's API Credentials
          signature_type=2,  # signatureType for the Safe proxy wallet
          funder=funder_address,  # Safe proxy wallet address
          builder_config=builder_config
      )

      # Orders automatically include builder headers
      order = client.create_order({
          "price": 0.40,
          "side": "BUY",
          "size": 5,
          "token_id": "YOUR_TOKEN_ID"
      })

      response = client.post_order(order)
      ```
    </CodeGroup>

    <Warning>
      Never commit credentials to version control. Use environment variables or a secrets manager.
    </Warning>
  </Tab>
</Tabs>

***

## Authentication Headers

The SDK automatically generates and attaches these headers to each request:

| Header                    | Description                          |
| ------------------------- | ------------------------------------ |
| `POLY_BUILDER_API_KEY`    | Your builder API key                 |
| `POLY_BUILDER_TIMESTAMP`  | Unix timestamp of signature creation |
| `POLY_BUILDER_PASSPHRASE` | Your builder passphrase              |
| `POLY_BUILDER_SIGNATURE`  | HMAC signature of the request        |

<Info>
  With **local signing**, the SDK constructs and attaches these headers automatically. With **remote signing**, your server must return these headers (see Server Implementation above), and the SDK attaches them to the request.
</Info>

***

## Next Steps

<CardGroup cols={2}>
  <Card title="Relayer Client" icon="bolt" href="/developers/builders/relayer-client">
    Learn how to configure and use the Relay Client too!
  </Card>

  <Card title="CLOB Client Methods" icon="book" href="/developers/CLOB/clients/methods-overview">
    Explore the complete CLOB client reference
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt