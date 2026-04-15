import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Neuro-Quant Terminal", layout="wide")
st_autorefresh(interval=60000, key="datarefresh")

# Sidebar - Asset Selection
st.sidebar.title("Asset Control")
asset_choice = st.sidebar.selectbox("Select Market", ["EUR/USD", "XAU/USD (Gold)"])

# Visual styling (No emojis)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# Fetching Logic
def get_live_data(choice):
    av_key = st.secrets["AV_KEY"]
    if choice == "EUR/USD":
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={av_key}'
        data = requests.get(url).json()
        return float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    else:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GOLD&apikey={av_key}'
        data = requests.get(url).json()
        return float(data['Global Quote']['05. price'])

price = get_live_data(asset_choice)

# UI Layout
st.title(f"Neuro-Quant Master Terminal: {asset_choice}")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Current Market Price", value=f"{price:.2f}")

with col2:
    st.subheader("Session Status")
    st.write("Active: London / New York Overlap")

st.info(f"Monitoring {asset_choice} for V7 Breakout levels.")