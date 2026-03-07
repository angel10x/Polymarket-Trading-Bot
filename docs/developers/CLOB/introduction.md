# CLOB Introduction

Welcome to the Polymarket Order Book API! This documentation provides overviews, explanations, examples, and annotations to simplify interaction with the order book. The following sections detail the Polymarket Order Book and the API usage.

## System

Polymarket's Order Book, or CLOB (Central Limit Order Book), is hybrid-decentralized. It includes an operator for off-chain matching/ordering, with settlement executed on-chain, non-custodially, via signed order messages.

The exchange uses a custom Exchange contract facilitating atomic swaps between binary Outcome Tokens (CTF ERC1155 assets and ERC20 PToken assets) and collateral assets (ERC20), following signed limit orders. Designed for binary markets, the contract enables complementary tokens to match across a unified order book.

Orders are EIP712-signed structured data. Matched orders have one maker and one or more takers, with price improvements benefiting the taker. The operator handles off-chain order management and submits matched trades to the blockchain for on-chain execution.

## API

The Polymarket Order Book API enables market makers and traders to programmatically manage market orders. Orders of any amount can be created, listed, fetched, or read from the market order books. Data includes all available markets, market prices, and order history via REST and WebSocket endpoints.

## Security

Polymarket's Exchange contract has been audited by Chainsecurity ([View Audit](https://github.com/Polymarket/ctf-exchange/blob/main/audit/ChainSecurity_Polymarket_Exchange_audit.pdf)).

The operator's privileges are limited to order matching, non-censorship, and ensuring correct ordering. Operators can't set prices or execute unauthorized trades. Users can cancel orders on-chain independently if trust issues arise.

## Fees

### Schedule

> Subject to change

| Volume Level | Maker Fee Base Rate (bps) | Taker Fee Base Rate (bps) |
| ------------ | ------------------------- | ------------------------- |
| >0 USDC      | 0                         | 0                         |

### Overview

Fees apply symmetrically in output assets (proceeds). This symmetry ensures fairness and market integrity. Fees are calculated differently depending on whether you are buying or selling:

* **Selling outcome tokens (base) for collateral (quote):**

$$
feeQuote = baseRate \times \min(price, 1 - price) \times size
$$

* **Buying outcome tokens (base) with collateral (quote):**

$$
feeBase = baseRate \times \min(price, 1 - price) \times \frac{size}{price}
$$

## Additional Resources

* [Exchange contract source code](https://github.com/Polymarket/ctf-exchange/tree/main/src)
* [Exchange contract documentation](https://github.com/Polymarket/ctf-exchange/blob/main/docs/Overview.md)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt