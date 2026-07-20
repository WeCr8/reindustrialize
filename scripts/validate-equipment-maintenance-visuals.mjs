import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const readJson = (file) => JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
const fail = (message) => {
  console.error(`MAINTENANCE VISUAL CHECK FAILED: ${message}`);
  process.exit(1);
};

const manifest = readJson("data/equipment-maintenance-visuals.json");
const machines = readJson("data/machines.json").machines;
const roster = readJson("data/hiring-roster.json").candidates;
const spriteAtlas = readJson("packages/assets/sprites/atlas.json");
const expectedStates = ["available", "locked_out", "service_in_progress", "restored"];

if (JSON.stringify(manifest.stateOrder) !== JSON.stringify(expectedStates)) {
  fail(`stateOrder must be ${expectedStates.join(" -> ")}`);
}

const pngSize = (file) => {
  const bytes = fs.readFileSync(file);
  if (bytes.length < 26 || bytes.subarray(1, 4).toString("ascii") !== "PNG") fail(`${file} is not a PNG`);
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20), colorType: bytes[25] };
};

for (const [atlasId, atlas] of Object.entries(manifest.atlases)) {
  const registered = spriteAtlas[atlasId];
  if (!registered) fail(`${atlasId} is missing from packages/assets/sprites/atlas.json`);
  const file = path.join(root, atlas.file);
  if (!fs.existsSync(file)) fail(`${atlas.file} is missing`);
  const image = pngSize(file);
  if (image.width !== atlas.width || image.height !== atlas.height) fail(`${atlasId} dimensions are ${image.width}x${image.height}, expected ${atlas.width}x${atlas.height}`);
  if (image.colorType !== 6) fail(`${atlasId} must be RGBA PNG with transparency`);
  if (atlas.columns !== 4 || atlas.rows !== 4 || image.width % 4 || image.height % 4) fail(`${atlasId} must be an exact 4x4 atlas`);
  if (registered.file !== path.basename(atlas.file) || registered.columns !== 4 || registered.rows !== 4 || registered.frames !== 16) fail(`${atlasId} registry metadata is incomplete`);
}

const records = [...manifest.equipment, ...manifest.facilityAssets];
const byMachine = new Map();
for (const record of records) {
  if (byMachine.has(record.machineId)) fail(`duplicate record for ${record.machineId}`);
  byMachine.set(record.machineId, record);
  const atlas = manifest.atlases[record.atlas];
  if (!atlas) fail(`${record.machineId} references unknown atlas ${record.atlas}`);
  if (!Number.isInteger(record.row) || record.row < 0 || record.row >= atlas.rows) fail(`${record.machineId} has invalid atlas row`);
  for (const field of ["fault", "preventiveTask", "returnToServiceCheck", "implementationStatus"]) {
    if (!record[field] || String(record[field]).trim().length < 4) fail(`${record.machineId} is missing ${field}`);
  }
  if (!Array.isArray(record.qualifiedRoles) || record.qualifiedRoles.length === 0) fail(`${record.machineId} has no qualified maintenance roles`);
  for (const role of record.qualifiedRoles) {
    const worker = roster.find((candidate) => candidate.role === role && candidate.maintenanceQualified && candidate.qualifications.includes(record.machineId));
    if (!worker) fail(`${record.machineId} role ${role} has no matching qualified hire`);
  }
}

for (const machine of machines) {
  if (!byMachine.has(machine.id)) fail(`${machine.id} has no four-state maintenance visual`);
}
if (!byMachine.has("restroom_station")) fail("restroom_station facility maintenance visual is missing");

const playable = records.filter((record) => record.implementationStatus === "playable").map((record) => record.machineId);
const orientation = records.filter((record) => record.implementationStatus !== "playable").map((record) => record.machineId);
console.log(`Maintenance visuals OK: ${records.length} assets, ${Object.keys(manifest.atlases).length} atlases, ${expectedStates.length} states each.`);
console.log(`Mechanically playable: ${playable.join(", ")}. Visual/orientation ready: ${orientation.join(", ")}.`);
