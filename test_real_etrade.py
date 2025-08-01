#!/usr/bin/env python3
"""
Real E*TRADE API Test
Tests actual connection to E*TRADE API
"""

import os
from dotenv import load_dotenv
from tradingagents.brokers.etrade_real_client import ETradeRealClient

load_dotenv()

def test_real_etrade_connection():
    """Test real E*TRADE API connection."""
    print("🚀 Testing Real E*TRADE API Connection")
    print("=" * 60)
    
    # Initialize real E*TRADE client
    client = ETradeRealClient(sandbox=False)  # Live trading
    
    # Test 1: Get account information
    print("\n📊 Test 1: Getting Account Information")
    print("-" * 40)
    account_info = client.get_account_info()
    print(f"Account Info: {account_info}")
    
    # Test 2: Get positions
    print("\n📈 Test 2: Getting Current Positions")
    print("-" * 40)
    positions = client.get_positions()
    print(f"Positions: {positions}")
    
    # Test 3: Get market price
    print("\n💰 Test 3: Getting Market Price")
    print("-" * 40)
    symbol = "SNDL"
    price = client.get_market_price(symbol)
    print(f"Current price of {symbol}: ${price}")
    
    # Test 4: List orders
    print("\n📋 Test 4: Listing Orders")
    print("-" * 40)
    orders = client.list_orders()
    print(f"Orders: {orders}")
    
    # Test 5: Place a small test order
    print("\n🔄 Test 5: Placing Test Order")
    print("-" * 40)
    print("⚠️  WARNING: This will place a REAL order!")
    print("Press Ctrl+C to cancel, or any key to continue...")
    input()
    
    # Place a small test order
    result = client.place_market_order("SNDL", 1, "buy")
    print(f"Order Result: {result}")
    
    if result.get("status") == "SUBMITTED":
        order_id = result.get("orderId")
        print(f"✅ Order submitted with ID: {order_id}")
        
        # Check order status
        print("\n📊 Checking Order Status...")
        status = client.get_order_status(order_id)
        print(f"Order Status: {status}")
    else:
        print(f"❌ Order failed: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    test_real_etrade_connection() 