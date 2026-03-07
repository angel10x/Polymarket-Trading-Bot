# Get related tags (relationships) by tag id



## OpenAPI

````yaml api-reference/gamma-openapi.json get /tags/{id}/related-tags
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
  /tags/{id}/related-tags:
    get:
      tags:
        - Tags
      summary: Get related tags (relationships) by tag id
      operationId: getRelatedTagsById
      parameters:
        - $ref: '#/components/parameters/pathId'
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
          description: Related tag relationships
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/RelatedTag'
components:
  parameters:
    pathId:
      name: id
      in: path
      required: true
      schema:
        type: integer
  schemas:
    RelatedTag:
      type: object
      properties:
        id:
          type: string
        tagID:
          type: integer
          nullable: true
        relatedTagID:
          type: integer
          nullable: true
        rank:
          type: integer
          nullable: true

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt