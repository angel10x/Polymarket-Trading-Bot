# Historical Timeseries Data

> Fetches historical price data for a specified market token.


The CLOB provides detailed price history for each traded token.

**HTTP REQUEST**

`GET /<clob-endpoint>/prices-history`

<Tip>We also have a Interactive Notebook to visualize the data from this endpoint available [here](https://colab.research.google.com/drive/1s4TCOR4K7fRP7EwAH1YmOactMakx24Cs?usp=sharing#scrollTo=mYCJBcfB9Zu4).</Tip>


## OpenAPI

````yaml GET /prices-history
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
  /prices-history:
    get:
      tags:
        - Pricing
      summary: Get price history for a traded token
      description: Fetches historical price data for a specified market token
      parameters:
        - name: market
          in: query
          required: true
          schema:
            type: string
          description: The CLOB token ID for which to fetch price history
          example: '1234567890'
        - name: startTs
          in: query
          required: false
          schema:
            type: number
          description: The start time, a Unix timestamp in UTC
          example: 1697875200
        - name: endTs
          in: query
          required: false
          schema:
            type: number
          description: The end time, a Unix timestamp in UTC
          example: 1697961600
        - name: interval
          in: query
          required: false
          schema:
            type: string
            enum:
              - 1m
              - 1w
              - 1d
              - 6h
              - 1h
              - max
          description: >-
            A string representing a duration ending at the current time.
            Mutually exclusive with startTs and endTs
          example: 1d
        - name: fidelity
          in: query
          required: false
          schema:
            type: number
          description: The resolution of the data, in minutes
          example: 60
      responses:
        '200':
          description: A list of timestamp/price pairs
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PriceHistoryResponse'
        '400':
          description: Bad request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '404':
          description: Market not found
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
    PriceHistoryResponse:
      type: object
      required:
        - history
      properties:
        history:
          type: array
          items:
            type: object
            required:
              - t
              - p
            properties:
              t:
                type: number
                description: UTC timestamp
                example: 1697875200
              p:
                type: number
                description: Price
                example: 1800.75
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