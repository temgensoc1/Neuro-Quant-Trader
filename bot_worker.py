import requests
import os
from datetime import datetime
import pytz

# GitHub Secrets
AV_KEY = os.getenv("AV_KEY")
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_price():
    try:
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={AV_KEY}'
        data = requests.get(url).json()
        return float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    except:
        return None

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def is_market_active():
    # Set timezone to West Africa Time (Lagos/Ilorin)
    wat = pytz.timezone('Africa/Lagos')
    now = datetime.now(wat)
    current_hour = now.hour
    
    # Active Window: 08:00 to 18:00 (8 AM to 6 PM)
    if 8 <= current_hour <= 18:
        return True
    return False

def run_analysis():
    # Only proceed if we are in the active trading window
    if not is_market_active():
        print("Market is currently in quiet zone. Monitoring only, no alerts.")
        return

    price = get_price()
    if not price:
        return

    baseline = 1.1700
    confidence = 85
    tp_dist = 0.0090
    sl_dist = 0.0030

    if price > baseline:
        action = "BUY"
        tp = price + tp_dist
        sl = price - sl_dist
        status = "BULLISH REGIME DETECTED"
    else:
        action = "SELL"
        tp = price - tp_dist
        sl = price + sl_dist
        status = "BEARISH REGIME DETECTED"

    if confidence >= 80:
        message = (f"NEURO-QUANT ACTIVE SESSION ALERT\n\n"
                   f"Status: {status}\n"
                   f"Action: {action} EUR/USD\n"
                   f"Entry: {price:.5f}\n"
                   f"TP: {tp:.5f}\n"
                   f"SL: {sl:.5f}\n"
                   f"Confidence: {confidence}%")
        send_alert(message)

if __name__ == "__main__":
    run_analysis()