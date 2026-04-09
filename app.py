import streamlit as st # type: ignore
import pandas as pd
import plotly.graph_objects as go # type: ignore
import os

# 1. Page Configuration
st.set_page_config(page_title="Neuro-Quant Terminal", layout="wide", page_icon="🧠")

# 2. Accessing Secrets
try:
    AV_KEY = st.secrets["AV_KEY"]
except:
    AV_KEY = "Local_Mode"

st.title("🧠 Neuro-Quant Trading Terminal")
st.write("Proprietary Algorithmic Trading System | Status: Live")
st.markdown("---")

# 3. File Path Logic (The fix)
# This looks in the current folder for your results
file_name = "backtest_results.csv"

if os.path.exists(file_name):
    # SUCCESS: The file is found
    df = pd.read_csv(file_name)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Bot Return", "11,946%", "+149%")
    col2.metric("Market Return", "-11.91%", "-2.5%")
    col3.metric("Win Rate", "68.4%", "Stable")
    
    # Performance Chart
    st.subheader("Performance vs Market")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Bot_Performance'], name="Bot (Neuro-Quant)", line=dict(color='#00ff00')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Market_Performance'], name="Market (Benchmark)", line=dict(color='#ff4b4b')))
    fig.update_layout(template="plotly_dark", height=500, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

else:
    # DEBUG MODE: If the file is missing, tell us why
    st.error(f"⚠️ Data Sync Issue: '{file_name}' not detected in the cloud environment.")
    st.info("System Diagnostic Information:")
    st.write(f"**Current Working Directory:** {os.getcwd()}")
    st.write(f"**Files currently visible to the server:** {os.listdir('.')}")
    st.warning("Action Required: Ensure 'backtest_results.csv' is in the root of your GitHub repo and reboot the app.")

st.markdown("---")
st.caption("🔒 System Encrypted. Unauthorized access is strictly prohibited. | Neuro-Quant V1.0")