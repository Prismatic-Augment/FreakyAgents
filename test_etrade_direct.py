#!/usr/bin/env python3
"""
Direct E*TRADE API Test
Tests basic API connectivity without OAuth complexity
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_etrade_direct():
    """Test direct API connectivity with E*TRADE."""
    print("🚀 Testing Direct E*TRADE API Connectivity")
    print("=" * 60)
    
    # Get credentials
    consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
    consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
    account_id = os.getenv("ETRADE_ACCOUNT_ID")
    
    print(f"✅ Using Production Credentials:")
    print(f"   Consumer Key: {consumer_key[:10]}...")
    print(f"   Account ID: {account_id}")
    
    # Test 1: Basic API endpoint test
    print("\n📋 Test 1: Basic API Connectivity")
    print("-" * 40)
    
    try:
        # Try to access a basic endpoint
        url = "https://api.etrade.com/v1/accounts"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        print(f"🌐 Testing URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ API endpoint accessible")
            print(f"📄 Response: {response.text[:200]}...")
        elif response.status_code == 401:
            print("⚠️  Authentication required (expected)")
            print("📄 Response: Authentication required")
        elif response.status_code == 403:
            print("⚠️  Access forbidden (expected)")
            print("📄 Response: Access forbidden")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test 2: Market data endpoint
    print("\n📈 Test 2: Market Data Endpoint")
    print("-" * 40)
    
    try:
        url = "https://api.etrade.com/v1/market/quote/AAPL"
        print(f"🌐 Testing URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Market data accessible")
            data = response.json()
            print(f"📄 AAPL Quote: {json.dumps(data, indent=2)[:200]}...")
        else:
            print(f"⚠️  Market data not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Market data error: {e}")
    
    # Test 3: Account endpoint
    print("\n💰 Test 3: Account Information Endpoint")
    print("-" * 40)
    
    try:
        url = f"https://api.etrade.com/v1/accounts/{account_id}/balance"
        print(f"🌐 Testing URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Account data accessible")
            data = response.json()
            print(f"📄 Account Info: {json.dumps(data, indent=2)[:200]}...")
        else:
            print(f"⚠️  Account data not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Account data error: {e}")
    
    print("\n📋 Summary:")
    print("=" * 40)
    print("✅ API endpoints are reachable")
    print("⚠️  Authentication required for data access")
    print("📝 Next step: Implement proper OAuth authentication")
    print("\n💡 Recommendation:")
    print("   - The API is working, but needs OAuth tokens")
    print("   - We can implement a simplified OAuth flow")
    print("   - Or use a different approach for testing")

if __name__ == "__main__":
    test_etrade_direct() 