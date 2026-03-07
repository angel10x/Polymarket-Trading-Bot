# How Are Prediction Markets Resolved?

> Markets are resolved by the UMA Optimistic Oracle, a smart-contract based optimistic oracle.

## Overview

* When the result of a market becomes clear, the market can be “resolved,” or permanently finalized.

* Markets are resolved according to the market's pre-defined rules, which can be found under market's the order book.

* When a market is resolved, holders of winning shares receive \$1 per share, losing shares become worthless, and trading of shares is no longer possible.

* To resolve a market, an outcome must first be “proposed,” which involves putting up a bond in USDC.e which will be forfeited if the proposal is unsuccessful.

* If the proposal is validated as accurate, the proposer will receive a reward for your proposal.

<Warning>
  If you propose a market too early, or are unsuccessful in your proposal, you will lose all of your \$750 bond. Do not propose a resolution unless you understand the process and are confident in your view.
</Warning>

### To propose a market resolution

<Steps>
  <Steps.Step>
    Navigate to the market you want to propose and click Resolution > Propose Resolution.

    <Note>You will be taken to the corresponding UMA oracle page for the market, which shows the bond required and reward for successful proposal.</Note>
  </Steps.Step>

  <Steps.Step>
    Ensure that you have enough USDC.e in your wallet on Polygon to supply the bond (usually \$750)
  </Steps.Step>

  <Steps.Step>
    Select the outcome you would like to propose from the drop-down menu.
  </Steps.Step>

  <Steps.Step>
    Connect your wallet and submit the transaction. It will now enter the UMA Oracle’s verification queue.
  </Steps.Step>
</Steps>

Once in the verification process, UMA will review the transaction to ensure it was proposed correctly. If approved, you will receive your bond amount back in your wallet plus the reward. If not approved, it will enter Uma’s dispute resolution process, which is described in detail here.

### To dispute a proposed resolution

Once a market is proposed for resolution it goes into a challenge period of 2 hours.

If you do not agree with a proposed resolution, you can [dispute the outcome](../markets/dispute).


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt