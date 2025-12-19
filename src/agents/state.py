from typing import TypedDict, Dict, Any

class AgentState(TypedDict):
    ticker: str
    user_query: str
    quant_data: Dict[str, Any]      # Role A
    rag_data: Dict[str, Any]        # Role B
    sentiment_data: Dict[str, Any]  # Role D
    final_report: str               # Role C