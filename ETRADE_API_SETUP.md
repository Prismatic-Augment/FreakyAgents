# E*TRADE API Setup Guide

This guide will help you connect your trading system to the real E*TRADE API for actual trading.

## 🚨 **IMPORTANT WARNING**

**This will enable REAL MONEY TRADING with your actual E*TRADE account.**
- ⚠️ **Real Money**: Orders will use your actual funds
- ⚠️ **No Refunds**: Trading losses are permanent
- ⚠️ **Risk**: Only trade what you can afford to lose
- ⚠️ **Testing**: Start with sandbox mode first

## 📋 **Prerequisites**

1. **E*TRADE Account**: Active brokerage account
2. **Developer Account**: E*TRADE Developer Portal access
3. **API Keys**: Consumer Key and Consumer Secret
4. **Account ID**: Your E*TRADE account number

## 🔧 **Step 1: E*TRADE Developer Portal Setup**

### 1.1 Register for Developer Access
1. Go to: https://developer.etrade.com/
2. Click "Get Started" or "Sign Up"
3. Create a developer account
4. Verify your email address

### 1.2 Create Application
1. Log into Developer Portal
2. Click "My Apps" → "Create New App"
3. Fill in application details:
   - **App Name**: "TradingAgents"
   - **Description**: "AI-powered trading system"
   - **Callback URL**: `http://localhost:8080/callback`
   - **Environment**: Production (for live trading)

### 1.3 Get API Credentials
1. After app creation, you'll get:
   - **Consumer Key**: Your API key
   - **Consumer Secret**: Your API secret
2. Save these securely

## 🔐 **Step 2: OAuth2 Authentication Setup**

### 2.1 Install Required Packages
```bash
pip install requests-oauthlib
```

### 2.2 Update Environment Variables
Add to your `.env` file:
```env
ETRADE_CONSUMER_KEY=your_consumer_key_here
ETRADE_CONSUMER_SECRET=your_consumer_secret_here
ETRADE_ACCOUNT_ID=your_account_id_here
ETRADE_CALLBACK_URL=http://localhost:8080/callback
```

## 🧪 **Step 3: Test Sandbox Mode**

### 3.1 Test API Connection
```bash
python3 test_real_etrade.py
```

### 3.2 Verify Account Access
- Check account balance
- Verify positions
- Test market data
- Confirm order placement

## 🚀 **Step 4: Enable Live Trading**

### 4.1 Update Configuration
In `main.py`, change:
```python
config["sandbox_mode"] = False  # Enable live trading
```

### 4.2 Test Small Order
```bash
python3 test_live_trading.py
```

## 📊 **Step 5: Monitor Trading**

### 5.1 Check E*TRADE Account
- Log into your E*TRADE account
- Go to "Orders" section
- Verify orders are being placed
- Monitor account balance

### 5.2 Review Trading Activity
- Check order history
- Monitor positions
- Review trade performance
- Track account balance

## ⚠️ **Safety Measures**

### Risk Management
1. **Start Small**: Begin with $1-5 orders
2. **Set Limits**: Use stop-loss orders
3. **Monitor Closely**: Check account regularly
4. **Test First**: Use sandbox mode initially

### Account Protection
1. **Daily Limits**: Set maximum daily loss
2. **Position Limits**: Limit per-trade size
3. **Stop Loss**: Automatic loss protection
4. **Emergency Stop**: Ability to halt trading

## 🔍 **Troubleshooting**

### Common Issues

#### 1. Authentication Failed
**Problem**: "Authentication failed" error
**Solution**: 
- Verify API credentials
- Check account permissions
- Ensure developer account is active

#### 2. Order Rejected
**Problem**: Orders being rejected
**Solution**:
- Check account balance
- Verify symbol is tradeable
- Ensure market hours
- Check account restrictions

#### 3. API Rate Limits
**Problem**: "Rate limit exceeded" error
**Solution**:
- Reduce API call frequency
- Implement request throttling
- Use batch requests when possible

### Error Codes

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 401 | Unauthorized | Check API credentials |
| 403 | Forbidden | Verify account permissions |
| 404 | Not Found | Check account ID |
| 429 | Rate Limited | Reduce request frequency |
| 500 | Server Error | Try again later |

## 📞 **Support Resources**

### E*TRADE Support
- **Developer Portal**: https://developer.etrade.com/
- **API Documentation**: https://developer.etrade.com/apis
- **Support Email**: developer-support@etrade.com

### Trading System Support
- **GitHub Issues**: Report bugs and issues
- **Documentation**: Check README files
- **Community**: Join trading forums

## 🎯 **Next Steps**

### After Setup
1. **Test Thoroughly**: Use sandbox mode extensively
2. **Start Small**: Begin with minimal position sizes
3. **Monitor Performance**: Track trading results
4. **Adjust Strategy**: Refine based on results

### Advanced Features
1. **Automated Trading**: Set up daily trading
2. **Risk Management**: Implement stop-loss orders
3. **Portfolio Tracking**: Monitor overall performance
4. **Performance Analytics**: Analyze trading results

## ⚖️ **Legal and Compliance**

### Important Disclaimers
- **Not Financial Advice**: This is for educational purposes
- **Risk of Loss**: Trading involves substantial risk
- **No Guarantees**: Past performance doesn't guarantee future results
- **Regulatory Compliance**: Follow all applicable laws

### Regulatory Requirements
- **Pattern Day Trader**: Be aware of PDT rules
- **Margin Requirements**: Understand margin trading rules
- **Tax Implications**: Consult with tax professional
- **Brokerage Rules**: Follow E*TRADE terms of service

## ✅ **Checklist**

- [ ] E*TRADE Developer account created
- [ ] API credentials obtained
- [ ] Environment variables configured
- [ ] Sandbox mode tested
- [ ] Account permissions verified
- [ ] Risk management configured
- [ ] Small test order placed
- [ ] Live trading enabled
- [ ] Monitoring system active

## 🚨 **Final Warning**

**Before enabling live trading:**
1. ✅ Test thoroughly in sandbox mode
2. ✅ Start with very small amounts
3. ✅ Monitor all trades closely
4. ✅ Have emergency stop procedures
5. ✅ Understand all risks involved

**Remember: This is REAL MONEY trading with actual financial risk!** 