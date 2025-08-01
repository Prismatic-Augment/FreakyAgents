#!/usr/bin/env python3
"""
Test E*TRADE Account ID Format
Find the correct account ID format for API calls
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def test_account_formats():
    """Test different account ID formats."""
    print("🔍 Testing E*TRADE Account ID Formats")
    print("=" * 60)
    
    account_id = os.getenv("ETRADE_ACCOUNT_ID")
    print(f"📋 Original Account ID: {account_id}")
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    # Test different account ID formats
    test_formats = [
        account_id,  # Original format
        f"{account_id}",  # String format
        f"v1/accounts/{account_id}/balance",  # Full path
        f"accounts/{account_id}/balance",  # Relative path
    ]
    
    for i, test_format in enumerate(test_formats, 1):
        print(f"\n🧪 Test {i}: {test_format}")
        print("-" * 40)
        
        if test_format.startswith("v1/") or test_format.startswith("accounts/"):
            url = f"https://api.etrade.com/{test_format}"
        else:
            url = f"https://api.etrade.com/v1/accounts/{test_format}/balance"
        
        print(f"🌐 Testing URL: {url}")
        
        response = oauth.make_authenticated_request('GET', url)
        
        if response:
            print(f"📊 Response Status: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ SUCCESS! Found working account format!")
                try:
                    data = response.json()
                    print(f"📄 Account Data: {json.dumps(data, indent=2)}")
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
    test_account_formats() 