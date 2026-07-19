import {readFile,stat} from 'node:fs/promises';
const catalog=JSON.parse(await readFile('videos/promo-catalog.json','utf8'));
for(const video of catalog.videos){const info=await stat(`videos/${video.file}`);if(info.size<1024*1024)throw new Error(`${video.id} is missing or too small`);}
console.log(`PASS: ${catalog.videos.length} categorized promo videos exist and exceed 1 MB`);
