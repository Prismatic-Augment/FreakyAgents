#!/usr/bin/env python3
"""
Find Correct E*TRADE Account ID
Try different account ID formats to find the correct one
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def find_account_id():
    """Find the correct account ID format."""
    print("🔍 Finding Correct E*TRADE Account ID")
    print("=" * 60)
    
    account_id = os.getenv("ETRADE_ACCOUNT_ID")
    print(f"📋 Current Account ID: {account_id}")
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    # Try different account ID formats based on E*TRADE documentation
    test_formats = [
        # Try the account ID as-is
        account_id,
        
        # Try with different prefixes/suffixes
        f"{account_id}",
        f"account_{account_id}",
        f"{account_id}_account",
        
        # Try different number formats
        str(int(account_id)),
        f"{int(account_id)}",
        
        # Try with dashes or underscores
        f"{account_id.replace('', '-')}",
        f"{account_id.replace('', '_')}",
        
        # Try shorter/longer versions
        account_id[:8],
        account_id[:6],
        f"{account_id}000",
    ]
    
    print(f"\n🧪 Testing {len(test_formats)} different account ID formats...")
    
    for i, test_format in enumerate(test_formats, 1):
        print(f"\n🧪 Test {i}: {test_format}")
        print("-" * 40)
        
        url = f"https://api.etrade.com/v1/accounts/{test_format}/balance"
        print(f"🌐 Testing URL: {url}")
        
        response = oauth.make_authenticated_request('GET', url)
        
        if response:
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS! Found working account ID format!")
                print(f"📄 Account ID: {test_format}")
                try:
                    data = response.json()
                    print(f"📄 Account Data: {json.dumps(data, indent=2)}")
                except:
                    print("📄 Response is not JSON")
                return test_format
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
    
    print("\n❌ No working account ID format found")
    print("💡 You may need to:")
    print("   1. Check your E*TRADE account for the correct account ID")
    print("   2. Contact E*TRADE support for the correct format")
    print("   3. Use the E*TRADE developer portal to find your account ID")
    
    return None

if __name__ == "__main__":
    find_account_id() 