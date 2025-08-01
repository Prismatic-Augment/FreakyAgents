#!/usr/bin/env python3
"""
Test E*TRADE Account ID Variations
Based on the screenshot showing "377 274549"
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def test_account_variations():
    """Test different account ID variations."""
    print("🔍 Testing E*TRADE Account ID Variations")
    print("=" * 60)
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    # Test different variations of "377 274549"
    test_variations = [
        "377274549",      # No space
        "377 274549",     # With space
        "377-274549",     # With dash
        "377_274549",     # With underscore
        "377274549",      # Original
        "37727454",       # Shorter
        "3772745490",     # Longer
        "37727454900",    # Even longer
    ]
    
    print(f"\n🧪 Testing {len(test_variations)} account ID variations...")
    
    for i, account_id in enumerate(test_variations, 1):
        print(f"\n🧪 Test {i}: {account_id}")
        print("-" * 40)
        
        url = f"https://api.etrade.com/v1/accounts/{account_id}/balance"
        print(f"🌐 Testing URL: {url}")
        
        response = oauth.make_authenticated_request('GET', url)
        
        if response:
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS! Found working account ID!")
                print(f"📄 Account ID: {account_id}")
                try:
                    data = response.json()
                    print(f"📄 Account Data: {json.dumps(data, indent=2)}")
                except:
                    print("📄 Response is not JSON")
                return account_id
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
    
    print("\n❌ No working account ID found")
    print("💡 The account ID might be:")
    print("   1. In a different format than expected")
    print("   2. Not yet activated for API access")
    print("   3. Requiring additional setup in E*TRADE developer portal")
    
    return None

if __name__ == "__main__":
    test_account_variations() 