import yfinance as yf
import pandas as pd
import os
import sys
import time
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import tickers from config
from pipeline.config_sp500 import SP500_COMPANIES  

FUND_DIR = "data/fundamentals"
os.makedirs(FUND_DIR, exist_ok=True)

def fetch_fundamentals(ticker, retries=3):
    """Fetch fundamentals for a single ticker with retries."""
    for attempt in range(retries):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "Ticker": ticker,
                "Company": SP500_COMPANIES.get(ticker, "Unknown"),
                "PE_Ratio": info.get("trailingPE"),
                "Forward_PE": info.get("forwardPE"),
                "EPS": info.get("trailingEps"),
                "Dividend_Yield": info.get("dividendYield"),
                "Market_Cap": info.get("marketCap"),
                "Beta": info.get("beta"),
                "52W_High": info.get("fiftyTwoWeekHigh"),
                "52W_Low": info.get("fiftyTwoWeekLow"),
            }
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed for {ticker}: {e}")
            time.sleep(2)  # short wait before retry
    print(f"❌ Skipping {ticker} after {retries} failed attempts")
    return None

def batch_fetch_fundamentals(tickers, batch_size=25, delay=(1,3)):
    """Fetch fundamentals in batches with throttling."""
    all_data = []
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i+batch_size]
        print(f"📊 Processing batch {i//batch_size+1} / {len(tickers)//batch_size+1}: {batch}")
        
        for t in batch:
            data = fetch_fundamentals(t)
            if data:
                all_data.append(data)

            # Sleep between requests (avoid rate limits)
            time.sleep(random.uniform(*delay))

        # Save intermediate results
        df = pd.DataFrame(all_data)
        df.to_csv(os.path.join(FUND_DIR, f"fundamentals_partial_{i}.csv"), index=False)

    # Final save
    df = pd.DataFrame(all_data)
    df.to_csv(os.path.join(FUND_DIR, "sp500_fundamentals.csv"), index=False)
    print(f"✅ Saved {len(df)} tickers to sp500_fundamentals.csv")

    return df


if __name__ == "__main__":
    # Use the ticker list from config_sp500.py
    tickers = list(SP500_COMPANIES.keys())
    df_fundamentals = batch_fetch_fundamentals(tickers, batch_size=20, delay=(1,3))
    print(df_fundamentals.head())
    print("Fundamentals fetching complete.")