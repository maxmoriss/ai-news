from pathlib import Path

RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://blog.google/technology/ai/rss/",
    "https://openai.com/blog/rss.xml",
    "https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml",
    "https://deepmind.google/blog/rss.xml",
    "https://www.artificialintelligence-news.com/feed/",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
]

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-v3.2"

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "posts"

TAGS = [
    "LLMs",
    "Computer Vision",
    "Robotics",
    "Research",
    "Policy",
    "Startups",
    "Open Source",
    "Hardware",
    "Ethics",
    "Products",
]

MAX_ARTICLE_AGE_HOURS = 36
