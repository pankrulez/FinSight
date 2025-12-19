from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import VECTOR_DB_DIR

def get_fundamental_analysis(ticker: str, query="risks"):
    # Uses free local CPU embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    try:
        db = Chroma(persist_directory=str(VECTOR_DB_DIR), embedding_function=embeddings, collection_name=f"{ticker}_10k")
        docs = db.similarity_search(query, k=2)
        return {"relevant_text": "\n".join([d.page_content for d in docs]) if docs else "No docs found."}
    except Exception as e:
        return {"relevant_text": f"Error retrieving docs: {str(e)}"}