# app/app.py for main dashboard

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import company names mapping
from pipeline.config_sp500 import SP500_COMPANIES  

PROCESSED_DIR = "data/processed"
FORECAST_DIR = "data/forecasts"
FUNDAMENTALS_FILE = "data/fundamentals/fundamentals.parquet"

# ------------------------
# Utility Functions
# ------------------------
def load_ticker_data(ticker):
    """Load processed Parquet file for a given ticker."""
    path = os.path.join(PROCESSED_DIR, f"{ticker}.parquet")
    if not os.path.exists(path):
        return None
    return pd.read_parquet(path)

def load_forecast_data(ticker):
    """Load Prophet forecast CSV for a given ticker."""
    path = os.path.join(FORECAST_DIR, f"{ticker}_forecast.csv")
    if not os.path.exists(path):
        return None
    return pd.read_csv(path, parse_dates=["ds"])

def load_fundamentals():
    """Load fundamentals dataset (parquet)."""
    if os.path.exists(FUNDAMENTALS_FILE):
        return pd.read_parquet(FUNDAMENTALS_FILE)
    return None


# ------------------------
# Streamlit Setup
# ------------------------
st.set_page_config(page_title="S&P 500 Dashboard", layout="wide")
st.title("📊 S&P 500 Stock Insights Dashboard")

# Sidebar
all_tickers = [f.replace(".parquet", "") for f in os.listdir(PROCESSED_DIR) if f.endswith(".parquet")]

# Create mapping: ticker -> "TICKER – Company Name"
ticker_labels = {t: f"{t} – {SP500_COMPANIES.get(t, 'Unknown')}" for t in all_tickers}

# Sidebar dropdown with full company names
selected_label = st.sidebar.selectbox("Select a Company", sorted(ticker_labels.values()))

# Reverse lookup: find ticker from selected label
ticker = [t for t, lbl in ticker_labels.items() if lbl == selected_label][0]

df = load_ticker_data(ticker)
fundamentals_df = load_fundamentals()

if df is not None:
    # ------------------------
    # KPI Section
    # ------------------------
    st.subheader(f"{ticker_labels[ticker]} Overview")
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    change = ((latest['Close'] - prev['Close']) / prev['Close']) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${latest['Close']:.2f}", f"{change:.2f}%")
    col2.metric("52W High", f"${df['Close'].max():.2f}")
    col3.metric("52W Low", f"${df['Close'].min():.2f}")

    # ------------------------
    # Tabs
    # ------------------------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Price & Indicators", "📊 Performance Summary", "🔮 Forecast", "📊 Multi-Ticker Comparison"]
    )

    
    # ---- Tab 1: Price, Indicators & Fundamentals ----
    with tab1:
        st.write("### Interactive Technical Chart")

        viz_option = st.selectbox(
            "Select Visualization",
            ["Candlestick + EMA/VWAP", "Relative Strength Index (RSI)", "Volatility (ATR)"]
        )

        if viz_option == "Candlestick + EMA/VWAP":
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                name="Price"
            ))
            if "EMA_20" in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df["EMA_20"], line=dict(color="blue", width=1), name="EMA 20"))
            if "EMA_50" in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df["EMA_50"], line=dict(color="orange", width=1), name="EMA 50"))
            if "VWAP" in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df["VWAP"], line=dict(color="green", width=1), name="VWAP"))
            fig.update_layout(xaxis_rangeslider_visible=False, height=600)
            st.plotly_chart(fig, use_container_width=True)

        elif viz_option == "Relative Strength Index (RSI)":
            if "RSI_14" in df.columns:
                rsi_fig = go.Figure()
                rsi_fig.add_trace(go.Scatter(x=df.index, y=df["RSI_14"], line=dict(color="purple", width=1), name="RSI"))
                rsi_fig.add_hline(y=70, line=dict(color="red", dash="dash"))
                rsi_fig.add_hline(y=30, line=dict(color="green", dash="dash"))
                rsi_fig.update_layout(height=400, title="Relative Strength Index (14-day)")
                st.plotly_chart(rsi_fig, use_container_width=True)
            else:
                st.warning("RSI not available for this ticker.")

        elif viz_option == "Volatility (ATR)":
            if "Volatility_ATR" in df.columns:
                atr_fig = go.Figure()
                atr_fig.add_trace(go.Scatter(x=df.index, y=df["Volatility_ATR"], line=dict(color="gray", width=1), name="ATR"))
                atr_fig.update_layout(height=400, title="Volatility (ATR)")
                st.plotly_chart(atr_fig, use_container_width=True)
            else:
                st.warning("ATR not available for this ticker.")

        # ------------------------
        # Fundamentals Snapshot
        # ------------------------
        st.write("### 📊 Fundamentals Snapshot")

        if fundamentals_df is not None and ticker in fundamentals_df.index:
            row = fundamentals_df.loc[ticker]

            fundamentals = {
                "PE Ratio": row.get("PE_Ratio", "N/A"),
                "EPS": row.get("EPS", "N/A"),
                "Dividend Yield": row.get("Dividend_Yield", "N/A"),
                "Market Cap": row.get("Market_Cap", "N/A"),
                "Sector PE": row.get("Sector_PE", "N/A"),
            }

            col1, col2, col3, col4 = st.columns(4)

            # P/E Ratio with sector benchmark
            pe_color = "green" if fundamentals["PE Ratio"] != "N/A" and fundamentals["Sector PE"] != "N/A" and fundamentals["PE Ratio"] < fundamentals["Sector PE"] else "red"
            col1.metric("P/E Ratio", fundamentals["PE Ratio"], f"vs Sector {fundamentals['Sector PE']}")
            col2.metric("EPS", fundamentals["EPS"])
            col3.metric("Dividend Yield", fundamentals["Dividend Yield"])
            col4.metric("Market Cap", fundamentals["Market Cap"])
        else:
            st.warning("No fundamentals available for this company.")


    # ---- Tab 2: Performance Summary ----
    with tab2:
        st.write("### Returns Summary")
        returns = {
            "1W": df["Close"].pct_change(5).iloc[-1] * 100,
            "1M": df["Close"].pct_change(21).iloc[-1] * 100,
            "6M": df["Close"].pct_change(126).iloc[-1] * 100,
            "1Y": df["Close"].pct_change(252).iloc[-1] * 100,
            "2Y": (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100,
        }
        perf_df = pd.DataFrame.from_dict(returns, orient="index", columns=["Return %"]).round(2)
        st.dataframe(perf_df.style.background_gradient(cmap="RdYlGn"))

    # ---- Tab 3: Forecast ----
    with tab3:
        st.write("### Prophet Forecast (Next 7 Days)")
        forecast_df = load_forecast_data(ticker)

        if forecast_df is not None:
            fig_fc = go.Figure()
            fig_fc.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Historical", line=dict(color="blue")))
            fig_fc.add_trace(go.Scatter(x=forecast_df["ds"], y=forecast_df["yhat"], mode="lines+markers", name="Forecast", line=dict(color="red")))
            fig_fc.add_trace(go.Scatter(
                x=pd.concat([forecast_df["ds"], forecast_df["ds"][::-1]]),
                y=pd.concat([forecast_df["yhat_upper"], forecast_df["yhat_lower"][::-1]]),
                fill="toself", fillcolor="rgba(255,0,0,0.2)", line=dict(color="rgba(255,255,255,0)"),
                name="Confidence Interval", hoverinfo="skip"
            ))
            fig_fc.update_layout(height=400, xaxis_title="Date", yaxis_title="Price", showlegend=True)
            st.plotly_chart(fig_fc, use_container_width=True)
        else:
            st.info("No forecast available. Run forecast.py first.")

    # ---- Tab 4: Multi-Ticker Comparison ----
    with tab4:
        st.write("### Compare Multiple Companies")
        tickers_selected_labels = st.multiselect(
            "Select companies to compare", 
            sorted(ticker_labels.values()), 
            default=[ticker_labels.get(ticker, ticker), "AAPL – Apple Inc.", "MSFT – Microsoft"]
        )

        # Convert back from labels -> tickers
        tickers_selected = [t for t, lbl in ticker_labels.items() if lbl in tickers_selected_labels]

        data_dict = {}
        for t in tickers_selected:
            df_t = load_ticker_data(t)
            if df_t is not None:
                df_t = df_t[["Close"]].copy()
                df_t["Normalized"] = df_t["Close"] / df_t["Close"].iloc[0] * 100
                data_dict[t] = df_t

        if data_dict:
            compare_fig = go.Figure()
            for t, d in data_dict.items():
                compare_fig.add_trace(go.Scatter(x=d.index, y=d["Normalized"], name=ticker_labels.get(t, t)))
            compare_fig.update_layout(height=500, title="Normalized Price Performance (rebased to 100)")
            st.plotly_chart(compare_fig, use_container_width=True)

            returns = {ticker_labels.get(t, t): (d["Close"].iloc[-1] / d["Close"].iloc[0] - 1) * 100 for t, d in data_dict.items()}
            returns_df = pd.DataFrame.from_dict(returns, orient="index", columns=["Return %"]).sort_values("Return %", ascending=False)

            bar_fig = go.Figure([go.Bar(x=returns_df.index, y=returns_df["Return %"], marker_color="teal")])
            bar_fig.update_layout(height=400, title="Cumulative Return (%)")
            st.plotly_chart(bar_fig, use_container_width=True)
