# Get midpoint price

> Retrieves the midpoint price for a specific token



## OpenAPI

````yaml api-reference/clob-subset-openapi.yaml get /midpoint
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
  /midpoint:
    get:
      tags:
        - Pricing
      summary: Get midpoint price
      description: Retrieves the midpoint price for a specific token
      parameters:
        - name: token_id
          in: query
          required: true
          schema:
            type: string
          description: The unique identifier for the token
          example: '1234567890'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MidpointResponse'
        '400':
          description: Bad request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: Invalid token id
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
    MidpointResponse:
      type: object
      required:
        - mid
      properties:
        mid:
          type: string
          description: The midpoint price (as string to maintain precision)
          example: '1800.75'
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