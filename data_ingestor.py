# import requests, config
# from datetime import datetime, timedelta
#
# def fetch_trending_news():
#     # Calculate to a strict 48-hour time boundary
#     current_time = datetime.now()
#     time_window_start = current_time - timedelta(hours=48)
#
#     # Format dates into YYYY-MM-DD strings
#     date_to = current_time.strftime("%Y-%m-%d")
#     date_from = time_window_start.strftime("%Y-%m-%d")
#
#     ticker_string = " OR ".join([key for key in config.COMPANY_LOOKUP.keys() if key.isupper()])
#
#     params = {
#         "language": "en",
#         "sortBy": "relevancy",
#         "from": date_from,
#         "to": date_to,
#         "pageSize": config.MAX_NEWS_ARTICLES,
#         "apiKey": config.NEWS_API_KEY,
#         "q": f"({ticker_string}) OR stocks OR market OR earnings"
#     }
#
#     data = requests.get(url="https://newsapi.org/v2/everything", params=params)
#     data.raise_for_status()
#     data = data.json()
#
#     news_pool = []
#     for article in data.get("articles", []):
#         news_pool.append(article["title"])
#         news_pool.append(article.get("description", ""))
#     return news_pool
#
#
# if __name__ == '__main__':
#     news = fetch_trending_news()

import requests
import config
from datetime import datetime, timedelta


def fetch_trending_news():
    # Calculate a strict 48-hour time boundary
    current_time = datetime.now()
    time_window_start = current_time - timedelta(hours=48)

    # Finnhub requires dates formatted as YYYY-MM-DD
    date_to = current_time.strftime("%Y-%m-%d")
    date_from = time_window_start.strftime("%Y-%m-%d")

    # Extract just the upper-case ticker keys (e.g., ['AAPL', 'NVDA', 'TSLA'])
    tickers = [key for key in config.COMPANY_LOOKUP.keys() if key.isupper()]

    news_pool = []

    # 1. Fetch Company-Specific News for your portfolio tickers
    for ticker in tickers:
        params = {
            "symbol": ticker,
            "from": date_from,
            "to": date_to,
            "token": config.FINNHUB_API_KEY  # Finnhub authentication token parameter
        }

        try:
            response = requests.get("https://finnhub.io/api/v1/company-news", params=params)
            response.raise_for_status()
            articles = response.json()

            # Finnhub returns a top-level list of news dictionaries
            for article in articles:
                # 'headline' and 'summary' map to NewsAPI's 'title' and 'description'
                headline = article.get("headline", "")
                summary = article.get("summary", "")

                if headline:
                    news_pool.append(headline)
                if summary:
                    news_pool.append(summary)

        except requests.exceptions.RequestException as e:
            # Gentle error fallback so one bad ticker doesn't crash the whole app
            print(f"Skipping {ticker}: Could not fetch news due to {e}")
            continue

    # 2. Fetch General Market News (Optional)
    # This acts as a replacement for your "stocks OR market OR earnings" fallback query
    try:
        market_params = {
            "category": "general",
            "token": config.FINNHUB_API_KEY
        }
        market_response = requests.get("https://finnhub.io/api/v1/news", params=market_params)
        market_response.raise_for_status()

        for article in market_response.json():
            headline = article.get("headline", "")
            summary = article.get("summary", "")
            if headline:
                news_pool.append(headline)
            if summary:
                news_pool.append(summary)
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch general market news: {e}")

    # Enforce your maximum news cap from the configuration file
    return news_pool[:config.MAX_NEWS_ARTICLES * 2]  # x2 because titles and descriptions are flat elements in the list


if __name__ == '__main__':
    news = fetch_trending_news()
    print(f"Collected {len(news)} total text elements.")