import json
import os
from datetime import datetime, timezone

from openai import OpenAI

from config import MODEL, OPENROUTER_BASE_URL, OUTPUT_DIR, TAGS


def summarize_articles(articles: list[dict]) -> dict:
    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

    tag_list = ", ".join(TAGS)
    articles_text = "\n\n".join(
        f"**{a['title']}** ({a['source']})\n{a['url']}\n{a['summary']}"
        for a in articles[:20]
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior tech journalist writing a daily AI news roundup blog post. "
                    "Write in a clear, engaging style. Group related stories. "
                    "For each story, include the source link inline as markdown. "
                    "End with a brief editorial take on the day's theme.\n\n"
                    f"Available tags (pick 2-4 most relevant): {tag_list}\n\n"
                    "Respond with valid JSON:\n"
                    '{"title": "short catchy title", "excerpt": "1-2 sentence summary", '
                    '"tags": ["Tag1", "Tag2"], "content": "full markdown post body"}'
                ),
            },
            {
                "role": "user",
                "content": f"Write today's AI news roundup from these articles:\n\n{articles_text}",
            },
        ],
        temperature=0.7,
    )

    raw = response.choices[0].message.content or "{}"
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        raw = raw.rsplit("```", 1)[0]
    return json.loads(raw)


def write_post(data: dict) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = f"{today}-ai-news"
    tags_yaml = "\n".join(f'  - "{tag}"' for tag in data.get("tags", ["LLMs"]))

    frontmatter = f"""---
title: "{data['title']}"
date: {today}
excerpt: "{data['excerpt']}"
tags:
{tags_yaml}
---"""

    content = f"{frontmatter}\n\n{data['content']}\n"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / f"{slug}.md"
    filepath.write_text(content)
    return str(filepath)
