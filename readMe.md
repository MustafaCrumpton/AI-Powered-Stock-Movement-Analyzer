## STILL IN PROGRESS

This project is an intelligent system that analyzes significant stock price movements and identifies news events that may have influenced them. By combining historical stock data, real-time news, and natural language processing (NLP), it provides insights into how public sentiment correlates with major market shifts.

##  What It Does

- Collects historical stock data for a given ticker and time period using `yFinance`.
- Automatically detects days with significant price movements based on customizable percentage thresholds.
- Fetches related financial news for those key dates using the Finnhub News API.
- Applies sentiment analysis using FinBERT (a finance-tuned BERT model) to quantify the tone of each news article.
- Outputs annotated results that show:
  - Date of significant movement
  - Related news headlines
  - Associated sentiment and confidence scores

##  Tech Stack

- **Python**
- **yFinance** – for historical stock data
- **Finnhub API** – for financial news
- **Transformers (FinBERT)** – for sentiment classification
- **Pandas** – for time series and data processing
- **Torch** – for deep learning inference
## Limitations:
Due to limitations in the yfinance library, this project is unable to draw stock data from specific dates. Rather, it draws the most significant news stories within the specified timeframe that can summarize why the stock has performed the way it has.
