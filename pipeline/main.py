from datetime import datetime, timezone

from config import OUTPUT_DIR
from fetch_news import fetch_articles
from generate_post import summarize_articles, write_post


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = f"{today}-ai-news"
    filepath = OUTPUT_DIR / f"{slug}.md"

    if filepath.exists():
        print(f"Post already exists: {filepath}")
        return

    print("Fetching articles...")
    articles = fetch_articles()
    if not articles:
        print("No articles found, skipping.")
        return

    print(f"Found {len(articles)} articles, generating summary...")
    data = summarize_articles(articles)

    path = write_post(data)
    print(f"Post written: {path}")


if __name__ == "__main__":
    main()
