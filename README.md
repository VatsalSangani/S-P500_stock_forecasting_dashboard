# 📊 S&P 500 Stock Forecasting Dashboard

An end-to-end **data engineering + data science pipeline** for analyzing and forecasting the **S&P 500 index companies**.  
The system combines **ETL, forecasting, fundamentals, and interactive dashboards**, deployed on **AWS EC2** with **S3 as storage** and **Docker + GitHub Actions for CI/CD**.

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

    %% Local ETL Pipeline
    subgraph Local["🖥️ Local Machine / Data Prep"]
        A1[Extract Raw Data<br/>(Yahoo Finance API)] --> A2[Transform Data<br/>(Indicators: EMA, VWAP, RSI, ATR)]
        A2 --> A3[Forecasting<br/>(Prophet 7-day Forecast)]
        A3 --> A4[Upload Processed + Forecasted Data]
    end

    %% AWS S3
    A4 -->|Upload| S3[(AWS S3<br/>sp500-dashboard-data)]

    %% Deployment Pipeline
    subgraph GitHub["🌐 GitHub Repo + Actions (CI/CD)"]
        G1[Push Code to main] --> G2[GitHub Actions Workflow]
        G2 -->|Deploy via SSH| EC2
    end

    %% EC2 & Dashboard
    subgraph EC2["⚡ AWS EC2 Instance"]
        S3 -->|Sync Data (sync_s3.sh)| E1[Dockerized Streamlit Dashboard]
        E1 --> E2[📊 Interactive Dashboard<br/>(8502 port)]
    end

    %% Users
    U[👨‍💻 End Users / Recruiters] -->|Access via Browser| E2
