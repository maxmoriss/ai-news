// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://maxmoriss.github.io',
  base: '/ai-news',
  vite: {
    plugins: [tailwindcss()],
  },
});
