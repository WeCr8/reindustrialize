import fs from 'node:fs';
const failures=[];
const read=file=>fs.readFileSync(file,'utf8');
const composition=read('demo/remotion/src/human-bot-gameplay.tsx');
const root=read('demo/remotion/src/root.tsx');
const landing=read('apps/playreind-landing/index.html');
const build=read('scripts/build-cloudflare-site.mjs');
for(const file of ['demo/remotion/public/screens/founder-selection-v8.png','demo/remotion/public/audio/hero_campaign_v7.mp3','apps/playreind-landing/public/media/gameplay-hero-v8.mp4'])if(!fs.existsSync(file)||fs.statSync(file).size<1024)failures.push(`missing or empty ${file}`);
if(!fs.existsSync('apps/playreind-landing/public/media/gameplay-hero-v8.vtt')||fs.statSync('apps/playreind-landing/public/media/gameplay-hero-v8.vtt').size<100)failures.push('missing or empty V8 captions');
for(const marker of ['HeroCampaignV8','campaignV8Segments','screens/founder-selection-v8.png','CHOOSE YOUR FOUNDER','campaignV7Captions','hero_campaign_v7.mp3'])if(!composition.includes(marker))failures.push(`composition missing ${marker}`);
for(const marker of ['id="HeroCampaignV8"','durationInFrames={1440}'])if(!root.includes(marker))failures.push(`registration missing ${marker}`);
for(const marker of ['gameplay-hero-v8.mp4','gameplay-hero-v8.vtt','improved founder selection'])if(!landing.includes(marker))failures.push(`landing missing ${marker}`);
if(!build.includes("'public', 'media', 'gameplay-hero-v8.mp4'"))failures.push('Cloudflare builder is not wired to V8');
if(failures.length){console.error(`FAIL: hero V8 (${failures.length})\n- ${failures.join('\n- ')}`);process.exit(1)}
console.log('PASS: Hero V8 includes the improved real founder-selection screen, 48-second narration/captions, and production web wiring.');
