from urllib.parse import quote
import feedparser
from datetime import datetime

NEWS_QUERIES_INDIA = [
    "NSE stocks", "BSE stocks", "India stock market", "Sensex", "Nifty",
    "RBI policy", "Indian IPO", "sector earnings India"
]

NEWS_QUERIES_US = [
    "US stock market", "S&P 500", "NASDAQ", "Dow Jones",
    "Fed policy", "US earnings season", "semiconductor industry"
]

NUM_ARTICLES_PER_QUERY = 10

def google_news_rss(query):
    return f"https://news.google.com/rss/search?q={quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"

def fetch_rss_items(query, limit):
    rss_url = google_news_rss(query)
    feed = feedparser.parse(rss_url)
    items = feed.entries[:limit]
    return items

def print_section(title):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title) + "\n")

def fetch_country_news(queries, country_tag):
    seen_links = set()
    all_items = []

    for query in queries:
        entries = fetch_rss_items(query, NUM_ARTICLES_PER_QUERY)
        for entry in entries:
            link = getattr(entry, 'link', "")
            if not link or link in seen_links:
                continue
            seen_links.add(link)

            items = {
                "country": country_tag,
                "query": query,
                "title": getattr(entry, 'title', ""),
                "link": link,
                "published": getattr(entry, 'published', ""),
                "source": getattr(entry, 'source', {}).get('title') if hasattr(entry, 'source') else "",
            }
            all_items.append(items)

    for item, it in enumerate(all_items, start = 1):
        print(f"{item:02d}. [{it['country']}] {it['title']}")
        if it["published"]:
            print(f"    Published: {it['published']}")
        print(f"    Link: {it['link']}")

        if it["query"]:
            print(f"    (Matched query: {it['query']})")
        print("")

def main():
    print_section("India market news")
    fetch_country_news(NEWS_QUERIES_INDIA, "IN")

    print_section("US market news")
    fetch_country_news(NEWS_QUERIES_US, "US")

    print("\nDone.")

if __name__ == "__main__":
    main()