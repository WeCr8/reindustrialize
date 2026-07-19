import {readFile,stat} from 'node:fs/promises';

const story=JSON.parse(await readFile('data/story-production.json','utf8'));
const audio=JSON.parse(await readFile('data/audio-generation.json','utf8'));
const scenes=JSON.parse(await readFile('data/player-scene-manifest.json','utf8'));
const runtime=await readFile('scripts/build_level_viewer_v4.py','utf8');
const voiceText=new Map(audio.voice.clips.map(x=>[x.id,x.text]));
const ids=new Set();let beats=0,voiced=0;
for(const [sequence,items] of Object.entries(story.sequences)){
  items.forEach((beat,index)=>{
    beats++;
    if(ids.has(beat.id))throw new Error(`Duplicate story beat: ${beat.id}`);ids.add(beat.id);
    if(beat.order!==index+1)throw new Error(`${sequence}/${beat.id} has incorrect order`);
    if(beat.status!=='implemented')throw new Error(`${sequence}/${beat.id} is active but not implemented`);
    if(!beat.visual)throw new Error(`${beat.id} has no visual`);
    if(beat.containsPlayer&&scenes.scenes[beat.visual]?.identityOverlay!==true)throw new Error(`${beat.id} lacks player identity overlay`);
    if(beat.voice){voiced++;if(voiceText.get(beat.voice)!==beat.text)throw new Error(`${beat.id} text does not exactly match ${beat.voice}`);}
  });
}
for(const name of ['welcome','path','choice'])await stat(`packages/assets/story-pre-founder-${name}-v1.png`);
for(const beat of Object.values(story.sequences).flat().filter(x=>x.voice))await stat(`packages/assets/audio/zach/${beat.voice}.mp3`);
for(const sequence of ['first_customer','nox_delivery','first_verified_article','first_hire','garage_graduation']){
  if(!story.sequences[sequence]?.length)throw new Error(`Missing playable Chapter 1 story sequence: ${sequence}`);
  if(!runtime.includes(`storySeen("${sequence}")`))throw new Error(`Missing one-time runtime hook for ${sequence}`);
}
for(const token of ['acceptCustomerContract(c)','placeNoxOrder(item)','hireCandidate(h)','showExpansion()','state.storySequences'])if(!runtime.includes(token))throw new Error(`Missing Chapter 1 story state hook: ${token}`);
console.log(`PASS: ${beats} implemented story beats, ${voiced} exact voice-caption pairs, required art and MP3 files present`);
