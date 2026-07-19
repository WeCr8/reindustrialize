import {readFile} from 'node:fs/promises';
const roadmap=JSON.parse(await readFile('data/release-roadmap.json','utf8'));
const progression=JSON.parse(await readFile('data/chapter-progression.json','utf8'));
const facilities=JSON.parse(await readFile('data/facilities.json','utf8')).facilities;
const tiers=JSON.parse(await readFile('data/progression.json','utf8')).tiers;
if(roadmap.currentRelease.status!=='completable_slice'||roadmap.currentRelease.publicProductionReady!==false)throw new Error('Current release must remain an honest completable slice, not production-ready');
if(roadmap.finalRelease.chapters!==progression.chapters.length)throw new Error('Roadmap chapter count differs from progression data');
for(const [roadmapKey,progressionKey] of [['mainStoryHours','mainStoryPlayerHours'],['completionistHours','completionistPlayerHours']])if(JSON.stringify(roadmap.finalRelease[roadmapKey])!==JSON.stringify(progression.campaignTime[progressionKey]))throw new Error(`${roadmapKey} differs from progression data`);
if(roadmap.finalRelease.easterEggs!==progression.easterEggs.total)throw new Error('Easter egg total differs from progression data');
for(const chapter of progression.chapters.slice(0,-1)){const facility=facilities.find(x=>x.id===chapter.facility);const expected=chapter.gate.jobsShipped??chapter.gate.jobsShippedInChapter;if(facility?.moveGate?.jobsInChapter!==expected)throw new Error(`${chapter.facility} job move gate differs from chapter progression`);}
const expectedStatuses=['playable','development','locked','locked','locked','locked'];
const rising={jobs:[],operations:[],quality:[],headcount:[],concurrency:[],area:[]};
const delivery=[],scrap=[],automation=[];
for(const [index,chapter] of progression.chapters.entries()){
  if(chapter.chapter!==index+1)throw new Error(`Chapter ${chapter.chapter} is out of order`);
  if(chapter.releaseStatus!==expectedStatuses[index])throw new Error(`Chapter ${chapter.chapter} must remain ${expectedStatuses[index]}`);
  if(JSON.stringify(chapter.levels)!==JSON.stringify([index*5+1,index*5+5]))throw new Error(`Chapter ${chapter.chapter} level band is not five contiguous levels`);
  if(!Array.isArray(chapter.taskArcs)||chapter.taskArcs.length<6)throw new Error(`Chapter ${chapter.chapter} needs at least six distinct task arcs`);
  const facility=facilities.find(item=>item.id===chapter.facility),tier=tiers.find(item=>item.tier===chapter.chapter);
  if(!facility||facility.chapter!==chapter.chapter)throw new Error(`Chapter ${chapter.chapter} facility link is invalid`);
  if(!tier)throw new Error(`Chapter ${chapter.chapter} tier is missing`);
  const facilityGate=facility.moveGate??facility.graduationGate;
  const jobs=chapter.gate.jobsShipped??chapter.gate.jobsShippedInChapter;
  for(const [key,value] of [['jobsInChapter',jobs],['requiredProductionOperations',chapter.gate.requiredProductionOperations],['minimumAverageQuality',chapter.gate.minimumAverageQuality],['headcount',chapter.gate.headcount],['peakConcurrentJobs',chapter.gate.peakConcurrentJobs??1]])if(facilityGate?.[key]!==value)throw new Error(`Chapter ${chapter.chapter} ${key} differs from its facility gate`);
  for(const [tierKey,value] of [['jobsInChapter',jobs],['requiredProductionOperations',chapter.gate.requiredProductionOperations],['minAverageQuality',chapter.gate.minimumAverageQuality],['headcount',chapter.gate.headcount],['peakConcurrentJobs',chapter.gate.peakConcurrentJobs??1]])if(tier.masteryGate[tierKey]!==value)throw new Error(`Chapter ${chapter.chapter} ${tierKey} differs from tier progression`);
  if(index>0){if(facilityGate.onTimeRate!==chapter.gate.onTimeRate||facilityGate.maximumScrapRate!==chapter.gate.maximumScrapRate||tier.masteryGate.onTimeRate!==chapter.gate.onTimeRate||tier.masteryGate.maximumScrapRate!==chapter.gate.maximumScrapRate)throw new Error(`Chapter ${chapter.chapter} delivery or scrap gate differs across sources`);}
  if(index>=3){if(facilityGate.automatedCells!==chapter.gate.validatedAutomatedCells||tier.masteryGate.automatedCells!==chapter.gate.validatedAutomatedCells)throw new Error(`Chapter ${chapter.chapter} automation gate differs across sources`);}
  if(chapter.gate.requiredProductionOperations<jobs*4)throw new Error(`Chapter ${chapter.chapter} requires fewer than four production operations per job`);
  rising.jobs.push(jobs);rising.operations.push(chapter.gate.requiredProductionOperations);rising.quality.push(chapter.gate.minimumAverageQuality);rising.headcount.push(chapter.gate.headcount);rising.concurrency.push(chapter.gate.peakConcurrentJobs??1);rising.area.push(facility.floorAreaSqFt);
  if(index>0){delivery.push(chapter.gate.onTimeRate);scrap.push(chapter.gate.maximumScrapRate);}
  if(index>=3)automation.push(chapter.gate.validatedAutomatedCells);
}
for(const [name,values] of Object.entries(rising))for(let i=1;i<values.length;i++)if(values[i]<=values[i-1])throw new Error(`${name} does not rise from Chapter ${i} to ${i+1}`);
for(let i=1;i<delivery.length;i++)if(delivery[i]<=delivery[i-1])throw new Error(`on-time requirement does not rise after Chapter ${i+1}`);
for(let i=1;i<scrap.length;i++)if(scrap[i]>=scrap[i-1])throw new Error(`scrap ceiling does not tighten after Chapter ${i+1}`);
for(let i=1;i<automation.length;i++)if(automation[i]<=automation[i-1])throw new Error(`automation requirement does not rise after Chapter ${i+3}`);
roadmap.milestones.forEach((item,index)=>{if(item.order!==index)throw new Error(`${item.id} has incorrect milestone order`);if(!item.exit)throw new Error(`${item.id} has no objective exit criterion`);});
if(roadmap.milestones.filter(x=>x.status==='in_progress').length!==1)throw new Error('Exactly one roadmap milestone must be in progress');
if(roadmap.milestones.at(-1)?.id!=='version_1_0')throw new Error('Roadmap must end at version_1_0');
console.log(`PASS: 6-chapter curve rises ${rising.jobs.join('→')} jobs, ${rising.operations.join('→')} operations, ${rising.headcount.join('→')} staff, and ${rising.area.join('→')} sq ft; quality, delivery, scrap, concurrency, automation, source parity, and release truth verified.`);
