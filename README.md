# 📊 S&P 500 Stock Forecasting Dashboard

## 🚀 Introduction
The S&P 500 Stock Forecasting & Insights Dashboard is a complete end-to-end data pipeline and visualization platform designed to deliver stock insights, forecasts, and financial metrics for companies in the S&P 500 index.
This project automates the ETL pipeline (Extract → Transform → Load), generates time-series forecasts using machine learning, and provides an interactive dashboard for exploring stock performance, technical indicators, fundamentals, and predictions.

## ✨ Key Highlights

- End-to-end pipeline from data ingestion → processing → forecasting → dashboard.
- Technical + fundamental analysis combined in one platform.
- 7-day Prophet forecasts with confidence intervals.
- Weekly refresh from AWS S3 → EC2 without manual intervention.
- Dockerized deployment with GitHub Actions for continuous integration.


---

## 🚀 Features
- **ETL Pipeline** (local system → S3)
  - Extract historical stock data
  - Compute technical indicators (EMA, VWAP, RSI, ATR)
  - Fetch company fundamentals (P/E ratio, EPS, Dividend Yield, Market Cap, etc.)
  - Forecast future prices using **Facebook Prophet**
  - Upload processed + forecasted data to **AWS S3**

- **Dashboard (AWS EC2 + Docker)**
  - 📈 **Interactive charts**: candlestick, EMA, VWAP, RSI, ATR
  - 📊 **Fundamentals snapshot**: P/E ratio vs sector benchmark, EPS, dividends, market cap
  - 🔮 **7-day Prophet forecast** with confidence intervals
  - 📊 **Multi-ticker comparison** with normalized growth & returns
  - Weekly updated with fresh S3 data

- **Deployment**
  - **CI/CD pipeline with GitHub Actions**
  - **Dockerized app** (lightweight, reproducible environment)
  - **AWS EC2 hosting**, **AWS S3 storage**

---

## ⚙️ Tech Stack
  - Languages: Python, Pandas, Plotly, Streamlit
  - Data: yfinance / Yahooquery API
  - Forecasting: Prophet
  - Deployment: AWS EC2, AWS S3, Docker, GitHub Actions
  - Orchestration: Bash scripts + CI/CD automation

---
## 🏗️ Architecture
 ```mermaid
flowchart TD
   A[Local System: Upload Data] -->|Raw + Fundamentals| B[S3 Bucket (sp500-dashboard-data)]
   B --> C[EC2 Instance (Docker)]
   C -->|Fetches Data| B
   GitHub[GitHub Actions CI/CD] -->|SSH + Docker Deploy| C
   C --> D[Streamlit Dashboard (Port 8502)]
   D --> U[End User / Recruiter]

   %% Deployment Pipeline
   subgraph GitHubRepo[GitHub Repository + Actions]
       G1[Push Code to main] --> G2[GitHub Actions Workflow]
       G2 -->|Deploy via SSH| C
   end

   %% EC2 & Dashboard
   subgraph EC2Instance[AWS EC2 Instance]
       B -->|Sync Data (sync_s3.sh)| E1[Dockerized Streamlit Dashboard]
       E1 --> E2[Interactive Dashboard (8502)]
   end

   %% Users
   U -->|Access via Browser| E2
