import pandas as pd

def get_ftse100_tickers():
    """
    Scrape current FTSE 100 tickers from Wikipedia.
    Returns a list of Yahoo Finance tickers with `.L` suffix.
    """
    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
    tables = pd.read_html(url)
    df = tables[3]  # Constituents table (check Wikipedia index)
    tickers = df["EPIC"].tolist()
    tickers = [t + ".L" for t in tickers]
    return tickers
