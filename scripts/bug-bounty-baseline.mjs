import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ignored = new Set(['node_modules', '.git', 'dist', 'cloudflare-dist', 'tmp', 'videos']);
const textExtensions = new Set(['.js','.mjs','.cjs','.ts','.tsx','.json','.html','.css','.md','.py','.ps1','.toml','.yaml','.yml','.env']);
const findings = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (ignored.has(entry.name)) continue;
    if (entry.name === '.env') continue;
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(file);
    else if (textExtensions.has(path.extname(entry.name).toLowerCase()) || entry.name.startsWith('.env')) inspect(file);
  }
}

function inspect(file) {
  if (fs.statSync(file).size > 5 * 1024 * 1024) return;
  const text = fs.readFileSync(file, 'utf8');
  const relative = path.relative(root, file).replaceAll('\\', '/');
  const checks = [
    ['private-key-material', /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/],
    ['cloudflare-token-literal', /(?:CLOUDFLARE_API_TOKEN|CLOUDFLARE_API_KEY)[ \t]*=[ \t]*["']?[A-Za-z0-9_-]{20,}/],
    ['elevenlabs-key-literal', /ELEVENLABS_API_KEY[ \t]*=[ \t]*["']?(?!\.env|process\.env|env\.)[A-Za-z0-9_-]{20,}/],
    ['dangerous-innerhtml-input', /innerHTML\s*=.*(?:location\.|URLSearchParams|postMessage|event\.data)/],
    ['javascript-url', /javascript\s*:/i]
  ];
  for (const [id, pattern] of checks) if (pattern.test(text)) findings.push({ id, file: relative });
}

walk(root);
const gitignore = fs.readFileSync(path.join(root, '.gitignore'), 'utf8');
if (!/^\.env\*/m.test(gitignore)) findings.push({ id: 'env-files-not-ignored', file: '.gitignore' });
if (findings.length) {
  console.error('BUG BOUNTY BASELINE FAILED');
  for (const finding of findings) console.error(`- ${finding.id}: ${finding.file}`);
  process.exit(1);
}
console.log('PASS: no private-key material, provider-token literals, obvious URL-script sinks, or direct untrusted innerHTML patterns found.');
