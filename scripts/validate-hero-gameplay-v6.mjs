import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadata = JSON.parse(fs.readFileSync(path.join(root, 'data/human-bot-gameplay-video.json'), 'utf8'));
const source = fs.readFileSync(path.join(root, 'demo/remotion/src/human-bot-gameplay.tsx'), 'utf8');
const rootSource = fs.readFileSync(path.join(root, 'demo/remotion/src/root.tsx'), 'utf8');
const build = fs.readFileSync(path.join(root, 'scripts/build-cloudflare-site.mjs'), 'utf8');
const segmentBlock = source.match(/export const heroV6Segments=\[([\s\S]*?)\];/)?.[1] || '';
const segments = [...segmentBlock.matchAll(/from:(\d+),duration:(\d+),label:'([^']+)',playbackRate:(\d*\.?\d+)/g)].map((m) => ({from:+m[1],duration:+m[2],label:m[3],playbackRate:+m[4]}));
const fail = [];
if (segments.length !== 5) fail.push('V6 must contain five gameplay-proof segments');
if (segments.reduce((sum, item) => sum + item.duration, 0) !== 1350) fail.push('V6 segments must fill exactly 45 seconds');
for (const item of segments) if (item.from + item.duration*item.playbackRate > metadata.durationFrames+1) fail.push(`${item.label} exceeds the ${metadata.durationFrames}-frame bot source`);
for (const phrase of ['FOUNDER','MOVE','CUT STOCK','CNC','A GRADE']) if (!segments.some((item) => item.label.includes(phrase))) fail.push(`missing visible proof label: ${phrase}`);
for (const token of ['OffthreadVideo muted','objectFit:\'cover\'','player_review_gameplay.mp3','zach_welcome.mp3','<Caption voice="player_review_gameplay"/>','<Caption voice="zach_welcome"/>','speaking?base*.28:base']) if (!source.includes(token)) fail.push(`V6 media requirement missing: ${token}`);
if (!rootSource.includes('id="HeroGameplayDemoV6"') || !rootSource.includes('width={1920} height={1080}')) fail.push('1920x1080 V6 composition registration missing');
for (const token of ["'public', 'media', 'gameplay-demo-v6.mp4'",'gameplay-demo-v6.mp4']) if (!build.includes(token)) fail.push(`Cloudflare V6 wiring missing: ${token}`);
if (!build.includes('gameplay-demo-v6.vtt') || !fs.existsSync(path.join(root,'apps/playreind-landing/gameplay-demo-v6.vtt'))) fail.push('native V6 WebVTT caption wiring missing');
for (const audio of ['garage_shift.mp3','player_review_gameplay.mp3','zach_welcome.mp3']) if (!fs.existsSync(path.join(root,'demo/remotion/public/audio',audio))) fail.push(`V6 audio missing: ${audio}`);
if (fail.length) { console.error(`FAIL: hero gameplay V6 (${fail.length})`); fail.forEach((x)=>console.error(`- ${x}`)); process.exit(1); }
console.log(`PASS: V6 uses five in-bounds real-gameplay segments, 45-second 1920x1080 framing, music ducking, two narrated/captioned perspectives, and versioned Cloudflare wiring.`);
