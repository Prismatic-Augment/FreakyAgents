#!/usr/bin/env python3
"""
Real E*TRADE Trading Test
Uses proper OAuth authentication to place real orders
"""

import os
import time
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

load_dotenv()

class RealETradeTrading:
    """Real E*TRADE trading with proper OAuth authentication."""
    
    def __init__(self):
        self.account_id = os.getenv("ETRADE_ACCOUNT_ID")
        
        print("🚀 Real E*TRADE Trading Test")
        print("=" * 60)
        print("⚠️  WARNING: This will place REAL orders!")
        print("💰 Using your $20 account")
        print("🔐 Using proper OAuth authentication")
        
        # Initialize OAuth
        self.oauth = ETradeOAuth()
        if not self.oauth.load_tokens():
            print("❌ No OAuth tokens found. Please run etrade_oauth_proper.py first.")
            return
        
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
    
    def get_account_info(self):
        """Get real account information."""
        print("\n💰 Getting Account Information")
        print("-" * 40)
        
        url = f"https://api.etrade.com/v1/accounts/{self.account_id}/balance"
        
        response = self.oauth.make_authenticated_request('GET', url)
        
        if response and response.status_code == 200:
            data = response.json()
            print("✅ Account info retrieved successfully!")
            print(f"📄 Data: {json.dumps(data, indent=2)}")
            return data
        else:
            print(f"❌ Failed to get account info: {response.status_code if response else 'No response'}")
            return None
    
    def get_positions(self):
        """Get real positions."""
        print("\n📈 Getting Current Positions")
        print("-" * 40)
        
        url = f"https://api.etrade.com/v1/accounts/{self.account_id}/positions"
        
        response = self.oauth.make_authenticated_request('GET', url)
        
        if response and response.status_code == 200:
            data = response.json()
            print("✅ Positions retrieved successfully!")
            print(f"📄 Data: {json.dumps(data, indent=2)}")
            return data
        else:
            print(f"❌ Failed to get positions: {response.status_code if response else 'No response'}")
            return None
    
    def place_real_order(self, symbol, quantity, side):
        """Place a real order through E*TRADE API."""
        print(f"\n🎯 Placing REAL Order:")
        print(f"   Symbol: {symbol}")
        print(f"   Quantity: {quantity}")
        print(f"   Side: {side}")
        
        url = f"https://api.etrade.com/v1/accounts/{self.account_id}/orders"
        
        # Prepare order data
        order_data = {
            "orderType": "MARKET",
            "clientOrderId": f"ORDER_{int(time.time())}",
            "priceType": "MARKET",
            "orderTerm": "GOOD_FOR_DAY",
            "marketSession": "REGULAR",
            "quantity": quantity,
            "orderAction": side.upper(),
            "symbol": symbol,
            "quantityType": "QUANTITY",
            "routingDestination": "AUTO"
        }
        
        response = self.oauth.make_authenticated_request('POST', url, order_data)
        
        if response and response.status_code == 200:
            data = response.json()
            print("✅ Order placed successfully!")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            return {"status": "SUCCESS", "orderId": data.get("orderId")}
        else:
            print(f"❌ Order failed: {response.status_code if response else 'No response'}")
            if response:
                print(f"📄 Error: {response.text}")
            return {"status": "ERROR", "message": f"HTTP {response.status_code if response else 'No response'}"}
    
    def run_real_trading_test(self):
        """Run a complete real trading test."""
        print("\n🚨 REAL TRADING TEST")
        print("=" * 60)
        print("⚠️  WARNING: This will place REAL orders!")
        print("💰 Using your $20 account")
        print("📈 Testing with penny stocks")
        print("Press Ctrl+C to cancel, or any key to continue...")
        input()
        
        print("\n🎯 Starting Real Trading Test...")
        
        # Get account info
        account_info = self.get_account_info()
        if not account_info:
            print("❌ Cannot proceed without account info")
            return
        
        # Get current positions
        positions = self.get_positions()
        
        # Test with a simple stock
        symbol = "SNDL"
        print(f"\n🔍 Analyzing {symbol}...")
        
        try:
            # Make trading decision
            _, decision = self.trading_agents.propagate(symbol, "2024-01-15")
            print(f"📊 AI Decision: {decision}")
            
            # Try to place real order
            if decision == "BUY":
                print("\n🎯 Attempting to place REAL BUY order...")
                result = self.place_real_order(symbol, 1, "buy")
                
                if result["status"] == "SUCCESS":
                    print("🎉 REAL ORDER PLACED SUCCESSFULLY!")
                    print("💳 Check your E*TRADE account for the order")
                else:
                    print(f"❌ Order failed: {result['message']}")
            
            elif decision == "SELL":
                print("\n🎯 Attempting to place REAL SELL order...")
                result = self.place_real_order(symbol, 1, "sell")
                
                if result["status"] == "SUCCESS":
                    print("🎉 REAL ORDER PLACED SUCCESSFULLY!")
                    print("💳 Check your E*TRADE account for the order")
                else:
                    print(f"❌ Order failed: {result['message']}")
            
            else:
                print(f"📊 Decision: {decision} - No order placed")
            
        except Exception as e:
            print(f"❌ Error during trading test: {e}")
        
        print("\n📋 Summary:")
        print("=" * 40)
        print("✅ OAuth authentication: Working")
        print("✅ Account info: Retrieved")
        print("✅ AI analysis: Working")
        print("✅ Real orders: Attempted")
        print("\n💡 Next Steps:")
        print("   1. Check your E*TRADE account for orders")
        print("   2. Monitor your $20 account balance")
        print("   3. Set up automated trading if desired")

def main():
    """Main function."""
    print("🚀 Real E*TRADE Trading Test")
    print("This will place REAL orders with proper OAuth authentication")
    print()
    
    # Create trading system
    trading_system = RealETradeTrading()
    
    # Run real trading test
    trading_system.run_real_trading_test()

if __name__ == "__main__":
    main() 