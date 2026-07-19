import { readFile, stat } from 'node:fs/promises';

const root = new URL('../', import.meta.url);
const json = async path => JSON.parse(await readFile(new URL(path, root), 'utf8'));
const story = await json('data/story-production.json');
const scenes = await json('data/player-scene-manifest.json');
const tour = await json('data/shop-tour.json');
const walkthroughs = (await json('data/station-walkthroughs.json')).walkthroughs;
const tasks = (await json('data/production-task-tutorials.json')).tasks;

const required = new Map();
const add = (path, reason) => {
  if (!required.has(path)) required.set(path, new Set());
  required.get(path).add(reason);
};

for (const [sequence, beats] of Object.entries(story.sequences)) {
  for (const beat of beats) {
    if (beat.status !== 'implemented') continue;
    if (beat.voice) add(`packages/assets/audio/zach/${beat.voice}.mp3`, `${sequence}/${beat.id} voice`);
    const scene = scenes.scenes[beat.visual];
    if (scene?.active) for (const asset of Object.values(scene.assets)) add(`packages/assets/${asset}`, `${sequence}/${beat.id} visual`);
  }
}
for (const name of ['welcome', 'path', 'choice']) add(`packages/assets/story-pre-founder-${name}-v1.png`, 'pre-founder visual');

const addPanel = (panel, reason) => {
  add(`packages/assets/audio/zach/${panel.voice}.mp3`, `${reason} voice`);
  if (panel.imageType === 'equipment') add(`packages/assets/equipment/${panel.image}.png`, `${reason} image`);
  if (panel.imageType === 'nox') add(`packages/assets/materials/${panel.image}.png`, `${reason} image`);
  if (panel.imageType === 'sprite') add(`packages/assets/sprites/${panel.image}.png`, `${reason} image`);
};
for (const stop of tour.stops) {
  addPanel(stop, `tour/${stop.id}`);
  addPanel({...stop, ...walkthroughs[stop.id]}, `walkthrough/${stop.id}`);
}
for (const task of tasks.filter(task => task.status === 'playable')) addPanel(task, `task/${task.id}`);

const errors = [];
let audio = 0;
let images = 0;
for (const [path, reasons] of required) {
  try {
    const info = await stat(new URL(path, root));
    if (!info.isFile() || info.size < 32) throw new Error(`file is empty or too small (${info.size} bytes)`);
    const bytes = await readFile(new URL(path, root));
    if (path.endsWith('.png')) {
      images++;
      if (!bytes.subarray(0, 8).equals(Buffer.from([137,80,78,71,13,10,26,10]))) throw new Error('invalid PNG signature');
      if (bytes.readUInt32BE(16) < 1 || bytes.readUInt32BE(20) < 1) throw new Error('invalid PNG dimensions');
    } else if (path.endsWith('.mp3')) {
      audio++;
      const id3 = bytes.subarray(0, 3).toString() === 'ID3';
      const frame = bytes[0] === 0xff && (bytes[1] & 0xe0) === 0xe0;
      if (!id3 && !frame) throw new Error('invalid MP3 header');
    }
  } catch (error) {
    errors.push(`${path}: ${error.message}; required by ${[...reasons].join(', ')}`);
  }
}
if (errors.length) throw new Error(`Runtime asset gate failed:\n- ${errors.join('\n- ')}`);
console.log(`PASS: ${required.size} required runtime assets (${images} PNG, ${audio} MP3) exist and have valid file signatures`);
