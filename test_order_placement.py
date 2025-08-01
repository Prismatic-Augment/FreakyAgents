#!/usr/bin/env python3
"""
Test E*TRADE Order Placement
Test if we can place orders without balance endpoint
"""

import os
import json
import time
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def test_order_placement():
    """Test order placement without balance endpoint."""
    print("🔍 Testing E*TRADE Order Placement")
    print("=" * 60)
    print("📋 Testing if we can place orders directly")
    print("⚠️  This will attempt to place a REAL order!")
    print()
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    account_key = "UNRhZvwSnnF1PJCK6slVfA"
    
    # Test order placement
    orders_url = f"https://api.etrade.com/v1/accounts/{account_key}/orders"
    print(f"🌐 Testing order placement: {orders_url}")
    print("-" * 40)
    
    # Prepare a small test order
    order_data = {
        "orderType": "MARKET",
        "clientOrderId": f"TEST_ORDER_{int(time.time())}",
        "priceType": "MARKET",
        "orderTerm": "GOOD_FOR_DAY",
        "marketSession": "REGULAR",
        "quantity": 1,
        "orderAction": "BUY",
        "symbol": "SNDL",
        "quantityType": "QUANTITY",
        "routingDestination": "AUTO"
    }
    
    print("📋 Order Data:")
    print(f"   Symbol: SNDL")
    print(f"   Quantity: 1")
    print(f"   Action: BUY")
    print(f"   Type: MARKET")
    print(f"   Estimated Cost: ~$1-5")
    print()
    
    print("⚠️  WARNING: This will attempt to place a REAL order!")
    print("Press Ctrl+C to cancel, or any key to continue...")
    input()
    
    response = oauth.make_authenticated_request('POST', orders_url, order_data)
    
    if response:
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Order placed successfully!")
            try:
                data = response.json()
                print(f"📄 Order Data: {json.dumps(data, indent=2)}")
            except:
                print("📄 Response is not JSON")
        elif response.status_code == 400:
            print("❌ Bad Request - order parameters issue")
            print("💡 This might mean:")
            print("   1. Insufficient funds")
            print("   2. Invalid order parameters")
            print("   3. Account restrictions")
        elif response.status_code == 401:
            print("❌ Unauthorized - OAuth issue")
        elif response.status_code == 500:
            print("❌ Internal Server Error - E*TRADE server issue")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    else:
        print("❌ No response received")

if __name__ == "__main__":
    test_order_placement() 