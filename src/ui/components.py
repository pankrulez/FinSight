import streamlit as st
import plotly.graph_objects as go

def render_custom_metric(title, value, subtitle, trend="neutral", tooltip=""):
    if trend == "up":
        trend_color, icon = "#10b981", "▲"
    elif trend == "down":
        trend_color, icon = "#ef4444", "▼"
    else:
        trend_color, icon = "#8b5cf6", "✦"
        
    html = f"""<div title="{tooltip}" style="background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); font-family: 'Inter', sans-serif;"><div style="color: #9ca3af; font-size: 0.875rem; font-weight: 500; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">{title}</div><div style="color: #f3f4f6; font-size: 1.875rem; font-weight: 700; margin-bottom: 8px;">{value}</div><div style="color: {trend_color}; font-size: 0.875rem; font-weight: 500; display: flex; align-items: center; gap: 4px;"><span>{icon}</span> {subtitle}</div></div>"""
    st.markdown(html, unsafe_allow_html=True)

def render_chart(ticker, data):
    if not data: return
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['dates'], open=data['open'], high=data['high'], low=data['low'], close=data['close'], name='OHLC'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma_50'], line=dict(color='#f59e0b', width=1.5), name='SMA 50'))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['sma_200'], line=dict(color='#8b5cf6', width=1.5), name='SMA 200'))
    
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), height=400, xaxis_rangeslider_visible=False, margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=True, gridcolor='#1f2937', zeroline=False))
    
    chart_config = {'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': f"{ticker}_technical_analysis", 'height': 600, 'width': 1000, 'scale': 2}, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
    st.plotly_chart(fig, use_container_width=True, config=chart_config)

def render_backtest_chart(backtest_res):
    if not backtest_res or "error" in backtest_res: return
    data = backtest_res['comparison_data']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['dates'], y=data['market_curve'], mode='lines', name='Buy & Hold', line=dict(color='#6b7280', dash='dash')))
    fig.add_trace(go.Scatter(x=data['dates'], y=data['strategy_curve'], mode='lines', name='AI Strategy', line=dict(color='#10b981', width=2.5)))

    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), height=350, hovermode="x unified", margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=True, gridcolor='#1f2937', zeroline=False))
    
    chart_config = {'displayModeBar': True, 'displaylogo': False, 'toImageButtonOptions': {'format': 'png', 'filename': "strategy_backtest_results", 'height': 500, 'width': 900, 'scale': 2}, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
    st.plotly_chart(fig, use_container_width=True, config=chart_config)