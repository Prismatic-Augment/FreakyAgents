import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": "/Users/yluo/Documents/Code/ScAI/FR1-data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "openai",
    "deep_think_llm": "o4-mini",
    "quick_think_llm": "gpt-4o-mini",
    "backend_url": "https://api.openai.com/v1",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
    # Trading settings
    "enable_real_trading": False,  # Set to True for real trading
    "broker": "etrade",
    "sandbox_mode": True,  # Use sandbox for testing
    # Risk management settings
    "max_position_size": 1000,  # Max $ per position
    "max_daily_loss": 500,  # Max daily loss in $
    "max_portfolio_risk": 0.02,  # 2% max portfolio risk
    "default_order_size": 10,  # Default shares to trade
}
