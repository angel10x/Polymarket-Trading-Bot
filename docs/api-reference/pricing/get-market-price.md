# Get market price

> Retrieves the market price for a specific token and side



## OpenAPI

````yaml api-reference/clob-subset-openapi.yaml get /price
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
  /price:
    get:
      tags:
        - Pricing
      summary: Get market price
      description: Retrieves the market price for a specific token and side
      parameters:
        - name: token_id
          in: query
          required: true
          schema:
            type: string
          description: The unique identifier for the token
          example: '1234567890'
        - name: side
          in: query
          required: true
          schema:
            type: string
            enum:
              - BUY
              - SELL
          description: The side of the market (BUY or SELL)
          example: BUY
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PriceResponse'
        '400':
          description: Bad request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              examples:
                invalid_token:
                  value:
                    error: Invalid token id
                invalid_side:
                  value:
                    error: Invalid side
        '404':
          description: Order book not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: No orderbook exists for the requested token id
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
components:
  schemas:
    PriceResponse:
      type: object
      required:
        - price
      properties:
        price:
          type: string
          description: The market price (as string to maintain precision)
          example: '1800.50'
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