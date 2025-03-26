# **📈 Fundamental News Impact on SP500 Price Movements**

## **📌 Project Overview**

This project analyzes the relationship between major **economic news releases** and **S&P 500 CFD price movements**. By understanding how macroeconomic context and news affects short-term price behavior, we can study market reactions, design better trading systems, and explore predictive modeling.

It combines **tick-level financial data** with **macroeconomic indicators** to create a rich, structured dataset ready for analysis, visualization, and machine learning.

---

## **🔍 Objectives**

- Analyze **SP500 behavior before and after major economic news events**
- Join **high-frequency price data** with macro context and news metadata
- Label and track **macro regimes** (e.g., recession, high inflation)
- Build a foundation for **strategy development and modeling**

---

## **📊 Datasets Used**

| Dataset | Description |
|--------|-------------|
| `tick_data` | Tick-level SP500 CFD prices (bid/ask) |
| `news_releases` | Economic event data (e.g., NFP, CPI), with timestamps and values |
| `macro_indicators` | Raw macroeconomic data (GDP, CPI, Unemployment, etc.) |
| `market_regime` | Labeled daily macro regimes (growth, policy, sentiment, etc.) |
| `daily_macro_summary` | One-row-per-day macro snapshot (GDP, CPI, yield spread, etc.) |
| `yield_curve` | 10Y vs. 2Y Treasury yields and spread |
| `vix_index` | Daily VIX index values from Yahoo Finance |

---

## **⚙️ Technologies Used**

- **SQLite** for efficient local database storage
- **Pandas, FRED API, yFinance** for data collection and transformation
- **Jupyter Notebook** for analysis, querying, and exploratory work
- **SQL** for joins, filtering, and preprocessing

---

## **🧱 Project Structure & Pipeline**

1. ✅ Load and inspect **tick data** and **news events**
2. ✅ Clean and normalize all datetime formats
3. ✅ Enrich news data with macroeconomic context:
    - Add daily macro summaries
    - Add labeled macro regimes (recession, expansion, etc.)
4. ✅ Enable analysis-ready joins: `tick_data` ↔ `news_releases` ↔ `daily_macro_summary`
5. 🔜 Build intraday analysis and model reactions to macro surprises

---

## **🧹 Data Cleaning & Preprocessing**

### ✅ `news_releases`
- Removed out-of-scope or NULL dates
- Shifted timestamps from UTC → GMT+2
- Formatted to match tick data precision (`%Y-%m-%d %H:%M:%f`)
- Split datetime into `date` and `time` columns for easier joins

### ✅ `tick_data`
- Standardized tick timestamps
- Trimmed to match news event window
- Added `date` and `time` columns for SQL compatibility

---

## **🌐 Macro Data Integration**

We fetched the following indicators via FRED and Yahoo Finance:

| Indicator | FRED Code / Source | Frequency |
|----------|---------------------|-----------|
| Real GDP Growth | `A191RL1Q225SBEA` | Quarterly |
| CPI (All Urban) | `CPIAUCSL` | Monthly |
| Unemployment Rate | `UNRATE` | Monthly |
| Fed Funds Rate | `FEDFUNDS` | Daily |
| M2 Money Supply | `M2SL` | Weekly |
| 10Y & 2Y Treasury Yields | `GS10`, `GS2` | Daily |
| Consumer Sentiment | `UMCSENT` | Monthly |
| VIX Index | `^VIX` via yFinance | Daily |

---

## **📆 Daily Macro Summary**

We created a `daily_macro_summary` table by:

- **Pivoting macro data** to wide format
- **Forward-filling** missing days with latest known values
- **Calculating yield spread** (10Y – 2Y)
- Ensuring **one row per day**, joinable to `news_releases`

---

## **🧠 Macro Regime Labeling**

We created macro regime labels using logic like:

| Regime Type | Logic |
|-------------|-------|
| `growth_regime` | GDP < 0 → recession; GDP > 1.5 → expansion |
| `policy_regime` | Fed Rate rising → tightening |
| `yield_curve_regime` | Yield spread < 0 → inverted |
| `sentiment_regime` | Sentiment < 70 → bearish; > 90 → bullish |
| `inflation_regime` | CPI YoY > 3% → high inflation |

> All regime labels are forward-filled daily and stored in `market_regime`.

---

## **🔗 Time-Based Joins**

All data is now **synchronized on a daily level**, so we can run clean joins like:

```sql
SELECT nr.datetime, nr.event, dms."US GDP Growth", r1.regime_label AS growth_regime
FROM news_releases nr
LEFT JOIN daily_macro_summary dms ON DATE(nr.date) = dms.date
LEFT JOIN market_regime r1 ON DATE(nr.date) = r1.date AND r1.regime_type = 'growth_regime'
WHERE nr.impact = 'High Impact Expected'
