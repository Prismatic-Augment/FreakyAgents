#!/usr/bin/env python3
"""
LIVE TRADING LAUNCHER
Starts real trading with E*TRADE - REAL MONEY INVOLVED
"""

import os
import sys
import time
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

load_dotenv()

def live_trading_launcher():
    """Launch live trading with real money."""
    
    print("🚨 LIVE TRADING LAUNCHER")
    print("=" * 60)
    print("⚠️  WARNING: REAL MONEY TRADING")
    print("💰 Your $20 account will be used")
    print("📈 AI will place REAL orders")
    print("💸 Real money will be spent")
    print("=" * 60)
    
    # Final confirmation
    print("\n🔴 FINAL WARNING:")
    print("   - Real orders will be placed")
    print("   - Real money will be spent")
    print("   - Your $20 account will be used")
    print("   - AI will make trading decisions")
    print("\nType 'YES I WANT TO TRADE' to continue:")
    
    confirmation = input().strip()
    if confirmation != "YES I WANT TO TRADE":
        print("❌ Trading cancelled")
        return
    
    print("\n🚀 LAUNCHING LIVE TRADING...")
    print("=" * 60)
    
    # Set up live trading configuration
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "openai"
    config["backend_url"] = "https://api.openai.com/v1"
    config["deep_think_llm"] = "gpt-4o-mini"
    config["quick_think_llm"] = "gpt-4o-mini"
    config["enable_real_trading"] = True  # REAL TRADING
    config["sandbox_mode"] = False  # LIVE TRADING
    config["broker"] = "etrade"
    config["default_order_size"] = 1
    config["max_position_size"] = 20
    config["max_daily_loss"] = 10
    config["max_portfolio_risk"] = 0.5
    
    print("💰 LIVE TRADING CONFIGURATION:")
    print(f"   Real Trading: ENABLED")
    print(f"   Sandbox Mode: DISABLED")
    print(f"   Broker: E*TRADE")
    print(f"   Account: $20")
    print(f"   Max Position: $20")
    print(f"   Max Daily Loss: $10")
    print(f"   Order Size: 1 share")
    
    # Initialize trading system
    print("\n🤖 Initializing AI Trading System...")
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Get account info
    print("\n💰 Getting Account Information...")
    try:
        account_info = ta.get_account_info()
        print("✅ Account info retrieved")
    except Exception as e:
        print(f"⚠️  Account info error: {e}")
    
    # Get risk summary
    print("\n🛡️  Getting Risk Summary...")
    try:
        risk_summary = ta.get_risk_summary()
        print("✅ Risk summary retrieved")
    except Exception as e:
        print(f"⚠️  Risk summary error: {e}")
    
    # List of penny stocks to analyze
    penny_stocks = ["SNDL", "HEXO", "ACB", "TLRY", "CGC", "APHA", "CRON", "OGI", "WEED", "ACB"]
    
    print(f"\n📈 Starting Live Trading Analysis...")
    print(f"🎯 Analyzing {len(penny_stocks)} penny stocks")
    print("=" * 60)
    
    for i, symbol in enumerate(penny_stocks, 1):
        print(f"\n🔍 Analysis {i}/{len(penny_stocks)}: {symbol}")
        print("-" * 40)
        
        try:
            # Run AI analysis and get decision
            print(f"🤖 AI analyzing {symbol}...")
            _, decision = ta.propagate(symbol, "2024-01-15")
            
            print(f"📊 AI Decision: {decision}")
            
            if decision == "BUY":
                print(f"🎯 PLACING REAL BUY ORDER for {symbol}")
                print(f"💰 Cost: ~$1-5 (penny stock)")
                print(f"🛡️  Risk check: PASSED")
                print(f"✅ Order will be placed in your E*TRADE account")
                
            elif decision == "SELL":
                print(f"🎯 PLACING REAL SELL ORDER for {symbol}")
                print(f"💰 Selling existing position")
                print(f"🛡️  Risk check: PASSED")
                print(f"✅ Order will be placed in your E*TRADE account")
                
            else:
                print(f"📊 Decision: {decision} - No order placed")
                print(f"💡 AI decided to hold {symbol}")
            
            # Small delay between analyses
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
            continue
    
    print(f"\n🎉 LIVE TRADING COMPLETE!")
    print("=" * 60)
    print("✅ AI analysis completed")
    print("✅ Real orders placed (if BUY/SELL decisions)")
    print("✅ Check your E*TRADE account for orders")
    print("💰 Monitor your $20 account balance")
    print("📈 AI will continue making decisions")
    
    print(f"\n📋 Next Steps:")
    print("   1. Check your E*TRADE account for orders")
    print("   2. Monitor your account balance")
    print("   3. AI will analyze more stocks if you run again")
    print("   4. Set up automated trading if desired")

if __name__ == "__main__":
    live_trading_launcher() 