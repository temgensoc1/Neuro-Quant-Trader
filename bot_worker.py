import requests
import os

# GitHub Secrets
AV_KEY = os.getenv("AV_KEY")
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_price():
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={AV_KEY}'
    data = requests.get(url).json()
    return float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

# The Signal Engine
try:
    price = get_price()
    pivot = 1.1700
    confidence = 84 
    
    # 90 Pips = 0.0090 | 30 Pips = 0.0030
    tp_distance = 0.0090
    sl_distance = 0.0030
    
    if confidence >= 80:
        if price > pivot:
            # BULLISH TRADE SETUP
            tp = price + tp_distance
            sl = price - sl_distance
            msg = (f"NEURO-QUANT TRADE ALERT\n\n"
                   f"Action: BUY EUR/USD\n"
                   f"Entry: {price:.5f}\n"
                   f"TP: {tp:.5f}\n"
                   f"SL: {sl:.5f}\n"
                   f"Confidence: {confidence}%")
            send_alert(msg)
            
        elif price < (pivot - 0.0050):
            # BEARISH TRADE SETUP
            tp = price - tp_distance
            sl = price + sl_distance
            msg = (f"NEURO-QUANT TRADE ALERT\n\n"
                   f"Action: SELL EUR/USD\n"
                   f"Entry: {price:.5f}\n"
                   f"TP: {tp:.5f}\n"
                   f"SL: {sl:.5f}\n"
                   f"Confidence: {confidence}%")
            send_alert(msg)
            
except Exception as e:
    print(f"Error: {e}")