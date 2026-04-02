import { getCollection } from "astro:content";
import type { APIRoute, GetStaticPaths } from "astro";

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await getCollection("posts");
  const tags = [...new Set(posts.flatMap((p) => p.data.tags))];
  return tags.map((tag) => ({
    params: { tag: tag.toLowerCase().replace(/\s+/g, "-") },
    props: { tag },
  }));
};

export const GET: APIRoute = async ({ params, props }) => {
  const posts = (await getCollection("posts"))
    .filter((p) => p.data.tags.includes(props.tag))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf())
    .map((p) => ({
      slug: p.id,
      title: p.data.title,
      date: p.data.date.toISOString(),
      excerpt: p.data.excerpt,
      tags: p.data.tags,
    }));
  return new Response(JSON.stringify(posts), {
    headers: { "Content-Type": "application/json" },
  });
};
