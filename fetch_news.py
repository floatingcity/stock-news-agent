from urllib.parse import quote_plus
from urllib.request import urlopen
import xml.etree.ElementTree as ET


GOOGLE_NEWS_RSS_URL = (
    "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
)


def fetch_news(ticker: str):
    query = quote_plus(f"{ticker} stock")
    url = GOOGLE_NEWS_RSS_URL.format(query=query)

    try:
        with urlopen(url, timeout=10) as response:
            rss_feed = response.read()
    except Exception:
        return []

    try:
        root = ET.fromstring(rss_feed)
    except ET.ParseError:
        return []

    headlines = []
    for item in root.findall("./channel/item/title"):
        title = (item.text or "").strip()
        if title:
            headlines.append(title)
        if len(headlines) == 10:
            break

    return headlines
