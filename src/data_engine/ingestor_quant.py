import yfinance as yf
from src.data_engine.database import save_stock_data, engine, StockPrice
from sqlalchemy.orm import sessionmaker

def ingest_data(ticker: str):
    print(f"📥 Ingesting Data for {ticker}...")
    
    # 1. Fetch from API
    stock = yf.Ticker(ticker)
    df = stock.history(period="5y") # Get 5 years for backtesting
    
    if df.empty:
        print(f"⚠️ No data found for {ticker}")
        return

    # 2. Clear old data for this ticker (To prevent duplicates in this MVP)
    # In a real app, you would 'Upsert' (Update Insert), but deleting is safer for now.
    with sessionmaker(bind=engine)() as session:
        session.query(StockPrice).filter(StockPrice.ticker == ticker).delete()
        session.commit()

    # 3. Save to SQL
    save_stock_data(ticker, df)

if __name__ == "__main__":
    # Load initial data for popular stocks
    tickers = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL", "BTC-USD", "ETH-USD"]
    for t in tickers:
        ingest_data(t)