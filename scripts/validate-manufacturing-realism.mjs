import {readFile} from 'node:fs/promises';

const realism=JSON.parse(await readFile('data/manufacturing-realism-contract.json','utf8'));
const progression=JSON.parse(await readFile('data/chapter-progression.json','utf8'));
const facilities=JSON.parse(await readFile('data/facilities.json','utf8'));
const fail=[];
const plans=new Map(realism.chapters.map(x=>[x.chapter,x]));
const facilityById=new Map(facilities.facilities.map(x=>[x.id,x]));
const areaKeys=['productionAndMachineClearance','aislesAndForkliftFlow','rawWipFinishedInventory','receivingAndShipping','inspectionAndMetrology','maintenanceAndToolroom','utilitiesAndPlantSupport','officesTrainingAmenities','expansionReserve'];
if(realism.chapters.length!==6)fail.push('realism contract must cover Chapters 1–6');
if(progression.campaignTime.mainStoryHours||!progression.campaignTime.mainStoryPlayerHours)fail.push('campaign time must distinguish player-hours from simulated elapsed time');
const summedHours=progression.chapters.reduce((sum,chapter)=>[sum[0]+chapter.targetHours[0],sum[1]+chapter.targetHours[1]],[0,0]);
if(JSON.stringify(summedHours)!==JSON.stringify(progression.campaignTime.mainStoryPlayerHours))fail.push(`chapter hours ${summedHours.join('–')} do not equal the main campaign target`);
if(progression.campaignTime.completionistPlayerHours[0]<=summedHours[0]||progression.campaignTime.completionistPlayerHours[1]<=summedHours[1])fail.push('completionist campaign must extend beyond the main story');
if(!progression.audienceDifficultyRule?.chapters1To2?.includes('family-friendly')||!progression.audienceDifficultyRule.rule?.includes('must not depend on obscure controls'))fail.push('family-friendly teach-through-play rule is missing');
for(const chapter of progression.chapters){
  const plan=plans.get(chapter.chapter),facility=facilityById.get(chapter.facility);if(!plan||!facility){fail.push(`Chapter ${chapter.chapter} lacks realism or facility data`);continue;}
  if(plan.facility!==chapter.facility)fail.push(`Chapter ${chapter.chapter} facility mismatch`);
  if(JSON.stringify(plan.playerHours)!==JSON.stringify(chapter.targetHours))fail.push(`Chapter ${chapter.chapter} player-hour target mismatch`);
  if(plan.keyRosterHeadcountGate!==chapter.gate.headcount)fail.push(`Chapter ${chapter.chapter} key roster gate mismatch`);
  if(plan.space.floorAreaSqFt!==facility.floorAreaSqFt)fail.push(`Chapter ${chapter.chapter} floor area mismatch`);
  const allocated=areaKeys.reduce((n,key)=>n+(plan.space[key]||0),0);if(allocated!==plan.space.floorAreaSqFt)fail.push(`Chapter ${chapter.chapter} space allocates ${allocated}, expected ${plan.space.floorAreaSqFt}`);
  if(plan.space.expansionReserve/plan.space.floorAreaSqFt<.1)fail.push(`Chapter ${chapter.chapter} expansion reserve is below 10%`);
  if(plan.space.aislesAndForkliftFlow/plan.space.floorAreaSqFt<.12)fail.push(`Chapter ${chapter.chapter} aisle/flow allocation is below 12%`);
  if(plan.space.productionAndMachineClearance/plan.productionMachines<250)fail.push(`Chapter ${chapter.chapter} machine footprint and clearance allowance is implausibly small`);
  if(plan.maximumSimultaneouslyRunningMachines>plan.productionMachines)fail.push(`Chapter ${chapter.chapter} runs more machines than it owns`);
  if(Math.ceil(plan.maximumSimultaneouslyRunningMachines/plan.maximumMachinesPerProductionOperator)>plan.simulatedSiteHeadcountPerShift[0])fail.push(`Chapter ${chapter.chapter} cannot staff its simultaneous machine plan`);
  if(plan.space.parkingStallsExterior<plan.simulatedSiteHeadcountPerShift[1])fail.push(`Chapter ${chapter.chapter} exterior parking does not cover peak shift occupancy`);
  if(chapter.chapter>=3){const frontlineSpan=plan.simulatedSiteHeadcountPerShift[1]/plan.frontlineLeaders,managerSpan=plan.frontlineLeaders/plan.operationsManagers;if(frontlineSpan<realism.peopleModel.frontlineLeaderSpan[0]||frontlineSpan>realism.peopleModel.frontlineLeaderSpan[1])fail.push(`Chapter ${chapter.chapter} frontline leader span is implausible`);if(managerSpan<realism.peopleModel.managerDirectReportSpan[0]||managerSpan>realism.peopleModel.managerDirectReportSpan[1])fail.push(`Chapter ${chapter.chapter} manager span is implausible`);if(plan.operationsManagers>realism.peopleModel.founderDirectReportMaximumAfterChapter3)fail.push(`Chapter ${chapter.chapter} overloads the founder's direct reports`);}
  if(chapter.chapter>1&&chapter.releaseStatus==='playable')fail.push(`Later Chapter ${chapter.chapter} must not be marked playable`);
}
const ch1=plans.get(1),gateText=JSON.stringify(progression.chapters[0].gate).toLowerCase();
for(const forbidden of realism.pacingSafety.chapter1ForbiddenGates)if(gateText.includes(forbidden.toLowerCase().replaceAll(' ',''))||gateText.includes(forbidden.toLowerCase()))fail.push(`Chapter 1 prematurely gates ${forbidden}`);
if(ch1.scoredPressures.some(x=>/oee|utilization|payroll|receivable|maintenance|commission/i.test(x)))fail.push('Chapter 1 scored pressures are too advanced');
if(ch1.graceShifts<20)fail.push('Chapter 1 must remain a generous teaching chapter');
for(let i=1;i<realism.chapters.length;i++){if(realism.chapters[i].productionMachines<=realism.chapters[i-1].productionMachines)fail.push(`Chapter ${i+1} machine growth is not increasing`);if(realism.chapters[i].simulatedSiteHeadcountPerShift[0]<realism.chapters[i-1].simulatedSiteHeadcountPerShift[0])fail.push(`Chapter ${i+1} staffing scale regresses`);}
if(realism.capacityModel.healthyScheduledUtilizationRange[1]>.9)fail.push('healthy utilization ceiling must retain recovery capacity');
if(realism.cashModel.minimumFixedCostReserveWeeks<6)fail.push('cash reserve floor is too low');
if(realism.peopleModel.independentRepeatWorkShifts[0]<realism.peopleModel.orientationShifts[1])fail.push('independent qualification is unrealistically faster than orientation');
if(realism.operationTimeRanges.customerPaymentTermsDays[0]<15)fail.push('customer payment timing is unrealistically immediate');
if(fail.length){console.error(fail.map(x=>'FAIL: '+x).join('\n'));process.exit(1);}
console.log('PASS: Chapters 1–6 human operations, time compression, staffing, capacity, cash, commissioning, and floor-space allocations are internally credible.');
