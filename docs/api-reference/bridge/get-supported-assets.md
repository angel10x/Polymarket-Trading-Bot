# Get supported assets

> Retrieve all supported chains and tokens for deposits.

**USDC.e on Polygon:**
Polymarket uses USDC.e (Bridged USDC from Ethereum) on Polygon as the native collateral for all markets. When you deposit assets from other chains, they are automatically bridged and swapped to USDC.e on Polygon, which is then used as collateral for trading on Polymarket.

**Minimum Deposit Amounts:**
Each asset has a `minCheckoutUsd` field indicating the minimum deposit amount required in USD. Make sure your deposit meets this minimum to avoid transaction failures.




## OpenAPI

````yaml api-reference/bridge-api-openapi.yaml get /supported-assets
openapi: 3.0.3
info:
  title: Polymarket Bridge API
  version: 1.0.0
  description: >
    HTTP API for Polymarket bridge and swap operations. 


    Polymarket uses USDC.e (Bridged USDC) on Polygon as collateral for all
    trading activities. This API enables users to bridge assets from various
    chains and swap them to USDC.e on Polygon for seamless trading.
servers:
  - url: https://bridge.polymarket.com
    description: Polymarket Bridge API
security: []
tags:
  - name: Bridge
    description: Bridge and swap operations for Polymarket
paths:
  /supported-assets:
    get:
      tags:
        - Bridge
      summary: Get supported assets
      description: >
        Retrieve all supported chains and tokens for deposits.


        **USDC.e on Polygon:**

        Polymarket uses USDC.e (Bridged USDC from Ethereum) on Polygon as the
        native collateral for all markets. When you deposit assets from other
        chains, they are automatically bridged and swapped to USDC.e on Polygon,
        which is then used as collateral for trading on Polymarket.


        **Minimum Deposit Amounts:**

        Each asset has a `minCheckoutUsd` field indicating the minimum deposit
        amount required in USD. Make sure your deposit meets this minimum to
        avoid transaction failures.
      responses:
        '200':
          description: Successfully retrieved supported assets
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SupportedAssetsResponse'
        '500':
          description: Server Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
components:
  schemas:
    SupportedAssetsResponse:
      type: object
      properties:
        supportedAssets:
          type: array
          items:
            $ref: '#/components/schemas/SupportedAsset'
          description: List of supported assets with minimum deposit amounts
    ErrorResponse:
      type: object
      properties:
        error:
          type: string
      required:
        - error
    SupportedAsset:
      type: object
      properties:
        chainId:
          type: string
          description: Chain ID
          example: '1'
        chainName:
          type: string
          description: Human-readable chain name
          example: Ethereum
        token:
          $ref: '#/components/schemas/Token'
        minCheckoutUsd:
          type: number
          description: Minimum deposit amount in USD
          example: 45
    Token:
      type: object
      properties:
        name:
          type: string
          description: Full token name
          example: USD Coin
        symbol:
          type: string
          description: Token symbol
          example: USDC
        address:
          type: string
          description: Token contract address
          example: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
        decimals:
          type: integer
          description: Token decimals
          example: 6

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt