# src/ml_engine/forecasting.py
import yfinance as yf
import pandas as pd
import joblib
from src.config import MODEL_PATH
from src.ml_engine.features import add_technical_indicators, interpret_signals

def get_technical_analysis(ticker: str, period="1y"):
    """
    Fetches live data, calculates technical indicators, 
    and runs the XGBoost model to predict the next closing price.
    """
    print(f"📊 Running Technical Analysis & ML Inference for {ticker}...")

    # 1. Fetch Live Data (Optimized for Cloud Deployment)
    stock = yf.Ticker(ticker)
    df = stock.history(period="2y") # Fetch enough history to calculate the 200-day SMA
    
    if df.empty:
        return {"error": f"No data found for {ticker} (Check symbol or internet)."}

    # 2. Add Technical Indicators
    df = add_technical_indicators(df)
    
    # Get the very last row for our "Current" snapshot
    latest = df.iloc[-1]
    
    # 3. Machine Learning Inference
    pred_msg = "ML Model Target: Pending Training"
    
    if MODEL_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
            
            # CRITICAL: Feature order must match trainer.py exactly
            features = ['Close', 'rsi', 'macd', 'macd_signal', 'sma_50', 'sma_200', 'atr']
            
            # Extract features for the latest day and reshape for XGBoost
            input_df = pd.DataFrame([latest[features]])
            
            # Predict the next day's close
            pred_delta = model.predict(input_df)[0]
            pred = latest['Close'] + pred_delta
            pred_msg = f"ML Model Target: ${pred:.2f}"
            
        except Exception as e:
            print(f"⚠️ Model Inference Failed: {e}")
            pred_msg = f"ML Model Target: Error loading model"
    
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
    
    # Append the ML prediction as a signal so the UI can parse it for the metric card
    signals.append(pred_msg)
    
    # 6. Prepare Chart Data (OHLC + SMAs) for Plotly
    # Limit to the last 120 days for a clean, zoomed-in dashboard view
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

if __name__ == "__main__":
    import json
    # Run this file directly to test the pipeline
    print(json.dumps(get_technical_analysis("AAPL"), indent=2, default=str))