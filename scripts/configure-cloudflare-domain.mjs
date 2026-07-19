import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const apply = process.argv.includes('--apply');
const envFile = path.join(root, '.env');
const local = {};
if (fs.existsSync(envFile)) {
  for (const line of fs.readFileSync(envFile, 'utf8').split(/\r?\n/)) {
    const match = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (match) local[match[1]] = match[2].trim().replace(/^['"]|['"]$/g, '');
  }
}
const token = process.env.CLOUDFLARE_API_TOKEN || local.CLOUDFLARE_API_TOKEN;
if (!token) throw new Error('CLOUDFLARE_API_TOKEN is not configured.');

const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };
async function cf(pathname, options = {}) {
  const response = await fetch(`https://api.cloudflare.com/client/v4${pathname}`, { ...options, headers });
  const body = await response.json();
  if (!response.ok || !body.success) {
    const detail = (body.errors || []).map(error => `${error.code}: ${error.message}`).join('; ');
    throw new Error(`Cloudflare API request failed (${response.status}): ${detail || 'unknown error'}`);
  }
  return body.result;
}

const zones = await cf('/zones?name=playreind.com&status=active');
if (zones.length !== 1) throw new Error(`Expected one active playreind.com zone, found ${zones.length}.`);
const zone = zones[0];
const records = await cf(`/zones/${zone.id}/dns_records?per_page=500`);
const squarespaceIps = new Set(['198.185.159.144','198.185.159.145','198.49.23.144','198.49.23.145']);
const conflicts = records.filter(record =>
  (record.name === 'playreind.com' && record.type === 'A' && squarespaceIps.has(record.content)) ||
  (record.name === 'www.playreind.com' && record.type === 'CNAME' && record.content.replace(/\.$/, '') === 'ext-sq.squarespace.com')
);
const protectedRecords = records.filter(record => ['MX','TXT'].includes(record.type));

console.log(`PASS: active Cloudflare zone ${zone.name}; status ${zone.status}.`);
console.log(`Protected mail/TXT records preserved: ${protectedRecords.length}.`);
if (!conflicts.length) console.log('No verified Squarespace web records remain.');
for (const record of conflicts) console.log(`${apply ? 'Removing' : 'Would remove'} ${record.type} ${record.name} -> ${record.content}`);

if (apply) {
  for (const record of conflicts) await cf(`/zones/${zone.id}/dns_records/${record.id}`, { method: 'DELETE' });
  console.log(`PASS: removed ${conflicts.length} verified Squarespace web record(s); no other DNS records changed.`);
} else {
  console.log('DRY RUN: no DNS records changed. Re-run with --apply after reviewing the list.');
}
