# pipeline/extract.py
import os
import time
import datetime
import pandas as pd
from yahooquery import Ticker

DATA_DIR = "data/raw"
YEARS = 2
LOG_FILE = "logs/missing_stocks.txt"

# throttling / resilience
MAX_RETRIES = 3
RETRY_SLEEP = 2.0            # seconds, backoff multiplier
REQUEST_SLEEP = 0.25         # seconds between tickers (~4 req/s)
BATCH_PAUSE_EVERY = 50       # pause every N tickers to be polite
BATCH_PAUSE_SECS = 5         # seconds to pause

def to_yahoo_symbol(symbol: str) -> str:
    """
    Convert symbols like 'BRK.B' -> 'BRK-B' for Yahoo, strip spaces.
    """
    return symbol.replace(".", "-").strip()

def log_missing(ticker: str):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{ticker}\n")

def save_raw(df: pd.DataFrame, ticker: str, folder: str = DATA_DIR):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{ticker}_raw.csv")
    df.to_csv(path)
    print(f"✅ Saved {ticker} → {path}")

def download_ticker(ticker: str, years: int = YEARS) -> pd.DataFrame | None:
    """
    Download 2y daily history for a single ticker via yahooquery.
    Returns DataFrame (indexed by date) or None on failure/empty.
    """
    end = datetime.date.today()
    start = end - datetime.timedelta(days=365 * years)
    ysym = to_yahoo_symbol(ticker)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            tk = Ticker(ysym)
            # history accepts ISO dates; returns DataFrame or empty
            df = tk.history(start=start.isoformat(), end=end.isoformat(), interval="1d")

            # yahooquery may return a Series with an error payload
            if isinstance(df, pd.Series):
                raise RuntimeError(f"yahooquery error: {df.to_dict()}")

            if df is None or df.empty:
                return None

            # When multiple symbols are requested, history returns a MultiIndex.
            # For single symbol it can still return MultiIndex, so handle both.
            if isinstance(df.index, pd.MultiIndex):
                # level 0 is symbol, level 1 is datetime
                try:
                    df = df.xs(ysym)
                except KeyError:
                    # Sometimes symbol keys come back upper/lower; fallback to first level
                    df = df.droplevel(0)

            # Ensure datetime index and sort
            if not isinstance(df.index, pd.DatetimeIndex):
                if "date" in df.columns:
                    df = df.set_index(pd.to_datetime(df["date"]))
                    df = df.drop(columns=["date"], errors="ignore")
            df = df.sort_index()

            # Keep common OHLCV fields if present (yahooquery is lower-case)
            keep = [c for c in ["open", "high", "low", "close", "adjclose", "volume", "dividends", "splits"] if c in df.columns]
            if keep:
                df = df[keep]

            return df

        except Exception as e:
            if attempt == MAX_RETRIES:
                print(f"❌ {ticker}: {e}")
                return None
            time.sleep(RETRY_SLEEP * attempt)

def run_extraction(tickers: list[str], skip_existing: bool = True):
    success = 0
    fail = 0

    for i, ticker in enumerate(tickers, start=1):
        out_path = os.path.join(DATA_DIR, f"{ticker}_raw.csv")
        if skip_existing and os.path.exists(out_path):
            print(f"⏭️  Skipping {ticker} (already exists)")
        else:
            df = download_ticker(ticker)
            if df is not None and not df.empty:
                save_raw(df, ticker)
                success += 1
            else:
                print(f"⚠️ No data for {ticker}")
                log_missing(ticker)
                fail += 1

            # polite throttling
            time.sleep(REQUEST_SLEEP)
            if i % BATCH_PAUSE_EVERY == 0:
                print(f"⏸️  Pausing {BATCH_PAUSE_SECS}s after {i} tickers to avoid rate limits...")
                time.sleep(BATCH_PAUSE_SECS)

    print(f"\n📊 Extraction complete: {success} tickers saved, {fail} failed.")
    if fail > 0:
        print(f"⚠️ See {LOG_FILE} for details.")
