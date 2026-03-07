# Merging Tokens

In addition to splitting collateral for a full set, the inverse can also happen; a full set can be "merged" for collateral. This operation can again happen at any time after a condition has been prepared on the CTF contract. One unit of each position in a full set is burned in return for 1 collateral unit. This operation happens via the `mergePositions()` function on the CTF contract with the following parameters:

* `collateralToken`: IERC20 - The address of the positions' backing collateral token.
* `parentCollectionId`: bytes32 - The ID of the outcome collections common to the position being merged and the merge target positions. Null in Polymarket case.
* `conditionId`: bytes32 - The ID of the condition to merge on.
* `partition`: uint\[] - An array of disjoint index sets representing a nontrivial partition of the outcome slots of the given condition. E.G. A|B and C but not A|B and B|C (is not disjoint). Each element's a number which, together with the condition, represents the outcome collection. E.G. 0b110 is A|B, 0b010 is B, etc. In the Polymarket case 1|2.
* `amount` - The number of full sets to merge. Also the amount of collateral to receive.


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt