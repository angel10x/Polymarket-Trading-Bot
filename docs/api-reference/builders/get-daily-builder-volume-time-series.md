# Get daily builder volume time-series

> Returns daily time-series volume data with multiple entries per builder (one per day), each including a `dt` timestamp. No pagination.



## OpenAPI

````yaml api-reference/data-api-openapi.yaml get /v1/builders/volume
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
  /v1/builders/volume:
    get:
      tags:
        - Builders
      summary: Get daily builder volume time-series
      description: >-
        Returns daily time-series volume data with multiple entries per builder
        (one per day), each including a `dt` timestamp. No pagination.
      parameters:
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
          description: |
            The time period to fetch daily records for.
      responses:
        '200':
          description: Success - Returns array of daily volume records
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/BuilderVolumeEntry'
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
    BuilderVolumeEntry:
      type: object
      properties:
        dt:
          type: string
          format: date-time
          description: The timestamp for this volume entry in ISO 8601 format
          example: '2025-11-15T00:00:00Z'
        builder:
          type: string
          description: The builder name or identifier
        builderLogo:
          type: string
          description: URL to the builder's logo image
        verified:
          type: boolean
          description: Whether the builder is verified
        volume:
          type: number
          description: Trading volume for this builder on this date
        activeUsers:
          type: integer
          description: Number of active users for this builder on this date
        rank:
          type: string
          description: The rank position of the builder on this date
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