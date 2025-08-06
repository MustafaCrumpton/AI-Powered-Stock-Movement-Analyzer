import yfinance as yf
import pandas as pd
from newsFetcher import get_news_for_ticker


def get_stock_data_period(ticker: str, period: str = "1mo") -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)

    if df.empty:
        raise ValueError(f"No data returned for {ticker} over period '{period}'.")

    # Add percent change column
    df["Change (%)"] = df["Close"].pct_change() * 100
    df.dropna(inplace=True) #removes columns where no % change exists (NaN)

    return df


def get_significant_dates(df: pd.DataFrame, threshold: float = 3.0) -> list: 
    """
    Returns a list of dates where the stock moved more than the given % threshold. This ensures significant news is gathered.
    """
    return df[abs(df["Change (%)"]) > threshold].index.strftime("%Y-%m-%d").tolist()


def get_news_for_significant_dates(ticker, period, api_key): #api key provided by finnhub
    df = get_stock_data_period(ticker, period)
    sig_dates = get_significant_dates(df)

    all_news = []
    for date in sig_dates:
        articles = get_news_for_ticker(ticker, date, api_key) #TODO this function will be completed later
        for article in articles:
            article["associated_date"] = date
        all_news.extend(articles)
    
    return all_news

if __name__ == "__main__":
    pass