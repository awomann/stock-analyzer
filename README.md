# Analysis of AI Stock Sentiment

## Business Problem & Research Question
The original research question was: does a week of negative news sentiment predict a price decline the following week? This requires historical headline data paired with historical price data for lag analysis. However, yfinance.news provides only current headlines, not historical archives.

Rather than force an unsupported analysis, the project was scoped to answer a related but achievable question: what is the current sentiment landscape for AI-centric stocks, and how does it align with their 3-year price trajectory?

## Data
**Price Data**
- Source: yfinance
- Tickers: AMD, GOOGL, META, MSFT, NVDA
- Time span: March 15, 2023 – March 15, 2026
- Fields: Daily OHLCV bars (~3,750 rows)

**Sentiment Data**
- Source: yfinance.news (current headlines only)
- Model: mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis via Hugging Face Inference API
- Sample: 10 most recent headlines per ticker (50 total)
- Scoring: 3-class classification (positive, neutral, negative) with confidence scores
- Distribution: Neutral 40%, Positive 38%, Negative 22%
- Mean confidence: 0.97

**Scope Decision**
Full lag analysis would require three years of archived headlines, unavailable via yfinance.news without a paid news API. The project pairs current sentiment snapshot with historical price data instead.

## Methodology
**Phase 1 — Ingest:** Fetched OHLCV price data and current headlines via yfinance. Stored in SQLite (headline_db.sqlite) across two tables: prices and headlines. Idempotent — checks for duplicates before inserting.

**Phase 2 — Sentiment Scoring:** Passed each headline to the Hugging Face Inference API and appended label and confidence score to the headlines table.

**Phase 3 — Analysis & Visualization:** Computed quarterly average close prices and rate of change per ticker. Generated interactive Plotly dashboard combining price trends and sentiment profiles.

## Findings
**Price Performance (Q1 2023 – Q1 2026)**
All five stocks demonstrated substantial gains over the three-year period:
Ticker / Rate of Change
- NVDA / +603.2%
- META / +224.7%
- GOOGL / +214.7%
- AMD / +123.8%
- MSFT / +58.0%
NVDA's gain is exceptional—nearly 10x the baseline S&P 500 performance over the same period. META and GOOGL also significantly outpaced the broader market. Even the slowest gainer, MSFT, returned nearly 58%, reflecting sustained institutional confidence in AI-adjacent equities.

**Sentiment-Price Alignment:** No obvious correspondence between current sentiment tone and historical price trajectory. Stocks with the strongest gains show balanced or neutral-leaning sentiment today — consistent with either market efficiency (appreciation already priced in) or the data limitation (no historical headlines for comparison).

## Limitations & Future Work

**Limitations**

- Current sentiment snapshot only — no lagged analysis possible without historical headline data
- Small sample (50 headlines) — directional only, limited statistical power
- Descriptive analysis only — no correlation tests or regression performed
- Survivorship bias — all five stocks appreciated; failed AI-adjacent companies not included

**Future Work**

- Ingest archived headlines via a historical news API to enable lag correlation analysis
- Test alternative financial NLP models (FinBERT) for comparison
- Expand to non-AI stocks to test whether findings are sector-specific

## How to Run
**How to Run**

**Prerequisites**
Python 3.8+, Hugging Face API token (free at huggingface.co/settings/access-tokens)

git clone https://github.com/awomann/stock-analyzer.git
cd stock-analyzer
pip install -r requirements.txt

Add your token to a .env file:
HF_TOKEN=your_token_here

Run the pipeline:
python -m src.analysis

Output: outputs/stock_dashboard.html — open in a browser to view.
First run takes 2–3 minutes. Subsequent runs are faster due to SQLite caching. To refresh headlines, delete headline_db.sqlite and re-run.

**Project Structure**
stock-analyzer/
├── src/
│   ├── __init__.py
│   ├── analysis.py       # Main pipeline
│   └── sentiment.py      # Hugging Face API wrapper
├── outputs/
│   └── stock_dashboard.html
├── headline_db.sqlite
├── stock_analyzer.ipynb
├── requirements.txt
└── README.md

