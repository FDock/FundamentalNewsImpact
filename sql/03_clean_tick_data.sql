-- =============================================
-- PROJECT: SP500 CFD short-term reaction to High-Impact News
-- AUTHOR: FDock
-- PURPOSE: Clean and trim tick-level data for alignment with macro news analysis
-- =============================================

-- Step 1: If needed, reformat datetime from raw string (manual cleanup)
-- Only do this if your tick CSV is poorly formatted (e.g. '20240101 13:00:00.123')
-- Otherwise, comment this block out
-- UPDATE tick_data
-- SET datetime = 
--     SUBSTR(datetime, 1, 4) || '-' || 
--     SUBSTR(datetime, 6, 2) || '-' || 
--     SUBSTR(datetime, 9, 2) || ' ' || 
--     SUBSTR(datetime, 12);

-- Step 2: Add derived date and time columns for joins and filtering
ALTER TABLE tick_data ADD COLUMN date TEXT;
ALTER TABLE tick_data ADD COLUMN time TEXT;

UPDATE tick_data
SET 
    date = strftime('%Y-%m-%d', datetime),
    time = strftime('%H:%M:%f', datetime);

-- Step 3: Trim excessive future data
DELETE FROM tick_data 
WHERE datetime > '2024-12-27';

-- Step 4: Remove ticks outside active trading hours (13:00–20:00 GMT)
DELETE FROM tick_data
WHERE time < '13:00:00.000' OR time > '20:00:00.000';
