import requests
from typing import List, Dict, Any, Optional

BASE_URL = "https://data-api.polymarket.com"

def get_user_positions(wallet_address: str) -> Optional[List[Dict[str, Any]]]:
    """
    Fetches the current positions for a given wallet address from Polymarket.
    """
    url = f"{BASE_URL}/positions"
    params = {"user": wallet_address}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching positions for {wallet_address}: {e}")
        return None

def detect_order_changes(
    positions_tn: List[Dict[str, Any]], 
    positions_tn_plus_1: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Compares two lists of positions to detect executed orders.
    """
    map_tn = {p['asset']: p for p in positions_tn}
    map_tn_plus_1 = {p['asset']: p for p in positions_tn_plus_1}
    
    all_assets = set(map_tn.keys()) | set(map_tn_plus_1.keys())
    orders = []

    for asset in all_assets:
        p_tn = map_tn.get(asset)
        p_tn_plus_1 = map_tn_plus_1.get(asset)

        # New Position (Buy)
        if p_tn is None and p_tn_plus_1 is not None:
            orders.append({
                'asset': asset,
                'type': 'BUY',
                'size': p_tn_plus_1['size'],
                'price': p_tn_plus_1['avgPrice'],
                'title': p_tn_plus_1.get('title'),
                'outcome': p_tn_plus_1.get('outcome'),
                'conditionId': p_tn_plus_1.get('conditionId'),
                'slug': p_tn_plus_1.get('slug')
            })
        
        # Position Completely Sold (Sell)
        elif p_tn is not None and p_tn_plus_1 is None:
            orders.append({
                'asset': asset,
                'type': 'SELL',
                'size': p_tn['size'],
                'price': None, 
                'title': p_tn.get('title'),
                'outcome': p_tn.get('outcome'),
                'conditionId': p_tn.get('conditionId'),
                'slug': p_tn.get('slug')
            })

        # Position Size Changed
        elif p_tn is not None and p_tn_plus_1 is not None:
            size_diff = float(p_tn_plus_1['size']) - float(p_tn['size'])
            
            if abs(size_diff) < 1e-9:
                continue

            order = {
                'asset': asset,
                'title': p_tn_plus_1.get('title'),
                'outcome': p_tn_plus_1.get('outcome'),
                'conditionId': p_tn_plus_1.get('conditionId'),
                'slug': p_tn_plus_1.get('slug')
            }

            if size_diff > 0:
                # Buy Order: Calculate effective price from average price changes
                cost_tn_plus_1 = float(p_tn_plus_1['size']) * float(p_tn_plus_1['avgPrice'])
                cost_tn = float(p_tn['size']) * float(p_tn['avgPrice'])
                exec_price = (cost_tn_plus_1 - cost_tn) / size_diff
                
                order.update({
                    'type': 'BUY',
                    'size': size_diff,
                    'price': exec_price
                })
            else:
                # Sell Order: Calculate effective price from realized PnL changes
                size_sold = -size_diff
                pnl_diff = float(p_tn_plus_1.get('realizedPnl', 0)) - float(p_tn.get('realizedPnl', 0))
                exec_price = float(p_tn['avgPrice']) + (pnl_diff / size_sold)

                order.update({
                    'type': 'SELL',
                    'size': size_sold,
                    'price': exec_price
                })
            
            orders.append(order)

    return orders
