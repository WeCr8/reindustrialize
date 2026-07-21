import {readFile,stat} from 'node:fs/promises';
const registry=JSON.parse(await readFile('data/production-task-tutorials.json','utf8')).tasks;
const audio=JSON.parse(await readFile('data/audio-generation.json','utf8'));
const voices=new Map(audio.voice.clips.map(x=>[x.id,x.text]));
const required=['order_material','accept_job','cut_raw_stock','select_primary_tool','set_stickout','complete_tool_kit','prepare_cnc_run','run_cnc_cycle','review_quality_result'];
const ids=new Set(registry.map(x=>x.id));for(const id of required)if(!ids.has(id))throw new Error(`Active task ${id} has no tutorial`);
for(const task of registry){if(task.status!=='playable')throw new Error(`${task.id} is active but not playable`);if(voices.get(task.voice)!==task.text)throw new Error(`${task.id} narration mismatch`);if(!task.location||!task.image||!task.prerequisites||!task.success||!task.instructions?.length)throw new Error(`${task.id} is incomplete`);await stat(`packages/assets/audio/zach/${task.voice}.mp3`);if(task.imageType==='equipment')await stat(`packages/assets/equipment/${task.image}.png`);}
console.log(`PASS: ${registry.length} active tasks have location, image, exact Zach narration, instructions, success state, and validation status`);
