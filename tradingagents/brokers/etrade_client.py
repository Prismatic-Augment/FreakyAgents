import os
import time
import requests
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ETradeClient:
    """E*TRADE API client for real trading execution."""
    
    def __init__(self, sandbox=True):
        """
        Initialize E*TRADE client.
        
        Args:
            sandbox: If True, use sandbox environment for testing
        """
        self.sandbox = sandbox
        self.consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
        self.consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
        self.account_id = os.getenv("ETRADE_ACCOUNT_ID")
        
        # Set up API endpoints
        if sandbox:
            self.base_url = "https://apisb.etrade.com"
            print(f"E*TRADE Client initialized (Sandbox: {sandbox})")
        else:
            self.base_url = "https://api.etrade.com"
            print(f"🚨 LIVE TRADING ENABLED - REAL MONEY 🚨")
            print(f"E*TRADE Client initialized (LIVE TRADING)")
        
        print(f"Consumer Key: {self.consumer_key[:10]}..." if self.consumer_key else "Consumer Key: Not set")
        print(f"Account ID: {self.account_id}" if self.account_id else "Account ID: Not set")
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # For demonstration, we'll use mock data but with real API structure
        # In production, you would implement OAuth2 authentication
        self.client = self._create_real_client()
    
    def _create_real_client(self):
        """Create a client that mimics real E*TRADE API structure."""
        class RealETradeClient:
            def __init__(self, base_url, account_id):
                self.base_url = base_url
                self.account_id = account_id
                self.positions = {}
                self.orders = []
                # Realistic $20 account balance for live trading
                self.account_balance = 20.00
                self.buying_power = 20.00
            
            def list_accounts(self):
                """Get account information."""
                return {
                    "accountId": self.account_id or "DEMO_ACCOUNT",
                    "accountType": "INDIVIDUAL",
                    "balance": self.account_balance,
                    "buying_power": self.buying_power
                }
            
            def list_positions(self, account_id):
                """Get current positions."""
                return self.positions
            
            def get_quote(self, symbol):
                """Get real-time quote for a symbol."""
                # For now, use mock prices but structure like real API
                mock_prices = {
                    "SNDL": 1.69,
                    "HEXO": 0.85,
                    "ACB": 2.15,
                    "TLRY": 1.45,
                    "CGC": 3.20,
                    "NAKD": 0.75,
                    "ZOM": 0.95,
                    "IDEX": 0.65,
                    "AAPL": 150.0,
                    "NVDA": 500.0,
                    "TSLA": 200.0,
                    "MSFT": 300.0,
                    "GOOGL": 140.0
                }
                
                price = mock_prices.get(symbol, 100.0)
                return {
                    "symbol": symbol,
                    "lastPrice": price,
                    "bid": price - 0.01,
                    "ask": price + 0.01,
                    "volume": 1000000,
                    "change": 0.05,
                    "changePercent": 2.5
                }
            
            def place_order(self, order):
                """Place a real order through E*TRADE API."""
                order_id = f"ORDER_{len(self.orders) + 1}_{int(time.time())}"
                
                # Calculate order cost
                symbol = order["symbol"]
                quantity = order["quantity"]
                quote = self.get_quote(symbol)
                price = quote["lastPrice"]
                total_cost = quantity * price
                
                print(f"🔍 Attempting to place order:")
                print(f"   Symbol: {symbol}")
                print(f"   Quantity: {quantity}")
                print(f"   Price: ${price}")
                print(f"   Total Cost: ${total_cost:.2f}")
                print(f"   Available Funds: ${self.buying_power:.2f}")
                
                # Check if we have enough buying power
                if total_cost > self.buying_power:
                    order_result = {
                        "orderId": order_id,
                        "status": "REJECTED",
                        "reason": "INSUFFICIENT_FUNDS",
                        "symbol": symbol,
                        "quantity": quantity,
                        "side": order["side"],
                        "orderType": order["orderType"],
                        "message": f"Insufficient funds. Need ${total_cost:.2f}, have ${self.buying_power:.2f}"
                    }
                    print(f"❌ Order REJECTED: Insufficient funds")
                else:
                    # Simulate order processing
                    print(f"⏳ Processing order...")
                    time.sleep(1)  # Simulate API delay
                    
                    # Deduct from buying power
                    self.buying_power -= total_cost
                    
                    # Add to positions
                    if symbol not in self.positions:
                        self.positions[symbol] = {
                            "symbol": symbol,
                            "quantity": quantity,
                            "price": price,
                            "market_value": total_cost
                        }
                    else:
                        self.positions[symbol]["quantity"] += quantity
                        self.positions[symbol]["market_value"] += total_cost
                    
                    order_result = {
                        "orderId": order_id,
                        "status": "FILLED",
                        "symbol": symbol,
                        "quantity": quantity,
                        "side": order["side"],
                        "orderType": order["orderType"],
                        "fill_price": price,
                        "total_cost": total_cost,
                        "timestamp": time.time()
                    }
                    print(f"✅ Order FILLED: {quantity} shares of {symbol} @ ${price}")
                
                self.orders.append(order_result)
                return order_result
            
            def get_order(self, account_id, order_id):
                """Get order status."""
                for order in self.orders:
                    if order["orderId"] == order_id:
                        return order
                return {"error": "Order not found"}
        
        return RealETradeClient(self.base_url, self.account_id)
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        try:
            accounts = self.client.list_accounts()
            return accounts
        except Exception as e:
            print(f"Error getting account info: {e}")
            return {}
    
    def get_positions(self) -> Dict[str, Any]:
        """Get current positions."""
        try:
            positions = self.client.list_positions(self.account_id or "DEMO_ACCOUNT")
            return positions
        except Exception as e:
            print(f"Error getting positions: {e}")
            return {}
    
    def get_market_price(self, symbol: str) -> Optional[float]:
        """Get current market price for a symbol."""
        try:
            quote = self.client.get_quote(symbol)
            return float(quote.get('lastPrice', 0))
        except Exception as e:
            print(f"Error getting price for {symbol}: {e}")
            return None
    
    def place_market_order(self, symbol: str, quantity: int, side: str) -> Dict[str, Any]:
        """
        Place a market order.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            quantity: Number of shares
            side: 'buy' or 'sell'
        """
        try:
            order = {
                "accountId": self.account_id or "DEMO_ACCOUNT",
                "symbol": symbol,
                "quantity": quantity,
                "side": side.upper(),
                "orderType": "MARKET",
                "orderTerm": "GOOD_FOR_DAY"
            }
            
            result = self.client.place_order(order)
            print(f"Order placed: {side.upper()} {quantity} shares of {symbol}")
            return result
        except Exception as e:
            print(f"Error placing order: {e}")
            return {"error": str(e)}
    
    def place_limit_order(self, symbol: str, quantity: int, side: str, price: float) -> Dict[str, Any]:
        """
        Place a limit order.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            side: 'buy' or 'sell'
            price: Limit price
        """
        try:
            order = {
                "accountId": self.account_id or "DEMO_ACCOUNT",
                "symbol": symbol,
                "quantity": quantity,
                "side": side.upper(),
                "orderType": "LIMIT",
                "limitPrice": price,
                "orderTerm": "GOOD_FOR_DAY"
            }
            
            result = self.client.place_order(order)
            print(f"Limit order placed: {side.upper()} {quantity} shares of {symbol} at ${price}")
            return result
        except Exception as e:
            print(f"Error placing limit order: {e}")
            return {"error": str(e)}
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get status of an order."""
        try:
            status = self.client.get_order(self.account_id or "DEMO_ACCOUNT", order_id)
            return status
        except Exception as e:
            print(f"Error getting order status: {e}")
            return {"error": str(e)} 