# AMM

The AMM strategy seeks to emulate the liquidity available in a concentrated liquidity AMM.
Note that `max_collateral` only bounds the amount of capital used as liquidity _at any given time_.
The only way to bound your total losses is to limit the amount of collateral in your account.

## Config

```[python]
{
    p_min,
    p_max,
    spread,
    delta,
    depth,
    max_collateral
}
```

## Pool Setup

Let $\text{Price}_A$, $\text{Price}_B$ be the midpoint prices of the two tokens, and let $\text{Pool}_A$ and $\text{Pool}_B$ be two concentrated liquidity pools: $\text{Pool}_A$ for the $\text{Token}_A:\text{Collateral}$ pair and $\text{Pool}_B$ for the $\text{Token}_B:\text{Collateral}$ pair.

For each $\text{Pool}$, we consider two liquidity bands, the first, $\text{L}$, the "left" band, in the range $[\text{price} - \text{delta}, \text{price}]$, and the second, $\text{R}$, the "right" band, in the range $[\text{price}, \text{price} + \text{delta}]$.
Since $\text{L}$ consists only of prices _less than or equal_ to $\text{price}$, any liquidity provided to $\text{L}$ will consist _only of_ $\text{Collateral}$. Likewise, since $\text{R}$ consists only of prices _greater than or equal_ to $\text{price}$, any liquidity provided to $\text{R}$ will consist _only of_ $\text{Token}$.

Now given quantities $\text{TokenDeposit}_A$ and $\text{CollateralDeposit}_A$, an LP deposits all of $\text{TokenDeposit}_A$ to $\text{L}_A$ and all of $\text{TokenDeposit}_A$ to $\text{R}_A$. Imagining that this is the only liquidity in $\text{Pool}_A$, this completely determines the relationship between size and cost for a single swap in $\text{Pool}_A$.

The LP does the same with $\text{Pool}_B$ given quantities $\text{TokenDeposit}_B$ and $\text{CollateralDeposit}_B$.

## Order Placement

### Buy Orders

The strategy places buy orders at prices

$$
\text{Prices} = \{P_1, P_2, \dots, P_k\},
$$

where

$$
\begin{align*}
P_1 &= P - \text{spread}, \\
P_k &= P - \text{depth}, \text{ and} \\
P_{i+1} &= P_i - \text{delta} \text{ for } i \in [0, k-1].
\end{align*}
$$

To $\text{Prices}$, we assign corresponding sizes

$$
\text{Sizes} = \{S_1, S_2, \dots, S_k\},
$$

and orders,

$$
\text{Orders} = \{O_1, O_2, \dots, O_k\},
$$

where, for each $i$, $O_i$ has size $S_i$ and price $P_i$.

To determine the size $S_i$ for a buy order $O_i$, we compute the size, _i.e._ the $\text{Token}$ amount, $S'_i$ required to move the marginal price of $\text{Pool}$ from $P$ to $P_i$. In other words, if $S_i'$ tokens are swapped into $\text{Pool}$, the resulting marginal price would be $P_i$.
Finally define the $S_i$ as follows:

$$
S_i = \begin{cases}
S'_1, & \text{if }\; i = 1, \text{ and}\\
S'_i - S'_{i-1} & \text{for } i \geq 2.
\end{cases}
$$

The sizes are chosen such that if these were the only orders on the order book, a trader would sell $S_i$ tokens to fill up every order down to and including $O_i$.

### Sell Orders

The same process is used to determine the sizes of sell orders, except that we define $\text{Prices}$ as follows:

$$
\text{Prices} = \{P_1, P_2, \dots, P_k\},
$$

where

$$
\begin{align*}
P_1 &= P + \text{spread}, \\
P_k &= P + \text{depth}, \text{ and} \\
P_{i+1} &= P_i + \text{delta} \text{ for } i \in [0, k-1].
\end{align*}
$$
