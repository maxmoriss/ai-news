from datetime import datetime, timedelta, timezone
from pathlib import Path

from fetch_news import fetch_articles, strip_html
from generate_post import write_post


def test_strip_html_removes_tags():
    assert strip_html("<p>Hello <b>world</b></p>") == "Hello world"


def test_strip_html_handles_empty():
    assert strip_html("") == ""


def test_strip_html_plain_text():
    assert strip_html("no tags here") == "no tags here"


def test_fetch_articles_returns_list():
    articles = fetch_articles()
    assert isinstance(articles, list)


def test_fetch_articles_have_required_keys():
    articles = fetch_articles()
    for article in articles[:3]:
        assert "title" in article
        assert "url" in article
        assert "published" in article
        assert "source" in article


def test_fetch_articles_sorted_by_date():
    articles = fetch_articles()
    if len(articles) >= 2:
        dates = [a["published"] for a in articles]
        assert dates == sorted(dates, reverse=True)


def test_fetch_articles_no_duplicate_urls():
    articles = fetch_articles()
    urls = [a["url"] for a in articles]
    assert len(urls) == len(set(urls))


def test_write_post_creates_file(tmp_path, monkeypatch):
    import config
    monkeypatch.setattr(config, "OUTPUT_DIR", tmp_path)
    import generate_post
    monkeypatch.setattr(generate_post, "OUTPUT_DIR", tmp_path)

    data = {
        "title": "Test Post",
        "excerpt": "A test excerpt",
        "tags": ["LLMs", "Research"],
        "content": "This is the post body.",
    }
    path = write_post(data)
    assert Path(path).exists()
    content = Path(path).read_text()
    assert "Test Post" in content
    assert "LLMs" in content
