import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd(),read=file=>JSON.parse(fs.readFileSync(path.join(root,file),'utf8'));
const matrix=read('data/visual-coverage-v1.json'),maps=[read('data/maps/bay_01.json'),read('data/maps/bay_02.json')],equipment=read('data/equipment-views.json'),scene=read('data/player-scene-manifest.json'),hires=read('data/hiring-roster.json'),founders=read('data/founder-profiles.json'),customers=read('data/customer-contracts.json'),tour=read('data/shop-tour.json'),tasks=read('data/production-task-tutorials.json'),atlas=read('packages/assets/sprites/atlas.json'),fail=[];
const exists=file=>fs.existsSync(path.join(root,file));
if(matrix.schemaVersion!==1||matrix.coverageVersion!=='0.7.0-alpha-visual-v1')fail.push('visual coverage matrix version is invalid');
if(matrix.chapters.length!==6)fail.push('visual coverage must describe all six chapters');
const statuses=['playable','development','locked','locked','locked','locked'];
for(const [index,chapter] of matrix.chapters.entries()){
  if(chapter.chapter!==index+1||chapter.releaseStatus!==statuses[index])fail.push(`chapter ${index+1} visual release truth is invalid`);
  if(!Array.isArray(chapter.missing)||!chapter.missing.length)fail.push(`chapter ${index+1} incorrectly claims no missing visuals`);
  for(const asset of chapter.implemented??[])if(!exists(asset))fail.push(`implemented visual is missing: ${asset}`);
}
for(const asset of matrix.globalImplemented)if(!exists(asset))fail.push(`global implemented visual is missing: ${asset}`);
if(maps[1].unlocksAtTier!==2)fail.push('Job Shop map must unlock at Chapter/Tier 2');
const source=fs.readFileSync(path.join(root,'scripts/build_level_viewer_v4.py'),'utf8');
for(const label of ['BLONDE M','BLONDE F','M.E. M','M.E. F','INDIAN M','INDIAN F'])if(source.includes(`<span>${label}</span>`))fail.push(`founder selector exposes demographic label ${label}`);
for(const [id,view] of Object.entries(equipment.views))if(!exists(`packages/assets/${view.asset}`))fail.push(`equipment open view missing: ${id}`);
const chapterOneMissing=new Set(matrix.chapters[0].missing);
for(const id of equipment.requiredFutureViews)if(![...chapterOneMissing,...matrix.chapters[1].missing].some(item=>item.includes(id.replaceAll('_','-'))||item.includes(id)))fail.push(`future equipment view not represented in visual backlog: ${id}`);
for(const [id,entry] of Object.entries(atlas))if(!exists(`packages/assets/sprites/${entry.file}`))fail.push(`sprite atlas entry missing file: ${id}`);
if(Object.keys(scene.founders).length!==10||founders.profiles.length!==10)fail.push('founder sprite/profile coverage is not 10');
if(!matrix.runtimeCounts||hires.candidates.length!==matrix.runtimeCounts.hires||customers.customers.length!==matrix.runtimeCounts.customers)fail.push('workforce or customer profile coverage changed without matrix update');
if(tasks.tasks.length!==9||tour.stops.length!==14)fail.push('task guide or tour coverage changed without matrix update');
for(const item of [...tasks.tasks,...tour.stops]){
  if(item.imageType==='equipment'&&!Object.hasOwn(equipment.views,item.station??item.sprite)&&!Object.values(equipment.views).some(view=>path.basename(view.asset,'.png')===item.image))fail.push(`unwired equipment illustration: ${item.id}`);
  if(item.imageType==='sprite'&&!Object.hasOwn(atlas,item.image))fail.push(`unwired tutorial sprite: ${item.id}`);
}
if(fail.length){console.error(fail.map(item=>'FAIL: '+item).join('\n'));process.exit(1)}
console.log(`PASS: visual matrix v1 verifies ${Object.keys(scene.founders).length} founders, ${hires.candidates.length} hires, ${customers.customers.length} customers, ${Object.keys(equipment.views).length} equipment views, ${tasks.tasks.length} task guides, ${tour.stops.length} tour stops, all runtime mappings, and honest Chapters 1–6 gaps.`);
