import re
from datetime import datetime, timedelta, timezone

import feedparser
from dateutil import parser as dateparser

from config import MAX_ARTICLE_AGE_HOURS, RSS_FEEDS


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def fetch_articles() -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=MAX_ARTICLE_AGE_HOURS)
    articles: list[dict] = []
    seen_urls: set[str] = set()

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                url = entry.get("link", "")
                if not url or url in seen_urls:
                    continue

                published = entry.get("published") or entry.get("updated")
                if not published:
                    continue

                try:
                    pub_date = dateparser.parse(published)
                except (ValueError, TypeError):
                    continue

                if pub_date is None:
                    continue
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                if pub_date < cutoff:
                    continue

                seen_urls.add(url)
                summary = strip_html(entry.get("summary", "") or entry.get("description", ""))
                title = strip_html(entry.get("title", "Untitled"))

                articles.append({
                    "title": title,
                    "url": url,
                    "summary": summary[:500],
                    "published": pub_date.isoformat(),
                    "source": feed.feed.get("title", feed_url),
                })
        except Exception:
            continue

    articles.sort(key=lambda a: a["published"], reverse=True)
    return articles
