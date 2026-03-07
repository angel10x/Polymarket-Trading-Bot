# Get multiple market prices

> Retrieves market prices for multiple tokens and sides



## OpenAPI

````yaml api-reference/clob-subset-openapi.yaml get /prices
openapi: 3.0.3
info:
  title: CLOB (Central Limit Order Book) API
  description: >-
    API for interacting with the Central Limit Order Book system, providing
    orderbook data, prices, midpoints, and spreads
  version: 1.0.0
  contact:
    name: CLOB API Team
  license:
    name: MIT
servers:
  - url: https://clob.polymarket.com/
    description: Production server
security: []
tags:
  - name: Orderbook
    description: Order book related operations
  - name: Pricing
    description: Price and midpoint operations
  - name: Spreads
    description: Spread calculation operations
paths:
  /prices:
    get:
      tags:
        - Pricing
      summary: Get multiple market prices
      description: Retrieves market prices for multiple tokens and sides
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PricesResponse'
        '400':
          description: Bad request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
components:
  schemas:
    PricesResponse:
      type: object
      additionalProperties:
        type: object
        additionalProperties:
          type: string
      description: Map of token_id to side to price
      example:
        '1234567890':
          BUY: '1800.50'
          SELL: '1801.00'
        '0987654321':
          BUY: '50.25'
          SELL: '50.30'
    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: string
          description: Error message describing what went wrong
          example: Invalid token id

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt