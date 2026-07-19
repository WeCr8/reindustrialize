import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

const base="apps/playreind-landing/public/";
test("public discovery files use canonical production URLs and honest release language",()=>{
  const robots=fs.readFileSync(base+"robots.txt","utf8"),sitemap=fs.readFileSync(base+"sitemap.xml","utf8"),llms=fs.readFileSync(base+"llms.txt","utf8"),manifest=JSON.parse(fs.readFileSync(base+"site.webmanifest","utf8"));
  assert.match(robots,/Sitemap: https:\/\/playreind\.com\/sitemap\.xml/);
  assert.match(sitemap,/<loc>https:\/\/playreind\.com\/<\/loc>/);
  assert.match(sitemap,/<loc>https:\/\/playreind\.com\/game\/<\/loc>/);
  assert.match(llms,/Chapter 1 is playable/);assert.match(llms,/Chapters 3 through 6 are planned and locked/);
  assert.equal(manifest.start_url,"/game/");assert.equal(manifest.icons[0].src,"/favicon.svg");
});

test("landing metadata exposes canonical, favicon, manifest, social image, and WebSite identity",()=>{
  const html=fs.readFileSync("apps/playreind-landing/index.html","utf8"),favicon=fs.readFileSync(base+"favicon.svg","utf8");
  for(const marker of ['rel="canonical" href="https://playreind.com/"','rel="icon" href="/favicon.svg"','rel="manifest" href="/site.webmanifest"','property="og:image"','"@type":"WebSite"'])assert.ok(html.includes(marker),marker);
  assert.match(favicon,/viewBox="0 0 512 512"/);
});

test("Cloudflare builder publishes discovery files and canonical game metadata",()=>{
  const builder=fs.readFileSync("scripts/build-cloudflare-site.mjs","utf8");
  assert.match(builder,/fs\.cpSync\(publicSource, out/);
  assert.ok(builder.includes('rel="canonical" href="https://playreind.com/game/"'));
  assert.ok(builder.includes('rel="icon" href="/favicon.svg"'));
});
