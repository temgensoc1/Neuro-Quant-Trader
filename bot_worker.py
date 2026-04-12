import requests
import os

# Use GitHub Secrets for security
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

# Logic: If price hits a pivot or confidence is high
price = get_price()
if price > 1.1700:
    send_alert(f"🤖 *AUTO-SCAN:* Bullish Bias confirmed at {price}. Check Terminal for levels.")
elif price < 1.1650:
    send_alert(f"🤖 *AUTO-SCAN:* Bearish Pressure at {price}. Monitoring for exit.")