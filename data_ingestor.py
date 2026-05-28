# import requests
# import config
# from datetime import datetime, timedelta
#
#
# def fetch_trending_news():
#     # Calculate a strict 48-hour time boundary
#     current_time = datetime.now()
#     time_window_start = current_time - timedelta(hours=48)
#
#     # Finnhub requires dates formatted as YYYY-MM-DD
#     date_to = current_time.strftime("%Y-%m-%d")
#     date_from = time_window_start.strftime("%Y-%m-%d")
#
#     # Extract just the upper-case ticker keys (e.g., ['AAPL', 'NVDA', 'TSLA'])
#     tickers = [key for key in config.COMPANY_LOOKUP.keys() if key.isupper()]
#
#     news_pool = []
#
#     # 1. Fetch Company-Specific News for your portfolio tickers
#     for ticker in tickers:
#         params = {
#             "symbol": ticker,
#             "from": date_from,
#             "to": date_to,
#             "token": config.FINNHUB_API_KEY  # Finnhub authentication token parameter
#         }
#
#         try:
#             response = requests.get("https://finnhub.io/api/v1/company-news", params=params)
#             response.raise_for_status()
#             articles = response.json()
#
#             # Finnhub returns a top-level list of news dictionaries
#             for article in articles:
#                 # 'headline' and 'summary' map to NewsAPI's 'title' and 'description'
#                 headline = article.get("headline", "")
#                 summary = article.get("summary", "")
#
#                 if headline:
#                     news_pool.append(headline)
#                 if summary:
#                     news_pool.append(summary)
#
#         except requests.exceptions.RequestException as e:
#             # Gentle error fallback so one bad ticker doesn't crash the whole app
#             print(f"Skipping {ticker}: Could not fetch news due to {e}")
#             continue
#
#     # 2. Fetch General Market News (Optional)
#     # This acts as a replacement for your "stocks OR market OR earnings" fallback query
#     try:
#         market_params = {
#             "category": "general",
#             "token": config.FINNHUB_API_KEY
#         }
#         market_response = requests.get("https://finnhub.io/api/v1/news", params=market_params)
#         market_response.raise_for_status()
#
#         for article in market_response.json():
#             headline = article.get("headline", "")
#             summary = article.get("summary", "")
#             if headline:
#                 news_pool.append(headline)
#             if summary:
#                 news_pool.append(summary)
#     except requests.exceptions.RequestException as e:
#         print(f"Could not fetch general market news: {e}")
#
#     # Enforce your maximum news cap from the configuration file
#     return news_pool[:config.MAX_NEWS_ARTICLES * 2]  # x2 because titles and descriptions are flat elements in the list
#
#
# if __name__ == '__main__':
#     news = fetch_trending_news()
#     print(f"Collected {len(news)} total text elements.")
############################################
# import requests
# import config
# from datetime import datetime, timedelta
#
#
# def fetch_trending_news():
#     # 1. Set up Alpha Vantage base configurations
#     url = "https://www.alphavantage.co/query"
#
#     # We pass 'sort=RELEVANCE' and a high limit (max 200) to grab the most impactful market news
#     params = {
#         "function": "NEWS_SENTIMENT",
#         "sort": "RELEVANCE",
#         "limit": 200,
#         "apikey": config.ALPHA_VANTAGE_API_KEY  # Ensure this matches your config file variable
#     }
#
#     # Strict 48-hour time boundary calculation
#     current_time = datetime.now()
#     time_window_start = current_time - timedelta(hours=48)
#
#     # Get portfolio tickers from your config file to use as a local filter whitelist
#     portfolio_tickers = set(key.upper() for key in config.COMPANY_LOOKUP.keys() if key.isupper())
#
#     news_pool = []
#
#     try:
#         # 2. Make exactly ONE API call for the entire market
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
#
#         # Catch Alpha Vantage API error/limit messages if they don't throw an HTTP error code
#         if "Information" in data:
#             print(f"Alpha Vantage Notice: {data['Information']}")
#             return []
#
#         articles = data.get("feed", [])
#
#         # 3. Filter and process the articles in Python
#         for article in articles:
#             pub_time_str = article.get("time_published", "")
#             try:
#                 pub_time = datetime.strptime(pub_time_str, "%Y%m%dT%H%M%S")
#             except ValueError:
#                 # Fallback if date string parsing fails
#                 pub_time = current_time
#
#             # Skip articles older than 48 hours
#             if pub_time < time_window_start:
#                 continue
#
#             headline = article.get("title", "")
#             summary = article.get("summary", "")
#
#             # Inspect what companies are tagged in this article
#             ticker_sentiment = article.get("ticker_sentiment", [])
#             article_tickers = {item.get("ticker") for item in ticker_sentiment}
#
#             # Check if this article mentions ANY of your portfolio tickers (Tesla, Apple, etc.)
#             is_portfolio_news = not article_tickers.isdisjoint(portfolio_tickers)
#
#             # If it matches your portfolio, OR if it's general major market news
#             if is_portfolio_news or not article_tickers:
#                 if headline:
#                     news_pool.append(headline)
#                 if summary:
#                     news_pool.append(summary)
#
#     except requests.exceptions.RequestException as e:
#         print(f"Could not fetch Alpha Vantage news data: {e}")
#         return []
#
#     # Enforce your maximum news cap from the configuration file
#     return news_pool[:config.MAX_NEWS_ARTICLES * 2]
#
#
# if __name__ == '__main__':
#     # Mocking config setups for a standalone run test if needed
#     # Ensure config.ALPHA_VANTAGE_API_KEY exists in your actual config file.
#     news = fetch_trending_news()
#     print(f"Collected {len(news)} total text elements.")

import requests
import config
from datetime import datetime, timedelta

def fetch_trending_news():
    # 1. Set up Marketaux base configurations
    url = "https://api.marketaux.com/v1/entity/stats"  # <--- Notice the change here

    # Strict 48-hour time boundary calculation
    current_time = datetime.utcnow()  # Marketaux explicitly operates in UTC
    time_window_start = current_time - timedelta(days=7)

    # Format to ISO 8601 string required by Marketaux (e.g., 2026-05-26T15:30)
    published_after_str = time_window_start.strftime("%Y-%m-%dT%H:%M")

    # Get portfolio tickers from your config file to use as a local whitelist filter
    portfolio_tickers = [key for key in config.COMPANY_LOOKUP.keys() if key.isupper()]

    params = {
        "api_token": config.MARKETAUX_API_TOKEN,
        "published_after": published_after_str,
        "filter_entities": "true",
        "language": "en",
        "limit": 100,  # Maximize the payload limit for the call
        "symbols": ",".join(portfolio_tickers)
    }

    try:
        # 2. Make the API call to Marketaux
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Catch Marketaux error payloads if they return 200 OK but contain error codes
        if "error" in data:
            print(f"Marketaux Error Notice: {data['error']['message']}")
            return []

        # ==================== INSERTED HERE ====================
        # Right at the end of your fetch_trending_news try block:
        articles = data.get("data", [])
        return articles  # Returns the raw objects list perfectly
        # =======================================================

    except requests.exceptions.RequestException as e:
        print(f"Could not fetch Marketaux news data: {e}")
        return []


if __name__ == '__main__':
    # Ensure config.MARKETAUX_API_TOKEN exists in your actual config file.
    news = fetch_trending_news()
    print(f"Collected {len(news)} total text elements.")
