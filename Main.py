from data_collection import get_stock_data_period
from data_collection import get_significant_dates
from newsFetcher import get_news_for_ticker
from sentiment_analysis import analyze_news_sentiment

def get_news_for_significant_dates(ticker, period, api_key):
    df = get_stock_data_period(ticker, period)
    sig_dates = get_significant_dates(df)

    all_news = []
    for date in sig_dates:
        articles = get_news_for_ticker(ticker, date, api_key)
        for article in articles:
            article["associated_date"] = date
        all_news.extend(articles)
    
    return all_news

if __name__ == "__main__":
    # === DEMO: Run full pipeline on a real stock ===
    ticker = "UNH"
    period = "1d"
    api_key = "d29a47pr01qhoenas9q0d29a47pr01qhoenas9qg"

    print(f"\n Running analysis for {ticker} over {period}...\n")

    try:
        # Step 1: Get news tied to significant price moves
        news_articles = get_news_for_significant_dates(ticker, period, api_key)

        if not news_articles:
            print("No significant news found for this period.")
        else:
            # Step 2: Analyze sentiment of that news
            analyzed = analyze_news_sentiment(news_articles)

            # Step 3: Display sample output
            print(f"\n News Sentiment for {ticker}:\n")
            for article in analyzed[:5]:  # show first 5
                print(f"{article['associated_date']} | {article['sentiment']} ({article['confidence']})")
                print(f"Headline: {article.get('headline')}")
                print(f"URL: {article.get('url', 'N/A')}\n")

    except Exception as e:
        print(f" Error during processing: {e}")

