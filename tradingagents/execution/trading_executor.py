from typing import Dict, Any, Optional
from datetime import datetime
from tradingagents.brokers.etrade_client import ETradeClient
from tradingagents.risk.risk_manager import TradingRiskManager

class TradingExecutor:
    """Executes real trades based on agent decisions."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.risk_manager = TradingRiskManager(config)
        
        # Initialize broker only if real trading is enabled
        self.broker = None
        if config.get("enable_real_trading", False):
            self.broker = ETradeClient(sandbox=config.get("sandbox_mode", True))
    
    def execute_decision(self, decision: str, symbol: str, quantity: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute trading decision.
        
        Args:
            decision: "BUY", "SELL", or "HOLD"
            symbol: Stock symbol
            quantity: Number of shares (uses default if None)
        
        Returns:
            Dict with execution results
        """
        if decision == "HOLD":
            return {"action": "HOLD", "message": "No action taken"}
        
        if not self.broker:
            return {
                "action": decision,
                "message": "Real trading disabled - decision logged only",
                "decision": decision,
                "symbol": symbol,
                "timestamp": datetime.now().isoformat()
            }
        
        # Get current price
        current_price = self.broker.get_market_price(symbol)
        if not current_price:
            return {"error": f"Could not get price for {symbol}"}
        
        # Determine quantity
        if quantity is None:
            quantity = self.config.get("default_order_size", 10)
        
        # Validate order with risk manager
        validation = self.risk_manager.validate_order(
            symbol, quantity, current_price, decision.lower()
        )
        
        if not validation["valid"]:
            return {
                "error": f"Order rejected: {validation['reason']}",
                "decision": decision,
                "symbol": symbol,
                "timestamp": datetime.now().isoformat()
            }
        
        # Execute order
        try:
            if decision == "BUY":
                result = self.broker.place_market_order(symbol, quantity, "buy")
            elif decision == "SELL":
                result = self.broker.place_market_order(symbol, quantity, "sell")
            else:
                return {"error": f"Invalid decision: {decision}"}
            
            # Record trade for risk management
            self.risk_manager.record_trade(symbol, quantity, current_price, decision.lower())
            
            # Get risk summary
            risk_summary = self.risk_manager.get_risk_summary()
            
            return {
                "action": decision,
                "symbol": symbol,
                "quantity": quantity,
                "price": current_price,
                "order_result": result,
                "risk_summary": risk_summary,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Order execution failed: {str(e)}"}
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        if not self.broker:
            return {"error": "Broker not initialized"}
        
        return self.broker.get_account_info()
    
    def get_positions(self) -> Dict[str, Any]:
        """Get current positions."""
        if not self.broker:
            return {"error": "Broker not initialized"}
        
        return self.broker.get_positions()
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get current risk summary."""
        return self.risk_manager.get_risk_summary() 