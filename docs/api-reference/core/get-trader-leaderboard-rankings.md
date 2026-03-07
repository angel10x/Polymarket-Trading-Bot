# Get trader leaderboard rankings

> Returns trader leaderboard rankings filtered by category, time period, and ordering.



## OpenAPI

````yaml api-reference/data-api-openapi.yaml get /v1/leaderboard
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
  /v1/leaderboard:
    get:
      tags:
        - Core
      summary: Get trader leaderboard rankings
      description: >-
        Returns trader leaderboard rankings filtered by category, time period,
        and ordering.
      parameters:
        - in: query
          name: category
          schema:
            type: string
            enum:
              - OVERALL
              - POLITICS
              - SPORTS
              - CRYPTO
              - CULTURE
              - MENTIONS
              - WEATHER
              - ECONOMICS
              - TECH
              - FINANCE
            default: OVERALL
          description: Market category for the leaderboard
        - in: query
          name: timePeriod
          schema:
            type: string
            enum:
              - DAY
              - WEEK
              - MONTH
              - ALL
            default: DAY
          description: Time period for leaderboard results
        - in: query
          name: orderBy
          schema:
            type: string
            enum:
              - PNL
              - VOL
            default: PNL
          description: Leaderboard ordering criteria
        - in: query
          name: limit
          schema:
            type: integer
            default: 25
            minimum: 1
            maximum: 50
          description: Max number of leaderboard traders to return
        - in: query
          name: offset
          schema:
            type: integer
            default: 0
            minimum: 0
            maximum: 1000
          description: Starting index for pagination
        - in: query
          name: user
          schema:
            $ref: '#/components/schemas/Address'
          description: Limit leaderboard to a single user by address
        - in: query
          name: userName
          schema:
            type: string
          description: Limit leaderboard to a single username
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/TraderLeaderboardEntry'
        '400':
          description: Bad Request
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
    TraderLeaderboardEntry:
      type: object
      properties:
        rank:
          type: string
          description: The rank position of the trader
        proxyWallet:
          $ref: '#/components/schemas/Address'
        userName:
          type: string
          description: The trader's username
        vol:
          type: number
          description: Trading volume for this trader
        pnl:
          type: number
          description: Profit and loss for this trader
        profileImage:
          type: string
          description: URL to the trader's profile image
        xUsername:
          type: string
          description: The trader's X (Twitter) username
        verifiedBadge:
          type: boolean
          description: Whether the trader has a verified badge
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