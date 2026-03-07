# Place Single Order

> Detailed instructions for creating, placing, and managing orders using Polymarket's CLOB API.

# Create and Place an Order

<Tip> This endpoint requires a L2 Header </Tip>

Create and place an order using the Polymarket CLOB API clients. All orders are represented as "limit" orders, but "market" orders are also supported. To place a market order, simply ensure your price is marketable against current resting limit orders, which are executed on input at the best price.

**HTTP REQUEST**

`POST /<clob-endpoint>/order`

### Request Payload Parameters

| Name      | Required | Type   | Description                      |
| --------- | -------- | ------ | -------------------------------- |
| order     | yes      | Order  | signed object                    |
| owner     | yes      | string | api key of order owner           |
| orderType | yes      | string | order type ("FOK", "GTC", "GTD") |

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
  from py_clob_client.clob_types import OrderArgs, OrderType
  from py_clob_client.order_builder.constants import BUY

  host: str = "https://clob.polymarket.com"
  key: str = "" #This is your Private Key. Export from reveal.polymarket.com or from your Web3 Application
  chain_id: int = 137 #No need to adjust this
  POLYMARKET_PROXY_ADDRESS: str = '' #This is the address you deposit/send USDC to to FUND your Polymarket account.

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

  order_args = OrderArgs(
      price=0.01,
      size=5.0,
      side=BUY,
      token_id="", #Token ID you want to purchase goes here. 
  )
  signed_order = client.create_order(order_args)

  ## GTC(Good-Till-Cancelled) Order
  resp = client.post_order(signed_order, OrderType.GTC)
  print(resp)
  ```

  ```javascript typescript theme={null}
  // GTC Order example
  //
  import { Side, OrderType } from "@polymarket/clob-client";

  async function main() {
    // Create a buy order for 100 YES for 0.50c
    // YES: 71321045679252212594626385532706912750332728571942532289631379312455583992563
    const order = await clobClient.createOrder({
      tokenID:
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      price: 0.5,
      side: Side.BUY,
      size: 100,
      feeRateBps: 0,
      nonce: 1,
    });
    console.log("Created Order", order);

    // Send it to the server

    // GTC Order
    const resp = await clobClient.postOrder(order, OrderType.GTC);
    console.log(resp);
  }

  main();
  // GTD Order example
  //
  import { Side, OrderType } from "@polymarket/clob-client";

  async function main() {
    // Create a buy order for 100 YES for 0.50c that expires in 1 minute
    // YES: 71321045679252212594626385532706912750332728571942532289631379312455583992563

    // There is a 1 minute of security threshold for the expiration field.
    // If we need the order to expire in 30 seconds the correct expiration value is:
    // now + 1 miute + 30 seconds
    const oneMinute = 60 * 1000;
    const seconds = 30 * 1000;
    const expiration = parseInt(
      ((new Date().getTime() + oneMinute + seconds) / 1000).toString()
    );

    const order = await clobClient.createOrder({
      tokenID:
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      price: 0.5,
      side: Side.BUY,
      size: 100,
      feeRateBps: 0,
      nonce: 1,
      // There is a 1 minute of security threshold for the expiration field.
      // If we need the order to expire in 30 seconds the correct expiration value is:
      // now + 1 miute + 30 seconds
      expiration: expiration,
    });
    console.log("Created Order", order);

    // Send it to the server

    // GTD Order
    const resp = await clobClient.postOrder(order, OrderType.GTD);
    console.log(resp);
  }

  main();
  // FOK BUY Order example
  //
  import { Side, OrderType } from "@polymarket/clob-client";

  async function main() {
    // Create a market buy order for $100
    // YES: 71321045679252212594626385532706912750332728571942532289631379312455583992563

    const marketOrder = await clobClient.createMarketOrder({
      side: Side.BUY,
      tokenID:
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      amount: 100, // $$$
      feeRateBps: 0,
      nonce: 0,
      price: 0.5,
    });
    console.log("Created Order", order);

    // Send it to the server
    // FOK Order
    const resp = await clobClient.postOrder(order, OrderType.FOK);
    console.log(resp);
  }

  main();
  // FOK SELL Order example
  //
  import { Side, OrderType } from "@polymarket/clob-client";

  async function main() {
    // Create a market sell order for 100 shares
    // YES: 71321045679252212594626385532706912750332728571942532289631379312455583992563

    const marketOrder = await clobClient.createMarketOrder({
      side: Side.SELL,
      tokenID:
        "71321045679252212594626385532706912750332728571942532289631379312455583992563",
      amount: 100, // shares
      feeRateBps: 0,
      nonce: 0,
      price: 0.5,
    });
    console.log("Created Order", order);

    // Send it to the server
    // FOK Order
    const resp = await clobClient.postOrder(order, OrderType.FOK);
    console.log(resp);
  }

  main();
  ```
</RequestExample>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt