#!/usr/bin/env python3
"""
Get E*TRADE Accounts List
Find the correct account ID format
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def get_accounts():
    """Get list of accounts from E*TRADE."""
    print("🔍 Getting E*TRADE Accounts List")
    print("=" * 60)
    
    oauth = ETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    # Try to get accounts list
    url = "https://api.etrade.com/v1/accounts"
    print(f"🌐 Getting accounts from: {url}")
    
    response = oauth.make_authenticated_request('GET', url)
    
    if response:
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Successfully retrieved accounts!")
                print(f"📄 Accounts Data: {json.dumps(data, indent=2)}")
                
                # Extract account IDs
                if 'AccountListResponse' in data:
                    accounts = data['AccountListResponse']['AccountList']['Account']
                    print(f"\n📋 Found {len(accounts)} accounts:")
                    for i, account in enumerate(accounts, 1):
                        account_id = account.get('accountId')
                        account_type = account.get('accountType')
                        print(f"   {i}. Account ID: {account_id} (Type: {account_type})")
                
            except Exception as e:
                print(f"❌ Error parsing response: {e}")
        else:
            print(f"❌ Failed to get accounts: {response.status_code}")
    else:
        print("❌ No response received")

if __name__ == "__main__":
    get_accounts() 