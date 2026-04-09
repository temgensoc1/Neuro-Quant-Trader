import pandas as pd
import joblib # type: ignore
import numpy as np

# 1. Load the Brain and the Smart Data
model = joblib.load("trading_brain.pkl")
df = pd.read_csv("smart_eurusd.csv", index_col=0, parse_dates=True)

# 2. Select the features (Must match the training features exactly)
features = ['Dist_EMA_20', 'RSI', 'RSI_Change', 'Momentum', 'Range']
X = df[features]

print("Simulating Real-World Trades...")

# 3. Generate Predictions (1 = Buy/Hold, 0 = Stay in Cash)
df['Signal'] = model.predict(X)

# 4. Calculate Market Returns
df['Market_Pct_Change'] = df['Close'].pct_change().shift(-1)

# 5. Add Transaction Costs (The "Broker Reality Check")
# A spread of 0.0001 is common for EUR/USD (1 pip)
spread = 0.0001
# We only pay the cost when we change our position (Buy or Sell)
df['Trade_Cost'] = (df['Signal'].diff().abs() * spread).fillna(0)

# 6. Calculate Bot Returns (Market gain minus the cost of trading)
df['Strategy_Returns'] = (df['Signal'] * df['Market_Pct_Change']) - df['Trade_Cost']

# 7. Calculate Cumulative Performance (Compounding Interest)
df['Market_Performance'] = (1 + df['Market_Pct_Change'].fillna(0)).cumprod()
df['Bot_Performance'] = (1 + df['Strategy_Returns'].fillna(0)).cumprod()

print("\n--- ADAPTIVE BACKTEST RESULTS ---")
total_return = (df['Bot_Performance'].iloc[-1] - 1) * 100
market_return = (df['Market_Performance'].iloc[-1] - 1) * 100

print(f"Total Strategy Return: {total_return:.2f}%")
print(f"Buy & Hold Market Return: {market_return:.2f}%")

# 8. Success Metric: Did we beat the market?
if total_return > market_return:
    print("\nRESULT: The bot outperformed the market! 🚀")
else:
    print("\nRESULT: The market performed better. Time to adjust the 'senses'.")

# 9. Save the results
df.to_csv("backtest_results.csv")
print("\nDetailed breakdown saved to backtest_results.csv")