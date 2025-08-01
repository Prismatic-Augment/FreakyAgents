#!/usr/bin/env python3
"""
Debug OAuth Authentication
Test OAuth step by step to identify issues
"""

import os
import json
from dotenv import load_dotenv
from etrade_oauth_proper import ETradeOAuth

load_dotenv()

def debug_oauth():
    """Debug OAuth authentication."""
    print("🔍 Debugging OAuth Authentication")
    print("=" * 60)
    
    oauth = ETradeOAuth()
    
    # Check if tokens exist
    if oauth.load_tokens():
        print("✅ Tokens loaded successfully")
        print(f"   Access Token: {oauth.access_token[:20]}..." if oauth.access_token else "   Access Token: None")
        print(f"   Token Secret: {oauth.access_token_secret[:20]}..." if oauth.access_token_secret else "   Token Secret: None")
    else:
        print("❌ No tokens found")
        return
    
    # Test OAuth signature creation
    print("\n🔐 Testing OAuth Signature Creation")
    print("-" * 40)
    
    url = "https://api.etrade.com/v1/accounts"
    
    # OAuth parameters
    params = {
        'oauth_consumer_key': oauth.consumer_key,
        'oauth_nonce': oauth._generate_nonce(),
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': oauth._generate_timestamp(),
        'oauth_token': oauth.access_token,
        'oauth_version': '1.0'
    }
    
    print(f"📋 OAuth Parameters:")
    for key, value in params.items():
        print(f"   {key}: {value}")
    
    try:
        # Create signature
        signature = oauth._create_signature('GET', url, params, oauth.access_token_secret)
        print(f"✅ Signature created: {signature}")
        
        # Create Authorization header
        auth_header = oauth._create_oauth_header(params)
        print(f"✅ Authorization header: {auth_header}")
        
    except Exception as e:
        print(f"❌ Error creating signature: {e}")
        return
    
    # Test API call with manual headers
    print("\n🌐 Testing API Call with Manual Headers")
    print("-" * 40)
    
    import requests
    
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        print(f"🌐 Making request to: {url}")
        print(f"📋 Headers: {headers}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print(f"📄 Response Text: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ API call successful!")
            try:
                data = response.json()
                print(f"📄 JSON Data: {json.dumps(data, indent=2)}")
            except:
                print("📄 Response is not JSON")
        else:
            print(f"❌ API call failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error making request: {e}")

if __name__ == "__main__":
    debug_oauth() 