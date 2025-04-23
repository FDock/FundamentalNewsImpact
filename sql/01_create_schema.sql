-- =============================================
-- PROJECT: SP500 CFD short-term reaction to High-Impact News
-- AUTHOR: FDock
-- PURPOSE: Analyze immediate impact of macroeconomic news on S&P 500 CFD for future strategy development
-- =============================================

-- === CLEAN UP EXISTING TABLES (FOR RERUNNING PIPELINE) ===
DROP TABLE IF EXISTS tick_data;
DROP TABLE IF EXISTS tick_data_backup;
DROP TABLE IF EXISTS news_releases;
DROP TABLE IF EXISTS macro_indicators;
DROP TABLE IF EXISTS market_regime;
DROP TABLE IF EXISTS yield_curve;
DROP TABLE IF EXISTS vix_index;

-- === CORE TABLES ===

CREATE TABLE tick_data (
    datetime DATETIME,
    bid REAL,
    ask REAL
);


CREATE TABLE news_releases (
    datetime DATETIME,
    currency TEXT,
    event TEXT,
    impact TEXT,
    actual REAL,
    actual_unit TEXT,
    forecast REAL,
    forecast_unit TEXT,
    previous REAL,
    previous_unit TEXT,
    previous_revised TEXT
);


-- === MACRO CONTEXT TABLES ===

CREATE TABLE macro_indicators (
    date DATE,
    indicator_name TEXT,
    value REAL,
    unit TEXT,
    frequency TEXT
);

CREATE TABLE market_regime (
    date DATE,
    regime_type TEXT,        -- 'growth_regime', 'policy_regime', etc.
    regime_label TEXT        -- 'expansion', 'recession', etc.
);

CREATE TABLE yield_curve (
    date DATE,
    treasury_10y REAL,
    treasury_2y REAL,
    spread REAL
);

CREATE TABLE vix_index (
    date DATE,
    vix_close REAL
);
