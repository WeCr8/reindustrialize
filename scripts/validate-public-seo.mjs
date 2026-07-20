import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const landingPath = path.join(root, 'apps/playreind-landing/index.html');
const publicDir = path.join(root, 'apps/playreind-landing/public');
const html = fs.readFileSync(landingPath, 'utf8');
const sitemap = fs.readFileSync(path.join(publicDir, 'sitemap.xml'), 'utf8');
const failures = [];
const requireText = (source, marker, message) => { if (!source.includes(marker)) failures.push(message); };

requireText(html, '<html lang="en-US">', 'Homepage language must be en-US.');
requireText(html, '<link rel="canonical" href="https://playreind.com/">', 'Canonical homepage URL is missing.');
requireText(html, 'name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1"', 'Search preview directives are missing.');
for (const type of ['WebSite', 'Organization', 'VideoGame', 'VideoObject']) requireText(html, `"@type":"${type}"`, `${type} structured data is missing.`);
for (const field of ['thumbnailUrl', 'uploadDate', 'duration', 'contentUrl']) requireText(html, `"${field}"`, `VideoObject.${field} is missing.`);
for (const marker of ['og:image:width', 'og:image:height', 'twitter:image:alt', 'aria-controls="heroVideo"', 'Campaign film transcript', 'id="people"', 'data-role-filter="founder"', 'Screenshots from']) requireText(html, marker, `Homepage marker ${marker} is missing.`);
for (const file of ['robots.txt', 'sitemap.xml', 'llms.txt', 'favicon.ico', 'favicon.svg', 'site.webmanifest', 'media/hero-poster-v7.webp', 'media/gameplay-hero-v8.mp4', 'media/gameplay-hero-v8.vtt', 'og/playreind-social-v7.jpg']) {
  if (!fs.existsSync(path.join(publicDir, file))) failures.push(`Public discovery asset is missing: ${file}`);
}
requireText(sitemap, 'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"', 'Video sitemap namespace is missing.');
for (const marker of ['<loc>https://playreind.com/</loc>', '<video:content_loc>https://playreind.com/media/gameplay-hero-v8.mp4</video:content_loc>', '<lastmod>2026-07-19</lastmod>']) requireText(sitemap, marker, `Sitemap marker is missing: ${marker}`);

const jsonLd = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
if (!jsonLd.length) failures.push('No JSON-LD block found.');
for (const [, source] of jsonLd) {
  try { JSON.parse(source); } catch (error) { failures.push(`Invalid JSON-LD: ${error.message}`); }
}
const title = html.match(/<title>([^<]+)<\/title>/)?.[1] ?? '';
const description = html.match(/<meta name="description" content="([^"]+)">/)?.[1] ?? '';
if (title.length < 30 || title.length > 65) failures.push(`Title length must be 30–65 characters; found ${title.length}.`);
if (description.length < 100 || description.length > 160) failures.push(`Meta description length must be 100–160 characters; found ${description.length}.`);

if (failures.length) {
  console.error(`FAIL: public SEO gate found ${failures.length} issue(s):\n- ${failures.join('\n- ')}`);
  process.exit(1);
}
console.log(`PASS: public SEO gate (${title.length}-character title, ${description.length}-character description, video discovery and social assets present).`);
