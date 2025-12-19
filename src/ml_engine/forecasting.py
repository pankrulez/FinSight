import yfinance as yf
import pandas as pd
import joblib
from src.config import logger
from src.config import MODEL_PATH
from src.ml_engine.features import add_technical_indicators, interpret_signals
from src.data_engine.database import get_stock_data # <--- Reads from your SQL DB

def get_technical_analysis(ticker: str, period="1y"):
    """
    Fetches data (DB first, then Live), runs indicators, ML inference, 
    and prepares data for the Dashboard charts.
    """
    print(f"📊 Running Technical Analysis for {ticker}...")

    # 1. Fetch Data (Hybrid Strategy: Cache-First)
    # Try reading from the local database first (Fast)
    df = get_stock_data(ticker)
    
    # If DB is empty or missing this ticker, fallback to API (Slow but reliable)
    if df.empty:
        print(f"⚠️ {ticker} not found in Database. Fetching live from Yahoo Finance...")
        stock = yf.Ticker(ticker)
        df = stock.history(period="2y") # Fetch enough for 200 SMA
    
    if df.empty:
        return {"error": f"No data found for {ticker} (Check symbol or internet)."}

    # 2. Add Technical Indicators (RSI, MACD, Bollinger, ATR, etc.)
    df = add_technical_indicators(df)
    
    # Filter data based on requested period to keep payload light
    # (But keep enough buffer for lookback calculations if needed later)
    if period == "1y":
        df = df.tail(300) 
    
    # Get the latest row for "Current" metrics
    latest = df.iloc[-1]
    
    # 3. Machine Learning Inference
    pred_msg = "Model not loaded."
    if MODEL_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
            
            # CRITICAL: Feature order must match training exactly
            features = ['Close', 'rsi', 'macd', 'macd_signal', 'sma_50', 'sma_200', 'atr']
            
            # Reshape for Sklearn/XGBoost (1 row, N columns)
            input_df = pd.DataFrame([latest[features]])
            
            pred = model.predict(input_df)[0]
            pred_msg = f"ML Model predicts next Close: ${pred:.2f}"
        except Exception as e:
            print(f"⚠️ Model Inference Failed: {e}")
            pred_msg = f"Model Error: {str(e)}"
    
    # 4. Build Metrics Dictionary (For the UI Cards)
    metrics = {
        "current_price": float(latest['Close']),
        "rsi": float(latest['rsi']),
        "macd": float(latest['macd']),
        "macd_signal": float(latest['macd_signal']),
        "sma_50": float(latest['sma_50']),
        "sma_200": float(latest['sma_200']),
        "atr": float(latest['atr'])
    }
    
    # 5. Generate Text Signals (Rule-Based)
    signals_output = interpret_signals(latest['Close'], metrics)
    signals = signals_output['signals']
    
    # Append the ML prediction as a signal
    signals.append(pred_msg)
    
    # 6. Prepare Chart Data (OHLC + SMAs) for Plotly
    # We take the last 120 days for a clean, zoomed-in view
    recent = df.tail(120)
    
    chart_data = {
        "dates": recent.index.astype(str).tolist(),
        "open": recent['Open'].tolist(),
        "high": recent['High'].tolist(),
        "low": recent['Low'].tolist(),
        "close": recent['Close'].tolist(),
        "sma_50": recent['sma_50'].tolist(),
        "sma_200": recent['sma_200'].tolist()
    }
    
    return {
        "metrics": metrics,
        "signals": signals,
        "chart_data": chart_data
    }

# --- Test Block ---
if __name__ == "__main__":
    import json
    # Run this file directly to test if DB reading works
    print(json.dumps(get_technical_analysis("AAPL"), indent=2, default=str))