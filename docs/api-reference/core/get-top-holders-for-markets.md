# Get top holders for markets



## OpenAPI

````yaml api-reference/data-api-openapi.yaml get /holders
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
  /holders:
    get:
      tags:
        - Core
      summary: Get top holders for markets
      parameters:
        - in: query
          name: limit
          schema:
            type: integer
            default: 20
            minimum: 0
            maximum: 20
          description: Maximum number of holders to return per token. Capped at 20.
        - in: query
          name: market
          required: true
          style: form
          explode: false
          schema:
            type: array
            items:
              $ref: '#/components/schemas/Hash64'
          description: Comma-separated list of condition IDs.
        - in: query
          name: minBalance
          schema:
            type: integer
            default: 1
            minimum: 0
            maximum: 999999
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/MetaHolder'
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
    MetaHolder:
      type: object
      properties:
        token:
          type: string
        holders:
          type: array
          items:
            $ref: '#/components/schemas/Holder'
    ErrorResponse:
      type: object
      properties:
        error:
          type: string
      required:
        - error
    Holder:
      type: object
      properties:
        proxyWallet:
          $ref: '#/components/schemas/Address'
        bio:
          type: string
        asset:
          type: string
        pseudonym:
          type: string
        amount:
          type: number
        displayUsernamePublic:
          type: boolean
        outcomeIndex:
          type: integer
        name:
          type: string
        profileImage:
          type: string
        profileImageOptimized:
          type: string
    Address:
      type: string
      description: User Profile Address (0x-prefixed, 40 hex chars)
      pattern: ^0x[a-fA-F0-9]{40}$
      example: '0x56687bf447db6ffa42ffe2204a05edaa20f55839'

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt