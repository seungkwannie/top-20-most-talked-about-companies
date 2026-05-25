import requests, config
from datetime import datetime, timedelta

def fetch_trending_news():
    # Calculate to a strict 48-hour time boundary
    current_time = datetime.now()
    time_window_start = current_time - timedelta(hours=48)
    
    # Format dates into YYYY-MM-DD strings
    date_to = current_time.strftime("%Y-%m-%d")
    date_from = time_window_start.strftime("%Y-%m-%d")
    
    ticker_string = " OR ".join([key for key in config.COMPANY_LOOKUP.keys() if key.isupper()])
    
    params = {
        "language": "en",
        "sortBy": "relevancy",
        "from": date_from,
        "to": date_to,
        "pageSize": config.MAX_NEWS_ARTICLES,
        "apiKey": config.NEWS_API_KEY,
        "q": f"({ticker_string}) OR stocks OR market OR earnings"
    }
    
    data = requests.get(url="https://newsapi.org/v2/everything", params=params)
    data.raise_for_status()
    data = data.json()
    
    news_pool = []
    for article in data.get("articles", []):
        news_pool.append(article["title"])
        news_pool.append(article.get("description", ""))
    return news_pool


if __name__ == '__main__':
    news = fetch_trending_news()