#!/usr/bin/env python3
"""
Get E*TRADE Account List
Find the correct account key format by listing all accounts
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def get_account_list():
    """Get the list of accounts from E*TRADE."""
    print("🔍 Getting E*TRADE Account List")
    print("=" * 60)
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    # Try to get the account list
    url = "https://api.etrade.com/v1/accounts"
    print(f"🌐 Getting accounts from: {url}")
    
    response = oauth.make_authenticated_request('GET', url)
    
    if response:
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Account list retrieved successfully!")
                print(f"📄 Account Data: {json.dumps(data, indent=2)}")
                
                # Look for account keys
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
                
                return data
            except Exception as e:
                print(f"❌ Error parsing response: {e}")
                return None
        else:
            print(f"❌ Failed to get account list: {response.status_code}")
            return None
    else:
        print("❌ No response received")
        return None

if __name__ == "__main__":
    get_account_list() 