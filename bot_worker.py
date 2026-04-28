import requests
import os
from datetime import datetime
import pytz
import pandas as pd

# Secrets
AV_KEY = os.getenv("AV_KEY")
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ASSETS = {
    "EURUSD": {"res": 1.1750, "sup": 1.1650},
    "XAUUSD": {"res": 2400.00, "sup": 2360.00}
}

def get_market_data(symbol):
    """Fetches Intraday data for ATR and Trend calculation."""
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={"EURUSD" if symbol=="EURUSD" else "GOLD"}&interval=60min&apikey={AV_KEY}'
        data = requests.get(url).json()
        df = pd.DataFrame.from_dict(data['Time Series (60min)'], orient='index').astype(float)
        return df
    except:
        return None

def get_dxy_trend():
    """Checks if the Dollar Index is likely bullish or bearish."""
    try:
        # Simple Proxy: EURUSD tends to move inverse to USD strength
        # In a production environment, you'd fetch actual DXY index here
        return "NEUTRAL" 
    except:
        return "NEUTRAL"

def run_analysis():
    wat = pytz.timezone('Africa/Lagos')
    if not (8 <= datetime.now(wat).hour <= 18): return

    for symbol, config in ASSETS.items():
        df = get_market_data(symbol)
        if df is None: continue
        
        # 1. Calculate Indicators
        price = df['4. close'].iloc[0]
        sma50 = df['4. close'].iloc[:50].mean() # 50-hour Moving Average
        atr = (df['2. high'] - df['3. low']).iloc[:14].mean()
        
        # 2. Trend Logic
        is_uptrend = price > sma50
        
        # 3. Execution (With Trend Filter)
        sl = atr * 1.5
        tp = atr * 3.0
        fmt = "{:.5f}" if symbol == "EURUSD" else "{:.2f}"

        # BUY Logic: Only if breakout AND in uptrend
        if price > config["res"] and is_uptrend:
            msg = f"NEURO-QUANT V9: {symbol} BULLISH TREND\nPrice: {fmt.format(price)}\nTP: {fmt.format(price + tp)}\nSL: {fmt.format(price - sl)}"
            send_alert(msg)
            
        # SELL Logic: Only if breakout AND in downtrend
        elif price < config["sup"] and not is_uptrend:
            msg = f"NEURO-QUANT V9: {symbol} BEARISH TREND\nPrice: {fmt.format(price)}\nTP: {fmt.format(price - tp)}\nSL: {fmt.format(price + sl)}"
            send_alert(msg)

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_analysis()