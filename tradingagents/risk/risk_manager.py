import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class TradingRiskManager:
    """Risk management for real trading."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_position_size = config.get("max_position_size", 1000)  # Max $ per position
        self.max_daily_loss = config.get("max_daily_loss", 500)  # Max daily loss in $
        self.max_portfolio_risk = config.get("max_portfolio_risk", 0.02)  # 2% max portfolio risk
        self.daily_trades = []
        self.positions = {}
        self.portfolio_value = 10000  # Mock portfolio value
    
    def validate_order(self, symbol: str, quantity: int, price: float, side: str) -> Dict[str, Any]:
        """
        Validate if an order meets risk requirements.
        
        Returns:
            Dict with 'valid' boolean and 'reason' string
        """
        order_value = quantity * price
        
        # Check position size limit
        if order_value > self.max_position_size:
            return {
                "valid": False,
                "reason": f"Order value ${order_value:.2f} exceeds max position size ${self.max_position_size}"
            }
        
        # Check daily loss limit
        if side.lower() == "sell":
            current_loss = self._calculate_daily_loss()
            if current_loss + order_value > self.max_daily_loss:
                return {
                    "valid": False,
                    "reason": f"Order would exceed daily loss limit of ${self.max_daily_loss}"
                }
        
        # Check portfolio concentration
        if self.portfolio_value > 0:
            concentration = order_value / self.portfolio_value
            if concentration > self.max_portfolio_risk:
                return {
                    "valid": False,
                    "reason": f"Order concentration {concentration:.2%} exceeds max {self.max_portfolio_risk:.2%}"
                }
        
        # Check if we have enough buying power for buy orders
        if side.lower() == "buy":
            available_cash = self._get_available_cash()
            if order_value > available_cash:
                return {
                    "valid": False,
                    "reason": f"Order value ${order_value:.2f} exceeds available cash ${available_cash:.2f}"
                }
        
        return {"valid": True, "reason": "Order validated"}
    
    def _calculate_daily_loss(self) -> float:
        """Calculate today's realized losses."""
        today = datetime.now().date()
        today_trades = [trade for trade in self.daily_trades if trade["date"].date() == today]
        return sum(trade.get("loss", 0) for trade in today_trades)
    
    def _get_portfolio_value(self) -> float:
        """Get current portfolio value."""
        return self.portfolio_value
    
    def _get_available_cash(self) -> float:
        """Get available cash for trading."""
        # Mock implementation - in real trading, this would come from broker
        return 5000  # Mock available cash
    
    def record_trade(self, symbol: str, quantity: int, price: float, side: str):
        """Record a completed trade for risk tracking."""
        trade = {
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "side": side,
            "date": datetime.now(),
            "value": quantity * price
        }
        
        # Calculate P&L for sell orders
        if side.lower() == "sell":
            # Mock P&L calculation - in real trading, you'd track cost basis
            trade["pnl"] = quantity * (price - 100)  # Mock cost basis of $100
            trade["loss"] = max(0, -trade["pnl"])  # Only track losses
        
        self.daily_trades.append(trade)
        print(f"Trade recorded: {side.upper()} {quantity} shares of {symbol} at ${price:.2f}")
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get current risk summary."""
        daily_loss = self._calculate_daily_loss()
        total_trades_today = len([t for t in self.daily_trades if t["date"].date() == datetime.now().date()])
        
        return {
            "daily_loss": daily_loss,
            "max_daily_loss": self.max_daily_loss,
            "remaining_daily_loss": self.max_daily_loss - daily_loss,
            "total_trades_today": total_trades_today,
            "portfolio_value": self.portfolio_value,
            "available_cash": self._get_available_cash()
        }
    
    def reset_daily_limits(self):
        """Reset daily trading limits (call this daily)."""
        self.daily_trades = []
        print("Daily trading limits reset") 