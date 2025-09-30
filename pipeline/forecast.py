# Prophet forecast

import os
import pandas as pd
from prophet import Prophet

PROCESSED_DIR = "data/processed"
FORECAST_DIR = "data/forecasts"

def forecast_ticker(ticker, days=7):
    path = os.path.join(PROCESSED_DIR, f"{ticker}.parquet")
    if not os.path.exists(path):
        return None

    df = pd.read_parquet(path).copy()
    df = df.reset_index()  # ensure index is a column

    # Try to detect the date column
    if "Date" in df.columns:
        df = df.rename(columns={"Date": "ds"})
    elif "index" in df.columns:
        df = df.rename(columns={"index": "ds"})
    else:
        df = df.rename(columns={df.columns[0]: "ds"})  # fallback: assume first column is date

    # Ensure we have 'Close' -> 'y'
    if "Close" not in df.columns:
        print(f"⚠️ Skipping {ticker}: no Close column found")
        return None

    df = df.rename(columns={"Close": "y"})
    df = df[["ds", "y"]].dropna()

    if len(df) < 30:  # Prophet needs enough data
        print(f"⚠️ Skipping {ticker}: not enough data points ({len(df)})")
        return None

    # Train Prophet
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    # Forecast
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    forecast_df = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(days)
    return forecast_df

def run_forecasts(tickers, days=7):
    os.makedirs(FORECAST_DIR, exist_ok=True)
    for ticker in tickers:
        try:
            forecast_df = forecast_ticker(ticker, days)
            if forecast_df is not None:
                out_path = os.path.join(FORECAST_DIR, f"{ticker}_forecast.csv")
                forecast_df.to_csv(out_path, index=False)
                print(f"✅ Saved forecast for {ticker} → {out_path}")
        except Exception as e:
            print(f"❌ Error forecasting {ticker}: {e}")

if __name__ == "__main__":
    tickers = [f.replace(".parquet", "") for f in os.listdir(PROCESSED_DIR) if f.endswith(".parquet")]
    run_forecasts(tickers, days=7)
