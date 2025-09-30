from pipeline import run_extraction, run_transformation, run_forecasts, SP500_TICKERS
import os

if __name__ == "__main__":
    print("🚀 Starting pipeline")

    # 1. Extract raw data (skip if already downloaded)
    # print("\n📥 Extracting raw stock data...")
    # run_extraction(SP500_TICKERS)

    # 2. Transform raw → processed
    print("\n🔧 Transforming raw data...")
    run_transformation()

    # 3. Forecast (Prophet → next 7 days)
    print("\n🔮 Running forecasts...")
    tickers = [t.replace(".parquet", "") for t in os.listdir("data/processed") if t.endswith(".parquet")]
    run_forecasts(tickers, days=7)

    print("\n✅ Pipeline complete! Dashboard is ready → run: streamlit run app/app.py")
