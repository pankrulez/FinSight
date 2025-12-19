# src/api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.ml_engine.forecasting import get_technical_analysis
from src.data_engine.sentiment import get_market_sentiment

# 1. Initialize App
app = FastAPI(
    title="FinSight AI API",
    description="Algorithmic Trading Analysis as a Service",
    version="2.0"
)

# 2. Define Request/Response Models (Validation)
class AnalysisRequest(BaseModel):
    ticker: str
    period: str = "1y"

# 3. Define Endpoints
@app.get("/")
def health_check():
    """Confirms the API is running."""
    return {"status": "online", "system": "FinSight AI"}

@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):
    """
    Returns full technical analysis (Signals, RSI, MACD).
    """
    ticker = ticker.upper()
    data = get_technical_analysis(ticker)
    
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    
    return data

@app.get("/sentiment/{ticker}")
def analyze_sentiment(ticker: str):
    """
    Returns AI Sentiment Score from News.
    """
    ticker = ticker.upper()
    return get_market_sentiment(ticker)

# 4. Run instructions
# In terminal: uvicorn src.api.main:app --reload
# View Docs: http://127.0.0.1:8000/docs