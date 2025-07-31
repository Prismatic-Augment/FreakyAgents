#!/usr/bin/env python3
"""
Test script for TradingAgents E*TRADE integration.
This script demonstrates the real trading capabilities.
"""

import os
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Load environment variables
load_dotenv()

def test_etrade_integration():
    """Test the E*TRADE integration with TradingAgents."""
    
    print("🚀 TradingAgents E*TRADE Integration Test")
    print("=" * 50)
    
    # Create configuration
    config = DEFAULT_CONFIG.copy()
    config["enable_real_trading"] = True
    config["sandbox_mode"] = True  # Use sandbox for safety
    config["default_order_size"] = 1  # Small test order
    config["max_position_size"] = 500  # Conservative position size
    config["max_daily_loss"] = 200  # Conservative daily loss limit
    
    # Initialize TradingAgents
    print("📊 Initializing TradingAgents with E*TRADE integration...")
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Test symbols
    test_symbols = ["AAPL", "NVDA", "TSLA"]
    
    for symbol in test_symbols:
        print(f"\n🔍 Analyzing {symbol}...")
        
        try:
            # Run analysis and get decision
            _, decision = ta.propagate(symbol, "2024-01-15")
            print(f"📈 Decision for {symbol}: {decision}")
            
            # Get account info
            account_info = ta.get_account_info()
            print(f"💰 Account Info: {account_info}")
            
            # Get risk summary
            risk_summary = ta.get_risk_summary()
            print(f"⚠️  Risk Summary: {risk_summary}")
            
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
    
    print("\n✅ E*TRADE integration test completed!")

def test_risk_management():
    """Test risk management features."""
    
    print("\n🛡️  Testing Risk Management")
    print("=" * 30)
    
    config = DEFAULT_CONFIG.copy()
    config["enable_real_trading"] = True
    config["sandbox_mode"] = True
    config["default_order_size"] = 100  # Large order to test limits
    config["max_position_size"] = 1000  # Small limit
    config["max_daily_loss"] = 500
    
    ta = TradingAgentsGraph(debug=False, config=config)
    
    # Test risk management
    risk_summary = ta.get_risk_summary()
    print(f"Initial Risk Summary: {risk_summary}")
    
    # Test account info
    account_info = ta.get_account_info()
    print(f"Account Info: {account_info}")

def test_paper_trading():
    """Test paper trading mode."""
    
    print("\n📝 Testing Paper Trading Mode")
    print("=" * 30)
    
    config = DEFAULT_CONFIG.copy()
    config["enable_real_trading"] = False  # Disable real trading
    config["sandbox_mode"] = True
    
    ta = TradingAgentsGraph(debug=False, config=config)
    
    # Run analysis without real trading
    _, decision = ta.propagate("MSFT", "2024-01-15")
    print(f"Paper Trading Decision: {decision}")
    
    # Should show that real trading is disabled
    account_info = ta.get_account_info()
    print(f"Account Info (Paper Trading): {account_info}")

if __name__ == "__main__":
    print("🎯 Starting TradingAgents E*TRADE Integration Tests")
    print("=" * 60)
    
    # Test 1: Basic integration
    test_etrade_integration()
    
    # Test 2: Risk management
    test_risk_management()
    
    # Test 3: Paper trading
    test_paper_trading()
    
    print("\n🎉 All tests completed!")
    print("\n📋 Next Steps:")
    print("1. Set up your E*TRADE developer account")
    print("2. Update .env file with your E*TRADE credentials")
    print("3. Set enable_real_trading to True for live trading")
    print("4. Adjust risk parameters based on your tolerance") 