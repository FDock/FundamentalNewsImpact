-- =============================================
-- PROJECT: SP500 CFD short-term reaction to High-Impact News
-- AUTHOR: FDock
-- PURPOSE: Create delta views for tick-level price reaction to news
-- =============================================

-- DROP old views if they exist
DROP VIEW IF EXISTS event_price_delta_1min;
DROP VIEW IF EXISTS event_price_delta_5min;
DROP VIEW IF EXISTS event_price_delta_15min;

-- 1 MIN WINDOW
CREATE VIEW event_price_delta_1min AS
WITH before_tick AS (
    SELECT nr.datetime AS event_datetime,
           nr.event,
           td.bid AS before_bid,
           td.ask AS before_ask
    FROM news_releases_clean nr
    LEFT JOIN tick_data td
        ON td.datetime = (
            SELECT MAX(t1.datetime)
            FROM tick_data t1
            WHERE t1.datetime < nr.datetime
              AND t1.datetime >= datetime(nr.datetime, '-1 minute')
        )
),
after_tick AS (
    SELECT nr.datetime AS event_datetime,
           nr.event,
           td.bid AS after_bid,
           td.ask AS after_ask
    FROM news_releases_clean nr
    LEFT JOIN tick_data td
        ON td.datetime = (
            SELECT MIN(t1.datetime)
            FROM tick_data t1
            WHERE t1.datetime > nr.datetime
              AND t1.datetime <= datetime(nr.datetime, '+1 minute')
        )
)
SELECT 
    b.event_datetime,
    b.event,
    b.before_bid,
    a.after_bid,
    ROUND(a.after_bid - b.before_bid, 4) AS delta_bid,
    b.before_ask,
    a.after_ask,
    ROUND(a.after_ask - b.before_ask, 4) AS delta_ask
FROM before_tick b
JOIN after_tick a
    ON b.event_datetime = a.event_datetime AND b.event = a.event;

-- 5 MIN WINDOW
CREATE VIEW event_price_delta_5min AS
WITH before_tick AS (
    SELECT nr.datetime AS event_datetime,
           nr.event,
           td.bid AS before_bid,
           td.ask AS before_ask
    FROM news_releases_clean nr
    LEFT JOIN tick_data td
        ON td.datetime = (
            SELECT MAX(t1.datetime)
            FROM tick_data t1
            WHERE t1.datetime < nr.datetime
              AND t1.datetime >= datetime(nr.datetime, '-5 minute')
        )
),
after_tick AS (
    SELECT nr.datetime AS event_datetime,
           nr.event,
           td.bid AS after_bid,
           td.ask AS after_ask
    FROM news_releases_clean nr
    LEFT JOIN tick_data td
        ON td.datetime = (
            SELECT MIN(t1.datetime)
            FROM tick_data t1
            WHERE t1.datetime > nr.datetime
              AND t1.datetime <= datetime(nr.datetime, '+5 minute')
        )
)
SELECT 
    b.event_datetime,
    b.event,
    ROUND(a.after_bid - b.before_bid, 4) AS delta_bid_5m,
    ROUND(a.after_ask - b.before_ask, 4) AS delta_ask_5m
FROM before_tick b
JOIN after_tick a
    ON b.event_datetime = a.event_datetime AND b.event = a.event;

-- 15 MIN WINDOW
CREATE VIEW event_price_delta_15min AS
WITH before_tick AS (
    SELECT nr.datetime AS event_datetime,
           nr.event,
           td.bid AS before_bid,
           td.ask AS before_ask
    FROM news_releases_clean nr
    LEFT JOIN tick_data td
        ON td.datetime = (
            SELECT MAX(t1.datetime)
            FROM tick_data t1
            WHERE t1.datetime < nr.datetime
              AND t1.datetime >= datetime(nr.datetime, '-15 minute')
        )
),
after_tick AS (
    SELECT nr.datetime AS event_datetime,
           nr.event,
           td.bid AS after_bid,
           td.ask AS after_ask
    FROM news_releases_clean nr
    LEFT JOIN tick_data td
        ON td.datetime = (
            SELECT MIN(t1.datetime)
            FROM tick_data t1
            WHERE t1.datetime > nr.datetime
              AND t1.datetime <= datetime(nr.datetime, '+15 minute')
        )
)
SELECT 
    b.event_datetime,
    b.event,
    ROUND(a.after_bid - b.before_bid, 4) AS delta_bid_15m,
    ROUND(a.after_ask - b.before_ask, 4) AS delta_ask_15m
FROM before_tick b
JOIN after_tick a
    ON b.event_datetime = a.event_datetime AND b.event = a.event;
