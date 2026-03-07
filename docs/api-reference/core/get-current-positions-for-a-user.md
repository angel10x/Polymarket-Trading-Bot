# Get current positions for a user

> Returns positions filtered by user and optional filters.



## OpenAPI

````yaml api-reference/data-api-openapi.yaml get /positions
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
  /positions:
    get:
      tags:
        - Core
      summary: Get current positions for a user
      description: Returns positions filtered by user and optional filters.
      parameters:
        - in: query
          name: user
          required: true
          schema:
            $ref: '#/components/schemas/Address'
          description: User address (required)
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
          name: sizeThreshold
          schema:
            type: number
            default: 1
            minimum: 0
        - in: query
          name: redeemable
          schema:
            type: boolean
            default: false
        - in: query
          name: mergeable
          schema:
            type: boolean
            default: false
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
          name: sortBy
          schema:
            type: string
            enum:
              - CURRENT
              - INITIAL
              - TOKENS
              - CASHPNL
              - PERCENTPNL
              - TITLE
              - RESOLVING
              - PRICE
              - AVGPRICE
            default: TOKENS
        - in: query
          name: sortDirection
          schema:
            type: string
            enum:
              - ASC
              - DESC
            default: DESC
        - in: query
          name: title
          schema:
            type: string
            maxLength: 100
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Position'
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
    Position:
      type: object
      properties:
        proxyWallet:
          $ref: '#/components/schemas/Address'
        asset:
          type: string
        conditionId:
          $ref: '#/components/schemas/Hash64'
        size:
          type: number
        avgPrice:
          type: number
        initialValue:
          type: number
        currentValue:
          type: number
        cashPnl:
          type: number
        percentPnl:
          type: number
        totalBought:
          type: number
        realizedPnl:
          type: number
        percentRealizedPnl:
          type: number
        curPrice:
          type: number
        redeemable:
          type: boolean
        mergeable:
          type: boolean
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
        negativeRisk:
          type: boolean
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