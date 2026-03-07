# Onchain Order Info

## How do I interpret the OrderFilled onchain event?

Given an OrderFilled event:

* `orderHash`: a unique hash for the Order being filled
* `maker`: the user generating the order and the source of funds for the order
* `taker`: the user filling the order OR the Exchange contract if the order fills multiple limit orders
* `makerAssetId`: id of the asset that is given out. If 0, indicates that the Order is a BUY, giving USDC in exchange for Outcome tokens. Else, indicates that the Order is a SELL, giving Outcome tokens in exchange for USDC.
* `takerAssetId`: id of the asset that is received. If 0, indicates that the Order is a SELL, receiving USDC in exchange for Outcome tokens. Else, indicates that the Order is a BUY, receiving Outcome tokens in exchange for USDC.
* `makerAmountFilled`: the amount of the asset that is given out.
* `takerAmountFilled`: the amount of the asset that is received.
* `fee`: the fees paid by the order maker


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt