# List teams



## OpenAPI

````yaml api-reference/gamma-openapi.json get /teams
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
  /teams:
    get:
      tags:
        - Sports
      summary: List teams
      operationId: listTeams
      parameters:
        - $ref: '#/components/parameters/limit'
        - $ref: '#/components/parameters/offset'
        - $ref: '#/components/parameters/order'
        - $ref: '#/components/parameters/ascending'
        - name: league
          in: query
          schema:
            type: array
            items:
              type: string
        - name: name
          in: query
          schema:
            type: array
            items:
              type: string
        - name: abbreviation
          in: query
          schema:
            type: array
            items:
              type: string
      responses:
        '200':
          description: List of teams
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Team'
components:
  parameters:
    limit:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 0
    offset:
      name: offset
      in: query
      schema:
        type: integer
        minimum: 0
    order:
      name: order
      in: query
      schema:
        type: string
      description: Comma-separated list of fields to order by
    ascending:
      name: ascending
      in: query
      schema:
        type: boolean
  schemas:
    Team:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
          nullable: true
        league:
          type: string
          nullable: true
        record:
          type: string
          nullable: true
        logo:
          type: string
          nullable: true
        abbreviation:
          type: string
          nullable: true
        alias:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt