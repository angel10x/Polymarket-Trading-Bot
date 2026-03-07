# Builder Program Introduction

> Learn about Polymarket's Builder Program and how to integrate

## What is a Builder?

A "builder" is a person, group, or organization that routes orders from their users to Polymarket.
If you've created a platform that allows users to trade on Polymarket via your system, this program is for you.

***

## Program Benefits

<CardGroup cols={3}>
  <Card title="Relayer Access" icon="gas-pump">
    All onchain operations are gasless through our relayer
  </Card>

  <Card title="Order Attribution" icon="tag">
    Get credited for orders and compete for grants on the Builder Leaderboard
  </Card>

  <Card title="Fee Share" icon="percent">
    Earn a share of fees on routed orders
  </Card>
</CardGroup>

### Relayer Access

We expose our relayer to builders, providing gasless transactions for users with
Polymarket's Proxy Wallets deployed via [Relayer Client](/developers/builders/relayer-client).

When transactions are routed through proxy wallets, Polymarket pays all gas fees for:

* Deploying Gnosis Safe Wallets or Custom Proxy (Magic Link users) Wallets
* Token approvals (USDC, outcome tokens)
* CTF operations (split, merge, redeem)
* Order execution (via [CLOB API](/developers/CLOB/introduction))

<Warning>
  EOA wallets do not have relayer access. Users trading directly from an EOA pay their own gas fees.
</Warning>

### Trading Attribution

Attach custom headers to orders to identify your builder account:

* Orders attributed to your builder account
* Compete on the [Builder Leaderboard](https://builders.polymarket.com/) for grants
* Track performance via the Data API
  * [Leaderboard API](/api-reference/builders/get-aggregated-builder-leaderboard): Get aggregated builder rankings for a time period
  * [Volume API](/api-reference/builders/get-daily-builder-volume-time-series): Get daily time-series volume data for trend analysis

***

## Getting Started

1. **Get Builder Credentials**: Generate API keys from your [Builder Profile](/developers/builders/builder-profile)
2. **Configure Order Attribution**: Set up CLOB client to credit trades to your account ([guide](/developers/builders/order-attribution))
3. **Enable Gasless Transactions**: Use the Relayer for gas-free wallet deployment and trading ([guide](/developers/builders/relayer-client))

<Tip>
  See [Example Apps](/developers/builders/examples) for complete Next.js reference implementations.
</Tip>

***

## SDKs & Libraries

<CardGroup cols={2}>
  <Card title="CLOB Client (TypeScript)" icon="github" href="https://github.com/Polymarket/clob-client">
    Place orders with builder attribution
  </Card>

  <Card title="CLOB Client (Python)" icon="github" href="https://github.com/Polymarket/py-clob-client">
    Place orders with builder attribution
  </Card>

  <Card title="Relayer Client (TypeScript)" icon="github" href="https://github.com/Polymarket/builder-relayer-client">
    Gasless onchain transactions for your users
  </Card>

  <Card title="Relayer Client (Python)" icon="github" href="https://github.com/Polymarket/py-builder-relayer-client">
    Gasless onchain transactions for your users
  </Card>

  <Card title="Signing SDK (TypeScript)" icon="github" href="https://github.com/Polymarket/builder-signing-sdk">
    Sign builder authentication headers
  </Card>

  <Card title="Signing SDK (Python)" icon="github" href="https://github.com/Polymarket/py-builder-signing-sdk">
    Sign builder authentication headers
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt