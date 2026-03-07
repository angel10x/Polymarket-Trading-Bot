# Get user activity

> Returns on-chain activity for a user.



## OpenAPI

````yaml api-reference/data-api-openapi.yaml get /activity
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
  /activity:
    get:
      tags:
        - Core
      summary: Get user activity
      description: Returns on-chain activity for a user.
      parameters:
        - in: query
          name: limit
          schema:
            type: integer
            default: 100
            minimum: 0
            maximum: 500
        - in: query
          name: offset
          schema:
            type: integer
            default: 0
            minimum: 0
            maximum: 10000
        - in: query
          name: user
          required: true
          schema:
            $ref: '#/components/schemas/Address'
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
          name: type
          style: form
          explode: false
          schema:
            type: array
            items:
              type: string
              enum:
                - TRADE
                - SPLIT
                - MERGE
                - REDEEM
                - REWARD
                - CONVERSION
        - in: query
          name: start
          schema:
            type: integer
            minimum: 0
        - in: query
          name: end
          schema:
            type: integer
            minimum: 0
        - in: query
          name: sortBy
          schema:
            type: string
            enum:
              - TIMESTAMP
              - TOKENS
              - CASH
            default: TIMESTAMP
        - in: query
          name: sortDirection
          schema:
            type: string
            enum:
              - ASC
              - DESC
            default: DESC
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
                  $ref: '#/components/schemas/Activity'
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
    Activity:
      type: object
      properties:
        proxyWallet:
          $ref: '#/components/schemas/Address'
        timestamp:
          type: integer
          format: int64
        conditionId:
          $ref: '#/components/schemas/Hash64'
        type:
          type: string
          enum:
            - TRADE
            - SPLIT
            - MERGE
            - REDEEM
            - REWARD
            - CONVERSION
        size:
          type: number
        usdcSize:
          type: number
        transactionHash:
          type: string
        price:
          type: number
        asset:
          type: string
        side:
          type: string
          enum:
            - BUY
            - SELL
        outcomeIndex:
          type: integer
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