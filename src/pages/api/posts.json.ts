import { getCollection } from "astro:content";
import type { APIRoute } from "astro";

export const GET: APIRoute = async () => {
  const posts = (await getCollection("posts"))
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
