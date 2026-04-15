import requests
import os
from datetime import datetime
import pytz

# Secrets pulled from GitHub Environment
AV_KEY = os.getenv("AV_KEY")
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_market_data():
    try:
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={AV_KEY}'
        r = requests.get(url)
        data = r.json()
        return float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    except Exception as e:
        print(f"Data Fetch Error: {e}")
        return None

def is_kill_zone():
    # West Africa Time
    wat = pytz.timezone('Africa/Lagos')
    now = datetime.now(wat)
    # High Liquidity Window: 12:00 to 17:00 WAT
    return 12 <= now.hour <= 17

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def analyze_strategy():
    if not is_kill_zone():
        print("Outside High-Probability Kill Zone. Standing by.")
        return

    price = get_market_data()
    if not price: return

    # V6 Breakout Logic
    # We trade the breakout of a defined range to avoid 'choppy' markets
    resistance = 1.1750
    support = 1.1650
    
    if price > resistance:
        signal, action = "BULLISH BREAKOUT", "BUY"
        tp, sl = price + 0.0060, price - 0.0020
    elif price < support:
        signal, action = "BEARISH BREAKOUT", "SELL"
        tp, sl = price - 0.0060, price + 0.0020
    else:
        print("Price within neutral range. No trade.")
        return

    message = (f"NEURO-QUANT V6: {signal}\n\n"
               f"Action: {action} EUR/USD\n"
               f"Entry: {price:.5f}\n"
               f"TP: {tp:.5f}\n"
               f"SL: {sl:.5f}\n"
               f"Status: High Liquidity Entry")
    
    send_alert(message)

if __name__ == "__main__":
    analyze_strategy()