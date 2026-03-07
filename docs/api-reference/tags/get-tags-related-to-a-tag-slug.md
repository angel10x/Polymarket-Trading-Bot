# Get tags related to a tag slug



## OpenAPI

````yaml api-reference/gamma-openapi.json get /tags/slug/{slug}/related-tags/tags
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
  /tags/slug/{slug}/related-tags/tags:
    get:
      tags:
        - Tags
      summary: Get tags related to a tag slug
      operationId: getTagsRelatedToATagBySlug
      parameters:
        - $ref: '#/components/parameters/pathSlug'
        - name: omit_empty
          in: query
          schema:
            type: boolean
        - name: status
          in: query
          schema:
            type: string
            enum:
              - active
              - closed
              - all
      responses:
        '200':
          description: Related tags
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Tag'
components:
  parameters:
    pathSlug:
      name: slug
      in: path
      required: true
      schema:
        type: string
  schemas:
    Tag:
      type: object
      properties:
        id:
          type: string
        label:
          type: string
          nullable: true
        slug:
          type: string
          nullable: true
        forceShow:
          type: boolean
          nullable: true
        publishedAt:
          type: string
          nullable: true
        createdBy:
          type: integer
          nullable: true
        updatedBy:
          type: integer
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        updatedAt:
          type: string
          format: date-time
          nullable: true
        forceHide:
          type: boolean
          nullable: true
        isCarousel:
          type: boolean
          nullable: true

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt