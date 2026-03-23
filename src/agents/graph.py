import json
import re
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
    signals = quant.get('signals', [])
    quant_text = f"Price: ${metrics.get('current_price',0)}, RSI: {metrics.get('rsi',0)}, Signals: {signals}"
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    # BULLETPROOF DELIMITER PROMPT
    prompt = f"""
    You are a Senior Quantitative Analyst. Analyze {state['ticker']}.

    DATA CONTEXT:
    1. Technicals: {quant_text}
    2. Sentiment: Score {sent.get('score',0)} ({sent.get('label','Neutral')})
    3. Fundamentals/News: {rag.get('relevant_text','')}

    You MUST format your exact response using these specific tags. Do not add any text outside of these tags.

    [ELI5_SUMMARY]
    (Write a 2-3 sentence explanation of the data for a total beginner without financial jargon here).
    [/ELI5_SUMMARY]

    [PRO_MEMO]
    (Write the strict, professional Wall Street investment memo formatted in Markdown here. Include an Executive Summary, Technical Outlook, Catalyst Analysis, and Strategic Posture).
    [/PRO_MEMO]
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        # Extract the string safely
        content = response.content
        if isinstance(content, list):
            content = content[0].get("text", "") if isinstance(content[0], dict) else str(content[0])
            
        raw_content = str(content)
        
        # Robust Parsing using Regex to find whatever is inside our custom tags
        eli5_match = re.search(r'\[ELI5_SUMMARY\](.*?)\[/ELI5_SUMMARY\]', raw_content, re.DOTALL)
        memo_match = re.search(r'\[PRO_MEMO\](.*?)\[/PRO_MEMO\]', raw_content, re.DOTALL)
        
        eli5_summary = eli5_match.group(1).strip() if eli5_match else "Could not generate beginner summary."
        pro_memo = memo_match.group(1).strip() if memo_match else "Could not generate professional memo."
        
        return {
            "final_report": pro_memo,
            "eli5_summary": eli5_summary
        }
        
    except Exception as e:
        print(f"Parsing Error: {e}")
        return {
            "final_report": "Error parsing the LLM response.",
            "eli5_summary": "Error parsing the LLM response."
        }

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