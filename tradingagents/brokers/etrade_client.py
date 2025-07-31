import os
import time
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
        
        # For now, we'll create a mock client for demonstration
        # In production, you would use the actual E*TRADE SDK
        self.client = self._create_mock_client()
        
        print(f"E*TRADE Client initialized (Sandbox: {sandbox})")
        print(f"Consumer Key: {self.consumer_key[:10]}..." if self.consumer_key else "Consumer Key: Not set")
        print(f"Account ID: {self.account_id}" if self.account_id else "Account ID: Not set")
    
    def _create_mock_client(self):
        """Create a mock client for demonstration purposes."""
        class MockETradeClient:
            def __init__(self):
                self.positions = {}
                self.orders = []
                self.account_balance = 10000  # Mock balance
            
            def list_accounts(self):
                return {
                    "accountId": self.account_id or "DEMO_ACCOUNT",
                    "accountType": "INDIVIDUAL",
                    "balance": self.account_balance
                }
            
            def list_positions(self, account_id):
                return self.positions
            
            def get_quote(self, symbol):
                # Mock price data
                mock_prices = {
                    "AAPL": 150.0,
                    "NVDA": 500.0,
                    "TSLA": 200.0,
                    "MSFT": 300.0,
                    "GOOGL": 140.0
                }
                return {
                    "symbol": symbol,
                    "lastPrice": mock_prices.get(symbol, 100.0),
                    "bid": mock_prices.get(symbol, 100.0) - 0.1,
                    "ask": mock_prices.get(symbol, 100.0) + 0.1
                }
            
            def place_order(self, order):
                order_id = f"ORDER_{len(self.orders) + 1}"
                order_result = {
                    "orderId": order_id,
                    "status": "SUBMITTED",
                    "symbol": order["symbol"],
                    "quantity": order["quantity"],
                    "side": order["side"],
                    "orderType": order["orderType"]
                }
                self.orders.append(order_result)
                return order_result
            
            def get_order(self, account_id, order_id):
                for order in self.orders:
                    if order["orderId"] == order_id:
                        return order
                return {"error": "Order not found"}
        
        return MockETradeClient()
    
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