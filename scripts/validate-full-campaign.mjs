import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const matrix = JSON.parse(fs.readFileSync(path.join(root, 'data/full-campaign-completion.json'), 'utf8'));
const assertFull = process.argv.includes('--assert-1.0');
const allowedStatuses = new Set(['missing', 'partial', 'complete']);
const categories = matrix.requiredCategories;
const failures = [];

if (matrix.schemaVersion !== 1) failures.push('schemaVersion must be 1');
if (!Array.isArray(categories) || categories.length !== 7) failures.push('seven required proof categories must be declared');
if (!Array.isArray(matrix.chapters) || matrix.chapters.length !== 6) failures.push('exactly Chapters 1-6 must be declared');

for (let id = 1; id <= 6; id += 1) {
  const chapter = matrix.chapters.find((candidate) => candidate.id === id);
  if (!chapter) { failures.push(`Chapter ${id} missing`); continue; }
  for (const category of categories) {
    if (!chapter.requirements?.[category]) failures.push(`Chapter ${id} missing ${category} requirement`);
    const item = chapter.proof?.[category];
    if (item && (!allowedStatuses.has(item.status) || !item.evidence)) failures.push(`Chapter ${id} ${category} proof is invalid`);
    if (assertFull && item?.status !== 'complete') failures.push(`Chapter ${id} ${category} is not complete`);
    if (assertFull && item?.status === 'complete' && !fs.existsSync(path.join(root, item.evidence.split(' + ')[0].split(';')[0]))) {
      failures.push(`Chapter ${id} ${category} evidence path does not exist`);
    }
  }
}

const computedFull = matrix.chapters.every((chapter) => categories.every((category) => chapter.proof?.[category]?.status === 'complete'));
if (matrix.fullCampaignClaimAllowed !== computedFull) failures.push('fullCampaignClaimAllowed does not match proof state');
if (assertFull && matrix.productVersion !== '1.0') failures.push('productVersion must be 1.0 for a full-campaign claim');

if (failures.length) {
  console.error(`FAIL: full-campaign release truth gate (${failures.length} issue${failures.length === 1 ? '' : 's'}):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

const complete = matrix.chapters.map((chapter) => categories.filter((category) => chapter.proof?.[category]?.status === 'complete').length);
console.log(`PASS: campaign matrix is structurally honest; chapter proof coverage ${complete.join('/')} of ${categories.length}; full-campaign claim=${computedFull}.`);
