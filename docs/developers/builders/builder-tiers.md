# Builder Tiers

> Permissionless integration with tiered rate limits, rewards, and revenue generating opportunities as you scale

## Overview

Polymarket Builders lets anyone integrate without approval.
Tiers exist to manage rate limits while rewarding high performing integrations with weekly rewards, grants, and revenue sharing opportunities. Higher tiers also unlock engineering support, marketing promotion, and priority access.

## Feature Definitions

| Feature                     | Description                                                                     |
| --------------------------- | ------------------------------------------------------------------------------- |
| **Daily Relayer Txn Limit** | Maximum Relayer transactions per day for Safe/Proxy wallet operations           |
| **API Rate Limits**         | Rate limits for non-relayer endpoints (CLOB, Gamma, etc.)                       |
| **Subsidized Transactions** | Gas fees subsidized for Relayer and CLOB operations via Safe/Proxy wallets      |
| **Order Attribution**       | Orders tracked and attributed to your Builder profile                           |
| **RevShare Protocol**       | Infrastructure allowing Builders to charge fees on top of Polymarket's base fee |
| **Leaderboard Visibility**  | Visibility on the [Builder leaderboard](https://builders.polymarket.com/)       |
| **Weekly Rewards**          | Weekly USDC rewards program for visible builders based on volume                |
| **Grants**                  | Builder grants awarded based on innovation and exclusivity                      |
| **Telegram Channel**        | Private Builders channel for announcements and support                          |
| **Badge**                   | Verified Builder affiliate badge on your Builder profile                        |
| **Engineering Support**     | Direct access to engineering team                                               |
| **Marketing Support**       | Promotion via official Polymarket social accounts                               |
| **Weekly Rewards Boost**    | Multiplier on the weekly USDC rewards program for visible builders              |
| **Priority Access**         | Early access to new features and products                                       |
| **Market Suggestions**      | Ability to propose new prediction markets                                       |
| **Base Fee Split**          | Volume based fee split on Polymarket's base fee                                 |

## Tier Comparison

| Feature                     | Unverified |  Verified |  Partner  |
| --------------------------- | :--------: | :-------: | :-------: |
| **Daily Relayer Txn Limit** |   100/day  | 1,500/day | Unlimited |
| **API Rate Limits**         |  Standard  |  Standard |  Highest  |
| **Subsidized Transactions** |      ✅     |     ✅     |     ✅     |
| **Order Attribution**       |      ✅     |     ✅     |     ✅     |
| **RevShare Protocol**       |      ❌     |     ✅     |     ✅     |
| **Leaderboard Visibility**  |      ❌     |     ✅     |     ✅     |
| **Weekly Rewards**          |      ❌     |     ✅     |     ✅     |
| **Telegram Channel**        |      ❌     |     ✅     |     ✅     |
| **Badge**                   |      ❌     |     ✅     |     ✅     |
| **Engineering Support**     |      ❌     |  Standard |  Elevated |
| **Marketing Support**       |      ❌     |  Standard |  Elevated |
| **Grants**                  |      ❌     |     ❌     |     ✅     |
| **Weekly Reward Boosts**    |      ❌     |     ❌     |     ✅     |
| **Priority Access**         |      ❌     |     ❌     |     ✅     |
| **Market Suggestions**      |      ❌     |     ❌     |     ✅     |
| **Base Fee Split**          |      ❌     |     ❌     |     ✅     |

***

### Unverified

<Card title="100 transactions/day" icon="seedling">
  The default tier for all new builders. Create Builder API keys instantly from your Polymarket profile.
</Card>

**How to get started:**

1. Go to [polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder)
2. Create a builder profile and click **"+ Create New"** to generate builder API keys
3. Implement [builder signing](/developers/builders/order-attribution); required for Relayer access and CLOB order attribution

**Included:**

* Gasless trading on all CLOB orders through Safe/Proxy wallets
* Gas subsidized on all Relayer transactions through Safe/Proxy wallets up to daily limit
* Order attribution credit to your Builder profile
* Access to all client libraries and documentation

***

### Verified

<Card title="1,500 transactions/day" icon="badge-check">
  For builders who need higher throughput. Requires manual approval by Polymarket.
</Card>

**How to upgrade:**

Contact us with your Builder API Key, use case, expected volume, and relevant info (app, docs, X profile).

**Unlocks over Unverified:**

* 15x daily Relayer transaction limit
* RevShare Protocol Access
* Telegram channel
* Leaderboard visibility
* Eligible for Weekly Rewards Program
* Promotion and verified affiliate badge from @PolymarketBuild
* Grants eligibility

***

### Partner

<Card title="Unlimited transactions/day" icon="handshake">
  Enterprise tier for high-volume integrations and strategic partners like Base, MetaMask, Rainbow, and Bullpen.
</Card>

**How to apply:**

Reach out to discuss partnership opportunities.

**Unlocks over Verified:**

* Unlimited Relayer transactions
* Highest API rate limits
* Elevated engineering support
* Elevated and coordinated marketing support
* Ability to suggest markets
* Priority access to new features and products
* Multiplier on the Weekly Rewards Program
* Custom split agreement on Polymarket's base fee

***

## Contact

Ready to upgrade or have questions?

* [builder@polymarket.com](mailto:builder@polymarket.com)

***

## FAQ

<AccordionGroup>
  <Accordion title="How do I know if I'm verified?">
    Verification is displayed in your [Builder Profile](https://polymarket.com/settings?tab=builder) settings.
  </Accordion>

  <Accordion title="What happens if I exceed my daily limit?">
    Relayer requests beyond your daily limit will be rate-limited and return an error. Consider upgrading to Verified or Partner tier if you're hitting limits.
  </Accordion>

  <Accordion title="Can I get a temporary limit increase?">
    For special events or product launches, contact [builder@polymarket.com](mailto:builder@polymarket.com)
  </Accordion>
</AccordionGroup>

***

## Next Steps

<CardGroup cols={2}>
  <Card title="Get Your Builder Keys" icon="key" href="/developers/builders/builder-profile">
    Create Builder API credentials to get started
  </Card>

  <Card title="Use Your Builder Keys" icon="server" href="/developers/builders/relayer-client">
    Configure Builder API credentials to attribute orders
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt