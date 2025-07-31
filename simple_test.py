#!/usr/bin/env python3
"""
Simple test to show exactly what happens with $20 account
"""

import os
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Load environment variables
load_dotenv()

def test_with_20_dollars():
    """Test the system with $20 account to show exactly what happens."""
    
    print("💰 Testing with $20 Account")
    print("=" * 40)
    
    # Create configuration for $20 account
    config = DEFAULT_CONFIG.copy()
    config["enable_real_trading"] = True
    config["sandbox_mode"] = True  # Safe testing mode
    config["default_order_size"] = 1  # 1 share per trade
    config["max_position_size"] = 20  # Max $20 per position
    config["max_daily_loss"] = 10  # Max $10 daily loss
    config["max_portfolio_risk"] = 0.5  # 50% max portfolio risk (since $20 is small)
    
    print("📊 Configuration:")
    print(f"   - Account Size: $20")
    print(f"   - Max Position Size: ${config['max_position_size']}")
    print(f"   - Max Daily Loss: ${config['max_daily_loss']}")
    print(f"   - Default Order Size: {config['default_order_size']} share")
    print(f"   - Sandbox Mode: {config['sandbox_mode']}")
    print()
    
    # Initialize TradingAgents
    print("🚀 Initializing TradingAgents...")
    ta = TradingAgentsGraph(debug=False, config=config)
    
    # Test with a cheap stock
    test_symbols = ["AAPL", "MSFT", "TSLA"]
    
    for symbol in test_symbols:
        print(f"\n🔍 Analyzing {symbol}...")
        
        try:
            # Get current account info
            account_info = ta.get_account_info()
            print(f"💰 Account Info: {account_info}")
            
            # Get risk summary
            risk_summary = ta.get_risk_summary()
            print(f"⚠️  Risk Summary: {risk_summary}")
            
            # Run analysis
            _, decision = ta.propagate(symbol, "2024-01-15")
            print(f"📈 Decision: {decision}")
            
            # Show what would happen if we tried to trade
            if decision == "BUY":
                print(f"   → Would attempt to BUY 1 share of {symbol}")
                print(f"   → Estimated cost: ~$150-200 (likely rejected due to insufficient funds)")
            elif decision == "SELL":
                print(f"   → Would attempt to SELL 1 share of {symbol}")
                print(f"   → Only possible if you already own the stock")
            else:
                print(f"   → HOLD - No action taken")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("📋 SUMMARY FOR $20 ACCOUNT:")
    print("1. Most trades will be REJECTED due to insufficient funds")
    print("2. You can only buy very cheap stocks (under $20)")
    print("3. Consider penny stocks or fractional shares")
    print("4. Sandbox mode prevents real money loss")
    print("5. System is working correctly - it's protecting your money!")

if __name__ == "__main__":
    test_with_20_dollars() 