import streamlit as st
from src.ui.components import render_custom_metric, render_chart

def render_dashboard_tab(active_ticker, eli5, quant, sent, metrics, signals):
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"💡 **AI Translation:** {eli5}")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: render_custom_metric("Current Price", f"${metrics.get('current_price',0):.2f}", "Live Data", "neutral", "The most recent trading price.")
    with c2:
        s_score = sent.get('score', 0)
        render_custom_metric("News Sentiment", f"{s_score:.2f}", sent.get('label', 'Neutral'), "up" if s_score > 0 else "down", "Analyzes recent news articles.")
    with c3:
        pred_signal = next((s for s in signals if "ML Model" in s), None)
        pred = pred_signal.split(":")[-1].strip() if pred_signal else "Pending"
        render_custom_metric("AI Target", pred, "XGBoost Forecast", "up" if "1" else "down", "Prediction for next closing price.") 
    with c4:
        rsi = metrics.get('rsi', 0)
        render_custom_metric("RSI Momentum", f"{rsi:.1f}", "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral", "up" if rsi < 30 else "down", "Relative Strength Index.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📚 What do these numbers actually mean?", expanded=False):
        st.markdown("* **AI Target:** We use an advanced algorithm (XGBoost) to guess where the price is heading next.\n* **RSI:** If it's **Overbought** (above 70), the stock is moving too fast.\n* **Sentiment:** We read thousands of news headlines using GenAI. Positive score = good news.")

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
        st.markdown("#### Catalyst Drivers", unsafe_allow_html=True)
        for h in sent.get('top_headlines', [])[:3]: st.info(f"📰 {h}")