import os
import re
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
                    "Format your response EXACTLY like this:\n"
                    "TITLE: your short catchy title here\n"
                    "EXCERPT: 1-2 sentence summary here\n"
                    "TAGS: Tag1, Tag2, Tag3\n"
                    "---\n"
                    "your full markdown post body here"
                ),
            },
            {
                "role": "user",
                "content": f"Write today's AI news roundup from these articles:\n\n{articles_text}",
            },
        ],
        temperature=0.7,
    )

    raw = response.choices[0].message.content or ""

    title_match = re.search(r"TITLE:\s*(.+)", raw)
    excerpt_match = re.search(r"EXCERPT:\s*(.+)", raw)
    tags_match = re.search(r"TAGS:\s*(.+)", raw)
    content_split = raw.split("---", 1)

    title = title_match.group(1).strip() if title_match else "AI News Roundup"
    excerpt = excerpt_match.group(1).strip() if excerpt_match else "Today's top AI stories."
    tags = [t.strip() for t in tags_match.group(1).split(",")][:4] if tags_match else ["LLMs"]
    content = content_split[1].strip() if len(content_split) > 1 else raw

    return {"title": title, "excerpt": excerpt, "tags": tags, "content": content}


def write_post(data: dict) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = f"{today}-ai-news"

    title = data["title"].replace('"', "'")
    excerpt = data["excerpt"].replace('"', "'")
    tags_yaml = "\n".join(f'  - "{tag}"' for tag in data.get("tags", ["LLMs"]))

    frontmatter = f"""---
title: "{title}"
date: {today}
excerpt: "{excerpt}"
tags:
{tags_yaml}
---"""

    content = f"{frontmatter}\n\n{data['content']}\n"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / f"{slug}.md"
    filepath.write_text(content)
    return str(filepath)
