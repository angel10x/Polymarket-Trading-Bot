# WSS Quickstart

The following code samples and explanation will show you how to subsribe to the Marker and User channels of the Websocket.
You'll need your API keys to do this so we'll start with that.

## Getting your API Keys

<CodeGroup>
  ```python DeriveAPIKeys-Python [expandable] theme={null}
  from py_clob_client.client import ClobClient

  host: str = "https://clob.polymarket.com"
  key: str = "" #This is your Private Key. If using email login export from https://reveal.magic.link/polymarket otherwise export from your Web3 Application
  chain_id: int = 137 #No need to adjust this
  POLYMARKET_PROXY_ADDRESS: str = '' #This is the address you deposit/send USDC to to FUND your Polymarket account.

  #Select from the following 3 initialization options to matches your login method, and remove any unused lines so only one client is initialized.

  ### Initialization of a client using a Polymarket Proxy associated with an Email/Magic account. If you login with your email use this example.
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=1, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client using a Polymarket Proxy associated with a Browser Wallet(Metamask, Coinbase Wallet, etc)
  client = ClobClient(host, key=key, chain_id=chain_id, signature_type=2, funder=POLYMARKET_PROXY_ADDRESS)

  ### Initialization of a client that trades directly from an EOA. 
  client = ClobClient(host, key=key, chain_id=chain_id)

  print( client.derive_api_key() )

  ```

  ```javascript DeriveAPIKeys-TS [expandable] theme={null}
  //npm install @polymarket/clob-client
  //npm install ethers
  //Client initialization example and dumping API Keys
  import {ClobClient, ApiKeyCreds } from "@polymarket/clob-client";
  import { Wallet } from "@ethersproject/wallet";

  const host = 'https://clob.polymarket.com';
  const signer = new Wallet("YourPrivateKey"); //This is your Private Key. If using email login export from https://reveal.magic.link/polymarket otherwise export from your Web3 Application

  // Initialize the clob client
  // NOTE: the signer must be approved on the CTFExchange contract
  const clobClient = new ClobClient(host, 137, signer);

  (async () => {
    const apiKey = await clobClient.deriveApiKey();
    console.log(apiKey);
  })();
  ```
</CodeGroup>

## Using those keys to connect to the Market or User Websocket

<CodeGroup>
  ```python WSS-Connection [expandable] theme={null}
  from websocket import WebSocketApp
  import json
  import time
  import threading

  MARKET_CHANNEL = "market"
  USER_CHANNEL = "user"


  class WebSocketOrderBook:
      def __init__(self, channel_type, url, data, auth, message_callback, verbose):
          self.channel_type = channel_type
          self.url = url
          self.data = data
          self.auth = auth
          self.message_callback = message_callback
          self.verbose = verbose
          furl = url + "/ws/" + channel_type
          self.ws = WebSocketApp(
              furl,
              on_message=self.on_message,
              on_error=self.on_error,
              on_close=self.on_close,
              on_open=self.on_open,
          )
          self.orderbooks = {}

      def on_message(self, ws, message):
          print(message)
          pass

      def on_error(self, ws, error):
          print("Error: ", error)
          exit(1)

      def on_close(self, ws, close_status_code, close_msg):
          print("closing")
          exit(0)

      def on_open(self, ws):
          if self.channel_type == MARKET_CHANNEL:
              ws.send(json.dumps({"assets_ids": self.data, "type": MARKET_CHANNEL}))
          elif self.channel_type == USER_CHANNEL and self.auth:
              ws.send(
                  json.dumps(
                      {"markets": self.data, "type": USER_CHANNEL, "auth": self.auth}
                  )
              )
          else:
              exit(1)

          thr = threading.Thread(target=self.ping, args=(ws,))
          thr.start()


      def subscribe_to_tokens_ids(self, assets_ids):
          if self.channel_type == MARKET_CHANNEL:
              self.ws.send(json.dumps({"assets_ids": assets_ids, "operation": "subscribe"}))

      def unsubscribe_to_tokens_ids(self, assets_ids):
          if self.channel_type == MARKET_CHANNEL:
              self.ws.send(json.dumps({"assets_ids": assets_ids, "operation": "unsubscribe"}))


      def ping(self, ws):
          while True:
              ws.send("PING")
              time.sleep(10)

      def run(self):
          self.ws.run_forever()


  if __name__ == "__main__":
      url = "wss://ws-subscriptions-clob.polymarket.com"
      #Complete these by exporting them from your initialized client. 
      api_key = ""
      api_secret = ""
      api_passphrase = ""

      asset_ids = [
          "109681959945973300464568698402968596289258214226684818748321941747028805721376",
      ]
      condition_ids = [] # no really need to filter by this one

      auth = {"apiKey": api_key, "secret": api_secret, "passphrase": api_passphrase}

      market_connection = WebSocketOrderBook(
          MARKET_CHANNEL, url, asset_ids, auth, None, True
      )
      user_connection = WebSocketOrderBook(
          USER_CHANNEL, url, condition_ids, auth, None, True
      )

      market_connection.subscribe_to_tokens_ids(["123"])
      # market_connection.unsubscribe_to_tokens_ids(["123"])

      market_connection.run()
      # user_connection.run()
  ```
</CodeGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.polymarket.com/llms.txt