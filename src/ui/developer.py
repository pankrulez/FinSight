import streamlit as st
import json
import plotly.graph_objects as go
from src.data_engine.ingestor_rag import ingest_fundamental_data
from src.ml_engine.trainer import train_model
from src.config import MODEL_DIR

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
            
            # --- NEW: Hyperparameter Tuning Expander ---
            with st.expander("⚙️ Advanced: Hyperparameter Tuning", expanded=False):
                st.caption("Adjust tree parameters to prevent overfitting or anchoring.")
                trees = st.slider("Number of Trees (n_estimators)", min_value=50, max_value=500, value=100, step=50)
                learn_rate = st.selectbox("Learning Rate", options=[0.01, 0.05, 0.1, 0.2], index=1)
                depth = st.slider("Max Tree Depth", min_value=2, max_value=10, value=3, step=1)
            
            # Pass the slider values into the training function
            if st.button(f"Retrain XGBoost Model", type="primary", use_container_width=True):
                with st.spinner(f"Training model with {trees} trees..."):
                    try:
                        metrics = train_model(active_ticker, n_trees=trees, lr=learn_rate, max_d=depth)
                        if metrics.get("status") == "success": 
                            st.success(f"Model retrained! Margin of Error: ±${metrics['mean_absolute_error']}")
                        else: 
                            st.error(metrics.get("message", "Unknown error."))
                    except Exception as e:
                        st.error(f"Training failed: {e}")
                        
    st.divider()
    
    # --- NEW: Model Diagnostics Dashboard ---
    metrics_path = MODEL_DIR / "model_metrics.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, "r") as f:
                saved_metrics = json.load(f)
                
            st.markdown("#### 📊 XGBoost Model Diagnostics")
            st.caption(f"Showing performance metrics for the last model trained on **{saved_metrics.get('ticker_trained_on', 'Unknown')}**.")
            
            # Key Performance Indicator Cards
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("MAE (Dollar Error)", f"${saved_metrics.get('mean_absolute_error', 0)}", help="Average dollar amount the prediction is off by.")
            mc2.metric("MAPE (Percentage)", f"{saved_metrics.get('mape', 0)}%", help="Mean Absolute Percentage Error. Lower is better.")
            mc3.metric("R-Squared", f"{saved_metrics.get('r2_score', 0)}", help="How well the indicators explain the price (1.0 is perfect).")
            mc4.metric("Data Processed", f"{saved_metrics.get('total_rows_processed', 0)} days", help=f"From {saved_metrics.get('training_start_date')} to {saved_metrics.get('training_end_date')}")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Feature Importance Chart
            st.markdown("##### Feature Importance Weights")
            if "feature_importance" in saved_metrics:
                fi = saved_metrics["feature_importance"]
                sorted_fi = dict(sorted(fi.items(), key=lambda item: item[1]))
                
                fig = go.Figure(go.Bar(
                    x=list(sorted_fi.values()), y=list(sorted_fi.keys()), orientation='h',
                    marker=dict(color='#3b82f6', opacity=0.8), text=[f"{v:.3f}" for v in sorted_fi.values()], textposition='auto'
                ))
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), height=300, margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(showgrid=True, gridcolor='#1f2937', title="Relative Weight"), yaxis=dict(showgrid=False))
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.warning(f"Could not load model metrics: {e}")
    else:
        st.info("No model currently trained. Click 'Retrain XGBoost Model' to begin.")
        
    st.divider()
    st.markdown("#### Raw System State Payload")
    st.json(result)