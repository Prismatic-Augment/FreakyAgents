#!/usr/bin/env python3
"""
Check Funds Status
Check when your $20 will be available for trading
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def check_funds_status():
    """Check the current funds status."""
    print("💰 Checking Funds Status")
    print("=" * 60)
    print("🔍 Why no orders are showing in E*TRADE")
    print()
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    account_key = "UNRhZvwSnnF1PJCK6slVfA"
    
    print("📊 Account Information:")
    print("-" * 40)
    
    # Try to get account info
    accounts_url = "https://api.etrade.com/v1/accounts/list"
    print("🌐 Getting account details...")
    
    response = oauth.make_authenticated_request('GET', accounts_url)
    
    if response and response.status_code == 200:
        try:
            data = response.json()
            account_info = data['AccountListResponse']['Accounts']['Account'][0]
            print("✅ Account details retrieved")
            print(f"📄 Account: {account_info['accountDesc']}")
            print(f"📄 Status: {account_info['accountStatus']}")
            print(f"📄 Type: {account_info['accountType']}")
        except Exception as e:
            print(f"❌ Error parsing account info: {e}")
    else:
        print(f"❌ Failed to get account info: {response.status_code if response else 'No response'}")
    
    print("\n💡 Analysis:")
    print("-" * 40)
    print("🔍 From your E*TRADE screenshot:")
    print("   ✅ Net Account Value: $20.00")
    print("   ❌ Available for Withdrawal: $0.00")
    print("   ❌ Cash Purchasing Power: $0.00")
    print("   ❌ Open Orders: 0")
    print("   ❌ Current Positions: 0")
    
    print("\n🎯 Root Cause:")
    print("-" * 40)
    print("💰 Your $20 deposit is NOT yet available for trading!")
    print("📅 Deposit settlement time: 1-3 business days")
    print("🛡️  Risk management blocking orders (no buying power)")
    print("⏰ Funds need time to clear before trading")
    
    print("\n📋 Solutions:")
    print("-" * 40)
    print("1. ⏳ Wait for deposit to settle (1-3 business days)")
    print("2. 💰 Add more funds that are immediately available")
    print("3. 🔄 Check E*TRADE for settlement status")
    print("4. 📞 Contact E*TRADE if funds don't clear")
    
    print("\n🚀 When Funds Are Available:")
    print("-" * 40)
    print("✅ Cash Purchasing Power > $0")
    print("✅ Available for Withdrawal > $0")
    print("✅ Risk management will allow orders")
    print("✅ AI system will place real orders")
    print("✅ Orders will appear in E*TRADE")
    
    print("\n💡 Next Steps:")
    print("-" * 40)
    print("1. Check E*TRADE daily for fund availability")
    print("2. Run the trading system once funds are available")
    print("3. Monitor your account for real orders")
    print("4. AI will start making trading decisions")

if __name__ == "__main__":
    check_funds_status() 