import os

# This file lives in: /scripts/utils/paths.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Jump two levels up: from /scripts/utils → /sp500_news_reaction
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

# Paths to key files and folders
DB_PATH = os.path.join(PROJECT_ROOT, "database.db")
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
TICK_WINDOW_DIR = os.path.join(PROJECT_ROOT, "data", "tick_windows")
FINAL_DATASET_PATH = os.path.join(PROJECT_ROOT, "data","final", "final_analysis_dataset.csv")

# Dev check
if __name__ == "__main__":
    print("✅ PROJECT_ROOT:", PROJECT_ROOT)
    print("📄 DB_PATH:", DB_PATH)
    print("📁 RAW_DATA_DIR:", RAW_DATA_DIR)
    print("📁 TICK_WINDOW_DIR:", TICK_WINDOW_DIR)
    print("📄 FINAL_DATASET_PATH:", FINAL_DATASET_PATH)