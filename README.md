# 📈 Fundamental News Impact on SP500 Price Movements

## 📌 Project Overview

This project analyzes the relationship between major **economic news releases** and **S&P 500 CFD price movements**. By understanding how macroeconomic context and news affects short-term price behavior, we can study market reactions, design better trading systems, and explore predictive modeling.

It combines **tick-level financial data** with **macroeconomic indicators** to create a rich, structured dataset ready for analysis, visualization, and machine learning.

---

## 🔍 Objectives

- Analyze **SP500 behavior before and after major economic news events**
- Join **high-frequency price data** with macro context and news metadata
- Label and track **macro regimes** (e.g., recession, high inflation)
- Build a foundation for **strategy development and modeling**

---

## 📊 Datasets Used

| Dataset | Description |
|--------|-------------|
| `tick_data` | Tick-level SP500 CFD prices (bid/ask) |
| `news_releases_clean` | Filtered economic events: only high-impact USD news |
| `macro_indicators` | Raw macroeconomic data (GDP, CPI, Unemployment, etc.) |
| `market_regime` | Labeled daily macro regimes (growth, policy, sentiment, etc.) |
| `yield_curve` | 10Y vs. 2Y Treasury yields and spread |
| `vix_index` | Daily VIX index values from Yahoo Finance |

---

## ⚙️ Technologies Used

- **SQLite** for efficient local database storage
- **Pandas, FRED API, yFinance** for data collection and transformation
- **Jupyter Notebook** for analysis, querying, and exploratory work
- **SQL** for joins, filtering, and preprocessing

---

## 🧱 Project Structure & Pipeline

1. ✅ Load and inspect **tick data** and **news events**
2. ✅ Clean and normalize all datetime formats
3. ✅ Filter news releases to retain only **USD high-impact events**
4. ✅ Remove low-activity trading hours from tick data
5. ✅ Enrich news data with macroeconomic context and regime labels
6. 🔜 Build intraday analysis and model reactions to macro surprises

---

## 🧹 Data Cleaning & Preprocessing

### ✅ `news_releases`
- Removed out-of-scope or NULL-dated entries
- Shifted timestamps from UTC → GMT+2
- Standardized datetime format to match tick data
- Created `news_releases_clean` table with only `USD` & `High Impact Expected` events
- Split datetime into `date` and `time` columns for easier joins

### ✅ `tick_data`
- Reformatted `datetime` to ensure consistency
- Removed out-of-range data beyond 2024-12-27
- Trimmed low-activity trading periods (outside 13:00–20:00 GMT)
- Added `date` and `time` columns for SQL operations
- Indexed `datetime` for fast joins with event data

---

## 📈 Indexes for Performance

To optimize analysis speed:

```sql
CREATE INDEX idx_news_datetime ON news_releases_clean(datetime);
CREATE INDEX idx_tick_datetime ON tick_data(datetime);
CREATE INDEX idx_news_event ON news_releases_clean(event);
