# Overview

All outcomes on Polymarket are tokenized on the Polygon network. Specifically, Polymarket outcomes shares are binary outcomes (ie "YES" and "NO") using Gnosis' Conditional Token Framework (CTF). They are distinct ERC1155 tokens related to a parent condition and backed by the same collateral. More technically, the binary outcome tokens are referred to as "positionIds" in Gnosis's documentation. "PositionIds" are derived from a collateral token and distinct "collectionIds". "CollectionIds" are derived from a "parentCollectionId", (always bytes32(0) in our case) a "conditionId", and a unique "indexSet".

The "indexSet" is a 256 bit array denoting which outcome slots are in an outcome collection; it MUST be a nonempty proper subset of a condition's outcome slots. In the binary case, which we are interested in, there are two "indexSets", one for the first outcome and one for the second. The first outcome's "indexSet" is 0b01 = 1 and the second's is 0b10 = 2. The parent "conditionId" (shared by both "collectionIds" and therefore "positionIds") is derived from a "questionId" (a hash of the UMA ancillary data), an "oracle" (the UMA adapter V2), and an "outcomeSlotCount" (always 2 in the binary case). The steps for calculating the ERC1155 token ids (positionIds) is as follows:

1. Get the conditionId
   1. Function:
      1. `getConditionId(oracle, questionId, outcomeSlotCount)`
   2. Inputs:
      1. `oracle`: address - UMA adapter V2
      2. `questionId`: bytes32 - hash of the UMA ancillary data
      3. `outcomeSlotCount`: uint - 2 for binary markets

2. Get the two collectionIds
   1. Function:
      1. `getCollectionId(parentCollectionId, conditionId, indexSet)`
   2. Inputs:
      1. `parentCollectionId`: bytes32 - bytes32(0)
      2. `conditionId`: bytes32 - the conditionId derived from (1)
      3. `indexSet`: uint - 1 (0b01) for the first and 2 (0b10) for the second.

3. Get the two positionIds
   1. Function:
      1. `getPositionId(collateralToken, collectionId)`
   2. Inputs:
      1. `collateralToken`: IERC20 - address of ERC20 token collateral (USDC)
      2. `collectionId`: bytes32 - the two collectionIds derived from (3)

Leveraging the relations above, specifically "conditionIds" -> "positionIds" the Gnosis CTF contract allows for "splitting" and "merging" full outcome sets. We explore these actions and provide code examples below.


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt