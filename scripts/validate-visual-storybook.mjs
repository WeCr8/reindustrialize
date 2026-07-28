import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd(),dir=path.join(root,'storybook/v1');
const m=JSON.parse(fs.readFileSync(path.join(dir,'storybook-manifest.json'),'utf8'));
const story=JSON.parse(fs.readFileSync(path.join(root,'data/story-production.json'),'utf8'));
const scene=JSON.parse(fs.readFileSync(path.join(root,'data/player-scene-manifest.json'),'utf8'));
const hiring=JSON.parse(fs.readFileSync(path.join(root,'data/hiring-roster.json'),'utf8'));
const html=fs.readFileSync(path.join(dir,'index.html'),'utf8'),fail=[];
const resolveBook=value=>path.resolve(dir,value);

if(m.founderCount!==10)fail.push('expected ten selectable founders');
if(m.employeeCount!==hiring.candidates.length)fail.push(`expected ${hiring.candidates.length} employees in storybook`);
const founderSelection=m.slides.filter(s=>s.section==='Founder Selection');
if(founderSelection.length!==10)fail.push('expected ten founder selection slides');
for(const s of founderSelection)if(!s.portraitAtlas||!Number.isInteger(s.portraitCell)||!s.sprite)fail.push(`founder selection slide ${s.number} lacks portrait or floor sprite`);

for(const f of Object.keys(scene.founders))for(const title of ['Founder Title','Chapter 1 · Garage Bay','Chapter 2 · Job Shop'])if(!m.slides.some(s=>s.founder===f&&s.title.startsWith(title)))fail.push(`missing ${title} proof for ${f}`);
const founders=Object.keys(scene.founders),milestones=['first_customer','nox_delivery','first_verified_article','first_hire','garage_graduation'];
for(const sequence of milestones)for(const beat of story.sequences[sequence])for(const founder of founders){const slide=m.slides.find(s=>s.storySequence===sequence&&s.storyBeat===beat.id&&s.founder===founder);if(!slide)fail.push(`missing ${sequence}/${beat.id} proof for ${founder}`);else{if(slide.text!==beat.text)fail.push(`caption drift in ${sequence}/${beat.id} for ${founder}`);if((slide.voice||null)!==(beat.voice||null))fail.push(`voice drift in ${sequence}/${beat.id} for ${founder}`);}}

for(const chapter of story.campaignPlan.chapters){const slides=m.slides.filter(s=>s.chapter===chapter.chapter);for(const phase of ['entry','learn','prove','operate','recover','graduate'])if(!slides.some(s=>s.campaignPhase===phase))fail.push(`storybook lacks Chapter ${chapter.chapter} ${phase} coverage`);for(const slide of slides.filter(s=>s.status!=='implemented')){if(slide.voice)fail.push(`planned Chapter ${chapter.chapter} slide falsely claims voice`);if(slide.image)fail.push(`planned Chapter ${chapter.chapter} slide falsely claims finished art`);}}

const workforce=m.slides.filter(s=>s.section==='Factory Workforce');
const conversations=m.slides.filter(s=>s.section==='Workforce Conversations');
if(workforce.length!==hiring.candidates.length||conversations.length!==hiring.candidates.length)fail.push('every employee needs both profile and conversation slides');
for(const hire of hiring.candidates){for(const section of ['Factory Workforce','Workforce Conversations']){const slide=m.slides.find(s=>s.section===section&&s.employeeId===hire.id);if(!slide){fail.push(`${hire.id} missing ${section} slide`);continue;}for(const field of ['portraitAtlas','spriteAtlas'])if(!slide[field]||!fs.existsSync(resolveBook(slide[field])))fail.push(`${hire.id} ${section} missing ${field}`);for(const field of ['portraitCell','spriteCell','portraitColumns','portraitRows','spriteColumns','spriteRows'])if(!Number.isInteger(slide[field]))fail.push(`${hire.id} ${section} invalid ${field}`);if(slide.portraitCell!==slide.spriteCell)fail.push(`${hire.id} profile/sprite identity cell mismatch`);}}

for(const slide of m.slides){if(slide.status!=='planned'&&!slide.image)fail.push(`implemented slide ${slide.number} lacks image`);for(const field of ['image','sprite','portraitAtlas','spriteAtlas','voiceSrc'])if(slide[field]&&!fs.existsSync(resolveBook(slide[field])))fail.push(`missing ${field} for slide ${slide.number}: ${slide[field]}`);if(slide.voice&&slide.status!=='planned'&&!slide.voiceSrc)fail.push(`implemented voice ${slide.voice} has no playable audio on slide ${slide.number}`);}

const packaged=[];for(const entry of fs.readdirSync(path.join(root,'packages/assets'),{recursive:true,withFileTypes:true})){if(!entry.isFile())continue;const full=path.join(entry.parentPath,entry.name);if(['.png','.mp3'].includes(path.extname(entry.name).toLowerCase()))packaged.push(path.relative(root,full).replaceAll('\\','/'));}
const catalogPaths=m.assetCatalog.map(item=>item.path),unique=new Set(catalogPaths);
if(unique.size!==catalogPaths.length)fail.push('asset catalog contains duplicate paths');
for(const file of packaged)if(!unique.has(file))fail.push(`packaged graphic/audio omitted from storybook catalog: ${file}`);
for(const item of m.assetCatalog){const full=path.join(root,item.path);if(!fs.existsSync(full))fail.push(`catalog asset missing: ${item.path}`);if(!['graphic','audio'].includes(item.kind))fail.push(`catalog asset kind invalid: ${item.path}`);if(!['implemented-reference','generated-candidate','source-reference','storybook-review'].includes(item.lifecycle))fail.push(`catalog lifecycle invalid: ${item.path}`);if(!html.includes(item.src))fail.push(`catalog asset is not referenced by HTML: ${item.path}`);}
if(m.assetSummary.total!==m.assetCatalog.length||m.assetSummary.graphics!==m.assetCatalog.filter(x=>x.kind==='graphic').length||m.assetSummary.audio!==m.assetCatalog.filter(x=>x.kind==='audio').length)fail.push('asset summary counts drifted');
if(!m.missingNeeds.length||m.assetSummary.missingNeeds!==m.missingNeeds.length)fail.push('missing production-needs queue is empty or miscounted');
for(const marker of ['data-view="slides"','data-view="assets"','data-view="needs"','Complete asset library','Production needs queue','spriteAtlas','voiceSrc'])if(!html.includes(marker))fail.push(`storybook HTML feature missing: ${marker}`);

const slidesDir=path.join(dir,'slides'),pngs=fs.existsSync(slidesDir)?fs.readdirSync(slidesDir).filter(file=>file.endsWith('.png')):[];
if(pngs.length!==m.slideCount)fail.push(`expected ${m.slideCount} PNGs, found ${pngs.length}`);
if(fail.length){console.error(fail.map(item=>'FAIL: '+item).join('\n'));process.exit(1)}
console.log(`PASS: storybook V${m.storybookVersion}: ${m.slideCount} slides, ${m.founderCount} founders, ${m.employeeCount} employee profile/sprite pairs, ${m.assetSummary.graphics} graphics, ${m.assetSummary.audio} audio files, and ${m.assetSummary.missingNeeds} explicit future needs.`);
