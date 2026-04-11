import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# 1. Logic for Trade Simulation
def generate_trade_log(balance, risk_per_trade, win_rate=0.684):
    trades = []
    current_balance = balance
    
    # Simulate the last 10 trades based on your 68.4% Win Rate
    for i in range(1, 11):
        is_win = np.random.choice([True, False], p=[win_rate, 1-win_rate])
        risk_amount = current_balance * (risk_per_trade / 100)
        
        if is_win:
            profit = risk_amount * 2.14  # Using your Profit Factor as the reward ratio
            current_balance += profit
            result = "✅ WIN"
        else:
            profit = -risk_amount
            current_balance += profit
            result = "❌ LOSS"
            
        trades.append({
            "Trade #": i,
            "Result": result,
            "Profit/Loss ($)": round(profit, 2),
            "Balance ($)": round(current_balance, 2)
        })
    return pd.DataFrame(trades)

# 2. Add to Main App
st.markdown("---")
st.subheader("🎲 Trade-by-Trade Simulation")
st.write("Simulating the next 10 trades based on your current Neural Model stats.")

# Get settings from your existing sidebar
# Note: Ensure 'acc_bal' and 'risk_pct' are defined in your sidebar code
try:
    sim_df = generate_trade_log(st.session_state.get('acc_bal', 10000), st.session_state.get('risk_pct', 1.0))
    
    # Display as a clean, professional table
    st.table(sim_df)
    
    # 3. Mini Equity Curve for the Simulation
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(x=sim_df["Trade #"], y=sim_df["Balance ($)"], 
                                 mode='lines+markers', line=dict(color='#00ff00')))
    fig_sim.update_layout(template="plotly_dark", title="Simulated Growth Path", height=300)
    st.plotly_chart(fig_sim, use_container_width=True)
except Exception as e:
    st.info("Adjust the sidebar parameters to initialize the simulation.")