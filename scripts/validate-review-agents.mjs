import fs from 'node:fs';

const manifest=JSON.parse(fs.readFileSync('data/review-agents.json','utf8')),fail=[];
const required=['senior_game_developer','narrative_designer','manufacturing_business_owner','audio_production_qa','visual_production_qa'];
if(manifest.version!==1)fail.push('review-agent manifest version must be 1');
if(!manifest.truthPolicy?.includes('Never describe'))fail.push('truth policy must forbid planned/stub completion claims');
const agents=Array.isArray(manifest.agents)?manifest.agents:[];
for(const id of required){const a=agents.find(x=>x.id===id);if(!a)fail.push(`missing ${id}`);else{if(!a.role||!a.mission)fail.push(`${id} missing role or mission`);if(!Array.isArray(a.mustReview)||a.mustReview.length<8)fail.push(`${id} needs at least 8 review areas`);if(!Array.isArray(a.blockingFindings)||a.blockingFindings.length<5)fail.push(`${id} needs at least 5 blocking findings`)}}
if(new Set(agents.map(x=>x.id)).size!==agents.length)fail.push('duplicate review-agent id');
if(fail.length){console.error('FAIL: '+fail.join('; '));process.exit(1)}
console.log(`PASS: ${agents.length} independent game review agents defined with truth policy, scopes, and blockers.`);
