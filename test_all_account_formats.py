#!/usr/bin/env python3
"""
Test All E*TRADE Account Key Formats
Automatically test different account key formats
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def test_all_account_formats():
    """Test all possible account key formats."""
    print("🔍 Testing All E*TRADE Account Key Formats")
    print("=" * 60)
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    # All possible account key formats to test
    account_formats = [
        # Original formats
        "377274549",
        "377 274549",
        "377-274549",
        "377_274549",
        
        # Different lengths
        "37727454",
        "3772745490",
        "37727454900",
        "377274549000",
        
        # With prefixes/suffixes
        "account_377274549",
        "377274549_account",
        "acc_377274549",
        "377274549_acc",
        
        # Different separators
        "377.274549",
        "377:274549",
        "377|274549",
        
        # Reversed or modified
        "274549377",
        "3772745491",
        "3772745492",
        
        # With letters
        "377274549A",
        "A377274549",
        "377274549X",
    ]
    
    print(f"🧪 Testing {len(account_formats)} different account key formats...")
    print()
    
    successful_formats = []
    
    for i, account_key in enumerate(account_formats, 1):
        print(f"🧪 Test {i}/{len(account_formats)}: {account_key}")
        
        url = f"https://api.etrade.com/v1/accounts/{account_key}/balance"
        
        response = oauth.make_authenticated_request('GET', url)
        
        if response:
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS! Account key works: {account_key}")
                successful_formats.append(account_key)
                
                try:
                    data = response.json()
                    print(f"   📄 Account Data: {json.dumps(data, indent=2)}")
                except:
                    print("   📄 Response is not JSON")
                break
            elif response.status_code == 400:
                print(f"   ❌ Bad Request - wrong format")
            elif response.status_code == 401:
                print(f"   ❌ Unauthorized - OAuth issue")
            elif response.status_code == 404:
                print(f"   ❌ Not Found - account doesn't exist")
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
        else:
            print(f"   ❌ No response received")
        
        # Small delay to avoid rate limiting
        import time
        time.sleep(0.5)
    
    print(f"\n🎯 Results:")
    print("=" * 40)
    
    if successful_formats:
        print(f"✅ Found {len(successful_formats)} working account key(s):")
        for account_key in successful_formats:
            print(f"   📋 {account_key}")
            print(f"   💡 Update your .env file with:")
            print(f"      ETRADE_ACCOUNT_ID={account_key}")
    else:
        print("❌ No working account key found")
        print("💡 You may need to:")
        print("   1. Contact E*TRADE support")
        print("   2. Check your developer portal")
        print("   3. Ensure your account is activated for API access")

if __name__ == "__main__":
    test_all_account_formats() 