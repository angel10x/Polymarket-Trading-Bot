# Cancel Orders(s)

> Multiple endpoints to cancel a single order, multiple orders, all orders or all orders from a single market.

# Cancel an single Order

<Tip> This endpoint requires a L2 Header. </Tip>

Cancel an order.

**HTTP REQUEST**

`DELETE /<clob-endpoint>/order`

### Request Payload Parameters

| Name    | Required | Type   | Description           |
| ------- | -------- | ------ | --------------------- |
| orderID | yes      | string | ID of order to cancel |

### Response Format

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

<CodeGroup>
  ```python Python theme={null}
  resp = client.cancel(order_id="0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88")
  print(resp)
  ```

  ```javascript Typescript theme={null}
  async function main() {
    // Send it to the server
    const resp = await clobClient.cancelOrder({
      orderID:
        "0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88",
    });
    console.log(resp);
    console.log(`Done!`);
  }
  main();
  ```
</CodeGroup>

# Cancel Multiple Orders

<Tip> This endpoint requires a L2 Header. </Tip>

**HTTP REQUEST**

`DELETE /<clob-endpoint>/orders`

### Request Payload Parameters

| Name | Required | Type      | Description                 |
| ---- | -------- | --------- | --------------------------- |
| null | yes      | string\[] | IDs of the orders to cancel |

### Response Format

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

<CodeGroup>
  ```python Python theme={null}
  resp = client.cancel_orders(["0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88", "0xaaaa..."])
  print(resp)
  ```

  ```javascript Typescript theme={null}
  async function main() {
    // Send it to the server
    const resp = await clobClient.cancelOrders([
      "0x38a73eed1e6d177545e9ab027abddfb7e08dbe975fa777123b1752d203d6ac88",
      "0xaaaa...",
    ]);
    console.log(resp);
    console.log(`Done!`);
  }
  main();
  ```
</CodeGroup>

# Cancel ALL Orders

<Tip> This endpoint requires a L2 Header. </Tip>

Cancel all open orders posted by a user.

**HTTP REQUEST**

`DELETE /<clob-endpoint>/cancel-all`

### Response Format

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

<CodeGroup>
  ```python Python theme={null}
  resp = client.cancel_all()
  print(resp)
  print("Done!")
  ```

  ```javascript Typescript theme={null}
  async function main() {
    const resp = await clobClient.cancelAll();
    console.log(resp);
    console.log(`Done!`);
  }

  main();
  ```
</CodeGroup>

# Cancel orders from market

<Tip> This endpoint requires a L2 Header. </Tip>

Cancel orders from market.

**HTTP REQUEST**

`DELETE /<clob-endpoint>/cancel-market-orders`

### Request Payload Parameters

| Name      | Required | Type   | Description                |
| --------- | -------- | ------ | -------------------------- |
| market    | no       | string | condition id of the market |
| asset\_id | no       | string | id of the asset/token      |

### Response Format

| Name          | Type      | Description                                                                |
| ------------- | --------- | -------------------------------------------------------------------------- |
| canceled      | string\[] | list of canceled orders                                                    |
| not\_canceled | {}        | a order id -> reason map that explains why that order couldn't be canceled |

<CodeGroup>
  ```python Python theme={null}
  resp = client.cancel_market_orders(market="0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af", asset_id="52114319501245915516055106046884209969926127482827954674443846427813813222426")
  print(resp)

  ```

  ```javascript Typescript theme={null}
  async function main() {
    // Send it to the server
    const resp = await clobClient.cancelMarketOrders({
      market:
        "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
      asset_id:
        "52114319501245915516055106046884209969926127482827954674443846427813813222426",
    });
    console.log(resp);
    console.log(`Done!`);
  }
  main();
  ```
</CodeGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt