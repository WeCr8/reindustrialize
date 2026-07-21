import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd(),data=JSON.parse(fs.readFileSync(path.join(root,'data/industry-specializations.json'),'utf8')),fail=[];
if(data.version!==1||data.status!=='planned')fail.push('blueprint must be version 1 and honestly planned');
if(!/not selectable or playable/i.test(data.releaseTruth))fail.push('release truth must reject current playability');
if(JSON.stringify(data.commonFoundation.chapters)!=='[1,2]')fail.push('Chapters 1-2 must remain the common foundation');
const timeline=new Map(data.choiceTimeline.map(step=>[step.chapter,step]));
if(timeline.get(3)?.commitment!=='none'||!timeline.get(4)?.commitment?.includes('primary specialization'))fail.push('Chapter 3 must explore and Chapter 4 must commit');
const mix=data.portfolioRules.contentMix;
if(mix.sharedFactorySystemsPercent+mix.sectorTailoringPercent+mix.signatureContentPercent!==100||mix.sharedFactorySystemsPercent<60)fail.push('content reuse mix is invalid');
if(data.specializations.length!==8)fail.push('exactly eight primary paths are required');
const ids=new Set(),names=new Set();
for(const item of data.specializations){
  if(ids.has(item.id)||names.has(item.displayName))fail.push(`duplicate specialization: ${item.id}`);ids.add(item.id);names.add(item.displayName);
  for(const chapter of ['3','4','5','6'])if(!Array.isArray(item.chapterProducts?.[chapter])||item.chapterProducts[chapter].length<3)fail.push(`${item.id}: Chapter ${chapter} needs three product steps`);
  for(const field of ['signatureProcesses','facilityModules','workforceEmphasis','qualificationThemes','customerArchetypes','riskLessons','signatureEquipment'])if(!Array.isArray(item[field])||item[field].length<3)fail.push(`${item.id}: ${field} is incomplete`);
  if(!item.capstone||!item.visualIdentity||!item.founderFantasy)fail.push(`${item.id}: identity or capstone missing`);
}
for(const required of ['aircraft_aerospace','space_launch','automotive_mobility','robotics_automation','energy_power','medical_precision','heavy_agriculture','durable_hardware'])if(!ids.has(required))fail.push(`required path missing: ${required}`);
if(fail.length){console.error(fail.map(value=>'FAIL: '+value).join('\n'));process.exit(1)}
console.log('PASS: eight honest Chapter 3-6 industry paths define products, processes, facilities, workforce, qualifications, customers, risks, equipment, and capstones.');
