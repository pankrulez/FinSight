import sys
import os
import streamlit as st
import yfinance as yf

# --- SQLITE FOR STREAMLIT CLOUD ---
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

# --- PATH SETUP ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# --- BACKEND IMPORTS ---
from src.agents.graph import build_graph
from src.agents.state import AgentState
from src.ml_engine.backtest import run_backtest
from src.ml_engine.features import add_technical_indicators

# --- FRONTEND IMPORTS (Now loaded directly from the src.ui folder) ---
from src.ui.dashboard import render_dashboard_tab
from src.ui.backtest import render_backtest_tab
from src.ui.report import render_report_tab
from src.ui.developer import render_developer_tab
from src.ui.guide import render_guide

# --- PAGE CONFIG & CSS ---
st.set_page_config(layout="wide", page_title="FinSight Pro", page_icon="📈")

st.markdown("""
    <style>
    /* --- Main Backgrounds --- */
    .stApp { background-color: #0b0f19; }
    .block-container { padding-top: 2rem; }
    [data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid #1f2937; }
    
    /* --- Fintech Blue Primary Buttons --- */
    [data-testid="baseButton-primary"] { 
        background-color: #3b82f6; 
        color: white; 
        border: none; 
        border-radius: 8px; 
        font-weight: 600; 
        transition: all 0.3s ease; 
    }
    [data-testid="baseButton-primary"]:hover { 
        background-color: #2563eb; 
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); 
        transform: translateY(-2px); 
    }
    
    /* --- 🎨 Premium Dropdown & Input Styling --- */
    /* Target the input fields and select box borders */
    .stTextInput>div>div>input, [data-baseweb="select"]>div { 
        background-color: #0b0f19 !important; 
        color: #f3f4f6 !important; 
        border: 1px solid #374151 !important; 
        border-radius: 6px !important; 
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    /* Add a subtle blue glow when the dropdown/input is clicked */
    .stTextInput>div>div>input:focus, [data-baseweb="select"]>div:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }
    /* Style the dropdown menu that pops open */
    [data-baseweb="popover"] > div {
        background-color: #111827 !important;
        border: 1px solid #374151 !important;
        border-radius: 6px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important;
    }
    /* Style the individual dropdown options on hover */
    ul[role="listbox"] li:hover {
        background-color: #1f2937 !important;
        color: #3b82f6 !important;
    }
    
    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        white-space: pre-wrap; 
        background-color: transparent; 
        border-radius: 4px 4px 0px 0px; 
        gap: 1px; 
        padding-top: 10px; 
        padding-bottom: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- CACHING LOGIC ---
@st.cache_data(ttl=3600, show_spinner=False)
def run_analysis_cached(ticker):
    app = build_graph()
    inputs: AgentState = {"ticker": ticker, "user_query": "Analyze", "quant_data": {}, "rag_data": {}, "sentiment_data": {}, "final_report": "", "eli5_summary": ""}
    return app.invoke(inputs)

@st.cache_data(ttl=3600)
def perform_backtest(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="5y")
    if df.empty: return None
    return run_backtest(add_technical_indicators(df))

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-top: -20px; margin-bottom: 20px;">
            <h2 style="color: #f3f4f6; font-weight: 800; margin-bottom: 0px;">FinSight <span style="color: #10b981;">Pro</span></h2>
            <span style="color: #9ca3af; font-size: 0.8rem; letter-spacing: 0.05em; text-transform: uppercase;">Intelligence Engine v2.1</span>
        </div>
        <hr style="margin-top: 0px; margin-bottom: 20px; border-color: #1f2937;">
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: #9ca3af; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;'>Market Parameters</p>", unsafe_allow_html=True)
    mode = st.radio("Asset Class", ["Stocks", "Crypto", "Custom"], label_visibility="collapsed")
    if mode == "Custom": ticker = st.text_input("Symbol", "AMD", help="Enter any valid Yahoo Finance ticker").upper()
    elif mode == "Crypto": ticker = st.selectbox("Symbol", ["BTC-USD", "ETH-USD", "SOL-USD"], label_visibility="collapsed")
    else: ticker = st.selectbox("Symbol", ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("🚀 Run Analysis", type="primary", use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background-color: #0b0f19; border: 1px solid #1f2937; border-radius: 8px; padding: 16px;">
            <p style="color: #6b7280; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px; margin-top: 0px;">System Status</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><span style="color: #9ca3af; font-size: 0.85rem;">Vector DB</span><span style="color: #10b981; font-size: 0.85rem; font-weight: 600;">● Synced</span></div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><span style="color: #9ca3af; font-size: 0.85rem;">LLM Agent</span><span style="color: #10b981; font-size: 0.85rem; font-weight: 600;">● Online</span></div>
            <div style="display: flex; justify-content: space-between; align-items: center;"><span style="color: #9ca3af; font-size: 0.85rem;">Market Data</span><span style="color: #10b981; font-size: 0.85rem; font-weight: 600;">● Live API</span></div>
        </div>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT & UI ISOLATION ---
if analyze_button:
    st.session_state['active_ticker'] = ticker

if 'active_ticker' in st.session_state:
    active_ticker = st.session_state['active_ticker']
    st.title(f"{active_ticker} Market Intelligence")
    
    success = False
    with st.spinner(f"Aggregating real-time data for {active_ticker}..."):
        try:
            result = run_analysis_cached(active_ticker)
            quant, sent = result.get('quant_data', {}), result.get('sentiment_data', {})
            metrics, signals = quant.get('metrics', {}), quant.get('signals', [])
            backtest_results = perform_backtest(active_ticker)
            success = True
        except Exception as e:
            error_message = str(e)

    if success:
        tab_dash, tab_backtest, tab_report, tab_dev, tab_guide = st.tabs([
            "🚀 Dashboard", "📈 Strategy Backtest", "📝 Investment Memo", "🛠️ Developer Data", "📖 Guide"
        ])
        
        with tab_dash:
            eli5 = result.get('eli5_summary', "Update your src/agents/graph.py to generate the plain English summary!")
            render_dashboard_tab(active_ticker, eli5, quant, sent, metrics, signals)
        
        with tab_backtest:
            render_backtest_tab(backtest_results)
            
        with tab_report:
            render_report_tab(active_ticker, result.get('final_report', ''))
            
        with tab_dev:
            render_developer_tab(active_ticker, result)
            
        with tab_guide:
            render_guide(is_tab=True)
    else:
        st.error(f"Analysis Failed: {error_message}")
else:
    render_guide(is_tab=False)