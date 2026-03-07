# Get valid sports market types

> Get a list of all valid sports market types available on the platform. Use these values when filtering markets by the sportsMarketTypes parameter.



## OpenAPI

````yaml api-reference/gamma-openapi.json get /sports/market-types
openapi: 3.0.3
info:
  title: Markets API
  version: 1.0.0
  description: REST API specification for public endpoints used by the Markets service.
servers:
  - url: https://gamma-api.polymarket.com
    description: Polymarket Gamma API Production Server
security: []
tags:
  - name: Health
    description: Health check endpoints
  - name: Sports
    description: Sports-related endpoints including teams and game data
  - name: Tags
    description: Tag management and related tag operations
  - name: Events
    description: Event management and event-related operations
  - name: Markets
    description: Market data and market-related operations
  - name: Comments
    description: Comment system and user interactions
  - name: Series
    description: Series management and related operations
  - name: Profiles
    description: User profile management
  - name: Search
    description: Search functionality across different entity types
paths:
  /sports/market-types:
    get:
      tags:
        - Sports
      summary: Get valid sports market types
      description: >-
        Get a list of all valid sports market types available on the platform.
        Use these values when filtering markets by the sportsMarketTypes
        parameter.
      operationId: getSportsMarketTypes
      responses:
        '200':
          description: List of valid sports market types
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SportsMarketTypesResponse'
components:
  schemas:
    SportsMarketTypesResponse:
      type: object
      properties:
        marketTypes:
          type: array
          description: List of all valid sports market types
          items:
            type: string

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt