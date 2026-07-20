import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const pages = ['index.html', 'game/index.html', 'videos/index.html'];
const failures = [];
const requireBuildOutput = process.argv.includes('--build-output');
const builder = fs.readFileSync(path.join(root, 'scripts/build-cloudflare-site.mjs'), 'utf8');
for (const marker of ['G-KRCJP5MHXH', 'googletagmanager.com/gtag/js', "gtag('consent','default'", '/privacy-consent.js']) {
  if (!builder.includes(marker)) failures.push(`builder: required analytics marker missing: ${marker}`);
}
for (const page of requireBuildOutput ? pages : []) {
  const file = path.join(root, 'cloudflare-dist', page);
  if (!fs.existsSync(file)) { failures.push(`${page}: missing build output`); continue; }
  const html = fs.readFileSync(file, 'utf8');
  const denied = html.indexOf("gtag('consent','default'");
  const google = html.indexOf('googletagmanager.com/gtag/js');
  if (denied < 0 || google < 0 || denied > google) failures.push(`${page}: denied consent must precede Google Analytics`);
  for (const key of ['analytics_storage', 'ad_storage', 'ad_user_data', 'ad_personalization']) {
    if (!new RegExp(`${key}:'denied'`).test(html)) failures.push(`${page}: ${key} is not denied by default`);
  }
  if (!html.includes('/privacy-consent.js')) failures.push(`${page}: shared consent controller missing`);
}
const controller = fs.readFileSync(path.join(root, 'apps/playreind-landing/public/privacy-consent.js'), 'utf8');
for (const event of ['game_start','game_resume','founder_select','control_mode','station_start','task_complete','hire_role','worker_assignment','equipment_purchase','maintenance_repair','chapter_milestone','facility_milestone']) {
  if (!controller.includes(`${event}:`)) failures.push(`controller: event ${event} missing from allowlist`);
}
if (!controller.includes('FORBIDDEN')) failures.push('controller: sensitive parameter guard missing');
if (failures.length) { console.error(failures.map(v => `FAIL: ${v}`).join('\n')); process.exit(1); }
console.log(`PASS: consent defaults, Google tag G-KRCJP5MHXH, shared controller, anonymous event allowlist${requireBuildOutput ? ', and built landing/game/video pages' : ''} validated.`);
