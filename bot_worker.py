import requests
import os
from datetime import datetime
import pytz

# Secrets
AV_KEY = os.getenv("AV_KEY")
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Strategy Config with Volatility Multipliers
# vol_mult: 1.0 is standard. Increase (e.g., 1.5) to widen SL/TP for high volatility.
ASSETS = {
    "EURUSD": {"res": 1.1750, "sup": 1.1650, "tp": 0.0060, "sl": 0.0020, "vol_mult": 1.0},
    "XAUUSD": {"res": 2400.00, "sup": 2360.00, "tp": 10.00, "sl": 4.00, "vol_mult": 1.2}
}

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
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def is_kill_zone():
    wat = pytz.timezone('Africa/Lagos')
    now = datetime.now(wat)
    return 8 <= now.hour <= 18

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def run_analysis():
    if not is_kill_zone():
        return

    for symbol, config in ASSETS.items():
        price = get_price(symbol)
        if not price: continue
        
        # Calculate dynamic levels
        mult = config["vol_mult"]
        tp_dist = config["tp"] * mult
        sl_dist = config["sl"] * mult

        if price > config["res"]:
            action = "BUY"
            tp = price + tp_dist
            sl = price - sl_dist
            
            # Formatting block: Ensures 5 decimals for EURUSD, 2 for XAUUSD
            fmt = "{:.5f}" if symbol == "EURUSD" else "{:.2f}"
            msg = (f"NEURO-QUANT V7: {symbol} BREAKOUT\n"
                   f"Action: {action}\n"
                   f"Entry: {fmt.format(price)}\n"
                   f"TP: {fmt.format(tp)}\n"
                   f"SL: {fmt.format(sl)}\n"
                   f"Status: Volatility Multiplier {mult}x")
            send_alert(msg)

        elif price < config["sup"]:
            action = "SELL"
            tp = price - tp_dist
            sl = price + sl_dist
            
            fmt = "{:.5f}" if symbol == "EURUSD" else "{:.2f}"
            msg = (f"NEURO-QUANT V7: {symbol} BREAKOUT\n"
                   f"Action: {action}\n"
                   f"Entry: {fmt.format(price)}\n"
                   f"TP: {fmt.format(tp)}\n"
                   f"SL: {fmt.format(sl)}\n"
                   f"Status: Volatility Multiplier {mult}x")
            send_alert(msg)

if __name__ == "__main__":
    run_analysis()