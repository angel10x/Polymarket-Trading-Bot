# How Are Prices Calculated?

> The prices probabilities displayed on Polymarket are the midpoint of the bid-ask spread in the orderbook.

## Initial Price

* When a market is created, there are initially zero shares and no pre-defined prices or odds.

* Market makers (a fancy term for traders placing limit orders) interested in buying YES or NO shares can place [Limit Orders](../trading/limit-orders) at the price they're willing to pay

* When offers for the YES and NO side equal \$1.00, the order is "matched" and that \$1.00 is converted into 1 YES and 1 NO share, each going to their respective buyers.

For example, if you place a limit order at \$0.60 for YES, that order is matched when someone places a NO order at \$0.40. *This becomes the initial market price.*

<Important>Polymarket is not a "bookie" and does not set prices / odds. Prices are set by what Polymarket users are currently willling to buy/sell shares at. All trades are peer-to-peer.</Important>

## Future Price

The prices displayed on Polymarket are the midpoint of the bid-ask spread in the orderbook — unless that spread is over \$0.10, in which case the last traded price is used.

Like the stock market, prices on Polymarket are a function of realtime supply & demand.

<VideoPlayer src="https://www.youtube.com/embed/v0CvPEYBzTI?si=9cirMPQ72orQzLyS" />

### Prices = Probabilities

In the market below, the probability of 37% is the midpoint between the 34¢ bid and 40¢ ask. If the bid-ask spread is wider than 10¢, the probability is shown as the last traded price.

<Frame>
  <img className="block w-full h-auto dark:hidden" style={{ maxWidth: '100%', height: 'auto' }} noZoom src="https://polymarket-upload.s3.us-east-2.amazonaws.com/how_are_prices_calculated.png" />
</Frame>

<Note>You may not be able to buy shares at the displayed probability / price because there is a bid-ask spread. In the above example, a trader wanting to buy shares would pay 40¢ for up to 4,200 shares, after which the price would rise to 43¢.</Note>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt