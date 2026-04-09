import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange # type: ignore

# 1. Initialize the tool (Using a 'demo' key for testing)
# Note: For personal projects, you can get a free key at alphavantage.co
fx = ForeignExchange(key='NWKOLSBK14MRIZCA')

print("Connecting to Alpha Vantage...")

try:
    # 2. Get Daily EUR/USD data
    # 'full' gives us the last 20 years of data!
    data, meta_data = fx.get_currency_exchange_daily(from_symbol='EUR', to_symbol='USD', outputsize='full')
    
    # 3. Clean and format the data
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Standardizing column names for our next scripts
    df.columns = ['Open', 'High', 'Low', 'Close']
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df = df.sort_index() # Put the oldest dates first (important for ML)

    print("\n--- EUR/USD DATA PREVIEW ---")
    print(df.tail()) # Shows the most recent 5 days
    print("\nTotal data points collected:", len(df))
    
    # 4. Save to CSV
    df.to_csv("eurusd_data.csv")
    print("\nSuccess! Raw data saved to eurusd_data.csv")

except Exception as e:
    print(f"Error during data pull: {e}")