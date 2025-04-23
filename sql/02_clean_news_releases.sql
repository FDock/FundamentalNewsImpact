-- =============================================
-- PROJECT: SP500 CFD short-term reaction to High-Impact News
-- AUTHOR: FDock
-- PURPOSE: Clean and filter raw macro news for modeling S&P500 price reactions
-- =============================================

-- Step 1: Remove null or out-of-range datetimes
DELETE FROM news_releases
WHERE datetime IS NULL 
   OR datetime < '2020-01-02'
   OR datetime > '2024-12-27';

-- Step 2: Convert datetime to GMT+2
UPDATE news_releases
SET datetime = datetime(datetime, '+2 hours');

-- Step 3: Standardize datetime format for compatibility
UPDATE news_releases
SET datetime = strftime('%Y-%m-%d %H:%M:%f', datetime);

-- Step 4: Create a cleaned + filtered version with added date/time columns
DROP TABLE IF EXISTS news_releases_clean;

CREATE TABLE news_releases_clean AS
SELECT *,
       strftime('%Y-%m-%d', datetime) AS date,
       strftime('%H:%M:%f', datetime) AS time
FROM news_releases
WHERE currency = 'USD'
  AND impact = 'High Impact Expected';
