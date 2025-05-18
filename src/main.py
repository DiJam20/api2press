import os
from datetime import datetime

from guardian_news import get_guardian_news


OUTPUT_DIR = os.path.expanduser('~/daily_print')
os.makedirs(OUTPUT_DIR, exist_ok=True)

ARTICLE_TOPICS = "world|commentisfree|lifeandstyle"
ARTICLE_AGE_HOURS = 12

def main():
    print(f"Fetching daily news and crossword: {datetime.now()}")

    # Get The Guardian news
    news_items = get_guardian_news(ARTICLE_TOPICS, ARTICLE_AGE_HOURS)
    print(f"Fetched {len(news_items)} news items from The Guardian")

    # Get NYT Mini Crossword message

    # Create HTML document
    # Convert to PDF

    # Send to printer

if __name__ == "__main__":
    main()