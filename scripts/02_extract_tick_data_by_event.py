import os
import sqlite3
import pandas as pd
from datetime import timedelta

from utils.paths import DB_PATH, TICK_WINDOW_DIR

# === PREPARE OUTPUT FOLDER ===
os.makedirs(TICK_WINDOW_DIR, exist_ok=True)

# === CONNECT TO DB ===
conn = sqlite3.connect(DB_PATH)

# === Load high-impact news events ===
news_df = pd.read_sql("""
    SELECT datetime, event
    FROM news_releases_clean
    ORDER BY datetime
""", conn)

# Convert datetime to pandas Timestamp
news_df['datetime'] = pd.to_datetime(news_df['datetime'])

# === Extract tick data windows for each event ===
count = 0
for _, row in news_df.iterrows():
    event_time = row['datetime']
    event_label = row['event'].replace(' ', '_').replace('/', '_').replace(':', '')

    # Define window ranges
    windows = {
        '1m': (event_time - timedelta(minutes=1), event_time + timedelta(minutes=1)),
        '5m': (event_time - timedelta(minutes=5), event_time + timedelta(minutes=5)),
        '15m': (event_time - timedelta(minutes=15), event_time + timedelta(minutes=15))
    }

    for label, (start_time, end_time) in windows.items():
        query = f"""
            SELECT * FROM tick_data
            WHERE datetime BETWEEN '{start_time}' AND '{end_time}'
        """
        ticks = pd.read_sql(query, conn)

        if ticks.empty:
            continue  # Skip if no data

        filename = f"{event_time:%Y-%m-%d}_{event_label}_{label}.csv"
        filepath = os.path.join(TICK_WINDOW_DIR, filename)
        ticks.to_csv(filepath, index=False)
        count += 1

print(f"\n✅ Saved tick windows for {count} event slices to: {TICK_WINDOW_DIR}")
conn.close()
