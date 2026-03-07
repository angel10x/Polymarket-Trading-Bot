# Get public profile by wallet address



## OpenAPI

````yaml api-reference/gamma-openapi.json get /public-profile
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
  /public-profile:
    get:
      tags:
        - Profiles
      summary: Get public profile by wallet address
      operationId: getPublicProfile
      parameters:
        - name: address
          in: query
          required: true
          description: The wallet address (proxy wallet or user address)
          schema:
            type: string
            pattern: ^0x[a-fA-F0-9]{40}$
          example: '0x7c3db723f1d4d8cb9c550095203b686cb11e5c6b'
      responses:
        '200':
          description: Public profile information
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicProfileResponse'
        '400':
          description: Invalid address format
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicProfileError'
              example:
                type: validation error
                error: invalid address
        '404':
          description: Profile not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PublicProfileError'
              example:
                type: not found error
                error: profile not found
components:
  schemas:
    PublicProfileResponse:
      type: object
      properties:
        createdAt:
          type: string
          format: date-time
          description: ISO 8601 timestamp of when the profile was created
          nullable: true
        proxyWallet:
          type: string
          description: The proxy wallet address
          nullable: true
        profileImage:
          type: string
          format: uri
          description: URL to the profile image
          nullable: true
        displayUsernamePublic:
          type: boolean
          description: Whether the username is displayed publicly
          nullable: true
        bio:
          type: string
          description: Profile bio
          nullable: true
        pseudonym:
          type: string
          description: Auto-generated pseudonym
          nullable: true
        name:
          type: string
          description: User-chosen display name
          nullable: true
        users:
          type: array
          description: Array of associated user objects
          nullable: true
          items:
            $ref: '#/components/schemas/PublicProfileUser'
        xUsername:
          type: string
          description: X (Twitter) username
          nullable: true
        verifiedBadge:
          type: boolean
          description: Whether the profile has a verified badge
          nullable: true
    PublicProfileError:
      type: object
      description: Error response for public profile endpoint
      properties:
        type:
          type: string
          description: Error type classification
        error:
          type: string
          description: Error message
    PublicProfileUser:
      type: object
      description: User object associated with a public profile
      properties:
        id:
          type: string
          description: User ID
        creator:
          type: boolean
          description: Whether the user is a creator
        mod:
          type: boolean
          description: Whether the user is a moderator

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt