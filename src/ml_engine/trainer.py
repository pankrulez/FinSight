import pandas as pd
import joblib
from xgboost import XGBRegressor
from src.config import RAW_DATA_DIR, MODEL_PATH
from src.ml_engine.features import add_technical_indicators

def train_model(ticker="AAPL"):
    print(f"🧠 Training model for {ticker}...")
    csv_path = RAW_DATA_DIR / f"{ticker}_raw.csv"
    
    if not csv_path.exists():
        print("❌ Data not found. Run ingestor_quant.py first.")
        return

    df = pd.read_csv(csv_path)
    df = add_technical_indicators(df)
    
    # Target: Predict Next Day's Close
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)
    
    features = ['Close', 'rsi', 'macd', 'macd_signal', 'sma_50', 'sma_200', 'atr']
    
    # Train (No shuffle for time-series!)
    split = int(len(df) * 0.8)
    model = XGBRegressor(n_estimators=100, learning_rate=0.05)
    model.fit(df[features].iloc[:split], df['Target'].iloc[:split])
    
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()