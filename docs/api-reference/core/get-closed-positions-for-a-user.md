# Get closed positions for a user

> Fetches closed positions for a user(address)



## OpenAPI

````yaml api-reference/data-api-openapi.yaml get /closed-positions
openapi: 3.0.3
info:
  title: Polymarket Data API
  version: 1.0.0
  description: >
    HTTP API for Polymarket data. This specification documents all public
    routes.
servers:
  - url: https://data-api.polymarket.com
    description: Relative server (same host)
security: []
tags:
  - name: Health
  - name: Core
  - name: Builders
  - name: Misc
paths:
  /closed-positions:
    get:
      tags:
        - Core
      summary: Get closed positions for a user
      description: Fetches closed positions for a user(address)
      parameters:
        - in: query
          name: user
          required: true
          schema:
            $ref: '#/components/schemas/Address'
          description: The address of the user in question
        - in: query
          name: market
          style: form
          explode: false
          schema:
            type: array
            items:
              $ref: '#/components/schemas/Hash64'
          description: >-
            The conditionId of the market in question. Supports multiple csv
            separated values. Cannot be used with the eventId param.
        - in: query
          name: title
          schema:
            type: string
            maxLength: 100
          description: Filter by market title
        - in: query
          name: eventId
          style: form
          explode: false
          schema:
            type: array
            items:
              type: integer
              minimum: 1
          description: >-
            The event id of the event in question. Supports multiple csv
            separated values. Returns positions for all markets for those event
            ids. Cannot be used with the market param.
        - in: query
          name: limit
          schema:
            type: integer
            default: 10
            minimum: 0
            maximum: 50
          description: The max number of positions to return
        - in: query
          name: offset
          schema:
            type: integer
            default: 0
            minimum: 0
            maximum: 100000
          description: The starting index for pagination
        - in: query
          name: sortBy
          schema:
            type: string
            enum:
              - REALIZEDPNL
              - TITLE
              - PRICE
              - AVGPRICE
              - TIMESTAMP
            default: REALIZEDPNL
          description: The sort criteria
        - in: query
          name: sortDirection
          schema:
            type: string
            enum:
              - ASC
              - DESC
            default: DESC
          description: The sort direction
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ClosedPosition'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '500':
          description: Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    Address:
      type: string
      description: User Profile Address (0x-prefixed, 40 hex chars)
      pattern: ^0x[a-fA-F0-9]{40}$
      example: '0x56687bf447db6ffa42ffe2204a05edaa20f55839'
    Hash64:
      type: string
      description: 0x-prefixed 64-hex string
      pattern: ^0x[a-fA-F0-9]{64}$
      example: '0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917'
    ClosedPosition:
      type: object
      properties:
        proxyWallet:
          $ref: '#/components/schemas/Address'
        asset:
          type: string
        conditionId:
          $ref: '#/components/schemas/Hash64'
        avgPrice:
          type: number
        totalBought:
          type: number
        realizedPnl:
          type: number
        curPrice:
          type: number
        timestamp:
          type: integer
          format: int64
        title:
          type: string
        slug:
          type: string
        icon:
          type: string
        eventSlug:
          type: string
        outcome:
          type: string
        outcomeIndex:
          type: integer
        oppositeOutcome:
          type: string
        oppositeAsset:
          type: string
        endDate:
          type: string
    ErrorResponse:
      type: object
      properties:
        error:
          type: string
      required:
        - error

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt