import feedparser
import datetime

# All your desired feeds
FEEDS = {
    "NY Times": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
    "Die Zeit": "https://newsfeed.zeit.de/politik/index",
    "Der Spiegel": "https://www.spiegel.de/politik/index.rss",
    "Le Monde": "https://www.lemonde.fr/politique/rss_full.xml",
    "The New Yorker": "https://www.newyorker.com/feed/news",
    "WSJ": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "Financial Times": "https://www.ft.com/news-feed?format=rss",
    "Politico EU": "https://www.politico.eu/feed/",
    "Politico US": "https://www.politico.com/rss/politics.xml",
    "Washington Post": "https://feeds.washingtonpost.com/rss/politics",
    "The Economist": "https://www.economist.com/politics-this-week/rss.xml",
    "WAZ Mülheim": "https://www.waz.de/staedte/muelheim/rss",
    "The Atlantic": "https://www.theatlantic.com/feed/all/"
}

def fetch_all_news():
    items = []
    for source, url in FEEDS.items():
        print(f"Loading {source}...")
        feed = feedparser.parse(url)
        for entry in feed.entries[:8]:  # Latest 8 per source
            # Parse timestamp (fallback if no date available)
            dt = entry.get('published_parsed') or entry.get('updated_parsed')
            timestamp = datetime.datetime(*dt[:6]) if dt else datetime.datetime.now()
            
            items.append({
                'source': source,
                'title': entry.title,
                'link': entry.link,
                'time': timestamp
            })
    # Sort by time (newest first)
    return sorted(items, key=lambda x: x['time'], reverse=True)

def generate_html(news_items):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Memeorandum CSS style
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Memeorandum Clone</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: white; color: black; margin: 10px; font-size: 13px; }}
        a {{ color: #0000cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .header {{ margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px; }}
        .header h1 {{ font-size: 24px; margin: 0; letter-spacing: -1px; }}
        .timestamp {{ font-size: 11px; color: #666; }}
        
        .container {{ display: flex; gap: 20px; }}
        .main-column {{ flex: 2; }}
        .side-column {{ flex: 1; border-left: 1px solid #eee; padding-left: 15px; font-size: 12px; }}
        
        .story-block {{ margin-bottom: 18px; }}
        .headline {{ font-size: 16px; font-weight: bold; line-height: 1.2; }}
        .source-name {{ color: #008000; font-size: 12px; font-weight: normal; margin-left: 5px; }}
        
        .discussion-line {{ margin-left: 20px; font-size: 12px; margin-top: 3px; color: #555; }}
        .discussion-source {{ color: #008000; font-style: normal; }}
        
        h3 {{ font-size: 14px; text-transform: uppercase; color: #444; border-bottom: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>memeorandum <span style="color:red">clone</span></h1>
        <div class="timestamp">Stand: {now} | Mülheim an der Ruhr Edition</div>
    </div>
    
    <div class="container">
        <div class="main-column">
"""

    # Top Stories (first 20)
    for item in news_items[:20]:
        html_content += f"""        <div class="story-block">
            <div class="headline">
                <a href="{item['link']}">{item['title']}</a>
                <span class="source-name">{item['source']}</span>
            </div>
        </div>
"""

    html_content += """        </div>
        <div class="side-column">
            <h3>Latest Updates</h3>
"""

    # Sidebar (remaining news)
    for item in news_items[20:60]:
        html_content += f"""            <div style="margin-bottom: 8px;">
                <a href="{item['link']}">{item['title']}</a> 
                <span class="discussion-source">({item['source']})</span>
            </div>
"""

    html_content += """        </div>
    </div>
</body>
</html>
"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Done! Open index.html in your browser.")

if __name__ == "__main__":
    news = fetch_all_news()
    generate_html(news)