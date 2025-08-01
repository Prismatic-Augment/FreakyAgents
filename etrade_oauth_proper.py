#!/usr/bin/env python3
"""
Proper E*TRADE OAuth Implementation
Based on official E*TRADE API documentation
"""

import os
import time
import hashlib
import hmac
import base64
import urllib.parse
import requests
from dotenv import load_dotenv

load_dotenv()

class ETradeOAuth:
    """Proper OAuth implementation for E*TRADE API."""
    
    def __init__(self):
        self.consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
        self.consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
        self.account_id = os.getenv("ETRADE_ACCOUNT_ID")
        
        # OAuth tokens
        self.request_token = None
        self.request_token_secret = None
        self.access_token = None
        self.access_token_secret = None
        
        print("🔐 E*TRADE OAuth Implementation")
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
    
    def _create_signature(self, method, url, params, token_secret=""):
        """Create OAuth signature according to E*TRADE specs."""
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
    
    def get_request_token(self):
        """Step 1: Get request token from E*TRADE."""
        print("\n📋 Step 1: Getting Request Token")
        print("-" * 40)
        
        url = "https://api.etrade.com/oauth/request_token"
        
        # OAuth parameters (exactly as shown in E*TRADE docs)
        params = {
            'oauth_callback': 'oob',
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': self._generate_nonce(),
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': self._generate_timestamp(),
            'oauth_version': '1.0'
        }
        
        # Create signature
        params['oauth_signature'] = self._create_signature('GET', url, params)
        
        # Create Authorization header (exactly as shown in E*TRADE docs)
        auth_header = self._create_oauth_header(params)
        
        # Make request
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            print(f"🌐 Requesting token from: {url}")
            print(f"📋 Authorization header: {auth_header}")
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
            if response.status_code == 200:
                # Parse response - handle both form-encoded and JSON responses
                response_text = response.text.strip()
                
                if response_text:
                    # Try to parse as form-encoded first
                    try:
                        response_params = dict(urllib.parse.parse_qsl(response_text))
                        self.request_token = response_params.get('oauth_token')
                        self.request_token_secret = response_params.get('oauth_token_secret')
                    except:
                        # If that fails, try JSON
                        try:
                            response_data = response.json()
                            self.request_token = response_data.get('oauth_token')
                            self.request_token_secret = response_data.get('oauth_token_secret')
                        except:
                            print("⚠️  Could not parse response format")
                            return False
                else:
                    print("⚠️  Empty response received")
                    return False
                
                if self.request_token and self.request_token_secret:
                    print("✅ Request token obtained successfully!")
                    print(f"   Token: {self.request_token}")
                    print(f"   Token Secret: {self.request_token_secret}")
                    
                    return True
                else:
                    print("❌ Request tokens not found in response")
                    print("📄 Full response: " + response_text)
                    return False
            else:
                print(f"❌ Failed to get request token: {response.status_code}")
                print(f"📄 Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error getting request token: {e}")
            return False
    
    def get_authorization_url(self):
        """Step 2: Get authorization URL."""
        print("\n🔗 Step 2: Getting Authorization URL")
        print("-" * 40)
        
        if not self.request_token:
            print("❌ No request token available")
            return None
        
        # Create authorization URL
        auth_url = f"https://us.etrade.com/e/t/etws/authorize?key={self.consumer_key}&token={urllib.parse.quote(self.request_token)}"
        
        print("✅ Authorization URL created:")
        print(f"   URL: {auth_url}")
        
        return auth_url
    
    def get_access_token(self, verifier):
        """Step 3: Exchange request token for access token."""
        print("\n🎯 Step 3: Getting Access Token")
        print("-" * 40)
        
        if not self.request_token or not self.request_token_secret:
            print("❌ No request token available")
            return False
        
        url = "https://api.etrade.com/oauth/access_token"
        
        # OAuth parameters
        params = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': self._generate_nonce(),
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': self._generate_timestamp(),
            'oauth_token': self.request_token,
            'oauth_verifier': verifier,
            'oauth_version': '1.0'
        }
        
        # Create signature
        params['oauth_signature'] = self._create_signature('GET', url, params, self.request_token_secret)
        
        # Create Authorization header
        auth_header = self._create_oauth_header(params)
        
        # Make request
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            print(f"🌐 Requesting access token from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
            if response.status_code == 200:
                # Parse response - handle both form-encoded and JSON responses
                response_text = response.text.strip()
                
                if response_text:
                    # Try to parse as form-encoded first
                    try:
                        response_params = dict(urllib.parse.parse_qsl(response_text))
                        self.access_token = response_params.get('oauth_token')
                        self.access_token_secret = response_params.get('oauth_token_secret')
                    except:
                        # If that fails, try JSON
                        try:
                            response_data = response.json()
                            self.access_token = response_data.get('oauth_token')
                            self.access_token_secret = response_data.get('oauth_token_secret')
                        except:
                            print("⚠️  Could not parse response format")
                            return False
                else:
                    print("⚠️  Empty response received")
                    return False
                
                if self.access_token and self.access_token_secret:
                    print("✅ Access token obtained successfully!")
                    print(f"   Access Token: {self.access_token}")
                    print(f"   Token Secret: {self.access_token_secret}")
                    
                    # Save tokens to file
                    self.save_tokens()
                    
                    return True
                else:
                    print("❌ Access tokens not found in response")
                    print("📄 Full response: " + response_text)
                    return False
            else:
                print(f"❌ Failed to get access token: {response.status_code}")
                print(f"📄 Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error getting access token: {e}")
            return False
    
    def save_tokens(self):
        """Save tokens to file for future use."""
        tokens = {
            'access_token': self.access_token,
            'access_token_secret': self.access_token_secret,
            'consumer_key': self.consumer_key,
            'consumer_secret': self.consumer_secret,
            'timestamp': time.time()
        }
        
        with open('.etrade_tokens.json', 'w') as f:
            import json
            json.dump(tokens, f)
        
        print("💾 Tokens saved to .etrade_tokens.json")
    
    def load_tokens(self):
        """Load tokens from file."""
        try:
            with open('.etrade_tokens.json', 'r') as f:
                import json
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

def main():
    """Main OAuth flow."""
    print("🚀 E*TRADE OAuth Setup")
    print("This will properly authenticate with E*TRADE API")
    print()
    
    oauth = ETradeOAuth()
    
    # Try to load existing tokens first
    if oauth.load_tokens():
        print("✅ Using existing tokens")
        return oauth
    
    # Step 1: Get request token
    if not oauth.get_request_token():
        print("❌ Failed to get request token")
        return None
    
    # Step 2: Get authorization URL
    auth_url = oauth.get_authorization_url()
    if not auth_url:
        print("❌ Failed to create authorization URL")
        return None
    
    # Step 3: User authorization
    print("\n🌐 Step 3: User Authorization")
    print("-" * 40)
    print("Please visit this URL in your browser:")
    print(f"   {auth_url}")
    print("\nAfter authorizing, you'll get a verification code.")
    print("Please copy and paste that code here:")
    
    verifier = input("Verification code: ").strip()
    
    if not verifier:
        print("❌ No verification code provided")
        return None
    
    # Step 4: Get access token
    if oauth.get_access_token(verifier):
        print("\n🎉 OAuth setup completed successfully!")
        print("You can now make authenticated API calls.")
        return oauth
    else:
        print("\n❌ OAuth setup failed.")
        return None

if __name__ == "__main__":
    oauth = main() 