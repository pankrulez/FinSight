import json
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
    
    # STRICT JSON PROMPT
    prompt = f"""
    You are a Senior Quantitative Analyst. Analyze {state['ticker']}.

    DATA CONTEXT:
    1. Technicals: {quant_text}
    2. Sentiment: Score {sent.get('score',0)} ({sent.get('label','Neutral')})
    3. Fundamentals/News: {rag.get('relevant_text','')}

    You MUST respond with a valid JSON object. Do not include introductory text.
    The JSON object must contain exactly these two keys:

    "pro_memo": A strict, professional Wall Street investment memo formatted in Markdown. 
                Include an Executive Summary, Technical Outlook, Catalyst Analysis, and Strategic Posture.
    "eli5_summary": A 2-3 sentence explanation of the data for a total beginner without financial jargon. Tell them what the data means for the stock.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        # Robust Parsing: Clean up the output in case the LLM wrapped it in markdown code blocks
        content = response.content
        if isinstance(content, list):
            # If it's a list of blocks, extract the text safely
            content = content[0].get("text", "") if isinstance(content[0], dict) else str(content[0])
            
        raw_content = str(content).strip()
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:]
        elif raw_content.startswith("```"):
            raw_content = raw_content[3:]
        
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
            
        parsed_response = json.loads(raw_content.strip())
        
        return {
            "final_report": parsed_response.get("pro_memo", "Memo generation failed."),
            "eli5_summary": parsed_response.get("eli5_summary", "Summary unavailable.")
        }
    except json.JSONDecodeError as e:
        # Fallback if the LLM disobeys the JSON constraint
        print(f"JSON Parsing Error: {e}")
        print(f"Raw Output: {response.content}")
        return {
            "final_report": response.content,
            "eli5_summary": "Could not generate a simple summary because the AI did not return a valid JSON format."
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