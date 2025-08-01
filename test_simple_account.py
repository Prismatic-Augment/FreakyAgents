#!/usr/bin/env python3
"""
Simple E*TRADE Account Test
Try to get account info with different formats
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def test_simple_account():
    """Test simple account access."""
    print("🔍 Simple E*TRADE Account Test")
    print("=" * 60)
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    # Try different account formats
    test_accounts = [
        "377274549",      # Original
        "37727454",       # Shorter
        "3772745490",     # Longer
        "37727454900",    # Even longer
    ]
    
    for account_id in test_accounts:
        print(f"\n🧪 Testing Account ID: {account_id}")
        print("-" * 40)
        
        url = f"https://api.etrade.com/v1/accounts/{account_id}/balance"
        print(f"🌐 URL: {url}")
        
        response = oauth.make_authenticated_request('GET', url)
        
        if response:
            print(f"📊 Status: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ SUCCESS!")
                try:
                    data = response.json()
                    print(f"📄 Data: {json.dumps(data, indent=2)}")
                except:
                    print("📄 Response is not JSON")
                break
            elif response.status_code == 400:
                print("❌ Bad Request - wrong account format")
            elif response.status_code == 401:
                print("❌ Unauthorized - OAuth issue")
            elif response.status_code == 404:
                print("❌ Not Found - account doesn't exist")
            else:
                print(f"❌ Unexpected status: {response.status_code}")
        else:
            print("❌ No response received")

if __name__ == "__main__":
    test_simple_account() 