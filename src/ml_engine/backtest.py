import pandas as pd
import numpy as np

def run_backtest(df: pd.DataFrame, initial_capital=10000):
    """
    Simulates a trading strategy on historical data.
    Strategy: Golden Cross (SMA 50 > SMA 200 = BUY, else SELL/CASH).
    """
    # Work on a copy to avoid SettingWithCopy warnings
    df = df.copy()
    
    # 1. Ensure we have the necessary columns
    if 'sma_50' not in df.columns or 'sma_200' not in df.columns:
        return {"error": "Missing SMA data for backtest"}
    
    # 2. Generate Signals (1 = Hold Stock, 0 = Hold Cash)
    # If SMA 50 > SMA 200, we stay in the market. Otherwise, we sit in cash.
    df['Signal'] = 0
    df.loc[df['sma_50'] > df['sma_200'], 'Signal'] = 1
    
    # Shift signal by 1 day because we trade based on yesterday's close
    df['Position'] = df['Signal'].shift(1)
    
    # 3. Calculate Daily Returns
    df['Market_Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Market_Return'] * df['Position']
    
    # 4. Calculate Cumulative Equity
    # We start with $10,000
    df['Market_Equity'] = initial_capital * (1 + df['Market_Return']).cumprod()
    df['Strategy_Equity'] = initial_capital * (1 + df['Strategy_Return']).cumprod()
    
    # Clean up NaN values at the start
    df.dropna(subset=['Market_Equity', 'Strategy_Equity'], inplace=True)
    
    # 5. Compute Final Metrics
    if df.empty:
        return {"error": "Not enough data for backtest"}

    final_market = df['Market_Equity'].iloc[-1]
    final_strategy = df['Strategy_Equity'].iloc[-1]
    
    market_perf = (final_market - initial_capital) / initial_capital * 100
    strategy_perf = (final_strategy - initial_capital) / initial_capital * 100
    
    return {
        "initial_capital": initial_capital,
        "final_market_equity": round(final_market, 2),
        "final_strategy_equity": round(final_strategy, 2),
        "market_return_pct": round(market_perf, 2),
        "strategy_return_pct": round(strategy_perf, 2),
        "comparison_data": {
            "dates": df.index.astype(str).tolist(),
            "market_curve": df['Market_Equity'].tolist(),
            "strategy_curve": df['Strategy_Equity'].tolist()
        }
    }