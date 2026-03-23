import yfinance as yf
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import Chroma
from src.config import VECTOR_DB_DIR
import os

def ingest_fundamental_data(ticker: str):
    """
    Fetches REAL company profiles and recent news from yfinance 
    and embeds them into the local Chroma vector database.
    """
    print(f"📚 Indexing real fundamental data for {ticker}...")
    stock = yf.Ticker(ticker)
    docs = []
    
    # 1. Fetch Company Profile (The "What do they do?" factor)
    try:
        info = stock.info
        summary = info.get('longBusinessSummary', '')
        if summary:
            docs.append(Document(
                page_content=f"Company Profile: {summary}",
                metadata={"source": "yfinance_profile", "type": "fundamental"}
            ))
    except Exception as e:
        print(f"   ⚠️ Could not fetch profile: {e}")

    # 2. Fetch Recent News Headlines (The "What is happening now?" factor)
    try:
        news = stock.news
        for article in news[:5]: # Grab the top 5 most recent articles
            title = article.get('title', '')
            publisher = article.get('publisher', '')
            content = f"Recent News: {title} (Published by {publisher})"
            docs.append(Document(
                page_content=content,
                metadata={"source": "yfinance_news", "type": "news"}
            ))
    except Exception as e:
        print(f"   ⚠️ Could not fetch news: {e}")

    if not docs:
        print(f"❌ No text data found to index for {ticker}.")
        return

    # 3. Initialize Free Embeddings (Runs on your CPU)
    print("   Loading local embedding model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Use a distinct collection name for the real data
    collection_name = f"{ticker}_fundamentals"
    
    # 4. Save to Chroma DB
    print(f"   Saving {len(docs)} documents to Chroma DB...")
    Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=str(VECTOR_DB_DIR),
        collection_name=collection_name
    )
    print(f"✅ Vector DB populated successfully for {ticker}.")

if __name__ == "__main__":
    # Test with a few major tickers
    for t in ["AAPL", "NVDA", "TSLA"]:
        ingest_fundamental_data(t)