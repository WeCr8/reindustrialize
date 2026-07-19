import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const fail = [];
const output = execFileSync('git', ['ls-files', '--cached'], { cwd: root, encoding: 'utf8' });
const files = output.split(/\r?\n/).filter(Boolean);
const forbidden = [
  /^\.env(?!\.example$)(?:\.|$)/,
  /^cloudflare-dist\//,
  /^dist\//,
  /^tmp\//,
  /^videos\//,
  /(?:^|\/)node_modules\//,
  /apps\/wecr8-info\/prototypes\/shop-floor-viewer\.html$/,
  /\.(?:mp4|webm|zip)$/i
];
const secretPatterns = [
  ['private key', /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/],
  ['Cloudflare credential', /(?:CLOUDFLARE_API_TOKEN|CLOUDFLARE_API_KEY)[ \t]*=[ \t]*["']?[A-Za-z0-9_-]{20,}/],
  ['ElevenLabs credential', /ELEVENLABS_API_KEY[ \t]*=[ \t]*["']?[A-Za-z0-9_-]{20,}/],
  ['Supabase service key', /SUPABASE_SERVICE_ROLE_KEY[ \t]*=[ \t]*["']?\S{20,}/],
  ['generic secret assignment', /(?:api[_-]?key|secret|token)["']?[ \t]*[:=][ \t]*["'][A-Za-z0-9_./+-]{32,}["']/i]
];

for (const relative of files) {
  if (forbidden.some(pattern => pattern.test(relative))) fail.push(`forbidden tracked path: ${relative}`);
  const absolute = path.join(root, relative);
  if (!fs.existsSync(absolute)) continue;
  const stat = fs.statSync(absolute);
  if (stat.size > 95 * 1024 * 1024) fail.push(`file exceeds 95 MiB: ${relative}`);
  if (stat.size > 5 * 1024 * 1024) continue;
  const text = fs.readFileSync(absolute, 'utf8');
  for (const [label, pattern] of secretPatterns) if (pattern.test(text)) fail.push(`${label} pattern: ${relative}`);
}

if (!files.length) fail.push('no files are staged/tracked for validation');
if (fail.length) {
  console.error('GIT RELEASE SECURITY CHECK FAILED');
  for (const item of fail) console.error(`- ${item}`);
  process.exit(1);
}
console.log(`PASS: ${files.length} prospective Git files contain no forbidden outputs, oversized files, or recognized secret literals.`);
