#!/usr/bin/env python3
import time
import json
import logging
import sys
import os
from ratelimit import limits, sleep_and_retry

# Ensure we can import from src
sys.path.append(os.getcwd())

from src.positions import get_user_positions, detect_order_changes
from src.trading import TradingModule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    wallets = config.get("wallets_to_track", [])
    rate_limit = config.get("rate_limit", 25)
    
    if not wallets:
        logger.error("No wallets to track in config.")
        return

    trading_module = TradingModule(config)
    
    @sleep_and_retry
    @limits(calls=rate_limit, period=10)
    def fetch_positions_safe(wallet_address):
        return get_user_positions(wallet_address)
    
    # Initialize state
    logger.info(f"Initializing state for {len(wallets)} wallets...")
    wallet_states = {}
    for wallet in wallets:
        positions = fetch_positions_safe(wallet)
        if positions is not None:
            wallet_states[wallet] = positions
            logger.info(f"Initialized {wallet[:8]}... with {len(positions)} positions")

    logger.info("Starting copy trader loop...")
    try:
        while True:
            for wallet in wallets:
                try:
                    current_positions = fetch_positions_safe(wallet)
                    if current_positions is None:
                        continue
                        
                    previous_positions = wallet_states.get(wallet, [])
                    changes = detect_order_changes(previous_positions, current_positions)
                    
                    if changes:
                        for change in changes:
                            logger.info(f"Detected change for {wallet[:8]}: {change['type']} {change['size']} shares of {change.get('title')}")
                            trading_module.execute_copy_trade(change)
                        
                    wallet_states[wallet] = current_positions
                    
                except Exception as e:
                    logger.error(f"Error tracking {wallet}: {e}")
            
            time.sleep(1) # Check every second (rate limiter handles API constraint)

    except KeyboardInterrupt:
        logger.info("Stopping...")

if __name__ == "__main__":
    main()
