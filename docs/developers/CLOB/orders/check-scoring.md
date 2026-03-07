# Check Order Reward Scoring

> Check if an order is eligble or scoring for Rewards purposes

<Tip> This endpoint requires a L2 Header. </Tip>

Returns a boolean value where it is indicated if an order is scoring or not.

**HTTP REQUEST**

`GET /<clob-endpoint>/order-scoring?order_id={...}`

### Request Parameters

| Name    | Required | Type   | Description                          |
| ------- | -------- | ------ | ------------------------------------ |
| orderId | yes      | string | id of order to get information about |

### Response Format

| Name | Type          | Description        |
| ---- | ------------- | ------------------ |
| null | OrdersScoring | order scoring data |

An `OrdersScoring` object is of the form:

| Name    | Type    | Description                              |
| ------- | ------- | ---------------------------------------- |
| scoring | boolean | indicates if the order is scoring or not |

# Check if some orders are scoring

> This endpoint requires a L2 Header.

Returns to a dictionary with boolean value where it is indicated if an order is scoring or not.

**HTTP REQUEST**

`POST /<clob-endpoint>/orders-scoring`

### Request Parameters

| Name     | Required | Type      | Description                                |
| -------- | -------- | --------- | ------------------------------------------ |
| orderIds | yes      | string\[] | ids of the orders to get information about |

### Response Format

| Name | Type          | Description         |
| ---- | ------------- | ------------------- |
| null | OrdersScoring | orders scoring data |

An `OrdersScoring` object is a dictionary that indicates the order by if it score.

<RequestExample>
  ```python Python theme={null}
  scoring = client.is_order_scoring(
      OrderScoringParams(
          orderId="0x..."
      )
  )
  print(scoring)

  scoring = client.are_orders_scoring(
      OrdersScoringParams(
          orderIds=["0x..."]
      )
  )
  print(scoring)
  ```

  ```javascript Typescript theme={null}
  async function main() {
    const scoring = await clobClient.isOrderScoring({
      orderId: "0x...",
    });
    console.log(scoring);
  }

  main();

  async function main() {
    const scoring = await clobClient.areOrdersScoring({
      orderIds: ["0x..."],
    });
    console.log(scoring);
  }

  main();

  ```
</RequestExample>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt