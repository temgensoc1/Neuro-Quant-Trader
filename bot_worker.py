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

def get_atr(symbol):
    """Calculates Institutional volatility (ATR 14)."""
    try:
        # Fetching last 14 hours of data
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={"EURUSD" if symbol=="EURUSD" else "GOLD"}&interval=60min&apikey={AV_KEY}'
        data = requests.get(url).json()
        df = pd.DataFrame.from_dict(data['Time Series (60min)'], orient='index').astype(float)
        # ATR Calculation: Average of (High - Low) over 14 periods
        atr = (df['2. high'] - df['3. low']).iloc[:14].mean()
        return atr
    except:
        return 0.0015 if symbol == "EURUSD" else 5.0 # Fallback

def get_price(symbol):
    try:
        if symbol == "XAUUSD":
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GOLD&apikey={AV_KEY}'
            r = requests.get(url).json()
            return float(r['Global Quote']['05. price'])
        else:
            url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={AV_KEY}'
            r = requests.get(url).json()
            return float(r['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    except:
        return None

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def run_analysis():
    # Only run during market hours (8 AM - 6 PM WAT)
    wat = pytz.timezone('Africa/Lagos')
    if not (8 <= datetime.now(wat).hour <= 18): return

    for symbol, config in ASSETS.items():
        price = get_price(symbol)
        atr = get_atr(symbol)
        if not price or not atr: continue
        
        # Institutional Logic: SL = 1.5x ATR, TP = 3x ATR
        sl = atr * 1.5
        tp = atr * 3.0
        fmt = "{:.5f}" if symbol == "EURUSD" else "{:.2f}"

        if price > config["res"]:
            msg = (f"NEURO-QUANT V8 (ATR): {symbol} BULLISH\n"
                   f"Price: {fmt.format(price)}\n"
                   f"TP: {fmt.format(price + tp)}\n"
                   f"SL: {fmt.format(price - sl)}\n"
                   f"ATR Filter: {fmt.format(atr)}")
            send_alert(msg)
        elif price < config["sup"]:
            msg = (f"NEURO-QUANT V8 (ATR): {symbol} BEARISH\n"
                   f"Price: {fmt.format(price)}\n"
                   f"TP: {fmt.format(price - tp)}\n"
                   f"SL: {fmt.format(price + sl)}\n"
                   f"ATR Filter: {fmt.format(atr)}")
            send_alert(msg)

if __name__ == "__main__":
    run_analysis()