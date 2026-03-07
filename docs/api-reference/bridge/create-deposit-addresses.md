# Create deposit addresses

> Generate unique deposit addresses for bridging assets to Polymarket.

**How it works:**
1. Request deposit addresses for your Polymarket wallet
2. Receive deposit addresses for each blockchain type (EVM, Solana, Bitcoin)
3. Send assets to the appropriate deposit address for your source chain
4. Assets are automatically bridged and swapped to USDC.e on Polygon
5. USDC.e is credited to your Polymarket wallet for trading




## OpenAPI

````yaml api-reference/bridge-api-openapi.yaml post /deposit
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
  /deposit:
    post:
      tags:
        - Bridge
      summary: Create deposit addresses
      description: >
        Generate unique deposit addresses for bridging assets to Polymarket.


        **How it works:**

        1. Request deposit addresses for your Polymarket wallet

        2. Receive deposit addresses for each blockchain type (EVM, Solana,
        Bitcoin)

        3. Send assets to the appropriate deposit address for your source chain

        4. Assets are automatically bridged and swapped to USDC.e on Polygon

        5. USDC.e is credited to your Polymarket wallet for trading
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DepositRequest'
            example:
              address: '0x56687bf447db6ffa42ffe2204a05edaa20f55839'
      responses:
        '201':
          description: Deposit addresses created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DepositResponse'
        '400':
          description: Bad Request - Invalid address or request body
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
    DepositRequest:
      type: object
      required:
        - address
      properties:
        address:
          $ref: '#/components/schemas/Address'
          description: Your Polymarket wallet address
    DepositResponse:
      type: object
      properties:
        address:
          type: object
          description: Deposit addresses for different blockchain networks
          properties:
            evm:
              type: string
              description: >-
                EVM-compatible deposit address (Ethereum, Polygon, Arbitrum,
                Base, etc.)
              example: '0x23566f8b2E82aDfCf01846E54899d110e97AC053'
            svm:
              type: string
              description: Solana Virtual Machine deposit address
              example: CrvTBvzryYxBHbWu2TiQpcqD5M7Le7iBKzVmEj3f36Jb
            btc:
              type: string
              description: Bitcoin deposit address
              example: bc1q8eau83qffxcj8ht4hsjdza3lha9r3egfqysj3g
        note:
          type: string
          description: Additional information about supported chains
          example: >-
            Only certain chains and tokens are supported. See /supported-assets
            for details.
    ErrorResponse:
      type: object
      properties:
        error:
          type: string
      required:
        - error
    Address:
      type: string
      description: Ethereum address (0x-prefixed, 40 hex chars)
      pattern: ^0x[a-fA-F0-9]{40}$
      example: '0x56687bf447db6ffa42ffe2204a05edaa20f55839'

````

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt