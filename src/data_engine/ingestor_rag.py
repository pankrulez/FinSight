# src/data_engine/ingestor_rag.py

from langchain_core.documents import Document
# --- CHANGED: Use Local Embeddings instead of OpenAI ---
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import Chroma
from src.config import VECTOR_DB_DIR
import shutil
import os

def ingest_mock_data(ticker: str):
    """
    Creates a dummy knowledge base for testing using Free Local Embeddings.
    """
    print(f"📚 Indexing mock data for {ticker}...")
    
    # 1. Define Dummy Data
    texts = [
        f"{ticker} reported a 10% increase in revenue due to AI adoption.",
        f"Key risks for {ticker} include supply chain disruptions in Asia.",
        f"{ticker} is facing a lawsuit regarding patent infringement.",
        f"Analysts project {ticker} will expand into the automotive sector next year."
    ]
    
    docs = [Document(page_content=t) for t in texts]
    
    # 2. Initialize Free Embeddings (Runs on your CPU)
    print("   Loading local embedding model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 3. CRITICAL: Clean up old OpenAI DB to prevent conflicts
    # If you try to mix OpenAI vectors with HuggingFace vectors, it crashes.
    collection_name = f"{ticker}_10k"
    
    # Create the Vector Database
    print(f"   Saving to {VECTOR_DB_DIR}...")
    Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=str(VECTOR_DB_DIR),
        collection_name=collection_name
    )
    print("✅ Vector DB populated successfully (Free Mode).")

if __name__ == "__main__":
    # Test with Apple
    ingest_mock_data("AAPL")