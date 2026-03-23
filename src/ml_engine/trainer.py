# src/ml_engine/trainer.py
import pandas as pd
import joblib
import json
import yfinance as yf
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.config import MODEL_DIR, MODEL_PATH
from src.ml_engine.features import add_technical_indicators

def train_model(ticker: str):
    """
    Fetches historical data, trains an XGBoost model, 
    evaluates its accuracy, and saves the artifacts.
    """
    print(f"🧠 Initiating XGBoost training sequence for {ticker}...")
    
    # 1. Fetch deep historical data for robust training
    stock = yf.Ticker(ticker)
    df = stock.history(period="10y") 
    
    if df.empty:
        return {"status": "error", "message": f"No data found for {ticker}."}

    # 2. Feature Engineering
    df = add_technical_indicators(df)
    
    # Target: Predict Tomorrow's Closing Price
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)
    
    features = ['Close', 'rsi', 'macd', 'macd_signal', 'sma_50', 'sma_200', 'atr']
    
    # 3. Train/Test Split (Chronological for Time Series)
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    X_train, y_train = train_df[features], train_df['Target']
    X_test, y_test = test_df[features], test_df['Target']
    
    # 4. Train the Model
    model = XGBRegressor(n_estimators=100, learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate Accuracy
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    
    # 6. Save Artifacts
    joblib.dump(model, MODEL_PATH)
    
    metrics = {
        "ticker_trained_on": ticker,
        "training_rows": len(train_df),
        "testing_rows": len(test_df),
        "mean_absolute_error": round(mae, 2),
        "mean_squared_error": round(mse, 2),
        "status": "success"
    }
    
    # Save metrics to a JSON file so the UI can read them
    with open(MODEL_DIR / "model_metrics.json", "w") as f:
        json.dump(metrics, f)
        
    print(f"✅ Model trained successfully. Average error margin: ${mae:.2f}")
    return metrics

if __name__ == "__main__":
    # Test block
    print(train_model("AAPL"))