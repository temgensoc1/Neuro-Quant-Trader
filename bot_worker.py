import requests
import os
from datetime import datetime
import pytz

# Secrets
AV_KEY = os.getenv("AV_KEY")
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Dynamic Multi-Asset Config
# EUR/USD: 60 pip TP | 20 pip SL
# XAU/USD: $10 (1000 point) TP | $4 (400 point) SL
ASSETS = {
    "EURUSD": {"res": 1.1750, "sup": 1.1650, "tp": 0.0060, "sl": 0.0020},
    "XAUUSD": {"res": 2400.00, "sup": 2360.00, "tp": 10.00, "sl": 4.00}
}

def get_price(symbol):
    try:
        if symbol == "XAUUSD":
            # Using Commodities endpoint for Gold
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GOLD&apikey={AV_KEY}'
            r = requests.get(url).json()
            return float(r['Global Quote']['05. price'])
        else:
            # Using Forex endpoint for EURUSD
            url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={AV_KEY}'
            r = requests.get(url).json()
            return float(r['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def is_kill_zone():
    wat = pytz.timezone('Africa/Lagos')
    now = datetime.now(wat)
    # 8 AM to 6 PM WAT (Covers London and NY Open)
    return 8 <= now.hour <= 18

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def run_analysis():
    if not is_kill_zone():
        print("Outside active sessions. Monitoring only.")
        return

    for symbol, config in ASSETS.items():
        price = get_price(symbol)
        if not price: continue

        if price > config["res"]:
            msg = (f"NEURO-QUANT V7: {symbol} BULLISH\n"
                   f"Price: {price:.2f}\n"
                   f"Action: BUY\n"
                   f"TP: {price + config['tp']:.2f} | SL: {price - config['sl']:.2f}")
            send_alert(msg)
        elif price < config["sup"]:
            msg = (f"NEURO-QUANT V7: {symbol} BEARISH\n"
                   f"Price: {price:.2f}\n"
                   f"Action: SELL\n"
                   f"TP: {price - config['tp']:.2f} | SL: {price + config['sl']:.2f}")
            send_alert(msg)

if __name__ == "__main__":
    run_analysis()