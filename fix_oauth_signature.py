#!/usr/bin/env python3
"""
Fix OAuth Signature
Based on exact E*TRADE documentation format
"""

import os
import json
import time
import hashlib
import hmac
import base64
import urllib.parse
import requests
from dotenv import load_dotenv

load_dotenv()

class CorrectETradeOAuth:
    """Correct OAuth implementation based on E*TRADE documentation."""

    def __init__(self):
        self.consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
        self.consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
        self.account_id = os.getenv("ETRADE_ACCOUNT_ID")

        # OAuth tokens
        self.access_token = None
        self.access_token_secret = None

        print("🔐 Correct E*TRADE OAuth Implementation")
        print("=" * 60)
        print(f"✅ Using Production Credentials:")
        print(f"   Consumer Key: {self.consumer_key[:10]}...")
        print(f"   Account ID: {self.account_id}")

    def _generate_nonce(self):
        """Generate a unique nonce."""
        return base64.b64encode(os.urandom(32)).decode('utf-8')

    def _generate_timestamp(self):
        """Generate current timestamp."""
        return str(int(time.time()))

    def _create_signature(self, method, url, params, token_secret=""):
        """Create OAuth signature according to E*TRADE docs."""
        # Sort parameters alphabetically
        sorted_params = sorted(params.items())
        
        # Create parameter string for signature base (with proper encoding)
        param_string = "&".join([f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted_params])
        
        # Create signature base string
        signature_base = f"{method.upper()}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_string, safe='')}"
        
        # Create signing key
        signing_key = f"{urllib.parse.quote(self.consumer_secret, safe='')}&{urllib.parse.quote(token_secret, safe='')}"
        
        # Create signature using HMAC-SHA1
        signature = hmac.new(
            signing_key.encode('utf-8'),
            signature_base.encode('utf-8'),
            hashlib.sha1
        ).digest()
        
        return base64.b64encode(signature).decode('utf-8')

    def _create_oauth_header(self, params):
        """Create OAuth Authorization header according to E*TRADE docs."""
        # Sort parameters alphabetically as required by OAuth
        sorted_params = sorted(params.items())
        
        # Build header string exactly as shown in E*TRADE docs
        header_parts = ['OAuth realm=""']
        for key, value in sorted_params:
            if key.startswith('oauth_'):
                # Use exact format from E*TRADE documentation
                header_parts.append(f'{key}="{urllib.parse.quote(str(value), safe="")}"')
        
        return ",".join(header_parts)

    def load_tokens(self):
        """Load tokens from file."""
        try:
            with open('.etrade_tokens.json', 'r') as f:
                tokens = json.load(f)

            self.access_token = tokens.get('access_token')
            self.access_token_secret = tokens.get('access_token_secret')

            if self.access_token and self.access_token_secret:
                print("✅ Loaded existing tokens")
                return True
            else:
                print("❌ No valid tokens found")
                return False

        except FileNotFoundError:
            print("❌ No token file found")
            return False

    def make_authenticated_request(self, method, url, data=None):
        """Make an authenticated request to E*TRADE API."""
        if not self.access_token or not self.access_token_secret:
            print("❌ No access token available")
            return None

        # OAuth parameters (exactly as shown in E*TRADE docs)
        params = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': self._generate_nonce(),
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': self._generate_timestamp(),
            'oauth_token': self.access_token,
            'oauth_version': '1.0'
        }

        # Create signature
        params['oauth_signature'] = self._create_signature(method, url, params, self.access_token_secret)

        # Create Authorization header (exactly as shown in E*TRADE docs)
        auth_header = self._create_oauth_header(params)

        # Make request
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        try:
            print(f"🌐 Making authenticated request: {method} {url}")
            print(f"📋 Authorization header: {auth_header[:100]}...")

            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            print(f"📊 Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"📄 Error response: {response.text}")

            return response

        except Exception as e:
            print(f"❌ Error making authenticated request: {e}")
            return None

def test_correct_oauth():
    """Test the correct OAuth implementation."""
    print("🔍 Testing Correct OAuth Implementation")
    print("=" * 60)
    
    oauth = CorrectETradeOAuth()
    if not oauth.load_tokens():
        print("❌ No OAuth tokens found")
        return
    
    account_key = "UNRhZvwSnnF1PJCK6slVfA"
    
    # Test balance endpoint with correct OAuth
    balance_url = f"https://api.etrade.com/v1/accounts/{account_key}/balance"
    print(f"🌐 Testing balance endpoint: {balance_url}")
    print("-" * 40)
    
    response = oauth.make_authenticated_request('GET', balance_url)
    
    if response:
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Correct OAuth implementation works!")
            try:
                data = response.json()
                print(f"📄 Balance Data: {json.dumps(data, indent=2)}")
            except:
                print("📄 Response is not JSON")
        elif response.status_code == 401:
            print("❌ Still getting signature invalid")
            print("💡 Need to fix signature calculation")
        elif response.status_code == 500:
            print("❌ Back to 500 error")
            print("💡 This might be a different issue")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    else:
        print("❌ No response received")

if __name__ == "__main__":
    test_correct_oauth() 