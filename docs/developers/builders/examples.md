# Examples

> Complete Next.js applications demonstrating Polymarket builder integration

## Overview

These open-source demo applications show how to integrate Polymarket's CLOB Client and Builder Relayer Client for gasless trading with builder order attribution.

<CardGroup cols={3}>
  <Card title="Authentication" icon="user-check">
    Multiple wallet providers
  </Card>

  <Card title="Gasless Trading" icon="gas-pump">
    Safe & Proxy wallet support
  </Card>

  <Card title="Full Integration" icon="puzzle-piece">
    Orders, positions, CTF ops
  </Card>
</CardGroup>

***

## Safe Wallet Examples

Deploy Gnosis Safe wallets for your users:

<CardGroup cols={2}>
  <Card title="wagmi + Safe" icon="wallet" href="https://github.com/Polymarket/wagmi-safe-builder-example">
    MetaMask, Phantom, Rabby, and other browser wallets
  </Card>

  <Card title="Privy + Safe" icon="shield-check" href="https://github.com/Polymarket/privy-safe-builder-example">
    Privy embedded wallets
  </Card>

  <Card title="Magic Link + Safe" icon="wand-magic-sparkles" href="https://github.com/Polymarket/magic-safe-builder-example">
    Magic Link email/social authentication
  </Card>

  <Card title="Turnkey + Safe" icon="key" href="https://github.com/Polymarket/turnkey-safe-builder-example">
    Turnkey embedded wallets
  </Card>
</CardGroup>

***

## What Each Demo Covers

<Tabs>
  <Tab title="Authentication">
    * User sign-in via wallet provider
    * User API credential derivation (L2 auth)
    * Builder config with remote signing
    * Signature types for Safe vs Proxy wallets
  </Tab>

  <Tab title="Wallet Operations">
    * Safe wallet deployment via Relayer
    * Batch token approvals (USDC.e + outcome tokens)
    * CTF operations (split, merge, redeem)
    * Transaction monitoring
  </Tab>

  <Tab title="Trading">
    * CLOB client initialization
    * Order placement with builder attribution
    * Position and order management
    * Market discovery via Gamma API
  </Tab>
</Tabs>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt