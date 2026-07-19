import {readFile,stat} from 'node:fs/promises';
const tour=JSON.parse(await readFile('data/shop-tour.json','utf8'));
const audio=JSON.parse(await readFile('data/audio-generation.json','utf8'));
const map=JSON.parse(await readFile('data/maps/bay_01.json','utf8'));
const walkthroughs=JSON.parse(await readFile('data/station-walkthroughs.json','utf8')).walkthroughs;
const voices=new Map(audio.voice.clips.map(x=>[x.id,x.text]));
const tourSprites=new Set(tour.stops.map(x=>x.sprite));
const uniqueMapSprites=new Set(map.placements.map(x=>x.sprite));
for(const [index,stop] of tour.stops.entries()){
  if(stop.order!==index+1)throw new Error(`${stop.id} has incorrect order`);
  if(!uniqueMapSprites.has(stop.sprite))throw new Error(`${stop.id} targets missing map sprite ${stop.sprite}`);
  if(voices.get(stop.voice)!==stop.text)throw new Error(`${stop.id} caption does not exactly match ${stop.voice}`);
  await stat(`packages/assets/audio/zach/${stop.voice}.mp3`);
  const walkthrough=walkthroughs[stop.id];
  if(!walkthrough)throw new Error(`${stop.id} has no operating walkthrough`);
  if(voices.get(walkthrough.voice)!==walkthrough.text)throw new Error(`${stop.id} walkthrough caption does not exactly match ${walkthrough.voice}`);
  await stat(`packages/assets/audio/zach/${walkthrough.voice}.mp3`);
  if(stop.imageType==='equipment')await stat(`packages/assets/equipment/${stop.image}.png`);
}
for(const sprite of uniqueMapSprites)if(!tourSprites.has(sprite))throw new Error(`Garage equipment ${sprite} has no tutorial stop`);
console.log(`PASS: ${tour.stops.length} two-phase tutorials cover ${uniqueMapSprites.size} Garage Bay equipment types with ${tour.stops.length*2} exact audio-caption panels`);
