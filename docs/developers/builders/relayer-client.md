# Relayer Client

> Use Polymarket's Polygon relayer to execute gasless transactions for your users

## Overview

The Relayer Client routes onchain transactions through Polymarket's infrastructure, providing gasless transactions for your users. Builder authentication is required to access the relayer.

<CardGroup cols={3}>
  <Card title="Gasless Transactions" icon="gas-pump">
    Polymarket pays all gas fees
  </Card>

  <Card title="Wallet Deployment" icon="wallet">
    Deploy Safe or Proxy wallets
  </Card>

  <Card title="CTF Operations" icon="arrows-split-up-and-left">
    Split, merge, and redeem positions
  </Card>
</CardGroup>

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

## Installation

<CodeGroup>
  ```bash TypeScript theme={null}
  npm install @polymarket/builder-relayer-client
  ```

  ```bash Python theme={null}
  pip install py-builder-relayer-client
  ```
</CodeGroup>

***

## Relayer Endpoint

All relayer requests are sent to Polymarket's relayer service on Polygon:

```
https://relayer-v2.polymarket.com/
```

***

## Signing Methods

<Tabs>
  <Tab title="Remote Signing (Recommended)">
    Remote signing keeps your credentials secure on a server you control.

    **How it works:**

    1. Client sends request details to your signing server
    2. Your server generates the HMAC signature
    3. Client attaches headers and sends to relayer

    ### Server Implementation

    Your signing server receives request details and returns the authentication headers:

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
      import { createWalletClient, http, Hex } from "viem";
      import { privateKeyToAccount } from "viem/accounts";
      import { polygon } from "viem/chains";
      import { RelayClient } from "@polymarket/builder-relayer-client";
      import { BuilderConfig } from "@polymarket/builder-signing-sdk";

      // Create wallet
      const account = privateKeyToAccount(process.env.PRIVATE_KEY as Hex);
      const wallet = createWalletClient({
        account,
        chain: polygon,
        transport: http(process.env.RPC_URL)
      });

      // Configure remote signing
      const builderConfig = new BuilderConfig({
        remoteBuilderConfig: { 
          url: "https://your-server.com/sign" 
        }
      });

      const RELAYER_URL = "https://relayer-v2.polymarket.com/";
      const CHAIN_ID = 137;

      const client = new RelayClient(
        RELAYER_URL,
        CHAIN_ID,
        wallet,
        builderConfig
      );
      ```

      ```python Python theme={null}
      import os
      from py_builder_relayer_client.client import RelayClient
      from py_builder_signing_sdk import BuilderConfig, RemoteBuilderConfig

      private_key = os.getenv("PRIVATE_KEY")

      # Configure remote signing
      builder_config = BuilderConfig(
          remote_builder_config=RemoteBuilderConfig(
              url="https://your-server.com/sign"
          )
      )

      client = RelayClient(
          "https://relayer-v2.polymarket.com",
          137,
          private_key,
          builder_config
      )
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Local Signing">
    Sign locally when your backend handles all transactions.

    **How it works:**

    1. Your system creates transactions on behalf of users
    2. Your system uses Builder API credentials locally to add headers
    3. Complete signed request is sent directly to the relayer

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { createWalletClient, http, Hex } from "viem";
      import { privateKeyToAccount } from "viem/accounts";
      import { polygon } from "viem/chains";
      import { RelayClient } from "@polymarket/builder-relayer-client";
      import { BuilderConfig } from "@polymarket/builder-signing-sdk";

      // Create wallet
      const account = privateKeyToAccount(process.env.PRIVATE_KEY as Hex);
      const wallet = createWalletClient({
        account,
        chain: polygon,
        transport: http(process.env.RPC_URL)
      });

      // Configure local signing
      const builderConfig = new BuilderConfig({
        localBuilderCreds: {
          key: process.env.POLY_BUILDER_API_KEY!,
          secret: process.env.POLY_BUILDER_SECRET!,
          passphrase: process.env.POLY_BUILDER_PASSPHRASE!
        }
      });

      const RELAYER_URL = "https://relayer-v2.polymarket.com/";
      const CHAIN_ID = 137;

      const client = new RelayClient(
        RELAYER_URL,
        CHAIN_ID,
        wallet,
        builderConfig
      );
      ```

      ```python Python theme={null}
      import os
      from py_builder_relayer_client.client import RelayClient
      from py_builder_signing_sdk import BuilderConfig, BuilderApiKeyCreds

      private_key = os.getenv("PRIVATE_KEY")

      # Configure local signing
      builder_config = BuilderConfig(
          local_builder_creds=BuilderApiKeyCreds(
              key=os.getenv("POLY_BUILDER_API_KEY"),
              secret=os.getenv("POLY_BUILDER_SECRET"),
              passphrase=os.getenv("POLY_BUILDER_PASSPHRASE"),
          )
      )

      client = RelayClient(
          "https://relayer-v2.polymarket.com",
          137,
          private_key,
          builder_config
      )
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

## Wallet Types

Choose your wallet type before using the relayer:

<Tabs>
  <Tab title="Safe Wallets">
    Gnosis Safe-based proxy wallets that require explicit deployment before use.

    * **Best for:** Most builder integrations
    * **Deployment:** Call `client.deploy()` before first transaction
    * **Gas fees:** Paid by Polymarket

    <CodeGroup>
      ```typescript TypeScript theme={null}
      const client = new RelayClient(
        "https://relayer-v2.polymarket.com", 
        137,
        eoaSigner, 
        builderConfig, 
        RelayerTxType.SAFE  // Default
      );

      // Deploy before first use
      const response = await client.deploy();
      const result = await response.wait();
      console.log("Safe Address:", result?.proxyAddress);
      ```

      ```python Python theme={null}
      from py_builder_relayer_client.client import RelayClient, RelayerTxType

      client = RelayClient(
          "https://relayer-v2.polymarket.com",
          137,
          private_key,
          builder_config,
          RelayerTxType.SAFE  # Default
      )

      # Deploy before first use
      response = client.deploy()
      result = response.wait()
      print(f"Safe Address: {result.proxy_address}")
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Proxy Wallets">
    Custom Polymarket proxy wallets that auto-deploy on first transaction.

    * **Used for:** Magic Link users from Polymarket.com
    * **Deployment:** Automatic on first transaction
    * **Gas fees:** Paid by Polymarket

    <CodeGroup>
      ```typescript TypeScript theme={null}
      const client = new RelayClient(
        "https://relayer-v2.polymarket.com", 
        137,
        eoaSigner, 
        builderConfig, 
        RelayerTxType.PROXY
      );

      // No deploy() needed - auto-deploys on first tx
      await client.execute([transaction], "First transaction");
      ```

      ```python Python theme={null}
      from py_builder_relayer_client.client import RelayClient, RelayerTxType

      client = RelayClient(
          "https://relayer-v2.polymarket.com",
          137,
          private_key,
          builder_config,
          RelayerTxType.PROXY
      )

      # No deploy() needed - auto-deploys on first tx
      client.execute([transaction], "First transaction")
      ```
    </CodeGroup>
  </Tab>
</Tabs>

<Accordion title="Wallet Comparison Table">
  | Feature           |     Safe Wallets    |      Proxy Wallets      |
  | ----------------- | :-----------------: | :---------------------: |
  | Deployment        | Explicit `deploy()` | Auto-deploy on first tx |
  | Gas Fees          |   Polymarket pays   |     Polymarket pays     |
  | ERC20 Approvals   |          ✅          |            ✅            |
  | CTF Operations    |          ✅          |            ✅            |
  | Send Transactions |          ✅          |            ✅            |
</Accordion>

***

## Usage

### Deploy a Wallet

For Safe wallets, deploy before executing transactions:

<CodeGroup>
  ```typescript TypeScript theme={null}
  const response = await client.deploy();
  const result = await response.wait();

  if (result) {
    console.log("Safe deployed successfully!");
    console.log("Transaction Hash:", result.transactionHash);
    console.log("Safe Address:", result.proxyAddress);
  }
  ```

  ```python Python theme={null}
  response = client.deploy()
  result = response.wait()

  if result:
      print("Safe deployed successfully!")
      print(f"Transaction Hash: {result.transaction_hash}")
      print(f"Safe Address: {result.proxy_address}")
  ```
</CodeGroup>

### Execute Transactions

The `execute` method sends transactions through the relayer. Pass an array of transactions to batch multiple operations in a single call.

<CodeGroup>
  ```typescript TypeScript theme={null}
  interface Transaction {
    to: string;    // Target contract or wallet address
    data: string;  // Encoded function call (use "0x" for simple transfers)
    value: string; // Amount of MATIC to send (usually "0")
  }

  const response = await client.execute(transactions, "Description");
  const result = await response.wait();

  if (result) {
    console.log("Transaction confirmed:", result.transactionHash);
  }
  ```

  ```python Python theme={null}
  # Transaction dict format:
  # { "to": str, "data": str, "value": str }

  response = client.execute(transactions, "Description")
  result = response.wait()

  if result:
      print(f"Transaction confirmed: {result.transaction_hash}")
  ```
</CodeGroup>

### Transaction Examples

<Tabs>
  <Tab title="Transfer">
    Transfer tokens to any address (e.g., withdrawals):

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { encodeFunctionData, parseUnits } from "viem";

      const transferTx = {
        to: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", // USDCe
        data: encodeFunctionData({
          abi: [{
            name: "transfer",
            type: "function",
            inputs: [
              { name: "to", type: "address" },
              { name: "amount", type: "uint256" }
            ],
            outputs: [{ type: "bool" }]
          }],
          functionName: "transfer",
          args: [
            "0xRecipientAddressHere",
            parseUnits("100", 6) // 100 USDCe (6 decimals)
          ]
        }),
        value: "0"
      };

      const response = await client.execute([transferTx], "Transfer USDCe");
      await response.wait();
      ```

      ```python Python theme={null}
      from web3 import Web3

      USDC_E = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

      transfer_tx = {
          "to": USDC_E,
          "data": Web3().eth.contract(
              address=USDC_E,
              abi=[{"name": "transfer", "type": "function", "inputs": [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}], "outputs": [{"type": "bool"}]}]
          ).encodeABI("transfer", ["0xRecipientAddressHere", 100 * 10**6]),
          "value": "0"
      }

      response = client.execute([transfer_tx], "Transfer USDCe")
      response.wait()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Approve">
    Set token allowances to enable trading:

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { encodeFunctionData, maxUint256 } from "viem";

      const approveTx = {
        to: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", // USDCe
        data: encodeFunctionData({
          abi: [{
            name: "approve",
            type: "function",
            inputs: [
              { name: "spender", type: "address" },
              { name: "amount", type: "uint256" }
            ],
            outputs: [{ type: "bool" }]
          }],
          functionName: "approve",
          args: [
            "0x4d97dcd97ec945f40cf65f87097ace5ea0476045", // CTF
            maxUint256
          ]
        }),
        value: "0"
      };

      const response = await client.execute([approveTx], "Approve USDCe for CTF");
      await response.wait();
      ```

      ```python Python theme={null}
      from web3 import Web3

      USDC_E = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
      CTF = "0x4d97dcd97ec945f40cf65f87097ace5ea0476045"
      MAX_UINT256 = 2**256 - 1

      approve_tx = {
          "to": USDC_E,
          "data": Web3().eth.contract(
              address=USDC_E,
              abi=[{"name": "approve", "type": "function", "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}], "outputs": [{"type": "bool"}]}]
          ).encodeABI("approve", [CTF, MAX_UINT256]),
          "value": "0"
      }

      response = client.execute([approve_tx], "Approve USDCe for CTF")
      response.wait()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Redeem Positions">
    Redeem winning conditional tokens after market resolution:

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { encodeFunctionData } from "viem";

      const redeemTx = {
        to: ctfAddress,
        data: encodeFunctionData({
          abi: [{
            name: "redeemPositions",
            type: "function",
            inputs: [
              { name: "collateralToken", type: "address" },
              { name: "parentCollectionId", type: "bytes32" },
              { name: "conditionId", type: "bytes32" },
              { name: "indexSets", type: "uint256[]" }
            ],
            outputs: []
          }],
          functionName: "redeemPositions",
          args: [collateralToken, parentCollectionId, conditionId, indexSets]
        }),
        value: "0"
      };

      const response = await client.execute([redeemTx], "Redeem positions");
      await response.wait();
      ```

      ```python Python theme={null}
      from web3 import Web3

      CTF = "0x4d97dcd97ec945f40cf65f87097ace5ea0476045"

      redeem_tx = {
          "to": CTF,
          "data": Web3().eth.contract(
              address=CTF,
              abi=[{"name": "redeemPositions", "type": "function", "inputs": [{"name": "collateralToken", "type": "address"}, {"name": "parentCollectionId", "type": "bytes32"}, {"name": "conditionId", "type": "bytes32"}, {"name": "indexSets", "type": "uint256[]"}], "outputs": []}]
          ).encodeABI("redeemPositions", [collateral_token, parent_collection_id, condition_id, index_sets]),
          "value": "0"
      }

      response = client.execute([redeem_tx], "Redeem positions")
      response.wait()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Split Positions">
    Split collateral tokens into conditional outcome tokens:

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { encodeFunctionData } from "viem";

      const splitTx = {
        to: ctfAddress,
        data: encodeFunctionData({
          abi: [{
            name: "splitPosition",
            type: "function",
            inputs: [
              { name: "collateralToken", type: "address" },
              { name: "parentCollectionId", type: "bytes32" },
              { name: "conditionId", type: "bytes32" },
              { name: "partition", type: "uint256[]" },
              { name: "amount", type: "uint256" }
            ],
            outputs: []
          }],
          functionName: "splitPosition",
          args: [collateralToken, parentCollectionId, conditionId, partition, amount]
        }),
        value: "0"
      };

      const response = await client.execute([splitTx], "Split positions");
      await response.wait();
      ```

      ```python Python theme={null}
      from web3 import Web3

      CTF = "0x4d97dcd97ec945f40cf65f87097ace5ea0476045"

      split_tx = {
          "to": CTF,
          "data": Web3().eth.contract(
              address=CTF,
              abi=[{"name": "splitPosition", "type": "function", "inputs": [{"name": "collateralToken", "type": "address"}, {"name": "parentCollectionId", "type": "bytes32"}, {"name": "conditionId", "type": "bytes32"}, {"name": "partition", "type": "uint256[]"}, {"name": "amount", "type": "uint256"}], "outputs": []}]
          ).encodeABI("splitPosition", [collateral_token, parent_collection_id, condition_id, partition, amount]),
          "value": "0"
      }

      response = client.execute([split_tx], "Split positions")
      response.wait()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Merge Positions">
    Merge conditional tokens back into collateral:

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { encodeFunctionData } from "viem";

      const mergeTx = {
        to: ctfAddress,
        data: encodeFunctionData({
          abi: [{
            name: "mergePositions",
            type: "function",
            inputs: [
              { name: "collateralToken", type: "address" },
              { name: "parentCollectionId", type: "bytes32" },
              { name: "conditionId", type: "bytes32" },
              { name: "partition", type: "uint256[]" },
              { name: "amount", type: "uint256" }
            ],
            outputs: []
          }],
          functionName: "mergePositions",
          args: [collateralToken, parentCollectionId, conditionId, partition, amount]
        }),
        value: "0"
      };

      const response = await client.execute([mergeTx], "Merge positions");
      await response.wait();
      ```

      ```python Python theme={null}
      from web3 import Web3

      CTF = "0x4d97dcd97ec945f40cf65f87097ace5ea0476045"

      merge_tx = {
          "to": CTF,
          "data": Web3().eth.contract(
              address=CTF,
              abi=[{"name": "mergePositions", "type": "function", "inputs": [{"name": "collateralToken", "type": "address"}, {"name": "parentCollectionId", "type": "bytes32"}, {"name": "conditionId", "type": "bytes32"}, {"name": "partition", "type": "uint256[]"}, {"name": "amount", "type": "uint256"}], "outputs": []}]
          ).encodeABI("mergePositions", [collateral_token, parent_collection_id, condition_id, partition, amount]),
          "value": "0"
      }

      response = client.execute([merge_tx], "Merge positions")
      response.wait()
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Batch Transactions">
    Execute multiple transactions atomically in a single call:

    <CodeGroup>
      ```typescript TypeScript theme={null}
      import { encodeFunctionData, parseUnits, maxUint256 } from "viem";

      const erc20Abi = [
        {
          name: "approve",
          type: "function",
          inputs: [
            { name: "spender", type: "address" },
            { name: "amount", type: "uint256" }
          ],
          outputs: [{ type: "bool" }]
        },
        {
          name: "transfer",
          type: "function",
          inputs: [
            { name: "to", type: "address" },
            { name: "amount", type: "uint256" }
          ],
          outputs: [{ type: "bool" }]
        }
      ] as const;

      // Approve CTF to spend USDCe
      const approveTx = {
        to: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        data: encodeFunctionData({
          abi: erc20Abi,
          functionName: "approve",
          args: ["0x4d97dcd97ec945f40cf65f87097ace5ea0476045", maxUint256]
        }),
        value: "0"
      };

      // Transfer some USDCe to another wallet
      const transferTx = {
        to: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        data: encodeFunctionData({
          abi: erc20Abi,
          functionName: "transfer",
          args: ["0xRecipientAddressHere", parseUnits("50", 6)]
        }),
        value: "0"
      };

      // Both transactions execute in one call
      const response = await client.execute(
        [approveTx, transferTx], 
        "Approve and transfer"
      );
      await response.wait();
      ```

      ```python Python theme={null}
      from web3 import Web3

      USDC_E = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
      CTF = "0x4d97dcd97ec945f40cf65f87097ace5ea0476045"
      MAX_UINT256 = 2**256 - 1

      erc20_abi = [
          {"name": "approve", "type": "function", "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}], "outputs": [{"type": "bool"}]},
          {"name": "transfer", "type": "function", "inputs": [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}], "outputs": [{"type": "bool"}]}
      ]

      contract = Web3().eth.contract(address=USDC_E, abi=erc20_abi)

      # Approve CTF to spend USDCe
      approve_tx = {
          "to": USDC_E,
          "data": contract.encodeABI("approve", [CTF, MAX_UINT256]),
          "value": "0"
      }

      # Transfer some USDCe to another wallet
      transfer_tx = {
          "to": USDC_E,
          "data": contract.encodeABI("transfer", ["0xRecipientAddressHere", 50 * 10**6]),
          "value": "0"
      }

      # Both transactions execute in one call
      response = client.execute([approve_tx, transfer_tx], "Approve and transfer")
      response.wait()
      ```
    </CodeGroup>

    <Info>
      Batching reduces latency and ensures all transactions succeed or fail together.
    </Info>
  </Tab>
</Tabs>

***

## Reference

### Contracts & Approvals

| Contract              | Address                                      | USDCe | Outcome Tokens |
| --------------------- | -------------------------------------------- | :---: | :------------: |
| USDCe                 | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` |   —   |        —       |
| CTF                   | `0x4d97dcd97ec945f40cf65f87097ace5ea0476045` |   ✅   |        —       |
| CTF Exchange          | `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E` |   ✅   |        ✅       |
| Neg Risk CTF Exchange | `0xC5d563A36AE78145C45a50134d48A1215220f80a` |   ✅   |        ✅       |
| Neg Risk Adapter      | `0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296` |   —   |        ✅       |

### Transaction States

| State             | Description                                  |
| ----------------- | -------------------------------------------- |
| `STATE_NEW`       | Transaction received by relayer              |
| `STATE_EXECUTED`  | Transaction executed onchain                 |
| `STATE_MINED`     | Transaction included in a block              |
| `STATE_CONFIRMED` | Transaction confirmed (final ✅)              |
| `STATE_FAILED`    | Transaction failed (terminal ❌)              |
| `STATE_INVALID`   | Transaction rejected as invalid (terminal ❌) |

### TypeScript Types

<Accordion title="View Type Definitions">
  ```typescript  theme={null}
  // Transaction type used in all examples
  interface Transaction {
    to: string;
    data: string;
    value: string;
  }

  // Wallet type selector
  enum RelayerTxType {
    SAFE = "SAFE",
    PROXY = "PROXY"
  }

  // Transaction states
  enum RelayerTransactionState {
    STATE_NEW = "STATE_NEW",
    STATE_EXECUTED = "STATE_EXECUTED",
    STATE_MINED = "STATE_MINED",
    STATE_CONFIRMED = "STATE_CONFIRMED",
    STATE_FAILED = "STATE_FAILED",
    STATE_INVALID = "STATE_INVALID"
  }

  // Response from relayer
  interface RelayerTransaction {
    transactionID: string;
    transactionHash: string;
    from: string;
    to: string;
    proxyAddress: string;
    data: string;
    state: string;
    type: string;
    metadata: string;
    createdAt: Date;
    updatedAt: Date;
  }
  ```
</Accordion>

***

## Next Steps

<CardGroup cols={2}>
  <Card title="Order Attribution" icon="tag" href="/developers/builders/order-attribution">
    Attribute orders to your builder account
  </Card>

  <Card title="Example Apps" icon="code" href="/developers/builders/examples">
    Complete integration examples
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt