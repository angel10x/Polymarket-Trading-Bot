# Resolution

# UMA Optimistic Oracle Integration

## Overview

Polymarket leverages UMA's Optimistic Oracle (OO) to resolve arbitrary questions, permissionlessly. From [UMA's docs](https://docs.uma.xyz/protocol-overview/how-does-umas-oracle-work):

"UMA's Optimistic Oracle allows contracts to quickly request and receive data information ... The Optimistic Oracle acts as a generalized escalation game between contracts that initiate a price request and UMA's dispute resolution system known as the Data Verification Mechanism (DVM). Prices proposed by the Optimistic Oracle will not be sent to the DVM unless it is disputed. If a dispute is raised, a request is sent to the DVM. All contracts built on UMA use the DVM as a backstop to resolve disputes. Disputes sent to the DVM will be resolved within a few days -- after UMA tokenholders vote on what the correct outcome should have been."

To allow CTF markets to be resolved via the OO, Polymarket developed a custom adapter contract called `UmaCtfAdapter` that provides a way for the two contract systems to interface.

## Clarifications

Recent versions (v2+) of the `UmaCtfAdapter` also include a bulletin board feature that allows market creators to issue "clarifications". Questions that allow updates will include the sentence in their ancillary data:

"Updates made by the question creator via the bulletin board on 0x6A5D0222186C0FceA7547534cC13c3CFd9b7b6A4F74 should be considered. In summary, clarifications that do not impact the question's intent should be considered."

Where the [transaction](https://polygonscan.com/tx/0xa14f01b115c4913624fc3f508f960f4dea252758e73c28f5f07f8e19d7bca066) reference outlining what outlining should be considered.

## Resolution Process

### Actions

* **Initiate** - Binary CTF markets are initialized via the `UmaCtfAdapter`'s `initialize()` function. This stores the question parameters on the contract, prepares the CTF and requests a price for a question from the OO. It returns a `questionID` that is also used to reference on the `UmaCtfAdapter`. The caller provides:
  1. `ancillaryData` - data used to resolve a question (i.e the question + clarifications)
  2. `rewardToken` - ERC20 token address used for payment of rewards and fees
  3. `reward` - Reward amount offered to a successful proposer. The caller must have set allowance so that the contract can pull this reward in.
  4. `proposalBond` - Bond required to be posted by OO proposers/disputers. If 0, the default OO bond is used.
  5. `liveness` - UMA liveness period in seconds. If 0, the default liveness period is used.

* **Propose Price** - Anyone can then propose a price to the question on the OO. To do this they must post the `proposalBond`. The liveness period begins after a price is proposed.

* **Dispute** - Anyone that disagrees with the proposed price has the opportunity to dispute the price by posting a counter bond via the OO, this proposed will now be escalated to the DVM for a voter-wide vote.

### Possible Flows

When the first proposed price is disputed for a `questionID` on the adapter, a callback is made and posted as the reward for this new proposal. This means a second `questionID`, making a new `questionID` to the OO (the reward is returned before the callback is made and posted as the reward for this new proposal). This allows for a second round of resolution, and correspondingly a second dispute is required for it to go to the DVM. The thinking behind this is to doubles the cost of a potential griefing vector (two disputes are required just one) and also allows far-fetched (incorrect) first price proposals to not delay the resolution. As such there are two possible flows:

* **Initialize (CTFAdapter) -> Propose (OO) -> Resolve (CTFAdapter)**
* **Initialize (CTFAdaptor) -> Propose (OO) -> Challenge (OO) -> Propose (OO) -> Resolve (CTFAdaptor)**
* **Initialize (CTFAdaptor) -> Propose (OO) -> Challenge (OO) -> Propose (OO) -> Challenge (CtfAdapter) -> Resolve (CTFAdaptor)**

## Deployed Addresses

### v3.0

| Network         | Address                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Polygon Mainnet | [0x157Ce2d672854c848c9b79C49a8Cc6cc89176a49](https://polygonscan.com/address/0x157Ce2d672854c848c9b79C49a8Cc6cc89176a49) |

### v2.0

| Network         | Address                                                                                                                     |
| --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Polygon Mainnet | [0x6A9D0222186C0FceA7547534cC13c3CFd9b7b6A4F74](https://polygonscan.com/address/0x6A9D222616C90FcA5754cd1333cFD9b7fb6a4F74) |

### v1.0

| Network         | Address                                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Polygon Mainnet | [0xC8B122858a4EF82C2d4eE2E6A276C719e692995130](https://polygonscan.com/address/0xCB1822859cEF82Cd2Eb4E6276C7916e692995130) |

## Additional Resources

* [Audit](https://github.com/Polymarket/uma-ctf-adapter/blob/main/audit/Polymarket_UMA_Optimistic_Oracle_Adapter_Audit.pdf)
* [Source Code](https://github.com/Polymarket/uma-ctf-adapter)
* [UMA Documentation](https://docs.uma.xyz/)
* [UMA Oracle Portal](https://oracle.uma.xyz/)


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt