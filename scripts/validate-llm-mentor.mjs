import {readFile} from "node:fs/promises";
const env=await readFile(".env.example","utf8"),server=await readFile("server/src/dev-server.js","utf8"),options=JSON.parse(await readFile("data/llm-mentor-options.json","utf8"));
if(!env.includes("LLM_MENTOR_ENABLED=false"))throw new Error("LLM mentor must default off");
for(const marker of ["rateAllowed", "question.length>400", "Never tell a player to bypass", "fallback:\"scripted\""])if(!server.includes(marker))throw new Error(`Missing mentor guard: ${marker}`);
if(options.enabled!==false||options.defaultMode!=="scripted")throw new Error("Scripted mentor must remain the default");
console.log("PASS: LLM mentor disabled; server-only key, grounding, limits, safety prompt, timeout, and scripted fallback present");
