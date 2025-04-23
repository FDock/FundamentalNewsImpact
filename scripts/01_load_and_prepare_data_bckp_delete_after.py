import os
import sqlite3
import pandas as pd
import yfinance as yf
from fredapi import Fred

from config import FRED_API_KEY
from utils.paths import DB_PATH, RAW_DATA_DIR

# === CONNECT TO DATABASE ===
conn = sqlite3.connect(DB_PATH)

# === Initialize FRED ===
fred = Fred(api_key=FRED_API_KEY)


# --- Load tick data ---
try:
    tick_df = pd.read_csv(os.path.join(RAW_DATA_DIR, "tick_data.csv"))
    tick_df.columns = ['datetime', 'bid', 'ask']  # ensure correct headers
    tick_df['datetime'] = pd.to_datetime(tick_df['datetime'])  # ✅ parse datetime
    tick_df.to_sql("tick_data", conn, if_exists="replace", index=False)
    print("✅ tick_data loaded into database.")
    print("🧮 Rows:", len(tick_df))
    print(tick_df.head())
except Exception as e:
    print(f"❌ Failed to load tick_data: {e}")

# --- Load news releases ---
try:
    news_df = pd.read_csv(os.path.join(RAW_DATA_DIR, "news_releases.csv"))
    news_df.columns = [col.strip().lower() for col in news_df.columns]  # normalize headers
    news_df['datetime'] = pd.to_datetime(news_df['datetime'])  # ✅ parse datetime
    news_df.to_sql("news_releases", conn, if_exists="replace", index=False)
    print("✅ news_releases loaded into database.")
    print("🧮 Rows:", len(news_df))
    print(news_df.head())
except Exception as e:
    print(f"❌ Failed to load news_releases: {e}")

# --- 1. Yield Curve ---
def fetch_yield_curve(start='2020-01-01'):
    y10 = fred.get_series('GS10', start)
    y2 = fred.get_series('GS2', start)
    df = pd.DataFrame({'treasury_10y': y10, 'treasury_2y': y2})
    df['spread'] = df['treasury_10y'] - df['treasury_2y']
    df = df.reset_index().rename(columns={'index': 'date'})
    df.to_sql('yield_curve', conn, if_exists='replace', index=False)

# --- 2. VIX Index (from Yahoo Finance) ---
def fetch_vix(start='2020-01-01'):
    vix = yf.download("^VIX", start=start)
    df = vix[['Close']].reset_index().rename(columns={'Close': 'vix_close', 'Date': 'date'})
    df.to_sql('vix_index', conn, if_exists='replace', index=False)

# --- 3. Macro Indicators (from FRED) ---
def fetch_macro_indicators():
    indicators = {
        'US GDP Growth': {'code': 'A191RL1Q225SBEA', 'unit': '%', 'frequency': 'quarterly'},
        'Unemployment Rate': {'code': 'UNRATE', 'unit': '%', 'frequency': 'monthly'},
        'CPI (All Urban Consumers)': {'code': 'CPIAUCSL', 'unit': 'index', 'frequency': 'monthly'},
        'Fed Funds Rate': {'code': 'FEDFUNDS', 'unit': '%', 'frequency': 'daily'},
        'M2 Money Supply': {'code': 'M2SL', 'unit': 'USD Bn', 'frequency': 'weekly'},
        '10-Year Treasury Yield': {'code': 'GS10', 'unit': '%', 'frequency': 'daily'},
        '2-Year Treasury Yield': {'code': 'GS2', 'unit': '%', 'frequency': 'daily'},
        'Consumer Sentiment (UMich)': {'code': 'UMCSENT', 'unit': 'index', 'frequency': 'monthly'}
    }

    rows = []
    for name, meta in indicators.items():
        try:
            series = fred.get_series(meta['code'], observation_start='2020-01-01')
            for date, value in series.items():
                rows.append({
                    'date': pd.to_datetime(date).date(),
                    'indicator_name': name,
                    'value': value,
                    'unit': meta['unit'],
                    'frequency': meta['frequency']
                })
            print(f"✅ {name} loaded")
        except Exception as e:
            print(f"❌ Failed to load {name}: {e}")

    df = pd.DataFrame(rows)
    df.to_sql('macro_indicators', conn, if_exists='replace', index=False)
    print("✅ All macro data saved to 'macro_indicators' table.")


def create_macro_regime_labels():
    df = pd.read_sql("SELECT * FROM macro_indicators", conn)
    pivot = df.pivot_table(index='date', columns='indicator_name', values='value', aggfunc='first').sort_index().ffill()
    pivot.index = pd.to_datetime(pivot.index)

    pivot['yield_spread'] = pivot['10-Year Treasury Yield'] - pivot['2-Year Treasury Yield']
    pivot['growth_regime'] = pivot['US GDP Growth'].apply(lambda x: 'recession' if x < 0 else 'expansion' if x > 1.5 else 'neutral')
    pivot['policy_regime'] = pivot['Fed Funds Rate'].diff().apply(lambda x: 'tightening' if x > 0 else 'easing' if x < 0 else 'neutral')
    pivot['yield_curve_regime'] = pivot['yield_spread'].apply(lambda x: 'inverted' if x < 0 else 'normal')
    pivot['sentiment_regime'] = pivot['Consumer Sentiment (UMich)'].apply(lambda x: 'bearish' if x < 70 else 'bullish' if x > 90 else 'neutral')
    pivot['inflation_regime'] = pivot['CPI (All Urban Consumers)'].pct_change(12).apply(lambda x: 'high' if x > 0.03 else 'normal')

    full_range = pd.date_range(start=pivot.index.min(), end=pivot.index.max(), freq='D')
    pivot = pivot.reindex(full_range).ffill()
    pivot.index.name = 'date'

    regime_cols = ['growth_regime', 'policy_regime', 'yield_curve_regime', 'sentiment_regime', 'inflation_regime']
    regime_df = pivot[regime_cols].reset_index().melt(id_vars='date', var_name='regime_type', value_name='regime_label')
    regime_df['date'] = regime_df['date'].dt.date
    regime_df.to_sql('market_regime', conn, if_exists='replace', index=False)
    print("✅ Daily forward-filled regime labels saved to 'market_regime'")


def create_daily_macro_summary():
    df = pd.read_sql("SELECT * FROM macro_indicators", conn)
    pivot = df.pivot_table(index='date', columns='indicator_name', values='value', aggfunc='first').sort_index()
    pivot.index = pd.to_datetime(pivot.index)

    full_range = pd.date_range(start=pivot.index.min(), end=pivot.index.max(), freq='D')
    pivot = pivot.reindex(full_range).ffill()
    pivot.index.name = 'date'

    pivot['yield_spread'] = pivot['10-Year Treasury Yield'] - pivot['2-Year Treasury Yield']
    pivot = pivot.reset_index()
    pivot['date'] = pivot['date'].dt.date
    pivot.to_sql('daily_macro_summary', conn, if_exists='replace', index=False)
    print("✅ Fully filled daily macro summary saved.")


# === Run All Steps ===
fetch_yield_curve()
fetch_vix()
fetch_macro_indicators()
create_macro_regime_labels()
create_daily_macro_summary()

# === Close Connection ===
conn.close()
print("🔌 SQLite connection closed.")
