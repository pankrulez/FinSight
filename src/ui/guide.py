import streamlit as st

def render_guide(is_tab=False):
    if not is_tab:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align: center; margin-bottom: 40px; font-family: 'Inter', sans-serif;">
                <h1 style="color: #f3f4f6; font-size: 3.5rem; font-weight: 800; margin-bottom: 10px; letter-spacing: -0.02em;">
                    FinSight <span style="color: #10b981;">Pro</span>
                </h1>
                <p style="color: #9ca3af; font-size: 1.2rem; font-weight: 400;">Your AI-Powered Quantitative Market Analyst</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 📖 How to use FinSight Pro")
        st.caption("Refer back to these steps anytime to maximize your analysis.")
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div style="background-color: #111827; border: 1px solid #1f2937; border-top: 4px solid #3b82f6; border-radius: 12px; padding: 24px; height: 180px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 1.5rem;">🎯</span>
                <span style="color: #f3f4f6; font-size: 1.1rem; font-weight: 600; font-family: 'Inter', sans-serif;">1. Select Your Asset</span>
            </div>
            <div style="color: #9ca3af; font-size: 0.95rem; line-height: 1.6; font-family: 'Inter', sans-serif;">Use the sidebar panel on the left to choose a standard Stock, Cryptocurrency, or enter a Custom Ticker symbol.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #111827; border: 1px solid #1f2937; border-top: 4px solid #10b981; border-radius: 12px; padding: 24px; height: 180px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 1.5rem;">🧠</span>
                <span style="color: #f3f4f6; font-size: 1.1rem; font-weight: 600; font-family: 'Inter', sans-serif;">3. Explore AI Insights</span>
            </div>
            <div style="color: #9ca3af; font-size: 0.95rem; line-height: 1.6; font-family: 'Inter', sans-serif;">Navigate through the tabs to view algorithmic charts, backtest strategies, and read plain-English GenAI translations.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background-color: #111827; border: 1px solid #1f2937; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 24px; height: 180px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 1.5rem;">⚡</span>
                <span style="color: #f3f4f6; font-size: 1.1rem; font-weight: 600; font-family: 'Inter', sans-serif;">2. Initialize Engine</span>
            </div>
            <div style="color: #9ca3af; font-size: 0.95rem; line-height: 1.6; font-family: 'Inter', sans-serif;">Click the primary <b style="color: #e2e8f0;">Run Analysis</b> button. The system will fetch live market data and execute the XGBoost forecasts.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #111827; border: 1px solid #1f2937; border-top: 4px solid #8b5cf6; border-radius: 12px; padding: 24px; height: 180px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 1.5rem;">🔄</span>
                <span style="color: #f3f4f6; font-size: 1.1rem; font-weight: 600; font-family: 'Inter', sans-serif;">4. Update Knowledge</span>
            </div>
            <div style="color: #9ca3af; font-size: 0.95rem; line-height: 1.6; font-family: 'Inter', sans-serif;">Go to the <b style="color: #e2e8f0;">Developer Data</b> tab and click <i>Update AI Knowledge Base</i> to fetch the absolute latest news.</div>
        </div>
        """, unsafe_allow_html=True)

    if not is_tab:
        st.markdown("""
            <div style="text-align: center; margin-top: 50px;">
                <span style="background-color: rgba(16, 185, 129, 0.1); color: #10b981; padding: 12px 24px; border-radius: 30px; font-weight: 600; font-size: 1rem; border: 1px solid rgba(16, 185, 129, 0.2); font-family: 'Inter', sans-serif; letter-spacing: 0.02em;">
                    👈 Configure your asset in the sidebar to begin
                </span>
            </div>
        """, unsafe_allow_html=True)