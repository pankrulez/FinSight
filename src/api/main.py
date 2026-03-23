# src/api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.graph import build_graph
from src.agents.state import AgentState

# 1. Initialize App
app = FastAPI(
    title="FinSight AI API",
    description="Algorithmic Trading & AI Analysis as a Service",
    version="3.0" # Upgraded version!
)

# 2. Initialize the AI Graph
agent_graph = build_graph()

# 3. Define Endpoints
@app.get("/")
def health_check():
    """Confirms the API is running."""
    return {"status": "online", "system": "FinSight AI Agent Engine"}

@app.get("/intelligence/{ticker}")
def get_full_intelligence(ticker: str):
    """
    Runs the full LangGraph pipeline: Quant -> RAG -> Sentiment -> LLM Memo.
    """
    ticker = ticker.upper()
    
    # Initialize the state just like we do in Streamlit
    inputs: AgentState = {
        "ticker": ticker, 
        "user_query": "Analyze", 
        "quant_data": {}, 
        "rag_data": {}, 
        "sentiment_data": {}, 
        "final_report": "",
        "eli5_summary": ""
    }
    
    try:
        # Trigger the AI Agents
        result = agent_graph.invoke(inputs)
        
        quant = result.get("quant_data", {})
        
        # Package a clean, enterprise-grade JSON payload for external apps
        return {
            "ticker": ticker,
            "metrics": quant.get("metrics", {}),
            "ai_signals": quant.get("signals", []),
            "sentiment_overview": result.get("sentiment_data", {}),
            "insights": {
                "eli5_translation": result.get("eli5_summary", ""),
                "professional_memo": result.get("final_report", "")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Engine Failed: {str(e)}")

# 4. Run instructions
# In terminal: python -m uvicorn src.api.main:app --reload
# View Interactive Docs: http://127.0.0.1:8000/docs