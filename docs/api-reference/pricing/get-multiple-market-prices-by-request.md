# Get multiple market prices by request

> Retrieves market prices for specified tokens and sides via POST request



## OpenAPI

````yaml api-reference/clob-subset-openapi.yaml post /prices
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
    post:
      tags:
        - Pricing
      summary: Get multiple market prices by request
      description: Retrieves market prices for specified tokens and sides via POST request
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/PriceRequest'
              maxItems: 500
            example:
              - token_id: '1234567890'
                side: BUY
              - token_id: '0987654321'
                side: SELL
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PricesResponse'
        '400':
          description: Bad request - Invalid payload, exceeds limit, or invalid side
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              examples:
                invalid_payload:
                  value:
                    error: Invalid payload
                exceeds_limit:
                  value:
                    error: Payload exceeds the limit
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
    PriceRequest:
      type: object
      required:
        - token_id
        - side
      properties:
        token_id:
          type: string
          description: The unique identifier for the token
          example: '1234567890'
        side:
          type: string
          enum:
            - BUY
            - SELL
          description: The side of the market (BUY or SELL)
          example: BUY
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