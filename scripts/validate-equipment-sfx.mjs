import { readFile, stat } from "node:fs/promises";

const manifest = JSON.parse(await readFile("data/audio-generation.json", "utf8"));
const required = [
  "machine_power_on", "machine_power_off", "cnc_idle", "spindle_start", "spindle_run", "spindle_stop",
  "coolant_on", "coolant_off", "end_mill_cut_aluminum", "drill_cut_aluminum", "ball_mill_cut_aluminum",
  "bandsaw_power_on", "bandsaw_power_off", "bandsaw_cut", "cnc_door_close", "manual_mill_run",
  "deburr_tool", "probe_touch", "air_blowoff", "cnc_rapid_traverse", "cnc_door_open",
  "machine_vise_clamp", "toolholder_load", "tool_drawer_open", "tool_torque_click", "bandsaw_vise_clamp",
  "planning_paperwork", "terminal_wake", "terminal_confirm", "chalk_marker", "lathe_chuck_clamp",
  "lathe_turret_index", "network_connect", "handoff_confirm", "mission_board_update", "cnc_tool_change",
  "lathe_cycle", "caliper_measure", "micrometer_click", "pallet_delivery", "quest_complete", "quality_pass",
  "quality_fail", "coins_xp", "facility_unlock",
  "amr_drive", "cobot_motion", "rfid_tool_scan",
  "shop_ambience_small", "factory_ambience_large", "job_shop_ambience", "shop_office_ambience", "factory_night_ambience",
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
for (const token of ["nextPoint?.rapid?\"G0\":\"G1\"", "cnc_rapid_traverse", "cnc_tool_change", "tscene.dataset.motionCode=\"M30\"", "M{{s}}", "G43 H01", "G80 G00", "M09", "M05", "G28 G91", "M30"]) {
  if (!runtime.includes(token)) throw new Error(`CNC sequence marker missing: ${token}`);
}
for (const station of ["nox_terminal", "saw_t1", "tool_cart", "presetter_t4", "toolcrib_rfid_t4", "vmc_t2", "lathe_cnc_t2", "planning_desk", "chalkboard", "mill_manual_t1", "bench_deburr_t1", "network_node_t3", "handoff_terminal_t4", "nox_pallet", "whiteboard", "amr_t5", "cobot_t5"]) {
  if (!runtime.includes(`${station}:`)) throw new Error(`Mapped station has no interaction SFX: ${station}`);
}
for (const token of ["ambienceVolume", "0.16", "setAmbienceLevel(true)", "setAmbienceLevel(false)", "job_shop_ambience", "shop_ambience_small", "AMBIENCE ON"]) {
  if (!runtime.includes(token)) throw new Error(`Ambience behavior missing: ${token}`);
}
console.log(`PASS: ${required.length} equipment SFX declared, present, and playable-event wiring verified.`);
