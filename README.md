# 📈 Fundamental News Impact on SP500 Price Movements

## 📌 Project Overview

This project analyzes the relationship between major **economic news releases** and **S&P 500 CFD price movements**. By combining **tick-level financial data** with **macroeconomic indicators**, we build an automated data pipeline that enables high-resolution event-based analysis — suitable for quant research, trading signal development, or exploratory data science.

---

## 🔍 Objectives

- Study **price behavior before and after high-impact macroeconomic news**
- Join **tick-level SP500 data** with structured macro context
- Label and track **macro regimes** (e.g., expansion, recession, policy tightening)
- Create an analysis-ready dataset for modeling and backtesting
- Build a reproducible pipeline with SQL, Python, and Bash

---

## 📊 Datasets Used

| Dataset               | Description                                                  |
|----------------------|--------------------------------------------------------------|
| `tick_data`          | Tick-level S&P 500 CFD prices (bid/ask)                      |
| `news_releases_clean`| Filtered macro news (USD-only, high-impact events)           |
| `macro_indicators`   | Raw economic indicators (GDP, CPI, Unemployment, etc.)       |
| `market_regime`      | Macro regime labels (growth, policy, sentiment, yield)       |
| `yield_curve`        | 10Y vs. 2Y Treasury yields and spread                        |
| `vix_index`          | Daily VIX values from Yahoo Finance                          |

---

## ⚙️ Technologies Used

- **SQLite** for local database storage
- **Pandas, FRED API, yFinance** for Python-based data transformation
- **SQL** for cleaning, enrichment, and feature logic
- **Jupyter Notebook** for visual analysis
- **Git Bash / Bash** for automating end-to-end pipeline

---

## 🧱 Project Pipeline

```bash
bash scripts/run_pipeline.sh
```

### 🔄 What It Does:
- Creates all SQLite tables and views
- Loads tick/news data from local CSVs
- Downloads macro data via FRED and Yahoo
- Populates context tables like `market_regime`
- Cleans & filters the data
- Extracts tick windows around macro events (±1m, 5m, 15m)
- Exports the final structured dataset to CSV

---

## 🧹 Data Cleaning & Preprocessing

### ✅ `news_releases`
- Removed out-of-scope or NULL-dated entries
- Shifted timestamps from UTC → GMT+2
- Filtered to `USD` & `High Impact Expected` only
- Added `date` and `time` for easier joins

### ✅ `tick_data`
- Normalized `datetime` format
- Removed non-trading hours (13:00–20:00 GMT)
- Trimmed to match news dataset date range
- Derived `date` and `time` columns
- Indexed for performance

---

## 📈 Indexes for Performance

```sql
CREATE INDEX idx_news_datetime ON news_releases_clean(datetime);
CREATE INDEX idx_tick_datetime ON tick_data(datetime);
CREATE INDEX idx_news_event ON news_releases_clean(event);
```

---

## 📂 Folder Structure

```
sp500_news_reaction/
├── analysis/
│   └── tick_reaction_analysis.ipynb
├── data/
│   ├── raw/
│   ├── tick_windows/
│   └── final_analysis_dataset.csv
├── scripts/
│   ├── 01_load_and_prepare_data.py
│   ├── 02_extract_tick_data_by_event.py
│   ├── 03_export_analysis_dataset.py
│   ├── utils/
│   │   ├── paths.py
│   │   └── config.py
│   └── run_pipeline.sh
├── sql/
│   ├── 01_create_schema.sql
│   ├── 02_clean_news_releases.sql
│   ├── 03_clean_tick_data.sql
│   ├── 04_create_indexes.sql
│   └── 05_analysis_views.sql
├── database.db
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Next Steps

- Visualize pre/post news price moves by category
- Engineer features: delta sizes, volatility, sentiment alignment
- Build classification models for market direction
- Backtest rule-based strategies using event features
- Explore clustering by reaction type

---

## 🧠 Author

**FDock**  


---

## 🛡️ Suggested .gitignore

```gitignore
*.db
__pycache__/
.ipynb_checkpoints/
.env
*.csv
```
