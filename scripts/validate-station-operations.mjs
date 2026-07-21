import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const read = (file) => JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
const operations = read("data/station-operations.json");
const maps = [read("data/maps/bay_01.json"), read("data/maps/bay_02.json")];
const roster = read("data/hiring-roster.json");
const failures = [];
const modes = new Set(["playable", "orientation", "management", "facility"]);

for (const map of maps) {
  for (const placement of map.placements) {
    const station = operations.stations[placement.sprite];
    if (!station) {
      failures.push(`${map.id || "map"}: ${placement.sprite} has no station operation definition`);
      continue;
    }
    for (const field of ["name", "mode", "mission", "details"]) {
      if (!String(station[field] || "").trim()) failures.push(`${placement.sprite}: missing ${field}`);
    }
    if (!modes.has(station.mode)) failures.push(`${placement.sprite}: invalid mode ${station.mode}`);
    if (!Number.isFinite(station.cycleMinutes) || station.cycleMinutes < 0) {
      failures.push(`${placement.sprite}: cycleMinutes must be a non-negative number`);
    }
  }
}

const queueableStations = operations.timeModel?.queueableStations || [];
for (const sprite of queueableStations) {
  const station = operations.stations[sprite];
  if (!station || station.mode !== "playable" || station.cycleMinutes <= 0) failures.push(`${sprite}: queue policy requires a timed playable station`);
  const qualified = roster.candidates.filter((candidate) => candidate.qualifications.includes(sprite));
  if (!qualified.length) failures.push(`${sprite}: timed worker queue has no qualified hire`);
}
for (const [sprite, station] of Object.entries(operations.stations)) {
  if (station.mode === "orientation" && queueableStations.includes(sprite)) failures.push(`${sprite}: orientation-only station cannot expose production queues`);
}

for (const [sprite, minutes] of [["saw_t1", 5], ["vmc_t2", 10]]) {
  const station = operations.stations[sprite];
  if (station?.mode !== "playable") failures.push(`${sprite}: must remain playable`);
  if (station?.cycleMinutes !== minutes) failures.push(`${sprite}: expected ${minutes}-minute standard cycle`);
}

if (operations.timeModel?.continuesWhileAway !== true || operations.timeModel?.continuesWhileClosed !== true) {
  failures.push("timeModel must continue while away and persist across reload");
}
if (operations.timeModel?.completionRequiresCollection !== true) failures.push("timeModel must require collection/inspection");

if (failures.length) {
  console.error(`FAIL: station operation contract\n- ${failures.join("\n- ")}`);
  process.exit(1);
}

console.log(`PASS: ${Object.keys(operations.stations).length} station definitions cover both maps; every production timer has qualified worker coverage and persistent collection-gated queues`);
