# TradingAgents E*TRADE Integration

This document explains how to use TradingAgents with E*TRADE for real trading.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in your project root:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# E*TRADE API Credentials
ETRADE_CONSUMER_KEY=your_etrade_consumer_key_here
ETRADE_CONSUMER_SECRET=your_etrade_consumer_secret_here
ETRADE_ACCOUNT_ID=your_etrade_account_id_here

# Optional: FinnHub API Key
FINNHUB_API_KEY=your_finnhub_api_key_here
```

### 3. Test the Integration

```bash
python test_etrade_integration.py
```

### 4. Run with Real Trading

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Enable real trading
config = DEFAULT_CONFIG.copy()
config["enable_real_trading"] = True
config["sandbox_mode"] = False  # Use real trading
config["default_order_size"] = 10

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("AAPL", "2024-01-15")
print(f"Decision: {decision}")
```

## 🔧 Configuration Options

### Trading Settings

```python
config = {
    "enable_real_trading": True,      # Enable/disable real trading
    "sandbox_mode": True,             # Use sandbox for testing
    "default_order_size": 10,         # Default shares per trade
    "max_position_size": 1000,        # Max $ per position
    "max_daily_loss": 500,            # Max daily loss in $
    "max_portfolio_risk": 0.02,       # 2% max portfolio risk
}
```

### Risk Management

The system includes comprehensive risk management:

- **Position Size Limits**: Maximum dollar amount per trade
- **Daily Loss Limits**: Maximum daily loss protection
- **Portfolio Concentration**: Maximum percentage of portfolio per position
- **Available Cash Validation**: Ensures sufficient buying power

## 📊 Features

### 1. Real Trading Execution

```python
# Execute trades based on agent decisions
execution_result = ta.trading_executor.execute_decision(
    decision="BUY",
    symbol="AAPL",
    quantity=10
)
```

### 2. Account Information

```python
# Get account details
account_info = ta.get_account_info()
positions = ta.get_positions()
```

### 3. Risk Monitoring

```python
# Get current risk summary
risk_summary = ta.get_risk_summary()
print(f"Daily Loss: ${risk_summary['daily_loss']}")
print(f"Remaining Daily Loss: ${risk_summary['remaining_daily_loss']}")
```

### 4. Paper Trading Mode

```python
# Test without real money
config["enable_real_trading"] = False
ta = TradingAgentsGraph(config=config)
_, decision = ta.propagate("NVDA", "2024-01-15")
# Decision logged but no real orders placed
```

## 🛡️ Safety Features

### Risk Controls

1. **Position Size Limits**: Prevents oversized trades
2. **Daily Loss Limits**: Stops trading if daily loss exceeded
3. **Portfolio Concentration**: Limits exposure to single positions
4. **Cash Validation**: Ensures sufficient funds before buying

### Sandbox Testing

Always test with sandbox mode first:

```python
config["sandbox_mode"] = True  # Use E*TRADE sandbox
config["enable_real_trading"] = True
```

## 📈 Usage Examples

### Example 1: Conservative Trading

```python
config = DEFAULT_CONFIG.copy()
config["enable_real_trading"] = True
config["sandbox_mode"] = True
config["default_order_size"] = 5
config["max_position_size"] = 500
config["max_daily_loss"] = 200

ta = TradingAgentsGraph(config=config)
_, decision = ta.propagate("AAPL", "2024-01-15")
```

### Example 2: Aggressive Trading

```python
config = DEFAULT_CONFIG.copy()
config["enable_real_trading"] = True
config["sandbox_mode"] = False  # Real trading
config["default_order_size"] = 50
config["max_position_size"] = 5000
config["max_daily_loss"] = 1000

ta = TradingAgentsGraph(config=config)
_, decision = ta.propagate("NVDA", "2024-01-15")
```

### Example 3: Portfolio Monitoring

```python
# Monitor your positions and risk
ta = TradingAgentsGraph(config=config)

# Get current status
account_info = ta.get_account_info()
positions = ta.get_positions()
risk_summary = ta.get_risk_summary()

print(f"Account Balance: ${account_info.get('balance', 0)}")
print(f"Daily Loss: ${risk_summary['daily_loss']}")
print(f"Positions: {len(positions)}")
```

## ⚠️ Important Notes

### 1. E*TRADE Developer Account

You need to:
1. Register at https://developer.etrade.com/
2. Apply for API access
3. Get your Consumer Key and Secret
4. Link your E*TRADE brokerage account

### 2. Risk Management

- Start with small position sizes
- Use sandbox mode for testing
- Monitor daily loss limits
- Set conservative risk parameters

### 3. Regulatory Compliance

- Ensure compliance with FINRA/SEC regulations
- Be aware of pattern day trader rules
- Follow best execution requirements

### 4. Testing Strategy

1. **Paper Trading**: Test with `enable_real_trading = False`
2. **Sandbox Testing**: Use E*TRADE sandbox environment
3. **Small Orders**: Start with minimal position sizes
4. **Monitor Closely**: Watch all trades during initial deployment

## 🔍 Troubleshooting

### Common Issues

1. **"Consumer Key Not Set"**
   - Check your `.env` file
   - Ensure E*TRADE credentials are correct

2. **"Order Rejected"**
   - Check risk management limits
   - Verify sufficient buying power
   - Review daily loss limits

3. **"Broker Not Initialized"**
   - Ensure `enable_real_trading = True`
   - Check E*TRADE credentials

### Debug Mode

Enable debug mode for detailed logging:

```python
ta = TradingAgentsGraph(debug=True, config=config)
```

## 📞 Support

For issues with:
- **TradingAgents**: Check the main README
- **E*TRADE API**: Contact E*TRADE Developer Support
- **Risk Management**: Review configuration settings

## 🎯 Next Steps

1. **Set up E*TRADE Developer Account**
2. **Update credentials in `.env`**
3. **Test with sandbox mode**
4. **Start with small position sizes**
5. **Monitor performance closely**
6. **Adjust risk parameters as needed**

Remember: **This is for research purposes only. Trading involves risk of loss.** 