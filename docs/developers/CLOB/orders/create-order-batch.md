# Place Multiple Orders (Batching)

> Instructions for placing multiple orders(Batch)

<Tip> This endpoint requires a L2 Header </Tip>

Polymarket’s CLOB supports batch orders, allowing you to place up to `15` orders in a single request. Before using this feature, make sure you're comfortable placing a single order first. You can find the documentation for that [here.](/developers/CLOB/orders/create-order)

**HTTP REQUEST**

`POST /<clob-endpoint>/orders`

### Request Payload Parameters

| Name      | Required | Type          | Description                                                      |
| --------- | -------- | ------------- | ---------------------------------------------------------------- |
| PostOrder | yes      | PostOrders\[] | list of signed order objects (Signed Order + Order Type + Owner) |

A `PostOrder` object is the form:

| Name      | Required | Type   | Description                                         |
| --------- | -------- | ------ | --------------------------------------------------- |
| order     | yes      | order  | See below table for details on crafting this object |
| orderType | yes      | string | order type ("FOK", "GTC", "GTD", "FAK")             |
| owner     | yes      | string | api key of order owner                              |

An `order` object is the form:

| Name          | Required | Type    | Description                                        |
| ------------- | -------- | ------- | -------------------------------------------------- |
| salt          | yes      | integer | random salt used to create unique order            |
| maker         | yes      | string  | maker address (funder)                             |
| signer        | yes      | string  | signing address                                    |
| taker         | yes      | string  | taker address (operator)                           |
| tokenId       | yes      | string  | ERC1155 token ID of conditional token being traded |
| makerAmount   | yes      | string  | maximum amount maker is willing to spend           |
| takerAmount   | yes      | string  | minimum amount taker will pay the maker in return  |
| expiration    | yes      | string  | unix expiration timestamp                          |
| nonce         | yes      | string  | maker's exchange nonce of the order is associated  |
| feeRateBps    | yes      | string  | fee rate basis points as required by the operator  |
| side          | yes      | string  | buy or sell enum index                             |
| signatureType | yes      | integer | signature type enum index                          |
| signature     | yes      | string  | hex encoded signature                              |

### Order types

* **FOK**: A Fill-Or-Kill order is an market order to buy (in dollars) or sell (in shares) shares that must be executed immediately in its entirety; otherwise, the entire order will be cancelled.
* **FAK**: A Fill-And-Kill order is a market order to buy (in dollars) or sell (in shares) that will be executed immediately for as many shares as are available; any portion not filled at once is cancelled.
* **GTC**: A Good-Til-Cancelled order is a limit order that is active until it is fulfilled or cancelled.
* **GTD**: A Good-Til-Date order is a type of order that is active until its specified date (UTC seconds timestamp), unless it has already been fulfilled or cancelled. There is a security threshold of one minute. If the order needs to expire in 90 seconds the correct expiration value is: now + 1 minute + 30 seconds

### Response Format

| Name        | Type      | Description                                                                                                                        |
| ----------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| success     | boolean   | boolean indicating if server-side err (`success = false`) -> server-side error                                                     |
| errorMsg    | string    | error message in case of unsuccessful placement (in case `success = false`, e.g. `client-side error`, the reason is in `errorMsg`) |
| orderId     | string    | id of order                                                                                                                        |
| orderHashes | string\[] | hash of settlement transaction order was marketable and triggered a match                                                          |

### Insert Error Messages

If the `errorMsg` field of the response object from placement is not an empty string, the order was not able to be immediately placed. This might be because of a delay or because of a failure. If the `success` is not `true`, then there was an issue placing the order. The following `errorMessages` are possible:

#### Error

| Error                                | Success | Message                                                                                 | Description                                                           |
| ------------------------------------ | ------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| INVALID\_ORDER\_MIN\_TICK\_SIZE      | yes     | order is invalid. Price breaks minimum tick size rules                                  | order price isn't accurate to correct tick sizing                     |
| INVALID\_ORDER\_MIN\_SIZE            | yes     | order is invalid. Size lower than the minimum                                           | order size must meet min size threshold requirement                   |
| INVALID\_ORDER\_DUPLICATED           | yes     | order is invalid. Duplicated. Same order has already been placed, can't be placed again |                                                                       |
| INVALID\_ORDER\_NOT\_ENOUGH\_BALANCE | yes     | not enough balance / allowance                                                          | funder address doesn't have sufficient balance or allowance for order |
| INVALID\_ORDER\_EXPIRATION           | yes     | invalid expiration                                                                      | expiration field expresses a time before now                          |
| INVALID\_ORDER\_ERROR                | yes     | could not insert order                                                                  | system error while inserting order                                    |
| EXECUTION\_ERROR                     | yes     | could not run the execution                                                             | system error while attempting to execute trade                        |
| ORDER\_DELAYED                       | no      | order match delayed due to market conditions                                            | order placement delayed                                               |
| DELAYING\_ORDER\_ERROR               | yes     | error delaying the order                                                                | system error while delaying order                                     |
| FOK\_ORDER\_NOT\_FILLED\_ERROR       | yes     | order couldn't be fully filled, FOK orders are fully filled/killed                      | FOK order not fully filled so can't be placed                         |
| MARKET\_NOT\_READY                   | no      | the market is not yet ready to process new orders                                       | system not accepting orders for market yet                            |

### Insert Statuses

When placing an order, a status field is included. The status field provides additional information regarding the order's state as a result of the placement. Possible values include:

#### Status

| Status    | Description                                                  |
| --------- | ------------------------------------------------------------ |
| matched   | order placed and matched with an existing resting order      |
| live      | order placed and resting on the book                         |
| delayed   | order marketable, but subject to matching delay              |
| unmatched | order marketable, but failure delaying, placement successful |

<RequestExample>
  ```python Python theme={null}
  from py_clob_client.client import ClobClient
  from py_clob_client.clob_types import OrderArgs, OrderType, PostOrdersArgs
  from py_clob_client.order_builder.constants import BUY


  host: str = "https://clob.polymarket.com"
  key: str = "" ##This is your Private Key. Export from https://reveal.magic.link/polymarket or from your Web3 Application
  chain_id: int = 137 #No need to adjust this
  POLYMARKET_PROXY_ADDRESS: str = '' #This is the address listed below your profile picture when using the Polymarket site.

  #Select from the following 3 initialization options to matches your login method, and remove any unused lines so only one client is initialized.


  ### Initialization of a client using a Polymarket Proxy associated with an Email/Magic account. If you login with your email use this example.
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client using a Polymarket Proxy associated with a Browser Wallet(Metamask, Coinbase Wallet, etc)
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client that trades directly from an EOA. 
  client = ClobClient(host, key=key, chain_id=chain_id)

  ## Create and sign a limit order buying 100 YES tokens for 0.50c each
  #Refer to the Markets API documentation to locate a tokenID: https://docs.polymarket.com/developers/gamma-markets-api/get-markets

  client.set_api_creds(client.create_or_derive_api_creds()) 

  resp = client.post_orders([
      PostOrdersArgs(
          # Create and sign a limit order buying 100 YES tokens for 0.50 each
          order=client.create_order(OrderArgs(
              price=0.01,
              size=5,
              side=BUY,
              token_id="88613172803544318200496156596909968959424174365708473463931555296257475886634",
          )),
          orderType=OrderType.GTC,  # Good 'Til Cancelled
      ),
      PostOrdersArgs(
          # Create and sign a limit order selling 200 NO tokens for 0.25 each
          order=client.create_order(OrderArgs(
              price=0.01,
              size=5,
              side=BUY,
              token_id="93025177978745967226369398316375153283719303181694312089956059680730874301533",
          )),
          orderType=OrderType.GTC,  # Good 'Til Cancelled
      )
  ])
  print(resp)
  print("Done!")
  ```

  ```javascript typescript theme={null}
  import { ethers } from "ethers";
  import { config as dotenvConfig } from "dotenv";
  import { resolve } from "path";
  import { ApiKeyCreds, Chain, ClobClient, OrderType, PostOrdersArgs, Side } from "../src";

  dotenvConfig({ path: resolve(__dirname, "../.env") });

  async function main() {
      const wallet = new ethers.Wallet(`${process.env.PK}`);
      const chainId = parseInt(`${process.env.CHAIN_ID || Chain.AMOY}`) as Chain;
      console.log(`Address: ${await wallet.getAddress()}, chainId: ${chainId}`);

      const host = process.env.CLOB_API_URL || "https://clob.polymarket.com";
      const creds: ApiKeyCreds = {
          key: `${process.env.CLOB_API_KEY}`,
          secret: `${process.env.CLOB_SECRET}`,
          passphrase: `${process.env.CLOB_PASS_PHRASE}`,
      };
      const clobClient = new ClobClient(host, chainId, wallet, creds);

      await clobClient.cancelAll();

      const YES = "71321045679252212594626385532706912750332728571942532289631379312455583992563";
      const orders: PostOrdersArgs[] = [
          {
              order: await clobClient.createOrder({
                  tokenID: YES,
                  price: 0.4,
                  side: Side.BUY,
                  size: 100,
              }),
              orderType: OrderType.GTC,
          },
          {
              order: await clobClient.createOrder({
                  tokenID: YES,
                  price: 0.45,
                  side: Side.BUY,
                  size: 100,
              }),
              orderType: OrderType.GTC,
          },
          {
              order: await clobClient.createOrder({
                  tokenID: YES,
                  price: 0.55,
                  side: Side.SELL,
                  size: 100,
              }),
              orderType: OrderType.GTC,
          },
          {
              order: await clobClient.createOrder({
                  tokenID: YES,
                  price: 0.6,
                  side: Side.SELL,
                  size: 100,
              }),
              orderType: OrderType.GTC,
          },
      ];

      // Send it to the server
      const resp = await clobClient.postOrders(orders);
      console.log(resp);
  }

  main();
  ```

  ```REQUEST Example Payload theme={null}
  [
      {'order': {'salt': 660377097, 'maker': '0x17A9568474b5fc84B1D1C44f081A0a3aDE750B2b', 'signer': '0x17A9568474b5fc84B1D1C44f081A0a3aDE750B2b', 'taker': '0x0000000000000000000000000000000000000000', 'tokenId': '88613172803544318200496156596909968959424174365708473463931555296257475886634', 'makerAmount': '50000', 'takerAmount': '5000000', 'expiration': '0', 'nonce': '0', 'feeRateBps': '0', 'side': 'BUY', 'signatureType': 0, 'signature': '0xccb8d1298d698ebc0859e6a26044c848ac4a4b0e20a391a4574e42b9c9bf237e5fa09fc00743e3e2d2f8e909a21d60f276ce083cc35c6661410b892f5bcbe2291c'}, 'owner': 'PRIVATEKEY', 'orderType': 'GTC'}, 
      {'order': {'salt': 1207111323, 'maker': '0x17A9568474b5fc84B1D1C44f081A0a3aDE750B2b', 'signer': '0x17A9568474b5fc84B1D1C44f081A0a3aDE750B2b', 'taker': '0x0000000000000000000000000000000000000000', 'tokenId': '93025177978745967226369398316375153283719303181694312089956059680730874301533', 'makerAmount': '50000', 'takerAmount': '5000000', 'expiration': '0', 'nonce': '0', 'feeRateBps': '0', 'side': 'BUY', 'signatureType': 0, 'signature': '0x0feca28666283824c27d7bead0bc441dde6df20dd71ef5ff7c84d3d1d5bf8aa4296fa382769dc11a92abe05b6f731d6c32556e9b4fb29e6eb50131af23a9ac941c'}, 'owner': 'PRIVATEKEY', 'orderType': 'GTC'}
  ]

  ```
</RequestExample>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt