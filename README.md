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
## 🏗️ Architecture
The following diagram illustrates the data flow and deployment architecture of the project:

![Architecture](Flowchart%20and%20Demo%20Pictures/Architecture_of_Project.png)

---

## ⚙️ Tech Stack

**Languages & Libraries**
- Python (Pandas, NumPy, Plotly, Streamlit, Prophet)
- Matplotlib (for visualization styles)
- PyArrow / Parquet (efficient storage)

**Machine Learning & Forecasting**
- Facebook Prophet (time series forecasting)
- Technical indicators (EMA, VWAP, RSI, ATR)

**Data Storage & Cloud**
- AWS S3 (data lake for processed + forecasted data)
- AWS EC2 (hosting the dashboard)
- IAM Roles & Policies (secure access)

**DevOps & Deployment**
- Docker (containerized app for reproducibility)
- GitHub Actions (CI/CD pipeline: auto-deploy to EC2)
- Bash (sync scripts, automation)

---

## 🎥 Demo  

### 🚀 Live Dashboard  
🔗 [Click here to explore the live S&P 500 Dashboard](http://13.42.17.17:8503/)  

> ⚠️ **Note:** The dashboard is hosted on an AWS EC2 instance. It may take a few seconds to load or could be offline outside active hours.  

### 🌐 System Architecture  
![Architecture](Flowchart%20and%20Demo%20Pictures/Architecture_of_Project.png)  

### 🖼️ Dashboard Screenshots  
![Demo Screenshot](Flowchart%20and%20Demo%20Pictures/Demo1.png)  

### 🎬 Dashboard in Action  
![Dashboard Demo 1](Flowchart%20and%20Demo%20Pictures/SP500Dashboard-gif1.gif)  
*Candlestick charts, EMA, VWAP, RSI, ATR indicators*  

![Dashboard Demo 2](Flowchart%20and%20Demo%20Pictures/SP500Dashboard-gif2.gif)  
*Prophet forecasts, fundamentals, and multi-ticker comparison*  


---

## Setup & Installation
Clone the Repository:
```
git clone https://github.com/VatsalSangani/S-P500_stock_forecasting_dashboard.git
cd S-P500_stock_forecasting_dashboard
```

Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

Install Dependencies:
```
pip install -r requirements_dashboard.txt
```

Run the dashboard locally:
```
streamlit run app/app.py
```

---

## ☁️ Deployment
- Data Pipeline: Local ETL + Prophet forecasting → upload processed + forecast data to AWS S3.
- Sync Script: EC2 instance uses scripts/sync_s3.sh to pull fresh data from S3.
- CI/CD: GitHub Actions automatically deploys updates to EC2 using Docker.
- Hosting: Streamlit dashboard runs in a container on EC2 (t3.micro) at port 8502.

---

## 🛠️ Future Improvements
- Automate weekly pipeline using Apache Airflow or AWS Lambda + EventBridge.
- Expand fundamentals with more financial ratios (ROE, Debt/Equity, etc.).
- Introduce user authentication for role-based dashboards (analyst vs manager).
- Optimize deployment using Kubernetes (k3s) + Terraform for production scaling.

---

## 📜 License
This project is licensed under the **MIT License** – you are free to use, modify, and distribute it with attribution.  
*(For academic and educational purposes only – not intended for financial trading or investment advice.)*

---

## 🤝 Acknowledgements
- [Streamlit](https://streamlit.io/) – for building interactive dashboards  
- [Plotly](https://plotly.com/) – for beautiful charts and candlesticks  
- [yFinance](https://pypi.org/project/yfinance/) – for stock price data  
- [Alpha Vantage](https://www.alphavantage.co/) – for fundamentals & indicators  
- [Facebook Prophet](https://facebook.github.io/prophet/) – for time-series forecasting  
- [AWS](https://aws.amazon.com/) – EC2 & S3 infrastructure  
- [GitHub Actions](https://github.com/features/actions) – CI/CD automation  

---

## 📬 Contact
👤 **Vatsal Sangani**  
- GitHub: [VatsalSangani](https://github.com/VatsalSangani)  
- LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com/in/vats-sangani/)    

If you found this project useful, feel free to ⭐ the repo and connect with me!

---
