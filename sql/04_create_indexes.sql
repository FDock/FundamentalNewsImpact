-- =============================================
-- PROJECT: SP500 CFD short-term reaction to High-Impact News
-- AUTHOR: FDock
-- PURPOSE: Create indexes to optimize query performance
-- =============================================

-- Time-based indexes for joins
CREATE INDEX IF NOT EXISTS idx_news_datetime ON news_releases_clean(datetime);
CREATE INDEX IF NOT EXISTS idx_tick_datetime ON tick_data(datetime);

-- Event filtering
CREATE INDEX IF NOT EXISTS idx_news_event ON news_releases_clean(event);

-- Optional: for date-based joins
CREATE INDEX IF NOT EXISTS idx_news_date ON news_releases_clean(date);
CREATE INDEX IF NOT EXISTS idx_tick_date ON tick_data(date);
