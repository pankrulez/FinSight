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
    pass

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
    .stApp { background-color: #0b0f19; }
    .block-container { padding-top: 2rem; }
    
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

# --- BULLETPROOF CUSTOM HTML COMPONENTS ---
def render_custom_metric(title, value, subtitle, trend="neutral", tooltip=""):
    """Renders a styled metric card with native HTML tooltips."""
    if trend == "up":
        trend_color = "#10b981"
        icon = "▲"
    elif trend == "down":
        trend_color = "#ef4444"
        icon = "▼"
    else:
        trend_color = "#8b5cf6"
        icon = "✦"
        
    html = f"""<div title="{tooltip}" style="background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); font-family: 'Inter', sans-serif;"><div style="color: #9ca3af; font-size: 0.875rem; font-weight: 500; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">{title}</div><div style="color: #f3f4f6; font-size: 1.875rem; font-weight: 700; margin-bottom: 8px;">{value}</div><div style="color: {trend_color}; font-size: 0.875rem; font-weight: 500; display: flex; align-items: center; gap: 4px;"><span>{icon}</span> {subtitle}</div></div>"""
    st.markdown(html, unsafe_allow_html=True)

# --- CACHING LOGIC ---
@st.cache_data(ttl=3600, show_spinner=False)
def run_analysis_cached(ticker):
    app = build_graph()
    inputs: AgentState = {
        "ticker": ticker, 
        "user_query": "Analyze", 
        "quant_data": {}, 
        "rag_data": {}, 
        "sentiment_data": {}, 
        "final_report": "",
        "eli5_summary": ""
    }
    return app.invoke(inputs)

@st.cache_data(ttl=3600)
def perform_backtest(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="5y")
    if df.empty: return None
    return run_backtest(add_technical_indicators(df))

# --- CHARTING ---
def render_chart(ticker, data):
    if not data: return
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['dates'], open=data['open'], high=data['high'], low=data['low'], close=data['close'], name='OHLC'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma_50'], line=dict(color='#f59e0b', width=1.5), name='SMA 50'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma_200'], line=dict(color='#8b5cf6', width=1.5), name='SMA 200'))
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
        height=400, xaxis_rangeslider_visible=False, margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=True, gridcolor='#1f2937', zeroline=False)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_backtest_chart(backtest_res):
    if not backtest_res or "error" in backtest_res: return
    data = backtest_res['comparison_data']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['dates'], y=data['market_curve'], mode='lines', name='Buy & Hold', line=dict(color='#6b7280', dash='dash')))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['strategy_curve'], mode='lines', name='AI Strategy', line=dict(color='#10b981', width=2.5)))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
        height=350, hovermode="x unified", margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=True, gridcolor='#1f2937', zeroline=False)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("### ⚡ FinSight Pro")
    st.caption("Intelligence Engine v2.1")
    st.divider()
    
    st.markdown("#### Market Parameters")
    mode = st.radio("Asset Class", ["Stocks", "Crypto", "Custom"], label_visibility="collapsed")
    if mode == "Custom": ticker = st.text_input("Symbol", "AMD").upper()
    elif mode == "Crypto": ticker = st.selectbox("Symbol", ["BTC-USD", "ETH-USD", "SOL-USD"], label_visibility="collapsed")
    else: ticker = st.selectbox("Symbol", ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"], label_visibility="collapsed")
    
    analyze_button = st.button("Run Analysis", type="primary", use_container_width=True)

# --- STATE MANAGEMENT ---
if analyze_button:
    st.session_state['active_ticker'] = ticker

if 'active_ticker' in st.session_state:
    active_ticker = st.session_state['active_ticker']
    
    st.title(f"{active_ticker} Market Intelligence")
    
    tab_dash, tab_backtest, tab_report, tab_dev = st.tabs([
        "🚀 Dashboard", "📈 Strategy Backtest", "📝 Investment Memo", "🛠️ Developer Data"
    ])
    
    with st.spinner(f"Aggregating real-time data for {active_ticker}..."):
        try:
            result = run_analysis_cached(active_ticker)
            quant, sent = result.get('quant_data', {}), result.get('sentiment_data', {})
            metrics, signals = quant.get('metrics', {}), quant.get('signals', [])
            backtest_results = perform_backtest(active_ticker)

            # --- TAB 1: DASHBOARD ---
            with tab_dash:
                st.markdown("<br>", unsafe_allow_html=True)
                
                # 1. ELI5 Summary Block
                eli5 = result.get('eli5_summary', "Update your src/agents/graph.py to generate the plain English summary!")
                st.info(f"💡 **AI Translation:** {eli5}")
                st.markdown("<br>", unsafe_allow_html=True)

                # 2. Metric Cards with Tooltips
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    render_custom_metric("Current Price", f"${metrics.get('current_price',0):.2f}", "Live Data", "neutral", "The most recent trading price of the asset.")
                with c2:
                    s_score = sent.get('score', 0)
                    render_custom_metric("News Sentiment", f"{s_score:.2f}", sent.get('label', 'Neutral'), "up" if s_score > 0 else "down", "Analyzes recent news articles to see if the media is generally positive (Bullish) or negative (Bearish).")
                with c3:
                    pred_signal = next((s for s in signals if "ML Model" in s), None)
                    pred = pred_signal.split(":")[-1].strip() if pred_signal else "Pending"
                    render_custom_metric("AI Target", pred, "XGBoost Forecast", "up" if "1" else "down", "Our Machine Learning model's prediction for the next closing price based on historical patterns.") 
                with c4:
                    rsi = metrics.get('rsi', 0)
                    render_custom_metric("RSI Momentum", f"{rsi:.1f}", "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral", "up" if rsi < 30 else "down", "Relative Strength Index. A score over 70 means the stock might be overpriced right now. Under 30 means it might be a bargain.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # 3. Educational Expander
                with st.expander("📚 What do these numbers actually mean?", expanded=False):
                    st.markdown("""
                    * **AI Target:** We use an advanced algorithm (XGBoost) that looks at years of past data to guess where the price is heading next. 
                    * **RSI (Relative Strength Index):** Think of this as a speedometer. If it's **Overbought** (above 70), the stock is moving too fast and might need to cool down (drop). If it's **Oversold** (below 30), it might be ready to bounce back up.
                    * **Sentiment:** We read thousands of news headlines using GenAI. If the score is positive, the news is good. If it's negative, the media is currently worried about this company.
                    * **Golden Cross / Death Cross:** A "Golden Cross" happens when short-term momentum overtakes long-term averages—it's a classic signal that a stock is entering a strong growth phase.
                    """)

                st.markdown("<br>", unsafe_allow_html=True)
                chart_col, insight_col = st.columns([2.8, 1.2], gap="large")
                
                with chart_col:
                    st.markdown("#### Price Action & Moving Averages")
                    render_chart(active_ticker, quant.get('chart_data', {}))
                    
                with insight_col:
                    st.markdown("#### Algorithmic Signals")
                    for s in signals:
                        if "Bullish" in s: st.success(s)
                        elif "Bearish" in s: st.error(s)
                        else: st.info(s)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### Catalyst Drivers")
                    for h in sent.get('top_headlines', [])[:3]: 
                        st.info(f"📰 {h}")

            # --- TAB 2: BACKTEST ---
            with tab_backtest:
                if backtest_results and "error" not in backtest_results:
                    # 1. Plain English Storytelling
                    initial = float(backtest_results['initial_capital'])
                    final_strat = float(backtest_results['final_strategy_equity'])
                    final_market = float(backtest_results['final_market_equity'])
                    profit_diff = final_strat - final_market
                    
                    st.markdown("### 📖 The Plain English Translation")
                    if profit_diff > 0:
                        st.success(f"If you had invested **${initial:,.0f}** using this AI strategy 5 years ago, you would have **${final_strat:,.0f}** today. That is **${profit_diff:,.0f} more** than if you had just bought and held the stock.")
                    else:
                        st.warning(f"If you had invested **${initial:,.0f}** using this AI strategy 5 years ago, you would have **${final_strat:,.0f}** today. For this specific stock, simply buying and holding the asset would have actually made you **${abs(profit_diff):,.0f} more**.")
                    
                    st.divider()

                    c1, c2, c3 = st.columns(3)
                    strat_ret = float(backtest_results['strategy_return_pct'])
                    market_ret = float(backtest_results['market_return_pct'])
                    
                    with c1: render_custom_metric("Initial Capital", f"${initial:,.0f}", "Starting Balance", "neutral", "The simulated starting amount.")
                    with c2: render_custom_metric("Strategy Return", f"{strat_ret}%", f"{strat_ret - market_ret:.2f}% Alpha", "up" if strat_ret > market_ret else "down", "Total return using the algorithmic trading rules.")
                    with c3: render_custom_metric("Buy & Hold Return", f"{market_ret}%", "S&P Baseline", "neutral", "Total return if you simply bought the stock on day 1 and never sold.")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    render_backtest_chart(backtest_results)
                    st.info("Strategy Logic: Buy when the short-term trend (SMA 50) crosses above the long-term trend (SMA 200). Move to Cash when it drops below.")
                else:
                    st.error("Backtest failed. Not enough historical data.")

            # --- TAB 3: REPORT ---
            with tab_report:
                st.markdown("<br>", unsafe_allow_html=True)
                head_col1, head_col2 = st.columns([3, 1])
                with head_col1:
                    st.markdown(f"### 📑 Strategic Intelligence Memo: `{active_ticker}`")
                    st.caption(f"**DATE:** Live | **CLASSIFICATION:** Internal | **AUTHOR:** FinSight AI")
                with head_col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 Download Memo (.md)", 
                        data=result['final_report'], 
                        file_name=f"{active_ticker}_Research_Memo.md",
                        use_container_width=True
                    )
                st.divider()
                with st.container(border=True):
                    st.markdown(result['final_report'])

            # --- TAB 4: DEVELOPER ---
            with tab_dev:
                st.json(result)

        except Exception as e:
            st.error(f"Analysis Failed: {e}")
else:
    st.info("👈 Configure your asset parameters in the sidebar and initialize the engine.")