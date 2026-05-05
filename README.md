# Analysis of AI Stock Sentiment

## Business Problem & Research Question
The original research question was: Does a week of negative news sentiment predict a price decline the following week? This would require historical headline data paired with historical price data for lag analysis.
However, yfinance.news provides only current headlines, not historical archives. Rather than force an unsupported lag analysis or introduce a paid news API dependency, the project was scoped to answer a related but achievable question: What is the current sentiment landscape for AI-centric stocks, and how does it align with their 3-year price trajectory?

This pairing—current sentiment snapshot + historical price context—allows us to assess whether market sentiment today reflects the substantial price gains over the past three years, and to identify any sentiment-price misalignment that might warrant further investigation.

## Data
**Price Data**
- Source: yfinance
- Tickers: AMD, GOOGL, META, MSFT, NVDA
- Time span: March 15, 2023 – Q1 2026 (3 years)
- Fields: Open, high, low, close, volume
- Frequency: Daily OHLCV bars
- Volume: ~750 trading days × 5 tickers = 3,750 rows

**Sentiment Data**
- Source: yfinance.news (current headlines only)
- Collection method: Headlines pulled via API and scored using distilroberta-finetuned-financial-news-sentiment-analysis, a DistilRoBERTa model fine-tuned on financial text.
- Sample size: 10 most recent headlines per ticker (50 total)
- Scoring: 3-class classification (positive, neutral, negative) with confidence scores per headline
- Overall sentiment distribution: Neutral 40%, Positive 38%, Negative 22%
- Quality: Mean confidence score 0.97 (median 0.998); only one headline below 0.55. High confidence across all predictions.

**Scope Decision**
Historical headline data was not available via yfinance.news, which returns only current headlines. A full lag analysis (negative sentiment → next-week price decline) would require three years of archived headlines—unavailable without a paid news API. Rather than introduce external dependencies, the project was scoped to pair current sentiment snapshot with historical price data to assess sentiment-price alignment (see Business Problem).

## Methodology
**Phase 1: Data Ingestion**
- Fetched daily OHLCV data for five stocks (AMD, GOOGL, META, MSFT, NVDA) from yfinance spanning March 15, 2023 – March 15, 2026.
- Fetched current news headlines for each stock via yfinance.Ticker().news API.
- Stored raw data in SQLite (headline_db.sqlite) across two tables: prices (ticker, date, close) and headlines (ticker, date, title, label, score).
- Script is idempotent: checks for duplicate headlines before inserting to avoid duplication on re-runs.

**Phase 2: Sentiment Scoring**
- Passed each headline through distilroberta-finetuned-financial-news-sentiment-analysis (DistilRoBERTa model fine-tuned on financial text).
- Model outputs: sentiment label (positive, neutral, negative) and confidence score.
- Appended results to headlines table for downstream analysis.

**Phase 3: Analysis & Visualization**
- Price trajectory: Computed quarterly average close prices for each stock across the 3-year window.
- Rate of change: Calculated percentage change from Q1 2023 close to Q1 2026 close for each ticker.
- Sentiment distribution: Aggregated headline counts by ticker and sentiment label to visualize current news tone.
- Dashboard: Generated interactive Plotly visualization (stock_dashboard.html) combining quarterly price trends with current sentiment profiles by ticker.

**Statistical Testing**
This project was scoped to descriptive analysis and visualization rather than formal hypothesis testing. The original hypothesis required three years of historical headline data (unavailable via yfinance.news); instead, the analysis pairs current sentiment snapshot with historical price context to assess alignment and identify patterns for future investigation.

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

**Current Sentiment Landscape**
Recent news sentiment (50 headlines, May 2026) is balanced across three categories:
- Neutral: 40% (business developments, earnings reports, product announcements)
- Positive: 38% (upside predictions, strong earnings, new deals)
- Negative: 22% (downgrades, capacity concerns, competitive pressures)

**Sentiment-Price Alignment**
The data reveals no obvious correspondence between current sentiment tone and historical price trajectory. Stocks with the strongest 3-year gains (NVDA, META, GOOGL) show balanced or neutral-leaning sentiment today, suggesting one of two possibilities:
- Market efficiency: Price appreciation has already incorporated positive long-term narratives about AI; current headlines reflect a more measured, informational tone rather than euphoria.
- Data limitation: Current sentiment snapshot cannot be compared to historical sentiment without three years of archived headlines. Correlation analysis would require paired historical data.

The high confidence of the sentiment model (mean 0.97, median 0.998) indicates reliable classification, but the lack of historical headlines prevents formal testing of whether sentiment predicts price movements at any lag.

## Limitations & Future Work

**Limitations**

**Data Scope**
- **Sentiment snapshot only:** Analysis uses 10 current headlines per ticker (50 total). Without three years of archived headlines, correlation between sentiment and price movement cannot be tested formally.
- **No lagged analysis:** The original hypothesis (negative sentiment → next-week price decline) requires paired historical data; `yfinance.news` provides current headlines only. A lag analysis was not possible without switching to a paid news API.
- **Small sample:** 50 headlines provide directional sentiment tone but limited statistical power for drawing generalizable conclusions.

**Model & Methodology**
- **Financial sentiment model:** DistilRoBERTa was fine-tuned on financial text but may misclassify nuanced language (e.g., "concerns about capacity" vs. "no capacity constraints"). Confidence scores are high, but domain-specific bias is possible.
- **Quarterly aggregation:** While quarterly alignment with financial reporting makes sense, it may smooth over intra-quarter volatility where sentiment-price relationships could exist.
- **Survivorship bias:** All five stocks survived the 3-year period and appreciated substantially. Failed or delisted AI-adjacent companies are absent from the analysis.

**Analytical Scope**
- **Descriptive vs. inferential:** Analysis is limited to visualization and ROC calculation. No correlation tests, regression, or statistical significance testing were performed due to lack of paired historical data.

**Future Work**

**Expand Historical Coverage**
- Ingest archived headlines (2023–present) from a historical news API (e.g., NewsAPI, Finnhub, Alpha Vantage) to enable three years of paired sentiment-price data.
- Compute lagged correlations (sentiment at time *t* vs. returns at time *t+1, t+2, etc.*) and test statistical significance.

**Refine Sentiment Analysis**
- Evaluate alternative financial NLP models (FinBERT, FinLLM) for comparison and sensitivity analysis.
- Implement manual review of low-confidence predictions (currently none, but useful for future datasets) to validate model outputs.
- Test sentiment aggregation methods beyond counts (e.g., weighted by confidence score, time decay for recency bias).

**Expand Analytical Methods**
- Test multiple time windows (daily, weekly, rolling 3-day) to identify which aggregation horizon best captures sentiment-price relationships.
- Incorporate alternative signals: headline volume (not just polarity), headline source credibility, analyst rating changes, options implied volatility.
- Perform backtesting on held-out recent data before deploying any signal as an investment heuristic.

**Broaden Stock Universe**
- Extend analysis to non-AI stocks to test whether sentiment-price relationships are sector-specific or general.
- Include failed or under-performing AI-adjacent companies to reduce survivorship bias.

## How to Run
**How to Run**

**Prerequisites**
- Python 3.8+
- Required packages: `yfinance`, `pandas`, `numpy`, `plotly`, `transformers`, `torch`

**Installation**
```bash
git clone https://github.com/awomann/stock-analyzer.git
cd stock-analyzer
pip install -r requirements.txt
```

**Running the Analysis**

1. **Execute the pipeline:**
   ```bash
   python -m src.analysis
   ```
   This script will:
   - Fetch 3 years of daily OHLCV data (2023-03-15 to 2026-03-15) for AMD, GOOGL, META, MSFT, NVDA
   - Fetch current news headlines via `yfinance.news`
   - Score each headline using the DistilRoBERTa financial sentiment model
   - Store price and headline data in `headline_db.sqlite` (idempotent; safe to re-run)
   - Generate quarterly price aggregations and sentiment counts
   - Output interactive dashboard to `outputs/stock_dashboard.html`

2. **View results:**
   Open `outputs/stock_dashboard.html` in a web browser to explore:
   - Quarterly close prices (2023–2026) for all five stocks
   - Rate of change (%) annotations for each ticker
   - Current sentiment distribution (positive, neutral, negative) by ticker

**Project Structure**
```
.
stock-analyzer/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── analysis.py          # Main pipeline (data ingest → sentiment → visualization)
│   └── sentiment.py         # Sentiment scoring wrapper (DistilRoBERTa inference)
├── outputs/
│   └── stock_dashboard.html # Interactive Plotly dashboard
├── headline_db.sqlite       # SQLite database (created on first run)
├── stock_analyzer.ipynb     # Jupyter notebook with exploratory analysis
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md
```

**Notes**
- First run will take 2–3 minutes (model download + API calls + inference)
- Subsequent runs are faster due to SQLite caching
- To refresh headlines, delete `headline_db.sqlite` and re-run
