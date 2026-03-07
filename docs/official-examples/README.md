# polymarket-examples

Code examples for Polymarket

See [examples](./examples/) for more information

## Examples

Polymarket uses smart contract wallets internally. Every account created using the Polymarket website is a smart contract wallet.

There are 2 kinds of smart contract wallets used: 

* Polymarket Proxy: This is a smart contract wallet developed internally at Polymarket, to be used with Magic/email accounts.
Only the address associated with the email account can execute functions for the wallet.

* Polymarket Safes: This is a slightly modified Gnosis safe to be used with various Browser wallets(including Metamask, Rainbow, Coinbase Wallet,etc). It is a multisig with only 1 signer, the wallet used to sign into the website.

### Proxy Wallet Examples

Code examples for interacting with Polymarket Proxy Wallets are available [here](./examples/proxyWallet/README.md)

Magic accounts use Proxy Wallets on the backend


### Safe Wallet Examples

Code examples for interacting with Safe Wallets are available [here](./examples/safeWallet/README.md)

Browser wallets(Metamask, Coinbase Wallet, etc) use Safes on the backend


### Usage
Populate your .env file based on .env.example.

Run examples using ts-node:
```bash
ts-node examples/safeWallet/split.ts
```