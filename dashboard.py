import pandas as pd
import plotly.graph_objects as go # type: ignore

# Load your backtest results
df = pd.read_csv("backtest_results.csv", index_col=0, parse_dates=True)

# Create a chart
fig = go.Figure()

# Add the Market (What the world did)
fig.add_trace(go.Scatter(x=df.index, y=df['Market_Performance'], name="Market (EUR/USD)"))

# Add the Bot (What your brain did)
fig.add_trace(go.Scatter(x=df.index, y=df['Bot_Performance'], name="Your Trading Bot"))

fig.update_layout(title="Bot vs. Market Performance", template="plotly_dark")
fig.show()