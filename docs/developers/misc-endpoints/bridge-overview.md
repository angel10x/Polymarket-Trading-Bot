# Overview

> Bridge and swap assets to Polymarket

## Overview

The Polymarket Bridge API enables seamless deposits between multiple blockchains and Polymarket.

### USDC.e on Polygon

**Polymarket uses USDC.e (Bridged USDC) on Polygon as collateral** for all trading activities. USDC.e is the bridged version of USDC from Ethereum, and it serves as the native currency for placing orders and settling trades on Polymarket.

When you deposit assets to Polymarket:

1. You can deposit from various supported chains (Ethereum, Solana, Arbitrum, Base, etc.)
2. Your assets are automatically bridged/swapped to USDC.e on Polygon
3. USDC.e is credited to your Polymarket wallet
4. You can now trade on any Polymarket market

## Base URL

```
https://bridge.polymarket.com
```

## Key Features

* **Multi-chain deposits**: Bridge assets from EVM chains (Ethereum, Arbitrum, Base, etc.), Solana, and Bitcoin
* **Automatic conversion**: Assets are automatically bridged/swapped to USDC.e on Polygon
* **Simple addressing**: One deposit address per blockchain type (EVM, SVM, BTC)

## Endpoints

* `POST /deposit` - Create unique deposit addresses for bridging assets
* `GET /supported-assets` - Get all supported chains and tokens


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt