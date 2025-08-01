from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# ⚠️ LIVE TRADING WARNING ⚠️
print("🚨 WARNING: LIVE TRADING ENABLED 🚨")
print("This will trade with REAL MONEY in your E*TRADE account!")
print("Your $20 account will be used for actual trades.")
print("Press Ctrl+C to cancel, or any key to continue...")
input()

# Create a custom config for $20 account trading
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"  # Use OpenAI for better results
config["backend_url"] = "https://api.openai.com/v1"
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 1
config["online_tools"] = True

# Trading settings
config["enable_real_trading"] = True  # ENABLE REAL TRADING
config["broker"] = "etrade"
config["sandbox_mode"] = False  # LIVE TRADING - NO SANDBOX
config["max_position_size"] = 20
config["max_daily_loss"] = 10
config["max_portfolio_risk"] = 0.5
config["default_order_size"] = 1

print("💰 LIVE TRADING CONFIGURATION:")
print(f"   - Real Trading: ENABLED")
print(f"   - Sandbox Mode: DISABLED")
print(f"   - Account: $20")
print(f"   - Max Position Size: $20")
print(f"   - Max Daily Loss: $10")
print(f"   - Default Order Size: 1 share")

# Initialize with E*TRADE integration
ta = TradingAgentsGraph(debug=True, config=config)

# Check your account status
print("\n💰 Account Status:")
account_info = ta.get_account_info()
print(f"   Balance: ${account_info.get('balance', 0)}")
print(f"   Buying Power: ${account_info.get('buying_power', 0)}")

# Check risk summary
risk_summary = ta.get_risk_summary()
print(f"   Daily Loss: ${risk_summary.get('daily_loss', 0)}")
print(f"   Remaining Daily Loss: ${risk_summary.get('remaining_daily_loss', 0)}")

# Penny stocks under $20 for $20 account
penny_stocks = [
    "SNDL",    # Sundial Growers (~$2)
    "HEXO",    # HEXO Corp (~$1)
    "ACB",     # Aurora Cannabis (~$3)
    "TLRY",    # Tilray (~$2)
    "CGC",     # Canopy Growth (~$4)
    "NAKD",    # Naked Brand (~$1)
    "ZOM",     # Zomedica (~$1)
    "IDEX",    # Ideanomics (~$1)
]

print(f"\n📈 Penny Stocks to Analyze:")
for stock in penny_stocks:
    print(f"   - {stock}")

# Analyze first penny stock
print(f"\n🔍 Analyzing {penny_stocks[0]}...")
_, decision = ta.propagate(penny_stocks[0], "2024-01-15")
print(f"Decision: {decision}")

# Check positions after trade
print("\n📊 Current Positions:")
positions = ta.get_positions()
if positions:
    for position in positions:
        print(f"   {position['symbol']}: {position['quantity']} shares @ ${position['price']}")
else:
    print("   No positions")

print("\n✅ LIVE TRADING COMPLETE!")
print("\n📋 Next Steps:")
print("1. Check your E*TRADE account for executed trades")
print("2. Monitor your $20 account balance")
print("3. Review trade performance")
print("4. Run again to analyze more penny stocks")
print("5. Set up daily trading schedule if desired")
