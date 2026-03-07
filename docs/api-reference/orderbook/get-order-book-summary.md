# Get order book summary

> Retrieves the order book summary for a specific token



## OpenAPI

````yaml api-reference/clob-subset-openapi.yaml get /book
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
  /book:
    get:
      tags:
        - Orderbook
      summary: Get order book summary
      description: Retrieves the order book summary for a specific token
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
                $ref: '#/components/schemas/OrderBookSummary'
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
              example:
                error: error getting the orderbook
components:
  schemas:
    OrderBookSummary:
      type: object
      required:
        - market
        - asset_id
        - timestamp
        - hash
        - bids
        - asks
        - min_order_size
        - tick_size
        - neg_risk
      properties:
        market:
          type: string
          description: Market identifier
          example: '0x1b6f76e5b8587ee896c35847e12d11e75290a8c3934c5952e8a9d6e4c6f03cfa'
        asset_id:
          type: string
          description: Asset identifier
          example: '1234567890'
        timestamp:
          type: string
          format: date-time
          description: Timestamp of the order book snapshot
          example: '2023-10-01T12:00:00Z'
        hash:
          type: string
          description: Hash of the order book state
          example: 0xabc123def456...
        bids:
          type: array
          items:
            $ref: '#/components/schemas/OrderLevel'
          description: Array of bid levels
        asks:
          type: array
          items:
            $ref: '#/components/schemas/OrderLevel'
          description: Array of ask levels
        min_order_size:
          type: string
          description: Minimum order size for this market
          example: '0.001'
        tick_size:
          type: string
          description: Minimum price increment
          example: '0.01'
        neg_risk:
          type: boolean
          description: Whether negative risk is enabled
          example: false
    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: string
          description: Error message describing what went wrong
          example: Invalid token id
    OrderLevel:
      type: object
      required:
        - price
        - size
      properties:
        price:
          type: string
          description: Price level (as string to maintain precision)
          example: '1800.50'
        size:
          type: string
          description: Total size at this price level
          example: '10.5'

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt