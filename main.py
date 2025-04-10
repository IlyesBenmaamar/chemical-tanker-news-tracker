import requests
from bs4 import BeautifulSoup
import feedparser

# Define keywords related to chemical tanker newbuilds
KEYWORDS = [
    'newbuild',
    'chemical tanker order',
    'new chemical tankers',
    'chemical tanker contract',
    'chemical carrier order',
    'chemical tanker delivery',
    'chemical tanker',
    'order',
    'contract',
    'delivery',
    'construction',
    'built',
    'newbuilds',
    'chemical tankers'
]

# RSS feeds (Splash247)
RSS_FEEDS = [
    'https://splash247.com/category/sector/tankers/feed/'
]

# Try to extract publish date from article page
def get_article_date(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')

        meta = soup.find('meta', {'name': 'pubdate'}) \
            or soup.find('meta', {'name': 'date'}) \
            or soup.find('meta', {'property': 'article:published_time'}) \
            or soup.find('meta', {'itemprop': 'datePublished'})

        if meta and meta.get('content'):
            return meta['content']
    except Exception:
        pass
    return "N/A"

# Fetch and filter articles from RSS feed
def fetch_rss_articles(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.summary.lower() for keyword in KEYWORDS):
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', 'N/A')
            })
    return articles

# Scrape TradeWinds and AXSMarine search results
def scrape_custom_websites():
    scraped_articles = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    # TradeWinds
    tw_url = "https://www.tradewindsnews.com/archive/?q=chemical%20tankers&othersections=Tankers&tema_path_facet=Chemical%5C%20tankers"
    res = requests.get(tw_url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    for link in soup.find_all('a', href=True):
        title = link.get_text(strip=True)
        href = link['href']
        if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
            full_link = f"https://www.tradewindsnews.com{href}" if href.startswith('/') else href
            scraped_articles.append({
                'title': title,
                'link': full_link,
                'published': get_article_date(full_link)
            })

    # AXSMarine (search results)
    axs_url = "https://public.axsmarine.com/?s=chemical+tankers"
    axs_res = requests.get(axs_url, headers=headers)
    axs_soup = BeautifulSoup(axs_res.content, 'html.parser')

    for link in axs_soup.find_all('a', href=True):
        title = link.get_text(strip=True)
        href = link['href']
        if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
            full_link = f"https://public.axsmarine.com{href}" if href.startswith('/') else href
            scraped_articles.append({
                'title': title,
                'link': full_link,
                'published': get_article_date(full_link)
            })

    return scraped_articles

# Scrape home/blog pages of Splash247 and AXSMarine for general article listings
def scrape_homepage_articles():
    scraped = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Splash247 category page
    splash_url = "https://splash247.com/category/sector/tankers/"
    splash_res = requests.get(splash_url, headers=headers)
    splash_soup = BeautifulSoup(splash_res.content, 'html.parser')

    for article in splash_soup.select("h2.entry-title a"):
        title = article.get_text(strip=True)
        href = article['href']
        if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
            scraped.append({
                'title': title,
                'link': href,
                'published': get_article_date(href)
            })

    # AXSMarine blog
    axs_blog_url = "https://public.axsmarine.com/blog"
    axs_blog_res = requests.get(axs_blog_url, headers=headers)
    axs_blog_soup = BeautifulSoup(axs_blog_res.content, 'html.parser')

    for link in axs_blog_soup.find_all('a', href=True):
        title = link.get_text(strip=True)
        href = link['href']
        if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
            full_link = f"https://public.axsmarine.com{href}" if href.startswith('/') else href
            scraped.append({
                'title': title,
                'link': full_link,
                'published': get_article_date(full_link)
            })

    return scraped

# (Optional: Keep this if you still want CLI results)
def display_articles():
    print("🔍 Searching for new chemical tanker builds...\n")
    all_results = []

    rss_count = 0
    for feed in RSS_FEEDS:
        articles = fetch_rss_articles(feed)
        rss_count += len(articles)
        all_results.extend(articles)

    scraped_articles = scrape_custom_websites()
    tw_count = len(scraped_articles)
    all_results.extend(scraped_articles)

    homepage_articles = scrape_homepage_articles()
    home_count = len(homepage_articles)
    all_results.extend(homepage_articles)

    print(f"✅ Found {rss_count} article(s) from RSS feeds.")
    print(f"✅ Found {tw_count} article(s) from TradeWinds and AXSMarine search.")
    print(f"✅ Found {home_count} article(s) from homepage/blog crawlers.\n")

    for article in all_articles:
        print(f"🚢 {article['title']}")
        print(f"🔗 {article['link']}")
        print(f"📅 {article['published']}")
        print("-" * 60)

    return all_results

# For dashboard use
def get_all_articles():
    all_articles = []
    for feed in RSS_FEEDS:
        all_articles.extend(fetch_rss_articles(feed))
    all_articles.extend(scrape_custom_websites())
    all_articles.extend(scrape_homepage_articles())
    return all_articles
