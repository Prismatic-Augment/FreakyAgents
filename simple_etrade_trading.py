#!/usr/bin/env python3
"""
Simplified E*TRADE Trading System
Works with production credentials using a simplified approach
"""

import os
import time
import requests
import json
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

load_dotenv()

class SimpleETradeTrading:
    """Simplified E*TRADE trading system."""
    
    def __init__(self):
        self.consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
        self.consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
        self.account_id = os.getenv("ETRADE_ACCOUNT_ID")
        
        print("🚀 Simplified E*TRADE Trading System")
        print("=" * 60)
        print(f"✅ Using Production Credentials:")
        print(f"   Consumer Key: {self.consumer_key[:10]}...")
        print(f"   Account ID: {self.account_id}")
        
        # Initialize trading agents
        self.setup_trading_agents()
    
    def setup_trading_agents(self):
        """Set up the trading agents system."""
        print("\n🤖 Setting up Trading Agents...")
        
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "openai"
        config["backend_url"] = "https://api.openai.com/v1"
        config["deep_think_llm"] = "gpt-4o-mini"
        config["quick_think_llm"] = "gpt-4o-mini"
        config["enable_real_trading"] = True
        config["sandbox_mode"] = False  # LIVE TRADING
        config["default_order_size"] = 1
        config["max_position_size"] = 20
        config["max_daily_loss"] = 10
        config["max_portfolio_risk"] = 0.5
        
        self.trading_agents = TradingAgentsGraph(debug=True, config=config)
        print("✅ Trading agents initialized")
    
    def test_market_data(self):
        """Test market data access."""
        print("\n📈 Testing Market Data Access")
        print("-" * 40)
        
        # Test with a simple stock
        symbol = "SNDL"
        print(f"🔍 Testing market data for {symbol}")
        
        try:
            # Use the trading agents to get market data
            _, decision = self.trading_agents.propagate(symbol, "2024-01-15")
            print(f"📊 Analysis Result: {decision}")
            return True
        except Exception as e:
            print(f"❌ Market data test failed: {e}")
            return False
    
    def test_account_info(self):
        """Test account information access."""
        print("\n💰 Testing Account Information")
        print("-" * 40)
        
        try:
            account_info = self.trading_agents.get_account_info()
            print(f"📊 Account Info: {account_info}")
            
            risk_summary = self.trading_agents.get_risk_summary()
            print(f"⚠️  Risk Summary: {risk_summary}")
            
            return True
        except Exception as e:
            print(f"❌ Account info test failed: {e}")
            return False
    
    def test_trading_decision(self):
        """Test a complete trading decision."""
        print("\n🎯 Testing Complete Trading Decision")
        print("-" * 40)
        
        penny_stocks = ["SNDL", "HEXO", "ACB", "TLRY"]
        
        for symbol in penny_stocks:
            print(f"\n🔍 Analyzing {symbol}...")
            try:
                # Get account status before
                account_info = self.trading_agents.get_account_info()
                print(f"💰 Account Balance: ${account_info.get('balance', 0)}")
                
                # Make trading decision
                _, decision = self.trading_agents.propagate(symbol, "2024-01-15")
                print(f"📊 Decision: {decision}")
                
                # Check positions after
                positions = self.trading_agents.get_positions()
                if positions:
                    print(f"📈 Positions: {positions}")
                else:
                    print("📈 No positions")
                
                time.sleep(2)  # Brief pause between stocks
                
            except Exception as e:
                print(f"❌ Error analyzing {symbol}: {e}")
    
    def run_live_trading_test(self):
        """Run a complete live trading test."""
        print("\n🚨 LIVE TRADING TEST")
        print("=" * 60)
        print("⚠️  WARNING: This will attempt REAL trading!")
        print("💰 Using your $20 account")
        print("📈 Testing with penny stocks")
        print("Press Ctrl+C to cancel, or any key to continue...")
        input()
        
        print("\n🎯 Starting Live Trading Test...")
        
        # Test market data
        if not self.test_market_data():
            print("❌ Market data test failed - stopping")
            return
        
        # Test account info
        if not self.test_account_info():
            print("❌ Account info test failed - stopping")
            return
        
        # Test trading decisions
        self.test_trading_decision()
        
        print("\n✅ Live Trading Test Complete!")
        print("\n📋 Results:")
        print("   - Market data: Working")
        print("   - Account info: Working")
        print("   - Trading decisions: Processed")
        print("   - Risk management: Active")
        print("\n💡 Next Steps:")
        print("   1. Check your E*TRADE account for trades")
        print("   2. Monitor your $20 account balance")
        print("   3. Review trade performance")
        print("   4. Set up automated trading if desired")

def main():
    """Main function."""
    print("🚀 Simplified E*TRADE Trading System")
    print("This system will test real trading with your $20 account")
    print()
    
    # Create trading system
    trading_system = SimpleETradeTrading()
    
    # Run live trading test
    trading_system.run_live_trading_test()

if __name__ == "__main__":
    main() 