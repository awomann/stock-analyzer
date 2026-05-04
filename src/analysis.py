import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from .sentiment import analyze_sentiment



stocks = ["NVDA", "META", "MSFT", "AMD", "GOOGL"]

df = yf.download(tickers=stocks, start="2023-03-15", end="2026-03-15")

headlines = []

for stock in stocks:
    news = yf.Ticker(stock).news
    for article in news:
        headlines.append({
            "ticker": stock,
            "title": article["content"]["title"],
            "date": article["content"]["pubDate"]
        })

headline_data = pd.DataFrame(headlines)

label_results = []
score_results = []

for title in headline_data["title"]:
    sentiment = analyze_sentiment(title)
    label_results.append(sentiment[0][0]["label"])
    score_results.append(sentiment[0][0]["score"])

headline_data["label"] = label_results
headline_data["score"] = score_results

reshaped_data = df["Close"].stack().reset_index().rename(columns={0: "close", "Ticker": "ticker", "Date": "date"})
reshaped_data = reshaped_data.set_index("date")

quarterly_close = reshaped_data.groupby(["ticker", pd.Grouper(freq="QE")])["close"].mean()
first_close = quarterly_close.groupby("ticker").first()
last_close = quarterly_close.groupby("ticker").last()
stock_roc = ((last_close - first_close) / first_close) * 100

quarterly_df = quarterly_close.reset_index()

price_chart = px.line(
    data_frame=quarterly_df, 
    x="date", 
    y="close", 
    color="ticker", 
    title="Q1 '23—Q2 '26 Quarterly Stock Prices"
    )

sentiment_count = headline_data.groupby(["ticker", "label"])["label"].count()
sentiment_df = sentiment_count.reset_index(name="count")

sentiment_chart = px.bar(
    data_frame=sentiment_df,
    x="ticker", 
    y="count", 
    color="label", 
    barmode="group",
    title="Recent News Headlines Sentiment", 
    color_discrete_map = {
        "positive": "#48a860", 
        "neutral": "#bebdb8", 
        "negative": "#cd5c5c"
        }
    )

fig = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=("Quarterly Close Price (2023-2026)", "Current News Sentiment by Ticker")
    )

for trace in price_chart.data:
    fig.add_trace(trace, row=1, col=1)

for trace in sentiment_chart.data:
    fig.add_trace(trace, row=2, col=1)

fig.update_layout(
    title_text="AI Stock Performance & Current Sentiment Analysis",
    height=800
)

for ticker in last_close.index:
    fig.add_annotation(
        x = "2026-03-31",
        y = last_close[ticker],
        text = f"+{stock_roc[ticker]:.1f}%",
        font = dict(size=10)
    )

fig.write_html("outputs/stock_dashboard.html")