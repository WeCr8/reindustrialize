import { spawnSync } from 'node:child_process';

const checks = [
  ['Runtime image and audio integrity', 'node', ['scripts/validate-runtime-assets.mjs']],
  ['Story order, visuals, voice, and captions', 'node', ['scripts/validate-story-production.mjs']],
  ['Garage tour coverage and narration', 'node', ['scripts/validate-shop-tour.mjs']],
  ['Playable task tutorials and validation states', 'node', ['scripts/validate-production-task-tutorials.mjs']],
  ['Founder variants and scene overlays', 'python', ['scripts/validate-player-scenes.py']],
  ['Visual runtime wiring and Chapter 1-6 coverage truth', 'node', ['scripts/validate-visual-coverage.mjs']],
  ['Audio production, playback, mix, and Chapter 1-6 coverage truth', 'node', ['scripts/validate-audio-production.mjs']],
  ['Human operations, difficulty pacing, and facility-space realism', 'node', ['scripts/validate-manufacturing-realism.mjs']],
  ['Full-campaign completion claims and evidence truth', 'node', ['scripts/validate-full-campaign.mjs']],
  ['Game data, progression, maps, and references', 'python', ['scripts/selfcheck.py', '--dry']],
  ['Current-to-1.0 growth roadmap consistency', 'node', ['scripts/validate-release-roadmap.mjs']],
];

console.log('\nREINDUSTRIALIZE REQUIRED PRODUCTION GATE');
console.log('Planned future scenes do not block a current build; every implemented/playable item does.\n');
let failed = false;
for (const [label, command, args] of checks) {
  const result = spawnSync(command, args, {stdio: 'inherit', shell: process.platform === 'win32'});
  if (result.status === 0) console.log(`[x] ${label}`);
  else {
    failed = true;
    console.error(`[ ] ${label} — FAILED`);
  }
}
if (failed) {
  console.error('\nBUILD BLOCKED: fix every unchecked production requirement above.');
  process.exit(1);
}
console.log('\n[x] RELEASE GATE COMPLETE — required images, audio, story, tutorials, scenes, and game data are in order.\n');
