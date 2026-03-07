# Get bid-ask spreads

> Retrieves bid-ask spreads for multiple tokens



## OpenAPI

````yaml api-reference/clob-subset-openapi.yaml post /spreads
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
  /spreads:
    post:
      tags:
        - Spreads
      summary: Get bid-ask spreads
      description: Retrieves bid-ask spreads for multiple tokens
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/BookRequest'
              maxItems: 500
            example:
              - token_id: '1234567890'
              - token_id: '0987654321'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SpreadsResponse'
        '400':
          description: Bad request - Invalid payload or exceeds limit
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
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: error getting the spread
components:
  schemas:
    BookRequest:
      type: object
      required:
        - token_id
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
          description: Optional side parameter for certain operations
          example: BUY
    SpreadsResponse:
      type: object
      additionalProperties:
        type: string
      description: Map of token_id to spread value
      example:
        '1234567890': '0.50'
        '0987654321': '0.05'
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