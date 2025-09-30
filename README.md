# SP500 Stock Forecasting Pipeline

A portfolio-style project for automated ETL, forecasting, and dashboarding of SP500 stocks using yfinance, Prophet, and Streamlit.

## Structure

- **.github/workflows/pipeline.yml**: GitHub Actions workflow for scheduled runs
- **data/**: Processed datasets (auto-updated)
  - **raw/**: Raw yfinance downloads
  - **processed/**: Cleaned + indicators
  - **forecasts/**: Prophet forecast outputs
- **pipeline/**: Core ETL + forecasting modules
- **app/**: Streamlit dashboard app
- **logs/**: Logs of skipped/missing tickers
- **notebooks/**: Jupyter notebooks for EDA
- **main.py**: Orchestrator script
- **requirements.txt**: Python dependencies

## Usage

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run the pipeline: `python main.py`
4. Launch dashboard: `streamlit run app/app.py`
