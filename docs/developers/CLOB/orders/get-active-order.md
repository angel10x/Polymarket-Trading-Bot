# Get Active Orders

<Tip> This endpoint requires a L2 Header. </Tip>

Get active order(s) for a specific market.

**HTTP REQUEST**

`GET /<clob-endpoint>/data/orders`

### Request Parameters

| Name      | Required | Type   | Description                          |
| --------- | -------- | ------ | ------------------------------------ |
| id        | no       | string | id of order to get information about |
| market    | no       | string | condition id of market               |
| asset\_id | no       | string | id of the asset/token                |

### Response Format

| Name | Type         | Description                                          |
| ---- | ------------ | ---------------------------------------------------- |
| null | OpenOrder\[] | list of open orders filtered by the query parameters |

<RequestExample>
  ```python Python theme={null}
  from py_clob_client.clob_types import OpenOrderParams

  resp = client.get_orders(
      OpenOrderParams(
          market="0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
      )
  )
  print(resp)
  print("Done!")
  ```

  ```javascript Typescript theme={null}
  async function main() {
    const resp = await clobClient.getOpenOrders({
      market:
        "0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
    });
    console.log(resp);
    console.log(`Done!`);
  }
  main();
  ```
</RequestExample>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt