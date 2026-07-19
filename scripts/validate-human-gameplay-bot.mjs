import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const report=JSON.parse(fs.readFileSync(path.join(root,'tmp/bot-runs/human-bot-run-20260718.json'),'utf8'));
const metadata=JSON.parse(fs.readFileSync(path.join(root,'data/human-bot-gameplay-video.json'),'utf8'));
const failures=[];
if(report.result!=='pass') failures.push('bot result is not pass');
if(!report.humanStyle) failures.push('humanStyle flag is false');
if(report.usedTeleport) failures.push('bot used teleportation');
if(report.usedDirectProgressMutation) failures.push('bot mutated progression directly');
if(report.finalState?.map!=='bay_02'||report.finalState?.jobs!==5) failures.push('campaign did not finish at bay_02 with five jobs');
if(report.pageErrors?.length) failures.push(`browser page errors: ${report.pageErrors.join('; ')}`);
if(report.actionCount<100) failures.push('visible action audit is unexpectedly short');
const files=[
 path.join(root,'demo/remotion/public',metadata.source),
 path.join(root,'videos/gameplay-longform/reindustrialize-human-bot-full-gameplay-v5.mp4'),
 path.join(root,'videos/horizontal-demos/reindustrialize-human-bot-demo-60s-v5.mp4'),
 path.join(root,'videos/gameplay-longform/reindustrialize-human-bot-feature-45s-v5.mp4'),
 path.join(root,'videos/vertical-shorts/reindustrialize-human-bot-short-30s-v5.mp4'),
 path.join(root,'videos/square-social/reindustrialize-human-bot-square-30s-v5.mp4'),
];
for(const file of files) if(!fs.existsSync(file)||fs.statSync(file).size<100000) failures.push(`missing or undersized media: ${path.relative(root,file)}`);
if(failures.length){console.error(failures.map(x=>`FAIL: ${x}`).join('\n'));process.exit(1)}
console.log(`PASS: human bot completed ${report.finalState.jobs} jobs in ${report.durationSeconds}s using ${report.actionCount} visible actions; five V5 MP4 exports verified.`);
