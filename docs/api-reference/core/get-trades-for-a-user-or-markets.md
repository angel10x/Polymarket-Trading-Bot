# Get trades for a user or markets



## OpenAPI

````yaml api-reference/data-api-openapi.yaml get /trades
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
  /trades:
    get:
      tags:
        - Core
      summary: Get trades for a user or markets
      parameters:
        - in: query
          name: limit
          schema:
            type: integer
            default: 100
            minimum: 0
            maximum: 10000
        - in: query
          name: offset
          schema:
            type: integer
            default: 0
            minimum: 0
            maximum: 10000
        - in: query
          name: takerOnly
          schema:
            type: boolean
            default: true
        - in: query
          name: filterType
          schema:
            type: string
            enum:
              - CASH
              - TOKENS
          description: Must be provided together with filterAmount.
        - in: query
          name: filterAmount
          schema:
            type: number
            minimum: 0
          description: Must be provided together with filterType.
        - in: query
          name: market
          style: form
          explode: false
          schema:
            type: array
            items:
              $ref: '#/components/schemas/Hash64'
          description: >-
            Comma-separated list of condition IDs. Mutually exclusive with
            eventId.
        - in: query
          name: eventId
          style: form
          explode: false
          schema:
            type: array
            items:
              type: integer
              minimum: 1
          description: Comma-separated list of event IDs. Mutually exclusive with market.
        - in: query
          name: user
          schema:
            $ref: '#/components/schemas/Address'
        - in: query
          name: side
          schema:
            type: string
            enum:
              - BUY
              - SELL
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Trade'
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
    Hash64:
      type: string
      description: 0x-prefixed 64-hex string
      pattern: ^0x[a-fA-F0-9]{64}$
      example: '0xdd22472e552920b8438158ea7238bfadfa4f736aa4cee91a6b86c39ead110917'
    Address:
      type: string
      description: User Profile Address (0x-prefixed, 40 hex chars)
      pattern: ^0x[a-fA-F0-9]{40}$
      example: '0x56687bf447db6ffa42ffe2204a05edaa20f55839'
    Trade:
      type: object
      properties:
        proxyWallet:
          $ref: '#/components/schemas/Address'
        side:
          type: string
          enum:
            - BUY
            - SELL
        asset:
          type: string
        conditionId:
          $ref: '#/components/schemas/Hash64'
        size:
          type: number
        price:
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
        name:
          type: string
        pseudonym:
          type: string
        bio:
          type: string
        profileImage:
          type: string
        profileImageOptimized:
          type: string
        transactionHash:
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