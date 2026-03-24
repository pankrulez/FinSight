import streamlit as st

def render_report_tab(active_ticker, final_report):
    st.markdown("<br>", unsafe_allow_html=True)
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown(f"### 📑 Strategic Intelligence Memo: `{active_ticker}`")
        st.caption(f"**DATE:** Live | **CLASSIFICATION:** Internal | **AUTHOR:** FinSight AI")
    with head_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("📥 Download Memo (.md)", data=final_report, file_name=f"{active_ticker}_Research_Memo.md", use_container_width=True)
    st.divider()
    with st.container(border=True):
        st.markdown(final_report)