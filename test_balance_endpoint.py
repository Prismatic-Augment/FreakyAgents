#!/usr/bin/env python3
"""
Test E*TRADE Balance Endpoint
Test the balance endpoint with fresh OAuth tokens
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def test_balance_endpoint():
    """Test the balance endpoint with fresh tokens."""
    print("🔍 Testing E*TRADE Balance Endpoint")
    print("=" * 60)
    print("📋 Testing with fresh OAuth tokens")
    print()
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    account_key = "UNRhZvwSnnF1PJCK6slVfA"
    
    # Test balance endpoint
    balance_url = f"https://api.etrade.com/v1/accounts/{account_key}/balance"
    print(f"🌐 Testing balance endpoint: {balance_url}")
    print("-" * 40)
    
    response = oauth.make_authenticated_request('GET', balance_url)
    
    if response:
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print(f"📄 Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Balance endpoint working!")
            try:
                data = response.json()
                print(f"📄 Balance Data: {json.dumps(data, indent=2)}")
            except:
                print("📄 Response is not JSON")
        elif response.status_code == 500:
            print("❌ Internal Server Error - E*TRADE server issue")
            print("💡 This might be:")
            print("   1. Temporary server issue")
            print("   2. Account not eligible for balance endpoint")
            print("   3. Need to contact E*TRADE support")
        elif response.status_code == 401:
            print("❌ Unauthorized - OAuth issue")
        elif response.status_code == 400:
            print("❌ Bad Request - wrong parameters")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    else:
        print("❌ No response received")

if __name__ == "__main__":
    test_balance_endpoint() 