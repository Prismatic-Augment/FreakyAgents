#!/usr/bin/env python3
"""
Live Trading Test Script
Tests the E*TRADE integration with real order placement
"""

import os
from dotenv import load_dotenv
from tradingagents.brokers.etrade_client import ETradeClient

load_dotenv()

def test_live_trading():
    """Test live trading functionality."""
    print("🚀 Testing Live Trading with E*TRADE")
    print("=" * 50)
    
    # Initialize E*TRADE client in live mode
    client = ETradeClient(sandbox=False)
    
    # Check account status
    print("\n💰 Account Status:")
    account_info = client.get_account_info()
    print(f"   Balance: ${account_info.get('balance', 0)}")
    print(f"   Buying Power: ${account_info.get('buying_power', 0)}")
    
    # Test penny stock trading
    penny_stocks = [
        ("SNDL", 1.69),
        ("HEXO", 0.85),
        ("ACB", 2.15),
        ("TLRY", 1.45),
        ("CGC", 3.20),
        ("NAKD", 0.75),
        ("ZOM", 0.95),
        ("IDEX", 0.65)
    ]
    
    print(f"\n📈 Testing Penny Stock Orders:")
    print("=" * 50)
    
    for symbol, price in penny_stocks:
        print(f"\n🔍 Testing {symbol} @ ${price}")
        
        # Get quote
        quote = client.get_market_price(symbol)
        print(f"   Quote: ${quote}")
        
        # Try to place order
        order = {
            "symbol": symbol,
            "quantity": 1,
            "side": "buy",
            "orderType": "market"
        }
        
        result = client.place_market_order(symbol, 1, "buy")
        print(f"   Order Result: {result['status']}")
        
        if result['status'] == 'FILLED':
            print(f"   ✅ Successfully bought 1 share of {symbol}")
        else:
            print(f"   ❌ Order failed: {result.get('message', 'Unknown error')}")
    
    # Check final positions
    print(f"\n📊 Final Account Status:")
    account_info = client.get_account_info()
    print(f"   Remaining Balance: ${account_info.get('balance', 0)}")
    print(f"   Remaining Buying Power: ${account_info.get('buying_power', 0)}")
    
    positions = client.get_positions()
    if positions:
        print(f"   Positions:")
        for symbol, position in positions.items():
            print(f"     {symbol}: {position['quantity']} shares @ ${position['price']}")
    else:
        print(f"   No positions")

if __name__ == "__main__":
    test_live_trading() 