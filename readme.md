# poly-market-maker

A production-ready Polymarket CLOB market-making engine designed for systematic liquidity provision.
Implements inventory-aware quoting, spread optimization, intelligent order management, and automated risk controls to maintain balanced exposure while maximizing spread capture on prediction markets.

Want to learn more or get setup help? Please connect with our techy team on Telegram: [@qntrade](https://t.me/qntrade) 🚀

## ⚙️ What This Bot Does

The **Polymarket Market Maker Bot** is a production-grade trading engine designed to provide automated liquidity on the Polymarket CLOB while maintaining controlled inventory and maximizing spread capture.

It enables:

- **Real-time market making** on the Polymarket Central Limit Order Book
- **Balanced YES/NO inventory management** to maintain controlled exposure
- **Intelligent quote placement** near the top of the orderbook
- **Optimized cancel/replace cycles** tuned for Polymarket's 500ms taker delay
- **Passive maker-only execution** to capture spreads and earn rebates
- **Automated risk controls** to prevent excessive exposure
- **Auto-redeem for settled markets**
- **Gas-efficient operations** through batching and lifecycle optimization
- **Low-latency orderbook updates** via WebSocket feeds

---

# 🚀 Core Features

## Inventory Balance & Exposure Control

Maintain controlled market exposure with automated inventory management.

- **Mirrored YES/NO positioning** to balance exposure across both sides
- **Net exposure limits** with configurable USD thresholds
- **Inventory skew detection** with automatic quote size adjustments
- **Dynamic rebalancing** to prevent runaway inventory accumulation
- **Target inventory levels** for consistent risk management

---

## Spread Farming Efficiency

Maximize profitability through intelligent spread capture.

- **Top-of-book quoting** for higher fill probability
- **Maker-only execution** to earn rebates and avoid taker fees
- **Optimized queue positioning** for improved execution priority
- **Fast quote updates** to reduce missed fills
- **Anti-crossing protection** to prevent accidental taker trades

---

## Cancel / Replace Optimization

Efficient order lifecycle management designed for Polymarket's execution mechanics.

- **Low-latency refresh cycles** (default: 1000ms)
- **500ms taker delay optimization**
- **Batch order cancellations** to reduce API calls and gas usage
- **Stale order detection** with automatic cancellation
- **Smooth quote transitions** without gaps or overlaps

---

## Market Discovery & Real-Time Data

Stay synchronized with the market through low-latency data streams.

- **Automatic market discovery** within configurable time windows
- **WebSocket orderbook feeds** for real-time L2 updates
- **Trade monitoring** for instant inventory adjustments
- **Efficient market metadata caching**

---

## Risk Management

Built-in safeguards to protect trading capital.

- **Hard exposure limits** on net USD exposure
- **Maximum position size controls**
- **Inventory skew protection**
- **Optional stop-loss thresholds**
- **Pre-trade validation checks**

---

## Auto-Redeem & Gas Optimization

Efficient on-chain interaction and settlement management.

- **Automatic redemption** for settled markets
- **Gas batching** to reduce transaction costs
- **Configurable gas pricing**
- **Optimized order lifecycle operations**

---

## Performance Monitoring

Advanced monitoring for professional trading operations.

- **Prometheus metrics** for orders, inventory, exposure, and PnL
- **Structured JSON logs** for full operational auditability
- **Passive fill-rate tracking**
- **Latency monitoring** for quote generation and execution

## ⚠️ Risk Management Best Practices

To trade safely and maintain controlled exposure on Polymarket, follow these guidelines:

1. **Start Small**  
   Begin with low `DEFAULT_SIZE` and `MAX_EXPOSURE_USD` values to limit initial risk.

2. **Monitor Inventory**  
   Keep an eye on inventory skew and adjust limits dynamically to maintain balanced YES/NO positions.

3. **Set Conservative Exposure Limits**  
   Use strict exposure caps to prevent runaway positions or over-leveraging.

4. **Test Thoroughly on Testnet**  
   Validate strategies and bot behavior on test networks before deploying with real funds.

5. **Monitor Gas Costs**  
   While gas batching helps reduce on-chain fees, always track gas usage during periods of high network activity.

6. **Regularly Review Logs**  
   Audit logs for risk check alerts, unexpected behaviors, and edge cases to ensure system integrity.

## 📞 Get Support

Need help setting up your Polymarket bot or want to optimize your trading strategy?  
Connect directly with our expert team and start trading smarter!  

🚀 **Fastest Support:** [Telegram: @qntrade](https://t.me/qntrade)  

Wishing you smooth fills and profitable spreads — happy trading! 📈
