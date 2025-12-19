import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import VECTOR_DB_DIR

# --- CACHING OPTIMIZATION ---
@st.cache_resource
def get_embedding_model():
    """
    Loads the model once and keeps it in memory.
    Using a smaller model (paraphrase-MiniLM) to save RAM.
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_fundamental_analysis(ticker: str, query="risks"):
    try:
        # 1. Get the cached model
        embeddings = get_embedding_model()
        
        # 2. Connect to DB
        db = Chroma(
            persist_directory=str(VECTOR_DB_DIR), 
            embedding_function=embeddings, 
            collection_name=f"{ticker}_10k"
        )
        
        # 3. Search
        docs = db.similarity_search(query, k=2)
        return {"relevant_text": "\n".join([d.page_content for d in docs]) if docs else "No docs found."}
        
    except Exception as e:
        return {"relevant_text": f"Error retrieving docs: {str(e)}"}