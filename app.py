import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# 1. Page Configuration
st.set_page_config(page_title="Neuro-Quant Terminal", layout="wide")
st_autorefresh(interval=60000, key="datarefresh")

# 2. Sidebar - Asset Selection
st.sidebar.title("Asset Control")
asset_choice = st.sidebar.selectbox("Select Market", ["EUR/USD", "XAU/USD (Gold)"])

# 3. Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00ff00; }
    .stAlert { background-color: #1e2129; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 4. Corrected Data Fetching Logic
def get_live_data(choice):
    # Use st.secrets for GitHub/Streamlit security
    try:
        av_key = st.secrets["AV_KEY"]
        
        if choice == "EUR/USD":
            url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={av_key}'
            data = requests.get(url).json()
            # Navigate the Forex JSON structure
            val = data['Realtime Currency Exchange Rate']['5. Exchange Rate']
            return float(val)
        
        else:
            # For Gold, we use the Global Quote endpoint
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GOLD&apikey={av_key}'
            data = requests.get(url).json()
            # Navigate the Commodities/Stock JSON structure
            val = data['Global Quote']['05. price']
            return float(val)
            
    except KeyError:
        st.error(f"API Limit reached or data unavailable for {choice}. Retrying in 60s...")
        return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# 5. UI Execution
st.title(f"Neuro-Quant Master Terminal: {asset_choice}")

price = get_live_data(asset_choice)

if price:
    col1, col2 = st.columns(2)

    with col1:
        # Formatting decimals: 5 for Forex, 2 for Gold
        format_str = "{:.5f}" if asset_choice == "EUR/USD" else "{:.2f}"
        st.metric(label="Current Market Price", value=format_str.format(price))

    with col2:
        st.subheader("Session Status")
        # Logic to check if we are in the Kill Zone (12-17 WAT)
        from datetime import datetime
        import pytz
        wat = pytz.timezone('Africa/Lagos')
        hour = datetime.now(wat).hour
        
        if 8 <= hour <= 18:
            st.success("MARKET ACTIVE: London/NY Session")
        else:
            st.warning("MARKET QUIET: Outside Trading Window")

    st.divider()
    st.info(f"V7 Strategy: Monitoring {asset_choice} for Institutional Breakouts.")
else:
    st.info("Waiting for API response...")