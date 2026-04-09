import pandas as pd
import numpy as np
import joblib
from alpha_vantage.foreignexchange import ForeignExchange # type: ignore

# 1. Setup - REPLACE 'YOUR_KEY' with your actual Alpha Vantage Key
fx = ForeignExchange(key='NWKOLSBK14MRIZCA') 
model = joblib.load("trading_brain.pkl")

print("Analysing Live Market for Strategy Entry...")

try:
    # 2. Get Fresh Data
    data, _ = fx.get_currency_exchange_daily(from_symbol='EUR', to_symbol='USD', outputsize='compact')
    df = pd.DataFrame.from_dict(data, orient='index')
    df.columns = ['Open', 'High', 'Low', 'Close']
    df.index = pd.to_datetime(df.index)
    df = df.astype(float).sort_index()

    # 3. Calculate Senses (Must match features.py exactly)
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['Dist_EMA_20'] = (df['Close'] - df['EMA_20']) / df['EMA_20']
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI_Change'] = df['RSI'].diff()
    df['Momentum'] = df['Close'].pct_change(periods=5)
    df['Range'] = (df['High'] - df['Low']) / df['Close']
    
    # Calculate ATR for the trade plan
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift()) # type: ignore
    low_close = np.abs(df['Low'] - df['Close'].shift()) # type: ignore
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    df['ATR'] = np.max(ranges, axis=1).rolling(14).mean() # type: ignore
    
    df.dropna(inplace=True)

    # 4. Predict
    features = ['Dist_EMA_20', 'RSI', 'RSI_Change', 'Momentum', 'Range']
    latest_row = df[features].tail(1)
    prediction = model.predict(latest_row)[0]
    prob = model.predict_proba(latest_row)[0]

    # 5. Trade Planning (Volatility-Adjusted)
    current_price = df['Close'].iloc[-1]
    atr = df['ATR'].iloc[-1]
    
    # SL is 1.5x the ATR (to avoid getting stopped out by noise)
    # TP is 3x the ATR (to ensure a 2:1 Reward ratio)
    sl_dist = atr * 1.5
    tp_dist = atr * 3.0

    if prediction == 1:
        signal_type = "BUY/LONG 📈"
        sl = current_price - sl_dist
        tp = current_price + tp_dist
        confidence = prob[1] * 100
    else:
        signal_type = "SELL/SHORT 📉"
        sl = current_price + sl_dist
        tp = current_price - tp_dist
        confidence = prob[0] * 100

    # 6. Final Output
    print("\n" + "="*35)
    print(f"DIRECTION: {signal_type}")
    print(f"CONFIDENCE: {confidence:.2f}%")
    print("-" * 35)
    print(f"ENTRY PRICE: {current_price:.5f}")
    print(f"STOP LOSS  : {sl:.5f} (Safety Net)")
    print(f"TAKE PROFIT: {tp:.5f} (Goal)")
    print("="*35)

except Exception as e:
    print(f"Error: {e}")