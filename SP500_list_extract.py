import pandas as pd

# Load CSV
df = pd.read_csv("constituents.csv")

# Create dictionary
SP500_COMPANIES = dict(zip(df["Symbol"], df["Security"]))

# Also create a plain list of tickers
SP500_TICKERS = list(SP500_COMPANIES.keys())

# Save into config_sp500.py
with open("config_sp500.py", "w", encoding="utf-8") as f:
    f.write("# Auto-generated from constituents.csv\n\n")
    f.write("SP500_COMPANIES = {\n")
    for symbol, name in SP500_COMPANIES.items():
        f.write(f'    "{symbol}": "{name}",\n')
    f.write("}\n\n")
    f.write("SP500_TICKERS = list(SP500_COMPANIES.keys())\n")

print(f"✅ Saved {len(SP500_COMPANIES)} companies into config_sp500.py")
