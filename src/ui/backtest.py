import streamlit as st
from src.ui.components import render_custom_metric, render_backtest_chart

def render_backtest_tab(backtest_results):
    if backtest_results and "error" not in backtest_results:
        initial = float(backtest_results['initial_capital'])
        final_strat = float(backtest_results['final_strategy_equity'])
        final_market = float(backtest_results['final_market_equity'])
        profit_diff = final_strat - final_market
        
        st.markdown("### 📖 The Plain English Translation")
        if profit_diff > 0:
            st.success(f"If you had invested **\${initial:,.0f}** using this AI strategy 5 years ago, you would have **\${final_strat:,.0f}** today. That is **\${profit_diff:,.0f} more** than if you had just bought and held the stock.")
        else:
            st.warning(f"If you had invested **\${initial:,.0f}** using this AI strategy 5 years ago, you would have **\${final_strat:,.0f}** today. For this specific stock, simply buying and holding the asset would have actually made you **\${abs(profit_diff):,.0f} more**.")
        st.divider()

        c1, c2, c3 = st.columns(3)
        strat_ret = float(backtest_results['strategy_return_pct'])
        market_ret = float(backtest_results['market_return_pct'])
        with c1: render_custom_metric("Initial Capital", f"${initial:,.0f}", "Starting Balance", "neutral")
        with c2: render_custom_metric("Strategy Return", f"{strat_ret}%", f"{strat_ret - market_ret:.2f}% Alpha", "up" if strat_ret > market_ret else "down")
        with c3: render_custom_metric("Buy & Hold Return", f"{market_ret}%", "S&P Baseline", "neutral")
        
        st.markdown("<br>", unsafe_allow_html=True)
        render_backtest_chart(backtest_results)
        st.info("Strategy Logic: Buy when short-term trend (SMA 50) > long-term trend (SMA 200).")
    else:
        st.error("Backtest failed. Not enough historical data.")