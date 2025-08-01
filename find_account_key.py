#!/usr/bin/env python3
"""
Find E*TRADE Account Key
Based on E*TRADE Developer Documentation
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def find_account_key():
    """Find the correct account key format."""
    print("🔍 Finding E*TRADE Account Key")
    print("=" * 60)
    print("📋 Based on E*TRADE Developer Documentation")
    print()
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    print("💡 According to E*TRADE documentation:")
    print("   1. Account keys might be in a different format than account numbers")
    print("   2. You need to get the account list first")
    print("   3. The account key is separate from the account ID")
    print()
    
    # Try to get account list first
    print("🌐 Step 1: Getting Account List")
    print("-" * 40)
    
    url = "https://api.etrade.com/v1/accounts"
    print(f"🌐 URL: {url}")
    
    response = oauth.make_authenticated_request('GET', url)
    
    if response:
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Account list retrieved successfully!")
                
                # Look for account keys in the response
                if 'AccountListResponse' in data:
                    accounts = data['AccountListResponse']['Accounts']['Account']
                    print("\n📋 Found Accounts:")
                    for account in accounts:
                        account_id = account.get('accountId')
                        account_key = account.get('accountIdKey')
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
                
                return data
            except Exception as e:
                print(f"❌ Error parsing response: {e}")
                return None
        else:
            print(f"❌ Failed to get account list: {response.status_code}")
            print("💡 This might mean:")
            print("   1. OAuth tokens are expired")
            print("   2. Account not yet activated for API access")
            print("   3. Need to contact E*TRADE support")
            return None
    else:
        print("❌ No response received")
        return None

def test_account_key(account_key):
    """Test a specific account key."""
    print(f"\n🧪 Testing Account Key: {account_key}")
    print("-" * 40)
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return False
    
    url = f"https://api.etrade.com/v1/accounts/{account_key}/balance"
    print(f"🌐 URL: {url}")
    
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
    print("🚀 E*TRADE Account Key Finder")
    print("This will help you find the correct account key format")
    print()
    
    # Try to find account key
    account_key = find_account_key()
    
    if account_key:
        print(f"\n🎯 Found account key: {account_key}")
        print("💡 Update your .env file with:")
        print(f"   ETRADE_ACCOUNT_ID={account_key}")
        
        # Test the account key
        if test_account_key(account_key):
            print("\n✅ Account key is working!")
            print("🚀 You can now enable real trading!")
        else:
            print("\n❌ Account key test failed")
    else:
        print("\n❌ Could not find account key")
        print("💡 You may need to:")
        print("   1. Contact E*TRADE support")
        print("   2. Check your developer portal")
        print("   3. Ensure your account is activated for API access") 