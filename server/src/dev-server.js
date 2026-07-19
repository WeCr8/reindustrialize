import http from "node:http";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import QRCode from "qrcode";
import { WebSocketServer, WebSocket } from "ws";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../..");
const gameFile = path.join(root, "apps/wecr8-info/prototypes/shop-floor-viewer.html");
const port = Number(process.env.PORT || 8787);
const sessions = new Map();
const mentorRate = new Map();
const mentorEnabled = process.env.LLM_MENTOR_ENABLED === "true";
const mentorKnowledge = ["data/zach-mentor-conversations.json", "data/shopclass.json", "data/audio-generation.json"].map(file => fs.readFileSync(path.join(root, file), "utf8")).join("\n").slice(0, 30000);

const lanAddress = () => {
  for (const values of Object.values(os.networkInterfaces())) {
    for (const value of values || []) if (value.family === "IPv4" && !value.internal) return value.address;
  }
  return "localhost";
};

const send = (res, status, type, body) => {
  res.writeHead(status, { "content-type": type, "cache-control": "no-store" });
  res.end(body);
};
const readJson = req => new Promise((resolve, reject) => {let raw="";req.on("data", chunk => {raw += chunk;if(raw.length>8192){reject(new Error("Request too large"));req.destroy();}});req.on("end",()=>{try{resolve(JSON.parse(raw||"{}"));}catch{reject(new Error("Invalid JSON"));}});req.on("error",reject);});
const rateAllowed = ip => {const now=Date.now(),windowMs=60000,limit=Math.max(1,Number(process.env.LLM_MAX_REQUESTS_PER_MINUTE||10));const recent=(mentorRate.get(ip)||[]).filter(t=>now-t<windowMs);if(recent.length>=limit)return false;recent.push(now);mentorRate.set(ip,recent);return true;};
async function mentorQuestion(req,res){
  if(!mentorEnabled)return send(res,503,"application/json",JSON.stringify({enabled:false,fallback:"scripted",message:"Free-form mentor questions are not enabled. Use the reviewed TALK WITH ZACH topics."}));
  const ip=req.socket.remoteAddress||"unknown";if(!rateAllowed(ip))return send(res,429,"application/json",JSON.stringify({error:"rate_limited"}));
  let body;try{body=await readJson(req);}catch(error){return send(res,400,"application/json",JSON.stringify({error:error.message}));}
  const question=String(body.question||"").trim(),task=String(body.task||"").trim().slice(0,300);if(question.length<3||question.length>400)return send(res,400,"application/json",JSON.stringify({error:"question_length"}));
  const apiBase=(process.env.LLM_API_BASE||"").replace(/\/$/,""),apiKey=process.env.LLM_API_KEY,model=process.env.LLM_MODEL;if(!apiBase.startsWith("https://")||!apiKey||!model)return send(res,503,"application/json",JSON.stringify({enabled:false,fallback:"scripted",message:"Mentor provider is not configured."}));
  const system=`You are Zach Goodbody, a plainspoken manufacturing shop teacher and business mentor in REINDUSTRIALIZE. The player owns and runs the company; you advise and teach why. Answer only manufacturing gameplay, machining fundamentals, quality, people development, and shop-business questions. Use the approved knowledge below. If it does not support an answer, say you do not know and direct the player to a qualified person, print, machine manual, or safety procedure. Never invent dimensions, feeds, speeds, tolerances, machine states, legal advice, or safety authorization. Never tell a player to bypass guards, interlocks, lockout/tagout, PPE, inspection, or the machine builder's instructions. Keep the answer under 130 words and provide one safe next step.\nAPPROVED KNOWLEDGE:\n${mentorKnowledge}`;
  try{const response=await fetch(apiBase+"/chat/completions",{method:"POST",headers:{authorization:`Bearer ${apiKey}`,"content-type":"application/json"},body:JSON.stringify({model,temperature:.2,max_tokens:220,messages:[{role:"system",content:system},{role:"user",content:`Current task: ${task||"not provided"}\nQuestion: ${question}`}] }),signal:AbortSignal.timeout(20000)});if(!response.ok)throw new Error(`provider_${response.status}`);const json=await response.json(),answer=json?.choices?.[0]?.message?.content?.trim();if(!answer)throw new Error("empty_answer");return send(res,200,"application/json",JSON.stringify({answer,source:"llm-grounded",model}));}catch(error){return send(res,502,"application/json",JSON.stringify({fallback:"scripted",message:"Zach's live answer is unavailable. Use the reviewed mentor topics.",error:String(error.message).slice(0,80)}));}
}

const controllerHtml = () => `<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><title>REINDUSTRIALIZE Controller</title><style>
*{box-sizing:border-box;touch-action:none}body{margin:0;background:#080b10;color:#fff;font-family:monospace;display:grid;min-height:100vh;place-items:center}.wrap{width:min(520px,96vw);text-align:center}.status{color:#3fd08a;margin:10px}.pad{display:grid;grid-template-columns:repeat(3,88px);gap:8px;justify-content:center}.b{height:78px;border:3px solid #e8b93b;background:#111820;color:#e8b93b;font-size:30px;border-radius:8px}.b:active,.b.on{background:#e8b93b;color:#080b10}.x{visibility:hidden}.action{margin-top:18px;width:184px;border-color:#3fd08a;color:#3fd08a}.settings{margin-top:18px;color:#9aa1ab}label{display:block;margin:10px}input{width:220px}
</style></head><body><main class="wrap"><h1>SHOP CONTROLLER</h1><div id="status" class="status">PAIRING…</div><div class="pad"><button class="b x"></button><button class="b" data-key="up">▲</button><button class="b x"></button><button class="b" data-key="left">◀</button><button class="b" data-key="action">●</button><button class="b" data-key="right">▶</button><button class="b x"></button><button class="b" data-key="down">▼</button><button class="b x"></button></div><button class="b action" data-key="menu">MENU</button><div class="settings"><label><input id="haptic" type="checkbox" checked> HAPTIC FEEDBACK</label><label>REPEAT SPEED <input id="speed" type="range" min="90" max="300" value="170"></label></div></main><script>
const token=new URLSearchParams(location.search).get('token')||'',status=document.querySelector('#status');if(!/^[a-f0-9]{32}$/.test(token)){status.textContent='INVALID PAIRING CODE';throw new Error('Invalid pairing token')}const protocol=location.protocol==='https:'?'wss':'ws';const ws=new WebSocket(protocol+'://'+location.host+'/pair?token='+encodeURIComponent(token)+'&role=controller');ws.onopen=()=>status.textContent='CONNECTED';ws.onclose=()=>status.textContent='DISCONNECTED';
const send=(key,state)=>{if(ws.readyState===1)ws.send(JSON.stringify({type:'input',key,state}));if(state&&document.querySelector('#haptic').checked&&navigator.vibrate)navigator.vibrate(18)};let timer;
document.querySelectorAll('[data-key]').forEach(b=>{const key=b.dataset.key;const down=e=>{e.preventDefault();b.classList.add('on');send(key,true);clearInterval(timer);if(!['action','menu'].includes(key))timer=setInterval(()=>send(key,true),+document.querySelector('#speed').value)};const up=e=>{e.preventDefault();b.classList.remove('on');clearInterval(timer);send(key,false)};b.addEventListener('pointerdown',down);b.addEventListener('pointerup',up);b.addEventListener('pointercancel',up);});
</script></body></html>`;

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (url.pathname === "/" || url.pathname === "/game") return send(res, 200, "text/html; charset=utf-8", fs.readFileSync(gameFile));
  if (url.pathname === "/controller") return send(res, 200, "text/html; charset=utf-8", controllerHtml());
  if (url.pathname === "/api/mentor-question" && req.method === "POST") return mentorQuestion(req,res);
  if (url.pathname === "/api/controller-session" && req.method === "POST") {
    const token = crypto.randomBytes(16).toString("hex");
    const base = `http://${lanAddress()}:${port}`;
    const controllerUrl = `${base}/controller?token=${token}`;
    sessions.set(token, { host: null, controller: null, expires: Date.now() + 30 * 60_000 });
    const qr = await QRCode.toDataURL(controllerUrl, { margin: 1, width: 256, color: { dark: "#111318", light: "#ffffff" } });
    return send(res, 200, "application/json", JSON.stringify({ token, controllerUrl, qr }));
  }
  send(res, 404, "text/plain", "Not found");
});

const wss = new WebSocketServer({ server, maxPayload: 1024 });
wss.on("connection", (socket, req) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const token = url.searchParams.get("token"); const role = url.searchParams.get("role");
  const session = sessions.get(token);
  let originHost="";try{originHost=new URL(req.headers.origin||"").host}catch{}
  if (originHost!==req.headers.host || !session || session.expires < Date.now() || !["host", "controller"].includes(role)) return socket.close(1008, "Invalid session");
  if (session[role]?.readyState === WebSocket.OPEN) return socket.close(1008, "Role already connected");
  session[role] = socket;
  const notify = () => session.host?.readyState === WebSocket.OPEN && session.host.send(JSON.stringify({ type: "status", connected: session.controller?.readyState === WebSocket.OPEN }));
  notify();
  socket.on("message", data => {if(role!=="controller"||session.host?.readyState!==WebSocket.OPEN)return;try{const message=JSON.parse(data.toString()),keys=new Set(["up","down","left","right","action","menu","run"]);if(message.type!=="input"||!keys.has(message.key)||typeof message.state!=="boolean")return;session.host.send(JSON.stringify({type:"input",key:message.key,state:message.state}));}catch{}});
  socket.on("close",()=>{if(session[role]===socket)session[role]=null;notify();});
});
setInterval(()=>{const now=Date.now();for(const [token,session] of sessions)if(session.expires<now){session.host?.close(1001,"Session expired");session.controller?.close(1001,"Session expired");sessions.delete(token);}},60_000).unref();

server.listen(port, "0.0.0.0", () => console.log(`REINDUSTRIALIZE: http://localhost:${port}/game`));
