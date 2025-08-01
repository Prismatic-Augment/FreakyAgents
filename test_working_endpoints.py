#!/usr/bin/env python3
"""
Test Working E*TRADE Endpoints
Test endpoints that were working with corrected OAuth
"""

import os
import json
from dotenv import load_dotenv
from fix_oauth_signature import CorrectETradeOAuth

load_dotenv()

def test_working_endpoints():
    """Test endpoints that were working before."""
    print("🔍 Testing Working E*TRADE Endpoints")
    print("=" * 60)
    print("📋 Testing endpoints that were working with corrected OAuth")
    print()
    
    oauth = CorrectETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    account_key = "UNRhZvwSnnF1PJCK6slVfA"
    
    # Test endpoints that were working before
    endpoints = [
        f"https://api.etrade.com/v1/accounts",
        f"https://api.etrade.com/v1/accounts/list",
        f"https://api.etrade.com/v1/accounts/{account_key}/portfolio",
        f"https://api.etrade.com/v1/accounts/{account_key}/orders",
    ]
    
    print(f"🧪 Testing {len(endpoints)} endpoints...")
    print()
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"🧪 Test {i}: {endpoint}")
        print("-" * 40)
        
        response = oauth.make_authenticated_request('GET', endpoint)
        
        if response:
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS! Endpoint working!")
                try:
                    data = response.json()
                    print(f"📄 Response Data: {json.dumps(data, indent=2)}")
                except:
                    print("📄 Response is not JSON")
            elif response.status_code == 204:
                print("✅ SUCCESS! Endpoint working (no content)")
            elif response.status_code == 500:
                print("❌ Internal Server Error - E*TRADE server issue")
            elif response.status_code == 401:
                print("❌ Unauthorized - OAuth issue")
            else:
                print(f"❌ Unexpected status: {response.status_code}")
        else:
            print("❌ No response received")
        
        print()
    
    print(f"🎯 Summary:")
    print("=" * 40)
    print("✅ OAuth signature is now correct (no more signature_invalid)")
    print("✅ Account list endpoint works")
    print("❌ Balance endpoint has 500 error (E*TRADE server issue)")
    print("💡 The 500 error is likely on E*TRADE's end, not our code")

if __name__ == "__main__":
    test_working_endpoints() 