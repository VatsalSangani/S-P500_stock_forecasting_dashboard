# Indicators, cleaning
import os
import pandas as pd
import ta  # technical indicators

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to Open, High, Low, Close, Adj Close, Volume."""
    rename_map = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "adjclose": "Adj Close",
        "volume": "Volume",
    }
    df = df.rename(columns={c: rename_map.get(c.lower(), c) for c in df.columns})
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add basic technical indicators using ta library."""
    df["EMA_20"] = ta.trend.EMAIndicator(close=df["Close"], window=20).ema_indicator()
    df["EMA_50"] = ta.trend.EMAIndicator(close=df["Close"], window=50).ema_indicator()
    df["RSI_14"] = ta.momentum.RSIIndicator(close=df["Close"], window=14).rsi()
    df["Volatility_ATR"] = ta.volatility.AverageTrueRange(
        high=df["High"], low=df["Low"], close=df["Close"], window=14
    ).average_true_range()
    df["VWAP"] = ta.volume.VolumeWeightedAveragePrice(
        high=df["High"], low=df["Low"], close=df["Close"], volume=df["Volume"]
    ).volume_weighted_average_price()
    return df


def process_file(file_path: str, output_dir: str = PROCESSED_DIR):
    """Process a single raw CSV into cleaned + enriched Parquet."""
    try:
        df = pd.read_csv(file_path, parse_dates=["date"], index_col="date")
    except Exception:
        df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")

    df = clean_columns(df)

    # Drop rows with NaN in OHLCV
    df = df.dropna(subset=["Open", "High", "Low", "Close", "Volume"])

    # Add indicators
    df = add_indicators(df)

    # Ensure output folder
    os.makedirs(output_dir, exist_ok=True)

    # Save as Parquet
    ticker = os.path.basename(file_path).replace("_raw.csv", "")
    out_path = os.path.join(output_dir, f"{ticker}.parquet")
    df.to_parquet(out_path)
    print(f"✅ Processed {ticker} → {out_path}")


def run_transformation():
    """Process all raw CSVs into Parquet files."""
    raw_files = [os.path.join(RAW_DIR, f) for f in os.listdir(RAW_DIR) if f.endswith("_raw.csv")]
    print(f"📊 Found {len(raw_files)} raw files to process")

    for file_path in raw_files:
        process_file(file_path)


if __name__ == "__main__":
    run_transformation()

