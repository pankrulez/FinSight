import sys
import os
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf

# --- SQLITE FOR STREAMLIT CLOUD ---
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass # Fails gracefully if running locally where standard sqlite3 is fine

# --- PATH SETUP ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.agents.graph import build_graph
from src.agents.state import AgentState
from src.ml_engine.backtest import run_backtest
from src.ml_engine.features import add_technical_indicators

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="FinSight Pro", page_icon="📈")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Modern Metric Cards with Muted Borders */
    [data-testid="stMetric"] {
        background-color: #1a1c24; 
        padding: 15px 20px; 
        border-radius: 8px;
        border: 1px solid #525266; /* Muted border: visible but not distracting */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    /* Smooth out tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    /* Hide top padding */
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CACHING OPTIMIZATION ---
@st.cache_data(ttl=3600, show_spinner=False)
def run_analysis_cached(ticker):
    app = build_graph()
    inputs: AgentState = {
        "ticker": ticker, 
        "user_query": "Analyze", 
        "quant_data": {}, 
        "rag_data": {}, 
        "sentiment_data": {}, 
        "final_report": ""
    }
    return app.invoke(inputs)

@st.cache_data(ttl=3600)
def perform_backtest(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="5y")
    if df.empty: return None
    df = add_technical_indicators(df)
    return run_backtest(df)

# --- CHARTING ENGINES ---
def render_chart(ticker, data):
    if not data: return
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data['dates'], open=data['open'], high=data['high'],
        low=data['low'], close=data['close'], name='OHLC'
    ))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma_50'], line=dict(color='orange', width=1.5), name='SMA 50'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma_200'], line=dict(color='#8800ff', width=1.5), name='SMA 200'))
    
    fig.update_layout(
        title=dict(text=f"{ticker} Price Action (120 Days)", font=dict(size=18)),
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)", 
        font=dict(color="white"),
        height=550, 
        xaxis_rangeslider_visible=False, 
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#2b2b36', zeroline=False)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_backtest_chart(backtest_res):
    if not backtest_res or "error" in backtest_res:
        st.warning("Could not run backtest.")
        return

    data = backtest_res['comparison_data']
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['dates'], y=data['market_curve'],
        mode='lines', name='Buy & Hold',
        line=dict(color='gray', dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['dates'], y=data['strategy_curve'],
        mode='lines', name='AI Strategy',
        line=dict(color='#00ff00', width=2)
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)", 
        font=dict(color="white"),
        height=450, 
        hovermode="x unified",
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#2b2b36', zeroline=False)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.header("⚡ FinSight Pro")
    st.markdown("Market Intelligence Engine")
    st.divider()
    
    mode = st.radio("Asset Class", ["Stocks", "Crypto", "Custom"])
    if mode == "Custom": 
        ticker = st.text_input("Symbol", "AMD").upper()
    elif mode == "Crypto": 
        ticker = st.selectbox("Symbol", ["BTC-USD", "ETH-USD", "SOL-USD"])
    else: 
        ticker = st.selectbox("Symbol", ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"])
    
    st.divider()
    analyze_button = st.button("Update Dashboard", type="primary", use_container_width=True)
    st.caption("v2.1 | Backtesting Enabled")

# --- MAIN APP UI ---
st.title(f"📊 {ticker} Overview")

# Use session state to keep data visible after button clicks within tabs
if analyze_button:
    st.session_state['active_ticker'] = ticker

if 'active_ticker' in st.session_state:
    active_ticker = st.session_state['active_ticker']
    
    tab_dash, tab_report, tab_backtest, tab_dev = st.tabs([
        "🚀 Dashboard", "📝 Investment Memo", "📈 Strategy", "🛠️ Data/Dev"
    ])
    
    with st.spinner(f"Aggregating intelligence for {active_ticker}..."):
        try:
            result = run_analysis_cached(active_ticker)
            quant = result.get('quant_data', {})
            sent = result.get('sentiment_data', {})
            metrics = quant.get('metrics', {})
            signals = quant.get('signals', [])
            
            backtest_results = perform_backtest(active_ticker)

            # --- TAB 1: DASHBOARD ---
            with tab_dash:
                # Top KPI Row
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Price", f"${metrics.get('current_price',0):.2f}")
                
                s_score = sent.get('score', 0)
                c2.metric("Sentiment", f"{s_score:.2f}", sent.get('label', 'Neutral'), delta_color="normal" if s_score > 0 else "inverse")
                
                pred = next((s for s in signals if "ML Model" in s), "N/A").split(":")[-1]
                c3.metric("AI Forecast", pred)
                
                rsi = metrics.get('rsi', 0)
                c4.metric("RSI", f"{rsi:.1f}", "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Asymmetrical Layout
                chart_col, insight_col = st.columns([2.8, 1.2])
                
                with chart_col:
                    render_chart(active_ticker, quant.get('chart_data', {}))
                    
                with insight_col:
                    st.subheader("🤖 AI Insights")
                    with st.expander("Technical Signals", expanded=True):
                        for s in signals:
                            if "Bullish" in s: st.success(s)
                            elif "Bearish" in s: st.error(s)
                            else: st.write(f"• {s}")
                            
                    with st.expander("Market Drivers", expanded=True):
                        headlines = sent.get('top_headlines', [])
                        if headlines:
                            for h in headlines: 
                                st.caption(f"📰 {h}")
                        else:
                            st.caption("No major headlines found recently.")

            # --- TAB 2: REPORT ---
            with tab_report:
                st.markdown(result['final_report'])
                st.download_button(
                    label="Download Full Memo", 
                    data=result['final_report'], 
                    file_name=f"{active_ticker}_memo.md",
                    use_container_width=True
                )

            # --- TAB 3: BACKTEST ---
            with tab_backtest:
                if backtest_results and "error" not in backtest_results:
                    st.subheader("Historical Strategy Simulation (5 Years)")
                    
                    b1, b2, b3 = st.columns(3)
                    b1.metric("Initial Capital", f"${backtest_results['initial_capital']:,}")
                    
                    strat_ret = float(backtest_results['strategy_return_pct'])
                    market_ret = float(backtest_results['market_return_pct'])
                    
                    b2.metric("Strategy Return", f"{strat_ret}%", delta=f"{strat_ret - market_ret:.2f}% vs Market")
                    b3.metric("Buy & Hold Return", f"{market_ret}%")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    render_backtest_chart(backtest_results)
                    st.info("Strategy Logic: Buy when SMA 50 > SMA 200 (Golden Cross). Move to Cash when SMA 50 < SMA 200.")
                else:
                    st.error("Backtest failed. Not enough historical data.")

            # --- TAB 4: DEVELOPER ---
            with tab_dev:
                st.json(result)

        except Exception as e:
            st.error(f"Analysis Failed: {e}")
else:
    st.info("👈 Select an asset and click 'Update Dashboard' to begin analysis.")