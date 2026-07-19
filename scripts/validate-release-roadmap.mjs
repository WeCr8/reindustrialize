import {readFile} from 'node:fs/promises';
const roadmap=JSON.parse(await readFile('data/release-roadmap.json','utf8'));
const progression=JSON.parse(await readFile('data/chapter-progression.json','utf8'));
const facilities=JSON.parse(await readFile('data/facilities.json','utf8')).facilities;
if(roadmap.currentRelease.status!=='completable_slice'||roadmap.currentRelease.publicProductionReady!==false)throw new Error('Current release must remain an honest completable slice, not production-ready');
if(roadmap.finalRelease.chapters!==progression.chapters.length)throw new Error('Roadmap chapter count differs from progression data');
for(const key of ['mainStoryHours','completionistHours'])if(JSON.stringify(roadmap.finalRelease[key])!==JSON.stringify(progression.campaignTime[key]))throw new Error(`${key} differs from progression data`);
if(roadmap.finalRelease.easterEggs!==progression.easterEggs.total)throw new Error('Easter egg total differs from progression data');
for(const chapter of progression.chapters.slice(0,-1)){const facility=facilities.find(x=>x.id===chapter.facility);const expected=chapter.gate.jobsShipped??chapter.gate.jobsShippedInChapter;if(facility?.moveGate?.jobsInChapter!==expected)throw new Error(`${chapter.facility} job move gate differs from chapter progression`);}
roadmap.milestones.forEach((item,index)=>{if(item.order!==index)throw new Error(`${item.id} has incorrect milestone order`);if(!item.exit)throw new Error(`${item.id} has no objective exit criterion`);});
if(roadmap.milestones.filter(x=>x.status==='in_progress').length!==1)throw new Error('Exactly one roadmap milestone must be in progress');
if(roadmap.milestones.at(-1)?.id!=='version_1_0')throw new Error('Roadmap must end at version_1_0');
console.log(`PASS: roadmap distinguishes current ${roadmap.currentRelease.label} from ${roadmap.finalRelease.chapters}-chapter ${roadmap.finalRelease.label} across ${roadmap.milestones.length} ordered milestones`);
