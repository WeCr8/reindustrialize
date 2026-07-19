import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'apps', 'wecr8-info', 'prototypes', 'shop-floor-viewer.html');
const landingSource = path.join(root, 'apps', 'playreind-landing', 'index.html');
const releaseManifestSource = path.join(root, 'data', 'release-manifest.json');
const marketingVideo = path.join(root, 'apps', 'playreind-landing', 'public', 'media', 'gameplay-demo-v6.mp4');
const out = path.join(root, 'cloudflare-dist');
const assetDir = path.join(out, 'assets', 'runtime');
const landingAssetDir = path.join(out, 'assets', 'landing');
const maxAssetBytes = 25 * 1024 * 1024;
const extensions = new Map([
  ['image/png', 'png'], ['image/jpeg', 'jpg'], ['image/webp', 'webp'],
  ['image/svg+xml', 'svg'], ['audio/mpeg', 'mp3'], ['audio/wav', 'wav'],
  ['audio/ogg', 'ogg'], ['font/woff2', 'woff2']
]);

if (!fs.existsSync(source)) throw new Error(`Missing generated game: ${source}`);
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(assetDir, { recursive: true });
fs.mkdirSync(landingAssetDir, { recursive: true });
fs.mkdirSync(path.join(out, 'game'), { recursive: true });
fs.mkdirSync(path.join(out, 'media'), { recursive: true });

let html = fs.readFileSync(source, 'utf8');
let extracted = 0;
let largest = { bytes: 0, file: '' };
const written = new Map();
function emitAsset(bytes, mime) {
  const hash = crypto.createHash('sha256').update(bytes).digest('hex').slice(0, 20);
  const ext = extensions.get(mime.toLowerCase()) || 'bin';
  const name = `${hash}.${ext}`;
  const target = path.join(assetDir, name);
  if (bytes.length > maxAssetBytes) throw new Error(`${name} is ${(bytes.length / 1048576).toFixed(1)} MiB; Cloudflare permits at most 25 MiB per asset.`);
  if (!written.has(name)) {
    fs.writeFileSync(target, bytes); written.set(name, bytes.length); extracted += 1;
    if (bytes.length > largest.bytes) largest = { bytes: bytes.length, file: name };
  }
  return `/assets/runtime/${name}`;
}
html = html.replace(/data:([a-z0-9.+-]+\/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]+)/gi, (uri, mime, encoded) => {
  const bytes = Buffer.from(encoded, 'base64');
  return emitAsset(bytes, mime);
});
html = html.replace(/"([A-Za-z0-9+/]{1024,}={0,2})"/g, (quoted, encoded) => {
  const bytes = Buffer.from(encoded, 'base64');
  const mime = bytes.subarray(0, 8).equals(Buffer.from([137,80,78,71,13,10,26,10])) ? 'image/png' :
    (bytes.subarray(0, 3).toString('ascii') === 'ID3' || (bytes[0] === 0xff && (bytes[1] & 0xe0) === 0xe0)) ? 'audio/mpeg' : null;
  return mime ? JSON.stringify(emitAsset(bytes, mime)) : quoted;
});
html = html.replace('im.src=stop.imageType==="equipment"?"data:image/png;base64,"+EQUIPMENT_VIEWS[stop.image]:stop.imageType==="nox"?"data:image/png;base64,"+NOX_MATERIALS_ART:"data:image/png;base64,"+SPRITES[stop.image]', 'im.src=stop.imageType==="equipment"?assetUrl(EQUIPMENT_VIEWS[stop.image]):stop.imageType==="nox"?assetUrl(NOX_MATERIALS_ART):assetUrl(SPRITES[stop.image])');
html = html.replace('</head>', '<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="https://playreind.com/game/"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest"></head>');

if (Buffer.byteLength(html) > maxAssetBytes) throw new Error(`Generated index.html remains larger than Cloudflare's 25 MiB limit.`);
fs.writeFileSync(path.join(out, 'game', 'index.html'), html);
let landingHtml = fs.readFileSync(landingSource, 'utf8');
landingHtml = landingHtml.replaceAll('/media/gameplay-demo-v5.mp4', '/media/gameplay-demo-v6.mp4');
landingHtml = landingHtml.replace('</video>', '<track kind="captions" src="/assets/landing/gameplay-demo-v6.vtt" srclang="en" label="English" default></video>');
const analyticsTag = `<script async src="https://www.googletagmanager.com/gtag/js?id=G-KRCJP5MHXH"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-KRCJP5MHXH');</script>`;
landingHtml = landingHtml.replace('</head>', `${analyticsTag}</head>`);
const includeMarketingVideo = fs.existsSync(marketingVideo) && process.env.PLAYREIND_SKIP_MARKETING_VIDEO !== '1';
if (!includeMarketingVideo) landingHtml = landingHtml.replace(/<video controls[\s\S]*?<\/video>/, '<a class="videoFallback" href="/game/" aria-label="Gameplay video unavailable; play the live alpha">▶ PLAY THE LIVE ALPHA</a>');
fs.writeFileSync(path.join(out, 'index.html'), landingHtml);
const publicSource = path.join(root, 'apps', 'playreind-landing', 'public');
if (!fs.existsSync(publicSource)) throw new Error(`Missing landing discovery files: ${publicSource}`);
fs.cpSync(publicSource, out, {recursive: true});
const releaseManifest = JSON.parse(fs.readFileSync(releaseManifestSource, 'utf8'));
let sourceRevision = process.env.CF_PAGES_COMMIT_SHA || process.env.GITHUB_SHA || 'unknown';
if (sourceRevision === 'unknown') {
  try { sourceRevision = execFileSync('git', ['rev-parse', 'HEAD'], {cwd: root, encoding: 'utf8'}).trim(); } catch {}
}
const releaseRecord = {
  product: 'REINDUSTRIALIZE',
  channel: 'alpha',
  version: releaseManifest.release,
  status: releaseManifest.status,
  sourceRevision,
  builtAt: new Date().toISOString(),
  gameplayEvidenceVersion: releaseManifest.gameplayEvidenceVersion,
  storybookEdition: releaseManifest.storybookEdition,
  liveUrl: 'https://playreind.com/',
  gameUrl: 'https://playreind.com/game/'
};
fs.writeFileSync(path.join(out, 'release.json'), JSON.stringify(releaseRecord, null, 2));
fs.copyFileSync(path.join(root, 'packages', 'assets', 'title-screen-zach-v2.png'), path.join(landingAssetDir, 'title-screen.png'));
fs.copyFileSync(path.join(root, 'apps', 'playreind-landing', 'gameplay-demo-v6.vtt'), path.join(landingAssetDir, 'gameplay-demo-v6.vtt'));
if (includeMarketingVideo) fs.copyFileSync(marketingVideo, path.join(out, 'media', 'gameplay-demo-v6.mp4'));
fs.writeFileSync(path.join(out, '_headers'), `/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  X-Frame-Options: SAMEORIGIN

/assets/runtime/*
  Cache-Control: public, max-age=31536000, immutable

/media/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/index.html
  Cache-Control: public, max-age=0, must-revalidate

/game/index.html
  Cache-Control: public, max-age=0, must-revalidate
`);
fs.writeFileSync(path.join(out, '_redirects'), `/game /game/ 301
/play /game/ 301
`);
fs.writeFileSync(path.join(out, '.assetsignore'), `.assetsignore
`);

const report = {
  domain: 'PlayReInd.com',
  generatedAt: new Date().toISOString(),
  source: path.relative(root, source).replaceAll('\\', '/'),
  files: extracted + (includeMarketingVideo ? 8 : 7),
  extractedRuntimeAssets: extracted,
  indexBytes: Buffer.byteLength(html),
  largestAsset: largest,
  marketingVideoIncluded: includeMarketingVideo,
  cloudflareIndividualAssetLimitBytes: maxAssetBytes
};
fs.writeFileSync(path.join(out, 'deployment-report.json'), JSON.stringify(report, null, 2));
console.log(`PASS: Cloudflare site built with ${extracted} runtime assets; index ${(report.indexBytes / 1048576).toFixed(1)} MiB; largest ${(largest.bytes / 1048576).toFixed(1)} MiB (${largest.file}).`);
