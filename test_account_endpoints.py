#!/usr/bin/env python3
"""
Test E*TRADE Account Endpoints
Find which endpoints work with the correct account key
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def test_account_endpoints():
    """Test different E*TRADE account endpoints."""
    print("🔍 Testing E*TRADE Account Endpoints")
    print("=" * 60)
    print("📋 Testing different endpoints with correct account key")
    print()
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    account_key = "UNRhZvwSnnF1PJCK6slVfA"
    
    # Test different account endpoints
    endpoints = [
        f"https://api.etrade.com/v1/accounts/{account_key}/balance",
        f"https://api.etrade.com/v1/accounts/{account_key}/positions",
        f"https://api.etrade.com/v1/accounts/{account_key}",
        f"https://api.etrade.com/v1/accounts/{account_key}/summary",
        f"https://api.etrade.com/v1/accounts/{account_key}/portfolio",
        f"https://api.etrade.com/v1/accounts/{account_key}/orders",
    ]
    
    print(f"🧪 Testing {len(endpoints)} different endpoints...")
    print()
    
    working_endpoints = []
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"🧪 Test {i}: {endpoint}")
        print("-" * 40)
        
        response = oauth.make_authenticated_request('GET', endpoint)
        
        if response:
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS! Endpoint works!")
                working_endpoints.append(endpoint)
                
                try:
                    data = response.json()
                    print(f"📄 Response Data: {json.dumps(data, indent=2)}")
                except:
                    print("📄 Response is not JSON")
            elif response.status_code == 500:
                print("❌ Internal Server Error - E*TRADE server issue")
            elif response.status_code == 400:
                print("❌ Bad Request - wrong endpoint")
            elif response.status_code == 401:
                print("❌ Unauthorized - OAuth issue")
            elif response.status_code == 404:
                print("❌ Not Found - endpoint doesn't exist")
            else:
                print(f"❌ Unexpected status: {response.status_code}")
        else:
            print("❌ No response received")
        
        print()
    
    print(f"🎯 Results:")
    print("=" * 40)
    
    if working_endpoints:
        print(f"✅ Found {len(working_endpoints)} working endpoint(s):")
        for endpoint in working_endpoints:
            print(f"   📋 {endpoint}")
    else:
        print("❌ No working endpoints found")
        print("💡 This might mean:")
        print("   1. E*TRADE server is having issues")
        print("   2. Account key is correct but endpoints are different")
        print("   3. Need to wait and try again later")

if __name__ == "__main__":
    test_account_endpoints() 