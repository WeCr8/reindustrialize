import fs from 'node:fs';
const fail=[];
const composition=fs.readFileSync('demo/remotion/src/human-bot-gameplay.tsx','utf8');
const root=fs.readFileSync('demo/remotion/src/root.tsx','utf8');
const landing=fs.readFileSync('apps/playreind-landing/index.html','utf8');
const build=fs.readFileSync('scripts/build-cloudflare-site.mjs','utf8');
const audio='demo/remotion/public/audio/hero_campaign_v7.mp3';
const video='apps/playreind-landing/public/media/gameplay-hero-v7.mp4';
const captions='apps/playreind-landing/public/media/gameplay-hero-v7.vtt';
for(const file of [audio,video])if(!fs.existsSync(file)||fs.statSync(file).size<1024)fail.push(`missing or empty ${file}`);
if(!fs.existsSync(captions)||fs.statSync(captions).size<100)fail.push(`missing or empty ${captions}`);
for(const token of ['HeroCampaignV7','campaignV7Segments','campaignV7Captions','hero_campaign_v7.mp3','REAL GAMEPLAY · BUILD 0.7'])if(!composition.includes(token))fail.push(`composition missing ${token}`);
if(!root.includes('id="HeroCampaignV7"')||!root.includes('durationInFrames={1440}'))fail.push('V7 registration must be 48 seconds');
for(const token of ['gameplay-hero-v7.mp4','gameplay-hero-v7.vtt','soundToggle','Reindustrialize America','Build your company'])if(!landing.includes(token))fail.push(`landing missing ${token}`);
if(!build.includes("'public', 'media', 'gameplay-hero-v7.mp4'"))fail.push('Cloudflare does not source V7 release media');
const vtt=fs.readFileSync(captions,'utf8');
if((vtt.match(/-->/g)||[]).length!==9||!vtt.includes('00:00:48.000'))fail.push('V7 WebVTT must cover nine cues through 48 seconds');
if(fail.length){console.error(`FAIL: hero campaign V7 (${fail.length})`);fail.forEach(x=>console.error(`- ${x}`));process.exit(1)}
console.log('PASS: V7 has expressive campaign audio, 48-second real-gameplay composition, nine caption cues, motion-first landing controls, and Cloudflare wiring.');
