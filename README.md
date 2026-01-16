# Bitcoin Market Data Pipeline (CoinGecko)

This project demonstrates an end-to-end data engineering and analytics pipeline using public market data from the CoinGecko API.
The pipeline follows a Bronze → Silver → Gold layered architecture with validation and visualization.

## 🥉 Bronze Layer - Data Ingestion

**Objective**

Fetch raw Bitcoin market data from an external API and store it without Modification.

**Details**

* Source: CoinGecko Market Chart API

* Data extracted:

    * Price

    * Market Capitalization

    * Total Volume Trading

* Raw API response is saved as JSON for traceability.

* A structured CSV is created from the raw response for downstream processing.

**Output**


```bash
data/raw/bitcoin_raw.json
data/raw/bitcoin_market_data.csv
```

### Attribution:
Data source: CoinGecko API

© CoinGecko

https://www.coingecko.com

## 🥈 Silver Layer - Data Cleaning & Normalization

**Objective**

Transform raw market data into a reliable daily time-series dataset.

**Transformations applied:**

* Checked for duplicate dates and applied aggregation rules where required:

    * Price → mean

    * Market Cap → mean

    * Volume → sum

* Created a complete daily date range (full_range) to ensure time-series continuity.

* Forward-filled missing values for:

    * Price

    * Market Capitalization

    * Filled missing volume values with 0.

* Implemented data quality validation:

* Asserted that no negative values exist in price, market cap, or volume.

* File is saved only if validation passes.

**Output**


```bash
data/processed/clean_bitcoin_market_data.csv
```

## 🥇 Gold Layer - Aggregation & Metrics

**Objective:**


Create business-ready monthly metrics for analysis.

**Transformations applied:**


* Created a YearMonth column for proper time-series aggregation.

* Aggregated metrics at monthly granularity:

    * Average Price

    * Average Market Capitalization

    * Total Volume

* Combined monthly metrics into a single Gold table using merges.

* Calculated Month-over-Month (MoM) percentage change for:

    * Average Price

    * Market Capitalization

    * Volume

**Output**


```bash
data/processed/bitcoin_monthly_metrics.csv
```


## 📈 Visualization Layer


**Objective:**


Validate trends and gain insights from the Gold dataset.


**Visualizations created:**

* Bar chart showing monthly average Bitcoin price.

* Combined bar + line chart:

    * Bars → Monthly average price

    * Line → Month-over-Month percentage change

* These visualizations were used to:

    * Validate aggregation correctness

    * Identify momentum shifts

    * Explain price movements over time


## 🛠️ Tech Stack 

* Python

* Pandas

* matplotlib

* requests

* python-dotenv

* Git & Github (versioning and release)


## 📌 Key Learnings:


* Built an API-driven data pipeline using layered architecture.


* Implemented time-series normalization and data quality checks.


* Applied defensive data engineering practices.


* Validated analytical results using both Python and visual inspection.
