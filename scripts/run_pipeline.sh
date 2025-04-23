set -e  # ⛔ stop on first error

#!/bin/bash

DB=./database.db

echo "⚙️  Building the database schema..."
sqlite3 $DB < sql/01_create_schema.sql

echo "📦 Loading raw data using Python (via py)..."
py scripts/01_load_and_prepare_data.py

echo "🧹 Running SQL cleaning steps..."
sqlite3 $DB < sql/02_clean_news_releases.sql
sqlite3 $DB < sql/03_clean_tick_data.sql
sqlite3 $DB < sql/04_create_indexes.sql
sqlite3 $DB < sql/05_analysis_views.sql

echo "📤 Extracting tick-by-tick windows..."
py scripts/02_extract_tick_data_by_event.py

echo "📄 Exporting final analysis dataset to CSV..."
py scripts/03_export_analysis_dataset.py

echo "✅ FULL PIPELINE COMPLETED SUCCESSFULLY!"
