import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const readJson = (file) => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const manifest = readJson('data/audio-generation.json');
const matrix = readJson('data/audio-coverage-matrix.json');
const runtime = fs.readFileSync(path.join(root, 'scripts/build_level_viewer_v4.py'), 'utf8');
const failures = [];
const ids = new Set();

function check(condition, message) { if (!condition) failures.push(message); }
function isMp3(file) {
  if (!fs.existsSync(file) || fs.statSync(file).size < 1000) return false;
  const bytes = fs.readFileSync(file).subarray(0, 3);
  return bytes.toString('ascii') === 'ID3' || (bytes[0] === 0xff && (bytes[1] & 0xe0) === 0xe0);
}
function verifyGenerated(kind, item, shippedDir = null) {
  const generated = path.join(root, 'packages/assets/audio/generated', kind, `${item.id}.mp3`);
  const receiptPath = path.join(root, 'packages/assets/audio/generated', kind, `${item.id}.receipt.json`);
  const generatedExists = fs.existsSync(generated), receiptExists = fs.existsSync(receiptPath);
  if (shippedDir) check(isMp3(path.join(root, shippedDir, `${item.id}.mp3`)), `${item.id} shipped MP3 missing or invalid`);
  if (!generatedExists && !receiptExists) return;
  check(isMp3(generated), `${kind}/${item.id} generated MP3 is invalid`);
  check(receiptExists, `${kind}/${item.id} receipt missing beside generated audio`);
  if (!generatedExists || !receiptExists) return;
  const receipt = readJson(path.relative(root, receiptPath));
  const hash = crypto.createHash('sha256').update(fs.readFileSync(generated)).digest('hex');
  check(receipt.id === item.id && receipt.kind === kind, `${kind}/${item.id} receipt identity mismatch`);
  check(receipt.sha256 === hash, `${kind}/${item.id} receipt hash mismatch`);
  if (kind === 'voice') check(receipt.request?.model_id === manifest.voice.modelId, `${item.id} voice model drift`);
  if (shippedDir) {
    const shipped = path.join(root, shippedDir, `${item.id}.mp3`);
    if (fs.existsSync(shipped)) {
      const shippedHash = crypto.createHash('sha256').update(fs.readFileSync(shipped)).digest('hex');
      check(shippedHash === hash, `${item.id} shipped audio differs from approved generated receipt`);
    }
  }
}

for (const clip of manifest.voice.clips) {
  check(!ids.has(clip.id), `duplicate audio ID ${clip.id}`); ids.add(clip.id);
  check(typeof clip.text === 'string' && clip.text.trim().length > 0, `${clip.id} has empty script`);
  if (clip.role === 'player') check(Boolean(clip.voiceId), `${clip.id} player voice ID missing`);
  else verifyGenerated('voice', clip, 'packages/assets/audio/zach');
}
for (const effect of manifest.sfx.effects) {
  check(!ids.has(effect.id), `duplicate audio ID ${effect.id}`); ids.add(effect.id);
  // cnc_cycle is a superseded generic prompt. Runtime deliberately uses the
  // drill/end-mill/ball-mill recordings so G1 engagement sounds physically differ.
  if (effect.id === 'cnc_cycle') check(!runtime.includes('"cnc_cycle"'), 'generic cnc_cycle must not replace cutter-specific runtime audio');
  else verifyGenerated('sfx', effect, 'packages/assets/audio/sfx');
}
for (const track of manifest.music.tracks) {
  check(!ids.has(track.id), `duplicate audio ID ${track.id}`); ids.add(track.id);
  verifyGenerated('music', track);
}

const voiceText = new Map(manifest.voice.clips.map((clip) => [clip.id, clip.text]));
for (const [file, records] of [
  ['data/story-production.json', Object.values(readJson('data/story-production.json').sequences).flat()],
  ['data/production-task-tutorials.json', readJson('data/production-task-tutorials.json').tasks],
  ['data/shop-tour.json', readJson('data/shop-tour.json').stops],
  ['data/station-walkthroughs.json', Object.values(readJson('data/station-walkthroughs.json').walkthroughs)]
]) {
  for (const record of records.filter((item) => item.voice)) {
    check(voiceText.get(record.voice) === record.text, `${file}/${record.id} caption does not exactly match ${record.voice}`);
  }
}

for (const match of runtime.matchAll(/playZach\("([a-z0-9_]+)"\)/g)) {
  check(voiceText.has(match[1]), `runtime references undeclared voice ${match[1]}`);
}
for (const token of [
  'ELEVENLABS_ZACH_VOICE_ID', 'item.role === "player" ? item.voiceId : voiceId',
  'function stopZach(', 'setAmbienceLevel(false)', 'ducked ? .38 : 1',
  'masterVolume*voiceVolume', 'masterVolume*sfxVolume*volume', 'masterVolume*ambienceVolume',
  'stopZach("VOICE: MUTED")', 'stopZach("VOICE: NARRATION PAUSED")',
  'cnc_rapid_traverse', 'end_mill_cut_aluminum', 'drill_cut_aluminum', 'ball_mill_cut_aluminum',
  'coolant_off', 'spindle_stop', 'M30'
]) check(runtime.includes(token) || fs.readFileSync(path.join(root, 'scripts/generate-elevenlabs-audio.mjs'), 'utf8').includes(token), `audio pipeline/runtime token missing: ${token}`);

check(matrix.schemaVersion === 1 && matrix.chapters?.length === 6, 'audio coverage matrix must contain Chapters 1-6');
for (const chapter of matrix.chapters || []) {
  for (const category of matrix.categories || []) {
    const item = chapter.coverage?.[category];
    check(Boolean(item?.status && item?.need), `Chapter ${chapter.chapter} missing ${category} status/need`);
    if (chapter.chapter > 1) check(item?.status !== 'implemented' || category === 'ambience', `Chapter ${chapter.chapter} falsely claims implemented ${category}`);
  }
}
check(!runtime.includes('founding_dawn') && matrix.chapters[0].coverage.music.status === 'generated-unwired', 'music runtime truth status drift');

if (failures.length) {
  console.error(`FAIL: audio production gate (${failures.length} issue${failures.length === 1 ? '' : 's'})`);
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}
console.log(`PASS: ${manifest.voice.clips.length} voice scripts, ${manifest.sfx.effects.length} SFX, ${manifest.music.tracks.length} planned/generated-local music prototypes, shipped MP3 integrity, optional production receipts/hashes, exact captions, runtime triggers, mix recovery, and Chapters 1-6 truth verified.`);
