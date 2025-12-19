import sys
# --- SQLITE FOR STREAMLIT CLOUD ---
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sys
import os
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf # Needed to fetch long history for backtest

# --- PATH SETUP ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.agents.graph import build_graph
from src.agents.state import AgentState
from src.ml_engine.backtest import run_backtest # <--- NEW IMPORT
from src.ml_engine.features import add_technical_indicators # Helper for backtest data

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="FinSight Pro", page_icon="📈")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    .stMetric {background-color: #1e1e1e; padding: 10px; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

# --- CACHING OPTIMIZATION ---
@st.cache_data(ttl=3600, show_spinner=False)
def run_analysis_cached(ticker):
    """Runs the graph and caches the result for 1 hour."""
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
    """Fetches 5 years of data to run a robust backtest."""
    stock = yf.Ticker(ticker)
    df = stock.history(period="5y")
    if df.empty: return None
    df = add_technical_indicators(df)
    return run_backtest(df)

# --- CHARTING ENGINES ---
def render_chart(ticker, data):
    """Draws a professional Candlestick chart."""
    if not data: return
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data['dates'], open=data['open'], high=data['high'],
        low=data['low'], close=data['close'], name='OHLC'
    ))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma_50'], line=dict(color='orange', width=1), name='SMA 50'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma_200'], line=dict(color='#8800ff', width=1), name='SMA 200'))
    
    fig.update_layout(
        title=f"{ticker} Price Action (120 Days)",
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font=dict(color="white"),
        height=500, xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_backtest_chart(backtest_res):
    """Draws the Equity Curve (Strategy vs Buy & Hold)."""
    if not backtest_res or "error" in backtest_res:
        st.warning("Could not run backtest.")
        return

    data = backtest_res['comparison_data']
    fig = go.Figure()
    
    # 1. Market (Buy & Hold)
    fig.add_trace(go.Scatter(
        x=data['dates'], y=data['market_curve'],
        mode='lines', name='Buy & Hold (Market)',
        line=dict(color='gray', dash='dash')
    ))
    
    # 2. Strategy (AI/Golden Cross)
    fig.add_trace(go.Scatter(
        x=data['dates'], y=data['strategy_curve'],
        mode='lines', name='AI Strategy (Trend)',
        line=dict(color='#00ff00', width=2)
    ))

    fig.update_layout(
        title="Strategy Performance vs Market (5 Years)",
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font=dict(color="white"),
        height=400, hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚡ FinSight Pro")
    mode = st.radio("Asset Class", ["Stocks", "Crypto", "Custom"], horizontal=True)
    if mode == "Custom": ticker = st.text_input("Symbol", "AMD").upper()
    elif mode == "Crypto": ticker = st.selectbox("Symbol", ["BTC-USD", "ETH-USD", "SOL-USD"])
    else: ticker = st.selectbox("Symbol", ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"])
    st.divider()
    st.caption("v2.1 | Backtesting Enabled")

# --- MAIN APP ---
st.title(f"📊 Market Intelligence: {ticker}")

if st.button("Initialize Analysis", type="primary"):
    
    # TABS: Now with "Strategy Performance"
    tab_dash, tab_report, tab_backtest, tab_dev = st.tabs(["🚀 Dashboard", "📝 Investment Memo", "📈 Strategy Performance", "🛠️ Developer"])
    
    with st.spinner(f"Analyzing {ticker} ecosystem..."):
        try:
            # 1. Run Agents
            result = run_analysis_cached(ticker)
            quant = result.get('quant_data', {})
            sent = result.get('sentiment_data', {})
            metrics = quant.get('metrics', {})
            signals = quant.get('signals', [])
            
            # 2. Run Backtest (Separate process)
            backtest_results = perform_backtest(ticker)

            # --- TAB 1: DASHBOARD ---
            with tab_dash:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Price", f"${metrics.get('current_price',0):.2f}")
                s_score = sent.get('score', 0)
                c2.metric("Sentiment", f"{s_score:.2f}", sent.get('label', 'Neutral'), delta_color="normal" if s_score > 0 else "inverse")
                pred = next((s for s in signals if "ML Model" in s), "N/A").split(":")[-1]
                c3.metric("AI Forecast", pred)
                rsi = metrics.get('rsi', 0)
                c4.metric("RSI", f"{rsi:.1f}", "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral")
                
                st.markdown("---")
                render_chart(ticker, quant.get('chart_data', {}))
                
                col_news, col_tech = st.columns(2)
                with col_news:
                    st.subheader("Headline Drivers")
                    for h in sent.get('top_headlines', []): st.info(h)
                with col_tech:
                    st.subheader("Technical Signals")
                    for s in signals:
                        if "Bullish" in s: st.success(s)
                        elif "Bearish" in s: st.error(s)
                        else: st.write(f"• {s}")

            # --- TAB 2: REPORT ---
            with tab_report:
                st.markdown(result['final_report'])
                st.download_button("Download Report", result['final_report'], file_name=f"{ticker}_report.md")

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
                    
                    render_backtest_chart(backtest_results)
                    st.caption("Strategy: Buy when SMA 50 > SMA 200 (Golden Cross). Sell/Cash when SMA 50 < SMA 200.")
                else:
                    st.error("Backtest failed. Not enough historical data.")

            # --- TAB 4: DEVELOPER ---
            with tab_dev:
                st.json(result)

        except Exception as e:
            st.error(f"Analysis Failed: {e}")