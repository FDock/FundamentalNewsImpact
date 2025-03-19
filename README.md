SP500 Price Movements

📌 Project Overview

This project analyzes the relationship between major economic news releases and SP500 CFD price movements. By understanding how news impacts price fluctuations, traders and analysts can refine trading strategies and risk management.

📊 Datasets Used

``: Tick-level price movements of SP500.

``: Economic news events with timestamps and impact levels.

🔍 Objective

Identify how major economic news releases influence SP500 prices.

Process tick-level and news data for cleaner, structured analysis.

Standardize and optimize datetime formats to enable efficient joins and queries.

📂 1. Examining and Understanding the CSV Data

Before importing large datasets, we used Jupyter Notebook to examine the CSV files, check data structure, and determine the correct delimiters.

📌 1.1 Previewing the First 10 Rows

To ensure we understood the dataset structure, we first examined the top 10 rows:

import pandas as pd

file_path = "C:/Users/Filip/Desktop/TickDataManager/Exported Tick Data/US500/USA_500_Index_GMT+2_US-DST_2_9_2025.csv"

# Read the first 10 lines to inspect structure
df = pd.read_csv(file_path, nrows=10)

# Display column names and preview data
print(df.head())
print(df.dtypes)

📌 1.2 Checking Last 10 Rows

To confirm the data consistency throughout the file, we also examined the last 10 rows:

# Efficient way to read the last 10 rows of a large CSV file
chunk_size = 100000  # Adjust based on file size
last_rows = pd.DataFrame()

for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    last_rows = chunk.tail(10)  # Keep only the last 10 rows of the last chunk

print(last_rows)

📌 1.3 Detecting Delimiters

To correctly import the CSV into SQLite, we checked which separator was being used:

df = pd.read_csv(file_path, sep=None, engine='python')  # Auto-detect delimiter
print(df.head())

After this inspection, we determined that the comma (``) was the correct delimiter, and we used it in the SQLite import process.

📂 2. Database Schema

``** Table**

CREATE TABLE tick_data (
    datetime DATETIME,  -- Tick timestamp
    bid REAL,           -- Bid price
    ask REAL            -- Ask price
);

``** Table**

CREATE TABLE news_releases (
    datetime DATETIME,  -- News release timestamp
    currency TEXT,      -- Currency affected
    event TEXT,         -- Event name
    impact TEXT,        -- Impact level (High, Medium, Low)
    actual REAL,        -- Actual reported value
    actual_unit TEXT,   -- Unit of actual value
    forecast REAL,      -- Forecasted value
    forecast_unit TEXT, -- Unit of forecast value
    previous REAL,      -- Previous reported value
    previous_unit TEXT, -- Unit of previous value
    previous_revised TEXT -- Any revision to previous value
);

🧹 3. Data Cleaning & Preprocessing

📌 3.1 Removing Excessive Dates

-- Remove old news before 2020-01-02
DELETE FROM news_releases WHERE datetime < '2020-01-02';

-- Remove future dates beyond 2024-12-27
DELETE FROM news_releases WHERE datetime > '2024-12-27';

-- Remove rows where datetime is NULL
DELETE FROM news_releases WHERE datetime IS NULL;

📌 3.2 Converting `` Timezone (UTC → GMT+2)

UPDATE news_releases
SET datetime = datetime(datetime, '+2 hours');

**📌 3.3 Formatting **** to Match **

UPDATE news_releases
SET datetime = strftime('%Y-%m-%d %H:%M:%f', datetime);

📌 3.4 Checking News Data After Cleaning

SELECT * FROM news_releases 
WHERE impact = 'High Impact Expected' AND currency = 'USD'
LIMIT 50;

🔄 4. Tick Data Formatting & Cleanup

📌 4.1 Reformatting `` (Ensuring Correct Format)

UPDATE tick_data
SET datetime = 
    SUBSTR(datetime, 1, 4) || '-' || 
    SUBSTR(datetime, 6, 2) || '-' || 
    SUBSTR(datetime, 9, 2) || ' ' || 
    SUBSTR(datetime, 12);

📌 4.2 Removing Tick Data Beyond `` Time Range

DELETE FROM tick_data WHERE datetime > '2024-12-27';

📆 5. Splitting `` & `` Columns

**📌 5.1 Adding `` Columns in **``

ALTER TABLE tick_data ADD COLUMN date TEXT;
ALTER TABLE tick_data ADD COLUMN time TEXT;

**📌 5.2 Populating `` Columns in **``

UPDATE tick_data
SET 
    date = strftime('%Y-%m-%d', datetime),
    time = strftime('%H:%M:%f', datetime);

**📌 5.3 Adding `` Columns in **``

ALTER TABLE news_releases ADD COLUMN date TEXT;
ALTER TABLE news_releases ADD COLUMN time TEXT;

**📌 5.4 Populating `` Columns in **``

UPDATE news_releases  
SET 
    date = strftime('%Y-%m-%d', datetime),
    time = strftime('%H:%M:%f', datetime);

📊 Next Steps

Perform analysis on SP500 price movements around major news events.

**Join **** and ** to examine price action before and after news releases.

Visualize market reactions using time-series plots.

Explore predictive modeling based on news impact trends.


