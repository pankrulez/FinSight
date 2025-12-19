from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from src.agents.state import AgentState
from src.ml_engine.forecasting import get_technical_analysis
from src.data_engine.vectorizer import get_fundamental_analysis
from src.data_engine.sentiment import get_market_sentiment

def quant_node(state: AgentState):
    return {"quant_data": get_technical_analysis(state['ticker'])}

def rag_node(state: AgentState):
    return {"rag_data": get_fundamental_analysis(state['ticker'])}

def sentiment_node(state: AgentState):
    return {"sentiment_data": get_market_sentiment(state['ticker'])}

def report_node(state: AgentState):
    quant = state.get('quant_data', {})
    rag = state.get('rag_data', {})
    sent = state.get('sentiment_data', {})
    
    # Format data for LLM
    metrics = quant.get('metrics', {})
    quant_text = f"Price: ${metrics.get('current_price',0)}, RSI: {metrics.get('rsi',0)}, Signals: {quant.get('signals',[])}"
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    prompt = f"""
    Act as a Senior Analyst. Analyze {state['ticker']}.
    
    DATA:
    1. Technicals: {quant_text}
    2. Sentiment: Score {sent.get('score',0)} ({sent.get('label','Neutral')})
    3. Fundamentals: {rag.get('relevant_text','')}
    
    Write a Markdown report. 
    Executive Summary MUST be bullet points. 
    Highlight any divergence between Price and Sentiment.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_report": response.content}

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("quant", quant_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("sentiment", sentiment_node)
    workflow.add_node("report", report_node)
    
    workflow.set_entry_point("quant")
    workflow.add_edge("quant", "rag")
    workflow.add_edge("rag", "sentiment")
    workflow.add_edge("sentiment", "report")
    workflow.add_edge("report", END)
    return workflow.compile()