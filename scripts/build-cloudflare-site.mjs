import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'apps', 'wecr8-info', 'prototypes', 'shop-floor-viewer.html');
const landingSource = path.join(root, 'apps', 'playreind-landing', 'index.html');
const videoLibrarySource = path.join(root, 'apps', 'playreind-landing', 'videos.html');
const releaseManifestSource = path.join(root, 'data', 'release-manifest.json');
const marketingVideo = path.join(root, 'apps', 'playreind-landing', 'public', 'media', 'gameplay-hero-v8.mp4');
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
fs.mkdirSync(path.join(out, 'media', 'screenshots'), { recursive: true });
fs.mkdirSync(path.join(out, 'videos'), { recursive: true });

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
const analyticsTag = `<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});</script><script async src="https://www.googletagmanager.com/gtag/js?id=G-KRCJP5MHXH"></script><script>gtag('js',new Date());gtag('config','G-KRCJP5MHXH',{anonymize_ip:true,allow_google_signals:false,allow_ad_personalization_signals:false,send_page_view:false});</script>`;
const privacyScript = scope => `${analyticsTag}<script defer src="/privacy-consent.js" data-scope="${scope}"></script>`;
html = html.replace('</head>', `<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="https://playreind.com/game/"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest">${privacyScript('game')}</head>`);

if (Buffer.byteLength(html) > maxAssetBytes) throw new Error(`Generated index.html remains larger than Cloudflare's 25 MiB limit.`);
fs.writeFileSync(path.join(out, 'game', 'index.html'), html);
let landingHtml = fs.readFileSync(landingSource, 'utf8');
landingHtml = landingHtml.replace('</head>', `${privacyScript('landing')}</head>`);
const includeMarketingVideo = fs.existsSync(marketingVideo) && process.env.PLAYREIND_SKIP_MARKETING_VIDEO !== '1';
if (!includeMarketingVideo) landingHtml = landingHtml.replace(/<video[\s\S]*?<\/video>/, '<a class="videoFallback" href="/game/" aria-label="Gameplay video unavailable; play the live alpha">▶ PLAY THE LIVE ALPHA</a>');
fs.writeFileSync(path.join(out, 'index.html'), landingHtml);
fs.writeFileSync(path.join(out, 'videos', 'index.html'), fs.readFileSync(videoLibrarySource, 'utf8').replace('</head>', `${privacyScript('videos')}</head>`));
const publicSource = path.join(root, 'apps', 'playreind-landing', 'public');
if (!fs.existsSync(publicSource)) throw new Error(`Missing landing discovery files: ${publicSource}`);
fs.cpSync(publicSource, out, {recursive: true});
const videoCatalog = [
  ['videos/gameplay-longform/reindustrialize-human-bot-feature-45s-v5.mp4', 'human-bot-feature-v5.mp4'],
  ['videos/horizontal-demos/reindustrialize-human-bot-demo-60s-v5.mp4', 'human-bot-demo-v5.mp4'],
  ['videos/vertical-shorts/reindustrialize-founder-selection-20s-v2.mp4', 'founder-selection-v2.mp4'],
  ['videos/vertical-shorts/reindustrialize-zach-mentor-30s-v2.mp4', 'zach-mentor-v2.mp4'],
  ['videos/vertical-shorts/reindustrialize-player-review-gameplay-30s-v2.mp4', 'player-review-v2.mp4'],
  ['videos/vertical-shorts/reindustrialize-human-bot-short-30s-v5.mp4', 'human-bot-short-v5.mp4'],
  ['videos/square-social/reindustrialize-human-bot-square-30s-v5.mp4', 'human-bot-square-v5.mp4'],
  ['videos/square-social/reindustrialize-business-growth-30s-v2.mp4', 'business-growth-v2.mp4']
];
for (const [sourceName, publicName] of videoCatalog) {
  const sourcePath = path.join(root, sourceName);
  if (!fs.existsSync(sourcePath)) {
    console.warn(`Optional campaign video unavailable in this checkout: ${sourceName}`);
    continue;
  }
  const bytes = fs.statSync(sourcePath).size;
  if (bytes > maxAssetBytes) throw new Error(`${sourceName} exceeds Cloudflare's 25 MiB asset limit.`);
  fs.copyFileSync(sourcePath, path.join(out, 'videos', publicName));
}
const libraryPath = path.join(out, 'videos', 'index.html');
let libraryHtml = fs.readFileSync(libraryPath, 'utf8');
libraryHtml = libraryHtml.replace(/<button class="card[^>]*data-src="([^"]+)"[\s\S]*?<\/button>/g, (card, sourceUrl) =>
  fs.existsSync(path.join(out, sourceUrl.replace(/^\//, ''))) ? card : '');
fs.writeFileSync(libraryPath, libraryHtml);
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
const characterAssets = [
  ['packages/assets/sprites/founder-profile-atlas-v1.png', 'founder-profiles.png'],
  ['packages/assets/sprites/av_m_founder_02_hd.png', 'founder-b-sprite.png'],
  ['packages/assets/sprites/av_f_founder_hd.png', 'founder-c-sprite.png'],
  ['packages/assets/sprites/workforce-profile-atlas-v1.png', 'workforce-profiles.png'],
  ['packages/assets/sprites/workforce-atlas-v1.png', 'workforce-sprites.png'],
  ['packages/assets/sprites/maintenance-team-profile-atlas-v1.png', 'maintenance-profiles.png'],
  ['packages/assets/sprites/maintenance-team-sprite-atlas-v2.png', 'maintenance-sprites.png']
];
for (const [sourceName, publicName] of characterAssets) {
  const sourcePath = path.join(root, sourceName);
  if (!fs.existsSync(sourcePath)) throw new Error(`Missing marketing character asset: ${sourceName}`);
  fs.copyFileSync(sourcePath, path.join(landingAssetDir, publicName));
}
const gameplayScreenshots = [
  ['demo/remotion/public/screens/02-ten-founder-selection.png', 'founder-selection.png'],
  ['demo/remotion/public/screens/04-playable-shop-objectives.png', 'shop-objectives.png'],
  ['demo/remotion/public/screens/05-nox-material-ordering.png', 'material-ordering.png'],
  ['demo/remotion/public/screens/07-hire-your-team.png', 'hire-team.png']
];
for (const [sourceName, publicName] of gameplayScreenshots) {
  const sourcePath = path.join(root, sourceName);
  if (!fs.existsSync(sourcePath)) throw new Error(`Missing marketing gameplay screenshot: ${sourceName}`);
  fs.copyFileSync(sourcePath, path.join(out, 'media', 'screenshots', publicName));
}
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

/release.json
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
