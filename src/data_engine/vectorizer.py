# src/data_engine/vectorizer.py

import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import VECTOR_DB_DIR

@st.cache_resource
def get_embedding_model():
    """Loads the model once and keeps it in memory to save RAM."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_fundamental_analysis(ticker: str, query="company business profile and recent news catalyst"):
    """
    Searches the local Chroma DB for context to feed the AI Agent.
    """
    try:
        embeddings = get_embedding_model()
        collection_name = f"{ticker}_fundamentals"
        
        # Connect to DB
        db = Chroma(
            persist_directory=str(VECTOR_DB_DIR), 
            embedding_function=embeddings, 
            collection_name=collection_name
        )
        
        # Search for the top 3 most relevant chunks
        docs = db.similarity_search(query, k=3)
        
        if docs:
            # Format cleanly for the LLM prompt
            formatted_text = "\n".join([f"- {d.page_content}" for d in docs])
            return {"relevant_text": formatted_text}
        else:
            return {"relevant_text": "No fundamental data available. The system relies purely on technicals."}
            
    except Exception as e:
        return {"relevant_text": f"Error retrieving docs. Ensure ingestor_rag.py has been run. Details: {str(e)}"}