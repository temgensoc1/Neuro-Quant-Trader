import pandas as pd
import numpy as np

# Load the raw data
df = pd.read_csv("eurusd_data.csv", index_col=0, parse_dates=True)

print("Building Adaptive Senses with Volatility Tracking...")

# --- FEATURE ENGINEERING ---

# 1. Trend & Distance
df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
df['Dist_EMA_20'] = (df['Close'] - df['EMA_20']) / df['EMA_20']

# 2. RSI & RSI Momentum
delta = df['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['RSI'] = 100 - (100 / (1 + rs))
df['RSI_Change'] = df['RSI'].diff()

# 3. Market Energy (Momentum & Range)
df['Momentum'] = df['Close'].pct_change(periods=5)
df['Range'] = (df['High'] - df['Low']) / df['Close']

# 4. VOLATILITY SENSOR (ATR)
high_low = df['High'] - df['Low']
high_close = np.abs(df['High'] - df['Close'].shift())
low_close = np.abs(df['Low'] - df['Close'].shift())
ranges = pd.concat([high_low, high_close, low_close], axis=1)
true_range = np.max(ranges, axis=1)
df['ATR'] = true_range.rolling(14).mean()

# 5. Target
df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

# --- CLEAN UP ---
df.dropna(inplace=True)
df.to_csv("smart_eurusd.csv")
print(f"Success! Smart data saved with ATR Volatility tracking.")