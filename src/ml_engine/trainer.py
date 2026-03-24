import pandas as pd
import joblib
import json
import yfinance as yf
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from src.config import MODEL_DIR, MODEL_PATH
from src.ml_engine.features import add_technical_indicators

def train_model(ticker: str, n_trees: int = 100, lr: float = 0.05, max_d: int = 3):
    """Fetches historical data, trains an XGBoost model, evaluates accuracy, and saves artifacts."""
    print(f"🧠 Initiating XGBoost training sequence for {ticker}...")
    
    stock = yf.Ticker(ticker)
    df = stock.history(period="10y") 
    
    if df.empty: return {"status": "error", "message": f"No data found for {ticker}."}

    df = add_technical_indicators(df)
    df['Target'] = df['Close'].shift(-1) - df['Close']
    df.dropna(inplace=True)
    
    features = ['Close', 'rsi', 'macd', 'macd_signal', 'sma_50', 'sma_200', 'atr']
    
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    X_train, y_train = train_df[features], train_df['Target']
    X_test, y_test = test_df[features], test_df['Target']
    
    model = XGBRegressor(
        n_estimators=n_trees, 
        learning_rate=lr, 
        max_depth=max_d, 
        random_state=42
    )
    model.fit(X_train, y_train)
    
    joblib.dump(model, MODEL_PATH)
    
    # Evaluate Accuracy (Convert predicted deltas back to actual prices for the metrics)
    predicted_deltas = model.predict(X_test)
    predicted_prices = X_test['Close'] + predicted_deltas
    actual_prices = X_test['Close'] + y_test
    
    mae = mean_absolute_error(actual_prices, predicted_prices)
    mse = mean_squared_error(actual_prices, predicted_prices)
    r2 = r2_score(actual_prices, predicted_prices)
    mape = mean_absolute_percentage_error(actual_prices, predicted_prices)
    
    importances = model.feature_importances_
    feature_importance_dict = {feat: float(imp) for feat, imp in zip(features, importances)}
    
    metrics = {
        "ticker_trained_on": ticker,
        "training_start_date": str(train_df.index[0].date()),
        "training_end_date": str(test_df.index[-1].date()),
        "total_rows_processed": len(df),
        "mean_absolute_error": round(mae, 2),
        "mape": round(mape * 100, 2), # Convert to percentage
        "r2_score": round(r2, 4),
        "feature_importance": feature_importance_dict,
        "status": "success"
    }
    
    with open(MODEL_DIR / "model_metrics.json", "w") as f:
        json.dump(metrics, f)
        
    print(f"✅ Model trained. MAPE: {mape*100:.2f}% | R2: {r2:.4f}")
    return metrics

if __name__ == "__main__":
    print(train_model("AAPL"))