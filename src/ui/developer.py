import streamlit as st
from src.data_engine.ingestor_rag import ingest_fundamental_data
from src.ml_engine.trainer import train_model

def render_developer_tab(active_ticker, result):
    st.markdown("### ⚙️ System Operations")
    
    op_col1, op_col2 = st.columns(2)
    with op_col1:
        with st.container(border=True):
            st.markdown("#### 📚 RAG Pipeline")
            if st.button(f"Update AI Knowledge Base", type="secondary", use_container_width=True):
                with st.spinner(f"Indexing live data for {active_ticker}..."):
                    try:
                        ingest_fundamental_data(active_ticker)
                        st.success(f"Vector DB rebuilt for {active_ticker}!")
                    except Exception as e:
                        st.error(f"Ingestion failed: {e}")
    with op_col2:
        with st.container(border=True):
            st.markdown("#### 🧠 ML Pipeline")
            if st.button(f"Retrain XGBoost Model", type="primary", use_container_width=True):
                with st.spinner(f"Training ML model..."):
                    try:
                        metrics = train_model(active_ticker)
                        if metrics.get("status") == "success": st.success(f"Model retrained! Margin of Error: ±${metrics['mean_absolute_error']}")
                        else: st.error(metrics.get("message", "Unknown error."))
                    except Exception as e:
                        st.error(f"Training failed: {e}")
    st.divider()
    st.markdown("#### Raw System State Payload")
    st.json(result)