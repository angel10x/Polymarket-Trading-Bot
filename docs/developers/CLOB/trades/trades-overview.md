# Trades Overview

## Overview

All historical trades can be fetched via the Polymarket CLOB REST API. A trade is initiated by a "taker" who creates a marketable limit order. This limit order can be matched against one or more resting limit orders on the associated book. A trade can be in various states as described below. Note: in some cases (due to gas limitations) the execution of a "trade" must be broken into multiple transactions which case separate trade entities will be returned. To associate trade entities, there is a bucket\_index field and a match\_time field. Trades that have been broken into multiple trade objects can be reconciled by combining trade objects with the same market\_order\_id, match\_time and incrementing bucket\_index's into a top level "trade" client side.

## Statuses

| Status    | Terminal? | Description                                                                                                                                               |
| --------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MATCHED   | no        | trade has been matched and sent to the executor service by the operator, the executor service submits the trade as a transaction to the Exchange contract |
| MINED     | no        | trade is observed to be mined into the chain, no finality threshold established                                                                           |
| CONFIRMED | yes       | trade has achieved strong probabilistic finality and was successful                                                                                       |
| RETRYING  | no        | trade transaction has failed (revert or reorg) and is being retried/resubmitted by the operator                                                           |
| FAILED    | yes       | trade has failed and is not being retried                                                                                                                 |


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt