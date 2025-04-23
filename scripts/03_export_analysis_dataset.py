import os
import sqlite3
import pandas as pd
from utils.paths import DB_PATH, FINAL_DATASET_PATH

# === PREPARE OUTPUT DIR ===
os.makedirs(os.path.dirname(FINAL_DATASET_PATH), exist_ok=True)

# === CONNECT TO DB ===
conn = sqlite3.connect(DB_PATH)

# === LOAD DELTA VIEWS ===
print("📥 Loading event_price_delta_1min...")
df_1m = pd.read_sql("SELECT * FROM event_price_delta_1min", conn)

print("📥 Loading event_price_delta_5min...")
df_5m = pd.read_sql("SELECT * FROM event_price_delta_5min", conn)

print("📥 Loading event_price_delta_15min...")
df_15m = pd.read_sql("SELECT * FROM event_price_delta_15min", conn)

# === MERGE ALL DELTAS ===
df = df_1m.merge(df_5m, on=["event_datetime", "event"], how="left")
df = df.merge(df_15m, on=["event_datetime", "event"], how="left")

# === EXPORT TO CSV ===
df.to_csv(FINAL_DATASET_PATH, index=False)
print("📊 Final dataset shape:", df.shape)
print(f"✅ Exported analysis dataset to: {FINAL_DATASET_PATH}")

# === DONE ===
conn.close()
