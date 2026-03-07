# Gamma Structure

Gamma provides some organizational models. These include events, and markets. The most fundamental element is always markets and the other models simply provide additional organization.

# Detail

1. **Market**
   1. Contains data related to a market that is traded on. Maps onto a pair of clob token ids, a market address, a question id and a condition id

2. **Event**
   1. Contains a set of markets
   2. Variants:
      1. Event with 1 market (i.e., resulting in an SMP)
      2. Event with 2 or more markets (i.e., resulting in an GMP)

# Example

* **\[Event]** Where will Barron Trump attend College?
  * **\[Market]** Will Barron attend Georgetown?
  * **\[Market]** Will Barron attend NYU?
  * **\[Market]** Will Barron attend UPenn?
  * **\[Market]** Will Barron attend Harvard?
  * **\[Market]** Will Barron attend another college?


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt