import requests
from datetime import datetime, timedelta

def get_news_for_ticker(ticker, date, api_key):
    """
    Fetches company news for a specific ticker around a given date (±1 day).
    
    Args:
        ticker (str): Stock ticker symbol, e.g., 'AAPL'.
        date (str): Date string in 'YYYY-MM-DD' format.
        api_key (str): Finnhub API key.
        
    Returns:
        list of dicts: Each dict contains 'headline', 'summary', 'url', 'datetime'.
    """
    # Define the date range (1 day before and after)
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    from_date = (date_obj - timedelta(days=1)).strftime("%Y-%m-%d")
    to_date = (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")
    
    url = "https://finnhub.io/api/v1/company-news"
    params = {
        "symbol": ticker,
        "from": from_date,
        "to": to_date,
        "token": api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching news: {response.status_code}")
        return []
    
    data = response.json()
    news_items = []
    
    for item in data:
        news_items.append({
            "headline": item.get("headline"),
            "summary": item.get("summary"),
            "url": item.get("url"),
            "datetime": datetime.fromtimestamp(item.get("datetime")).strftime("%Y-%m-%d %H:%M:%S")
        })
        
    return news_items


def get_news_for_significant_dates(ticker, period, api_key):
    """
    For a given stock ticker and period, find significant price movement dates,
    then fetch news articles around those dates using Finnhub API.
    
    Args:
        ticker (str): Stock ticker symbol, e.g., 'AAPL'
        period (str): Time period for stock history, e.g., '1mo', '1y'
        api_key (str): Finnhub API key
        
    Returns:
        list of news articles (dicts), each with an 'associated_date' key
    """
    from data_collection import get_stock_data_period, get_significant_dates

    df = get_stock_data_period(ticker, period)
    sig_dates = get_significant_dates(df)

    all_news = []
    for date in sig_dates:
        articles = get_news_for_ticker(ticker, date, api_key)
        for article in articles:
            article["associated_date"] = date
        all_news.extend(articles)
        
    return all_news

#Test Code
""""
if __name__ == "__main__":
    API_KEY = "API_KEY_HERE" # <----
    ticker = "AAPL"
    date = "2025-08-01"
    news = get_news_for_ticker(ticker, date, API_KEY)
    print(f"Fetched {len(news)} news articles for {ticker} around {date}:")
    for article in news[:3]:
        print(article["headline"])
"""