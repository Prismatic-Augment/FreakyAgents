#!/usr/bin/env python3
"""
E*TRADE OAuth2 Setup Script
Helps set up proper OAuth2 authentication for E*TRADE API
"""

import os
import webbrowser
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv()

def setup_etrade_oauth():
    """Set up OAuth2 authentication with E*TRADE."""
    print("🔐 Setting up E*TRADE OAuth2 Authentication")
    print("=" * 60)
    
    # Get credentials from environment
    consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
    consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
    
    if not consumer_key or not consumer_secret:
        print("❌ Error: E*TRADE credentials not found in .env file")
        return None
    
    print(f"✅ Found E*TRADE credentials")
    print(f"   Consumer Key: {consumer_key[:10]}...")
    
    # Create OAuth1 session (E*TRADE uses OAuth1)
    # Use 'oob' (out-of-band) callback as E*TRADE expects
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        callback_uri="oob"  # Out-of-band callback
    )
    
    # Step 1: Get request token
    print("\n📋 Step 1: Getting request token...")
    try:
        request_token_url = "https://api.etrade.com/oauth/request_token"
        response = oauth.fetch_request_token(request_token_url)
        
        oauth_token = response.get('oauth_token')
        oauth_token_secret = response.get('oauth_token_secret')
        
        print(f"✅ Request token obtained")
        print(f"   Token: {oauth_token}")
        
    except Exception as e:
        print(f"❌ Failed to get request token: {e}")
        return None
    
    # Step 2: Get authorization URL
    print("\n🔗 Step 2: Getting authorization URL...")
    try:
        auth_url = "https://us.etrade.com/e/t/etws/authorize"
        authorization_url = oauth.authorization_url(auth_url, oauth_token=oauth_token)
        
        print(f"✅ Authorization URL created")
        print(f"   URL: {authorization_url}")
        
    except Exception as e:
        print(f"❌ Failed to create authorization URL: {e}")
        return None
    
    # Step 3: Open browser for user authorization
    print("\n🌐 Step 3: Opening browser for authorization...")
    print("Please authorize the application in your browser.")
    print("After authorization, you'll get a verification code.")
    print("Copy that code and paste it here.")
    
    try:
        webbrowser.open(authorization_url)
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"Please manually visit: {authorization_url}")
    
    # Step 4: Get verification code from user
    print("\n📝 Step 4: Enter verification code...")
    print("After authorizing in your browser, you'll see a verification code.")
    print("Please copy and paste that code here:")
    
    oauth_verifier = input("Verification code: ").strip()
    
    if not oauth_verifier:
        print("❌ No verification code provided")
        return None
    
    # Step 5: Get access token
    print("\n🎯 Step 5: Getting access token...")
    try:
        access_token_url = "https://api.etrade.com/oauth/access_token"
        oauth_response = oauth.fetch_access_token(
            access_token_url,
            verifier=oauth_verifier
        )
        
        access_token = oauth_response.get('oauth_token')
        access_token_secret = oauth_response.get('oauth_token_secret')
        
        print("✅ Access token obtained successfully!")
        print(f"   Access Token: {access_token}")
        print(f"   Token Secret: {access_token_secret}")
        
        # Save tokens to file
        tokens = {
            'access_token': access_token,
            'access_token_secret': access_token_secret,
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret
        }
        
        with open('.etrade_tokens.json', 'w') as f:
            import json
            json.dump(tokens, f)
        
        print("💾 Tokens saved to .etrade_tokens.json")
        return oauth
        
    except Exception as e:
        print(f"❌ Failed to get access token: {e}")
        return None

if __name__ == "__main__":
    print("🚀 E*TRADE OAuth2 Setup")
    print("This script will help you authenticate with E*TRADE API")
    print("Make sure you have your E*TRADE credentials in .env file")
    print()
    
    oauth = setup_etrade_oauth()
    
    if oauth:
        print("\n🎉 OAuth2 setup completed successfully!")
        print("You can now use the E*TRADE API for real trading.")
    else:
        print("\n❌ OAuth2 setup failed.")
        print("Please check your credentials and try again.") 