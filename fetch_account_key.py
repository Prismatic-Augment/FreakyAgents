#!/usr/bin/env python3
"""
Fetch E*TRADE Account Key
Properly retrieve the account key from the API
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def fetch_account_key():
    """Fetch the account key from E*TRADE API."""
    print("🔍 Fetching E*TRADE Account Key")
    print("=" * 60)
    print("📋 This will retrieve the actual account key from the API")
    print("💡 The account key is NOT your account number!")
    print()
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return None
    
    # Try different account list endpoints
    endpoints = [
        "https://api.etrade.com/v1/accounts",
        "https://api.etrade.com/v1/accounts/list",
        "https://api.etrade.com/v1/accounts/",
    ]
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"🧪 Test {i}: {endpoint}")
        print("-" * 40)
        
        response = oauth.make_authenticated_request('GET', endpoint)
        
        if response:
            print(f"📊 Response Status: {response.status_code}")
            print(f"📄 Response: {response.text[:500]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ SUCCESS! Retrieved account list!")
                    
                    # Look for account key in the response
                    if 'AccountListResponse' in data:
                        accounts = data['AccountListResponse']['Accounts']['Account']
                        print("\n📋 Found Accounts:")
                        for account in accounts:
                            account_id = account.get('accountId')
                            account_key = account.get('accountIdKey') or account.get('accountKey')
                            account_type = account.get('accountType')
                            print(f"   Account ID: {account_id}")
                            print(f"   Account Key: {account_key}")
                            print(f"   Account Type: {account_type}")
                            print()
                            
                            if account_key:
                                print(f"🎯 Found Account Key: {account_key}")
                                print(f"💡 Use this account key in your .env file:")
                                print(f"   ETRADE_ACCOUNT_ID={account_key}")
                                return account_key
                    
                    # If no accountIdKey, look for other possible fields
                    print("🔍 Looking for account key in response...")
                    print(f"📄 Full response structure: {json.dumps(data, indent=2)}")
                    
                    return data
                    
                except Exception as e:
                    print(f"❌ Error parsing response: {e}")
                    print(f"📄 Raw response: {response.text}")
            elif response.status_code == 401:
                print("❌ Unauthorized - OAuth issue or API access not enabled")
                print("💡 This might mean:")
                print("   1. OAuth tokens are expired")
                print("   2. API access is not fully enabled")
                print("   3. Account is not eligible for API access")
            elif response.status_code == 400:
                print("❌ Bad Request - wrong endpoint or parameters")
            elif response.status_code == 404:
                print("❌ Not Found - endpoint doesn't exist")
            else:
                print(f"❌ Unexpected status: {response.status_code}")
        else:
            print("❌ No response received")
        
        print()
    
    print("❌ Could not retrieve account key from any endpoint")
    print("💡 This might mean:")
    print("   1. API access is not fully enabled")
    print("   2. Account is not eligible for API access")
    print("   3. Need to contact E*TRADE support")
    
    return None

def test_account_key(account_key):
    """Test the retrieved account key."""
    print(f"\n🧪 Testing Account Key: {account_key}")
    print("-" * 40)
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return False
    
    url = f"https://api.etrade.com/v1/accounts/{account_key}/balance"
    print(f"🌐 Testing URL: {url}")
    
    response = oauth.make_authenticated_request('GET', url)
    
    if response:
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Account key works!")
            try:
                data = response.json()
                print(f"📄 Account Data: {json.dumps(data, indent=2)}")
            except:
                print("📄 Response is not JSON")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"📄 Error: {response.text}")
            return False
    else:
        print("❌ No response received")
        return False

if __name__ == "__main__":
    print("🚀 E*TRADE Account Key Fetcher")
    print("This will properly retrieve your account key from the API")
    print()
    
    # Fetch account key
    account_key = fetch_account_key()
    
    if account_key:
        print(f"\n🎯 Retrieved account key: {account_key}")
        print("💡 Update your .env file with:")
        print(f"   ETRADE_ACCOUNT_ID={account_key}")
        
        # Test the account key
        if test_account_key(account_key):
            print("\n✅ Account key is working!")
            print("🚀 You can now enable real trading!")
        else:
            print("\n❌ Account key test failed")
    else:
        print("\n❌ Could not retrieve account key")
        print("💡 You may need to:")
        print("   1. Contact E*TRADE support to enable API access")
        print("   2. Ensure your account is eligible for API access")
        print("   3. Check that your OAuth tokens are valid") 