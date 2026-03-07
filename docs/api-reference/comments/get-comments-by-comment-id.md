# Get comments by comment id



## OpenAPI

````yaml api-reference/gamma-openapi.json get /comments/{id}
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
  /comments/{id}:
    get:
      tags:
        - Comments
      summary: Get comments by comment id
      operationId: getCommentsById
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
        - name: get_positions
          in: query
          schema:
            type: boolean
      responses:
        '200':
          description: Comments
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Comment'
components:
  schemas:
    Comment:
      type: object
      properties:
        id:
          type: string
        body:
          type: string
          nullable: true
        parentEntityType:
          type: string
          nullable: true
        parentEntityID:
          type: integer
          nullable: true
        parentCommentID:
          type: string
          nullable: true
        userAddress:
          type: string
          nullable: true
        replyAddress:
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
        profile:
          $ref: '#/components/schemas/CommentProfile'
        reactions:
          type: array
          items:
            $ref: '#/components/schemas/Reaction'
        reportCount:
          type: integer
          nullable: true
        reactionCount:
          type: integer
          nullable: true
    CommentProfile:
      type: object
      properties:
        name:
          type: string
          nullable: true
        pseudonym:
          type: string
          nullable: true
        displayUsernamePublic:
          type: boolean
          nullable: true
        bio:
          type: string
          nullable: true
        isMod:
          type: boolean
          nullable: true
        isCreator:
          type: boolean
          nullable: true
        proxyWallet:
          type: string
          nullable: true
        baseAddress:
          type: string
          nullable: true
        profileImage:
          type: string
          nullable: true
        profileImageOptimized:
          $ref: '#/components/schemas/ImageOptimization'
        positions:
          type: array
          items:
            $ref: '#/components/schemas/CommentPosition'
    Reaction:
      type: object
      properties:
        id:
          type: string
        commentID:
          type: integer
          nullable: true
        reactionType:
          type: string
          nullable: true
        icon:
          type: string
          nullable: true
        userAddress:
          type: string
          nullable: true
        createdAt:
          type: string
          format: date-time
          nullable: true
        profile:
          $ref: '#/components/schemas/CommentProfile'
    ImageOptimization:
      type: object
      properties:
        id:
          type: string
        imageUrlSource:
          type: string
          nullable: true
        imageUrlOptimized:
          type: string
          nullable: true
        imageSizeKbSource:
          type: number
          nullable: true
        imageSizeKbOptimized:
          type: number
          nullable: true
        imageOptimizedComplete:
          type: boolean
          nullable: true
        imageOptimizedLastUpdated:
          type: string
          nullable: true
        relID:
          type: integer
          nullable: true
        field:
          type: string
          nullable: true
        relname:
          type: string
          nullable: true
    CommentPosition:
      type: object
      properties:
        tokenId:
          type: string
          nullable: true
        positionSize:
          type: string
          nullable: true

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt