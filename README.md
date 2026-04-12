# Neuro-Quant Master Terminal V5

An institutional-grade algorithmic trading ecosystem built for EUR/USD market analysis. This system integrates Quantitative Finance with Neural Momentum Logic to provide high-conviction trade signals and 24/7 autonomous market monitoring.

## System Architecture
- Master Terminal: A real-time Streamlit dashboard for manual trade oversight and risk simulation.
- Autonomous Ghost Bot: A background engine powered by GitHub Actions that scans the market every 30 minutes.
- Neural Trade Detector: Logic-based signal generation with a 90-pip Take Profit and 30-pip Stop Loss protocol.
- Instant Synchronization: Seamless Telegram integration for live trade alerts (Entry, TP, SL, and Confidence scores).

## Tech Stack
- Language: Python 3.14
- Framework: Streamlit (UI/UX)
- Automation: GitHub Actions (CRON Scheduler)
- Data Source: Alpha Vantage API (Live Forex Feed)
- Messaging: Telegram Bot API
- Analytics: Pandas, Plotly, NumPy

## Project Structure
- app.py: The main user interface and terminal logic.
- bot_worker.py: The autonomous background scanner script.
- .github/workflows/scheduler.yml: Configuration for 24/7 automated execution.
- requirements.txt: Managed dependencies for cloud deployment.

## Trading Logic
The system utilizes a Neural Momentum strategy. Signals are released only when the internal Confidence Score exceeds 80%. 
- Risk Management: 1:3 Risk-to-Reward ratio.
- Targets: 90-pip Profit Target | 30-pip Stop Loss.
- Market Bias: Dynamic Bullish/Bearish regime detection based on a 1.1700 pivot.

---
**Developed by Michael | University of Ilorin Quant Lab**
*Disclaimer: This is a proprietary tool for educational and research purposes in Neuro-Quant analysis.*
