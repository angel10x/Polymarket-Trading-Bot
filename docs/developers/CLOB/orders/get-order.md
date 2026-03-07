# Get Order

> Get information about an existing order

<Tip>This endpoint requires a L2 Header. </Tip>

Get single order by id.

**HTTP REQUEST**

`GET /<clob-endpoint>/data/order/<order_hash>`

### Request Parameters

| Name | Required | Type   | Description                          |
| ---- | -------- | ------ | ------------------------------------ |
| id   | no       | string | id of order to get information about |

### Response Format

| Name  | Type      | Description        |
| ----- | --------- | ------------------ |
| order | OpenOrder | order if it exists |

An `OpenOrder` object is of the form:

| Name              | Type      | Description                                                    |
| ----------------- | --------- | -------------------------------------------------------------- |
| associate\_trades | string\[] | any Trade id the order has been partially included in          |
| id                | string    | order id                                                       |
| status            | string    | order current status                                           |
| market            | string    | market id (condition id)                                       |
| original\_size    | string    | original order size at placement                               |
| outcome           | string    | human readable outcome the order is for                        |
| maker\_address    | string    | maker address (funder)                                         |
| owner             | string    | api key                                                        |
| price             | string    | price                                                          |
| side              | string    | buy or sell                                                    |
| size\_matched     | string    | size of order that has been matched/filled                     |
| asset\_id         | string    | token id                                                       |
| expiration        | string    | unix timestamp when the order expired, 0 if it does not expire |
| type              | string    | order type (GTC, FOK, GTD)                                     |
| created\_at       | string    | unix timestamp when the order was created                      |

<RequestExample>
  ```python Python theme={null}
  order = clob_client.get_order("0xb816482a5187a3d3db49cbaf6fe3ddf24f53e6c712b5a4bf5e01d0ec7b11dabc")
  print(order)
  ```

  ```javascript Typescript theme={null}
  async function main() {
    const order = await clobClient.getOrder(
      "0xb816482a5187a3d3db49cbaf6fe3ddf24f53e6c712b5a4bf5e01d0ec7b11dabc"
    );
    console.log(order);
  }

  main();

  ```
</RequestExample>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt