import { readFile, stat } from "node:fs/promises";

const manifest = JSON.parse(await readFile("data/audio-generation.json", "utf8"));
const required = [
  "machine_power_on", "machine_power_off", "cnc_idle", "spindle_start", "spindle_run", "spindle_stop",
  "coolant_on", "coolant_off", "end_mill_cut_aluminum", "drill_cut_aluminum", "ball_mill_cut_aluminum",
  "bandsaw_power_on", "bandsaw_power_off", "bandsaw_cut", "cnc_door_close", "manual_mill_run",
  "deburr_tool", "probe_touch", "air_blowoff",
];
const declared = new Set(manifest.sfx.effects.map(effect => effect.id));
const runtime = await readFile("scripts/build_level_viewer_v4.py", "utf8");

for (const id of required) {
  if (!declared.has(id)) throw new Error(`Equipment SFX is not declared: ${id}`);
  const path = `packages/assets/audio/sfx/${id}.mp3`;
  const info = await stat(path);
  if (info.size < 1000) throw new Error(`Equipment SFX is empty or invalid: ${path}`);
}
for (const id of ["machine_power_on", "machine_power_off", "spindle_start", "spindle_stop", "coolant_on", "coolant_off", "end_mill_cut_aluminum", "drill_cut_aluminum", "ball_mill_cut_aluminum", "bandsaw_power_on", "bandsaw_power_off", "bandsaw_cut"]) {
  if (!runtime.includes(`"${id}"`)) throw new Error(`Playable event is not wired to SFX: ${id}`);
}
console.log(`PASS: ${required.length} equipment SFX declared, present, and playable-event wiring verified.`);
