import pandas as pd
from sqlalchemy import create_engine, Column, String, Float, Date, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import DATA_DIR
from datetime import date

# 1. Setup Database Path (Saves to data/finsight.db)
DB_PATH = f"sqlite:///{DATA_DIR}/finsight.db"
engine = create_engine(DB_PATH, echo=False)
Base = declarative_base()

# 2. Define Tables (The Schema)
class StockPrice(Base):
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

class SentimentLog(Base):
    __tablename__ = "sentiment_logs"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    date = Column(Date)
    score = Column(Float)
    label = Column(String)

# 3. Create Tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# --- HELPER FUNCTIONS ---

def save_stock_data(ticker: str, df: pd.DataFrame):
    """
    Saves a Pandas DataFrame (from yfinance) to SQLite.
    Optimized to avoid duplicates.
    """
    # Convert index to column if needed
    if 'Date' not in df.columns:
        df = df.reset_index()
    
    # Standardize columns
    df['date'] = pd.to_datetime(df['Date']).dt.date
    df['ticker'] = ticker
    
    # Rename for SQL mapping
    df = df.rename(columns={
        "Open": "open", "High": "high", "Low": "low", 
        "Close": "close", "Volume": "volume"
    })
    
    # Filter only relevant columns
    data_to_save = df[['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']]
    
    # Use Pandas magic to write to SQL (Replace existing for simplicity in MVP)
    # In production, you'd use 'append' and check for duplicates
    data_to_save.to_sql('stock_prices', con=engine, if_exists='append', index=False, method='multi', chunksize=500)
    print(f"✅ Saved {len(df)} rows for {ticker} to Database.")

def get_stock_data(ticker: str) -> pd.DataFrame:
    """Reads SQL data back into a Pandas DataFrame."""
    query = f"SELECT * FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date ASC"
    df = pd.read_sql(query, con=engine)
    
    if not df.empty:
        df['Date'] = pd.to_datetime(df['date'])
        df.set_index('Date', inplace=True)
        # Drop the extra SQL columns
        df.drop(columns=['id', 'date', 'ticker'], inplace=True, errors='ignore')
        # Capitalize columns to match yfinance format for other functions
        df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}, inplace=True)
        
    return df