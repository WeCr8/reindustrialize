#!/usr/bin/env python3
"""Viewer v3 — mobile-first: player-following camera, fit-to-screen integer-ish scaling,
compact phone HUD, D-pad + tap-to-walk. Desktop unchanged (full map + side panels)."""
import base64, json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
SPR = os.path.join(ROOT, "packages", "assets", "sprites")
sprites = {f[:-4]: base64.b64encode(open(os.path.join(SPR, f), "rb").read()).decode()
           for f in os.listdir(SPR) if f.endswith(".png")}
atlas = json.load(open(os.path.join(SPR, "atlas.json")))
maps = {m: json.load(open(os.path.join(ROOT, "data", "maps", m + ".json")))
        for m in ["bay_01", "bay_02"]}

html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>REINDUSTRIALIZE — Shop Floor</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
:root{--gold:#e8b93b;--green:#3fd08a;--panel:#111318;--orange:#e8491d;--sky:#4a9fd4;
--alert:#d0433f;--purple:#9b59d0;--blue:#4a6fd4;}
*{box-sizing:border-box;margin:0;image-rendering:pixelated;}
html,body{overscroll-behavior:none;}
body{background:repeating-conic-gradient(#4a4844 0 25%, #444240 0 50%) 0 0/64px 64px;
color:#c4c9d0;font-family:'VT323',monospace;font-size:20px;
display:flex;flex-direction:column;align-items:center;gap:8px;padding:8px;}
.panel{background:var(--panel);border:3px solid var(--gold);outline:2px solid #000;
box-shadow:4px 4px 0 rgba(0,0,0,.45);padding:8px 12px;}
.ttl{color:var(--gold);letter-spacing:1px;}
h1{color:var(--gold);font-size:24px;letter-spacing:2px;text-shadow:2px 2px 0 #000;}
#bar{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;}
button{font-family:inherit;font-size:17px;background:var(--panel);color:#8a919c;
border:2px solid #4a4f58;padding:2px 10px;cursor:pointer;}
button.on{color:var(--gold);border-color:var(--gold);}
#layout{display:grid;grid-template-columns:200px auto 230px;gap:10px;align-items:start;}
#cwrap{border:3px solid var(--gold);outline:2px solid #000;background:#000;
box-shadow:4px 4px 0 rgba(0,0,0,.45);line-height:0;}
canvas{display:block;touch-action:manipulation;}
/* player + quest */
#pp .nm{color:#fff;font-size:24px;} #pp .lvl{color:var(--gold);}
.bar{height:12px;background:#23262d;border:2px solid #000;margin:3px 0 6px;position:relative;}
.bar i{position:absolute;inset:0;border-right:2px solid #000;}
.hp i{background:linear-gradient(#e06a5f,#b03a34);width:100%;}
.xp i{background:linear-gradient(#6a8fe0,#3a5ab0);width:72%;}
.coin{color:var(--gold);font-size:22px;}
.sk{display:flex;justify-content:space-between;align-items:center;gap:6px;margin:3px 0;font-size:17px;}
.seg{display:flex;gap:2px;} .seg b{width:12px;height:10px;background:#23262d;border:1px solid #000;}
.seg b.on.g{background:var(--green);} .seg b.on.b{background:var(--blue);}
.seg b.on.y{background:var(--gold);} .seg b.on.p{background:var(--purple);}
#missions div{font-size:17px;margin:2px 0;color:#9aa1ab;}
#missions div.done{color:var(--green);}
#missions div.done::before{content:'☑ ';} #missions div::before{content:'☐ ';}
#qbar{height:14px;background:#23262d;border:2px solid #000;margin-top:6px;position:relative;}
#qbar i{position:absolute;inset:0;width:0%;background:linear-gradient(#7fe08a,#2f9a4a);border-right:2px solid #000;transition:width .3s;}
#qpct{color:var(--gold);text-align:right;font-size:18px;}
#dlg{display:flex;gap:10px;width:min(1120px,96vw);align-items:flex-start;}
#dport{width:72px;height:72px;flex:none;border:3px solid var(--gold);outline:2px solid #000;background:#0e1826;}
#dport img{width:100%;height:100%;}
#dtext{flex:1;color:#e6e6e6;font-size:21px;} #dname{color:var(--gold);font-size:18px;}
.hint{color:#8a919c;font-size:15px;}
kbd{background:#23262d;border:1px solid #4a4f58;padding:0 5px;border-radius:3px;}
/* mobile mini-HUD strip (hidden on desktop) */
#mini{display:none;width:100%;max-width:96vw;justify-content:space-between;align-items:center;
gap:8px;padding:5px 10px;font-size:19px;}
#mini .nm{color:#fff;} #mini .q{color:var(--green);}
/* D-pad */
#pad{display:none;position:fixed;left:12px;bottom:12px;z-index:30;
grid-template-columns:repeat(3,54px);grid-template-rows:repeat(3,54px);gap:4px;opacity:.93;}
#pad b{background:var(--panel);border:3px solid var(--gold);outline:2px solid #000;
display:flex;align-items:center;justify-content:center;font-size:24px;color:var(--gold);
user-select:none;-webkit-user-select:none;touch-action:manipulation;}
#pad b:active{background:var(--gold);color:#000;} #pad b.x{visibility:hidden;}
/* ---------- MOBILE ---------- */
@media (max-width: 900px), (pointer:coarse) and (max-width: 1100px){
  body{gap:6px;padding:6px;}
  h1{font-size:20px;}
  #layout{display:flex;flex-direction:column;align-items:center;gap:6px;width:100%;}
  #sideL,#sideR{display:none;}          /* menu/skills/full quest hidden; mini strip instead */
  #mini{display:flex;}
  #dlg{width:100%;padding:6px 8px;}
  #dport{width:56px;height:56px;}
  #dtext{font-size:19px;}
  .hint{display:none;}
  #bar button{font-size:15px;padding:2px 8px;}
}
@media (pointer:coarse){
  #pad{display:grid;}
  body{padding-bottom:196px;}
}
</style></head><body>
<h1>REINDUSTRIALIZE</h1>
<div id="bar">
  <button id="b1" class="on">BAY 01</button>
  <button id="b2">BAY 02</button>
  <button id="brun">▶ RUN</button>
  <button id="bover" class="on">LAYERS</button>
  <span class="hint"><kbd>←↑↓→</kbd>/<kbd>WASD</kbd> walk · tap floor to step</span>
</div>
<div id="mini" class="panel">
  <span class="nm">ZACH <span style="color:var(--gold)">L34</span></span>
  <span class="coin">🪙 <span id="coinsM">8250</span></span>
  <span class="q">QUEST <span id="qpctM">0%</span></span>
</div>
<div id="layout">
  <div id="sideL">
    <div class="panel" id="pp">
      <div class="nm">ZACH</div>
      <div><span class="lvl">LVL 34</span> CNC SPECIALIST</div>
      <div style="font-size:16px;color:#9aa1ab">HP</div><div class="bar hp"><i></i></div>
      <div style="font-size:16px;color:#9aa1ab">XP 2450/3400</div><div class="bar xp"><i></i></div>
      <div class="coin">🪙 <span id="coins">8250</span></div>
    </div>
    <div class="panel" style="margin-top:10px">
      <div class="ttl">MENU</div>
      <div style="color:#9aa1ab;font-size:18px">▸ PROFILE<br>&nbsp;&nbsp;SKILLS<br>&nbsp;&nbsp;PROJECTS<br>&nbsp;&nbsp;GEAR<br>&nbsp;&nbsp;OPTIONS</div>
    </div>
  </div>
  <div id="cwrap"><canvas id="cv"></canvas></div>
  <div id="sideR">
    <div class="panel">
      <div class="ttl">SKILLS</div>
      <div class="sk"><span>CNC PROGRAMMING</span><span class="seg"><b class="on g"></b><b class="on g"></b><b class="on g"></b><b class="on g"></b><b></b></span></div>
      <div class="sk"><span>AUTOMATION</span><span class="seg"><b class="on g"></b><b class="on g"></b><b class="on g"></b><b></b><b></b></span></div>
      <div class="sk"><span>SOFTWARE DEV</span><span class="seg"><b class="on b"></b><b class="on b"></b><b class="on b"></b><b class="on b"></b><b></b></span></div>
      <div class="sk"><span>PROBLEM SOLVING</span><span class="seg"><b class="on y"></b><b class="on y"></b><b class="on y"></b><b class="on y"></b><b class="on y"></b></span></div>
      <div class="sk"><span>COMMUNICATION</span><span class="seg"><b class="on p"></b><b class="on p"></b><b class="on p"></b><b></b><b></b></span></div>
    </div>
    <div class="panel" style="margin-top:10px">
      <div class="ttl">CURRENT QUEST</div>
      <div style="color:#fff">TOUR THE SHOP FLOOR</div>
      <div id="missions">
        <div data-m="planning_desk">VISIT THE PLANNING DESK</div>
        <div data-m="nox_terminal">OPEN NOX-NET</div>
        <div data-m="chalkboard">ENTER SHOP CLASS</div>
        <div data-m="vmc_t2">WALK TO THE VMC</div>
      </div>
      <div id="qbar"><i></i></div><div id="qpct">0%</div>
    </div>
  </div>
</div>
<div id="dlg" class="panel">
  <div id="dport"><img id="dportimg" alt="Zach"></div>
  <div><div id="dname">ZACH — LVL 34 CNC SPECIALIST</div><div id="dtext"></div><div class="hint" id="dhint"></div></div>
</div>
<div id="pad">
  <b class="x"></b><b data-d="up">▲</b><b class="x"></b>
  <b data-d="left">◀</b><b data-d="act">●</b><b data-d="right">▶</b>
  <b class="x"></b><b data-d="down">▼</b><b class="x"></b>
</div>
<script>
const SPRITES=__SPRITES__, ATLAS=__ATLAS__, MAPS=__MAPS__;
const IMG={}; let loaded=0, total=Object.keys(SPRITES).length;
for(const k in SPRITES){const im=new Image();im.onload=()=>{if(++loaded===total)start();};
im.src="data:image/png;base64,"+SPRITES[k];IMG[k]=im;}
document.getElementById("dportimg").src="data:image/png;base64,"+SPRITES["zach_portrait"];

const cv=document.getElementById("cv"), cx=cv.getContext("2d");
const T=32;
let map, running=false, overlays=true, frame=0;
let P={x:9,y:7,step:0};
let cam={x:0,y:0}, VW=20, VH=14;   // visible tiles (camera viewport)
const done=new Set(); let coins=8250;

const MSG={
 "planning_desk":["Planning desk. RFQ board and routing live here.","Jobs, routes, and NOX orders start here."],
 "nox_terminal":["NOX-NET terminal. Metal on your dock next day.","Play the order flow in nox-net-terminal.html."],
 "chalkboard":["Shop Class. Six lessons on this board.","Speeds, feeds, offsets, alloys, certs, handoffs."],
 "whiteboard":["Today's missions. Solve problems. Build tools. Help shops win.",""],
 "tool_cart":["Tool cart. Everything in its place.",""],
 "saw_t1":["Bandsaw. Square stock, square parts.",""],
 "mill_manual_t1":["Knee mill. Every machinist starts here.",""],
 "bench_deburr_t1":["Deburr bench. Break every edge.",""],
 "vmc_t2":["The VF-class VMC. Won't run until your G-code passes.","RPM = (SFM × 3.82) ÷ dia."],
 "lathe_cnc_t2":["CNC lathe. Constant surface speed thinking.","G96: S means surface feet."],
 "network_node_t3":["MTConnect node. See the truth about uptime.",""],
 "handoff_terminal_t4":["JobLine handoff terminal.","What ran / what's next / what's weird."],
 "presetter_t4":["Tool presetter. Measure offline, cut sooner.",""],
 "toolcrib_rfid_t4":["RFID tool crib. Tag it or hunt for it.",""],
 "cobot_t5":["Cobot. Runs your process faster — good or bad.",""],
 "amr_t5":["AMR pallet bot. Stay out of its lane.",""],
 "nox_pallet":["Certed NOX aluminum. Traceable to the heat lot.",""]
};
function say(a,b){document.getElementById("dtext").textContent=a;document.getElementById("dhint").textContent=b||"";}
function mission(sprite){
  const el=document.querySelector('#missions div[data-m="'+sprite+'"]');
  if(el&&!el.classList.contains("done")){
    el.classList.add("done"); done.add(sprite);
    coins+=250;
    document.getElementById("coins").textContent=coins;
    document.getElementById("coinsM").textContent=coins;
    const pct=Math.round(done.size/4*100);
    document.querySelector("#qbar i").style.width=pct+"%";
    document.getElementById("qpct").textContent=pct+"%";
    document.getElementById("qpctM").textContent=pct+"%";
    if(pct===100)say("Tour complete. This floor is yours — let's make some chips.","+1000 bonus");
  }
}

/* ---------- responsive sizing: camera viewport + fit-to-screen ---------- */
function fit(){
  const availW=Math.min(document.documentElement.clientWidth-16, 1120);
  const mobile=availW<900;
  if(map){
    VW=mobile?Math.min(map.size[0], Math.max(9, Math.floor(availW/ (availW<420?34:36)) )):map.size[0];
    VH=mobile?Math.min(map.size[1], 11):map.size[1];
  }
  cv.width=VW*T; cv.height=VH*T;
  // integer-preferring css scale that fits the screen
  let s=availW/(VW*T);
  if(s>=2)s=2; else if(s>=1.5&&!mobile)s=1.5;
  cv.style.width=Math.floor(VW*T*s)+"px";
  cv.style.height=Math.floor(VH*T*s)+"px";
  clampCam(); if(loaded===total&&map)draw();
}
addEventListener("resize",fit); addEventListener("orientationchange",()=>setTimeout(fit,100));

function clampCam(){
  if(!map)return;
  cam.x=Math.max(0,Math.min(P.x-Math.floor(VW/2), map.size[0]-VW));
  cam.y=Math.max(0,Math.min(P.y-Math.floor(VH/2), map.size[1]-VH));
}
function setMap(id){
  map=MAPS[id]; P.x=map.spawn[0]; P.y=map.spawn[1];
  fit(); clampCam();
  say(id==="bay_01"?"We are here to help reindustrialize and help manufacturing dominate in America.":"Job Shop tier. Toolroom top right — on purpose.");
}
function tileAt(x,y){
  const [w,h]=map.size;
  if(x===0||y===0||x===w-1||y===h-1){
    const z=map.zones, inZ=zn=>z[zn]&&x>=z[zn][0][0]&&x<=z[zn][1][0]&&y>=z[zn][0][1]&&y<=z[zn][1][1];
    if(inZ("receiving")&&x===0)return 4;
    if(inZ("shipping")&&x===w-1)return 4;
    return 3;
  }
  return (x*7+y*13)%9===0?1:0;
}
function blocked(x,y){
  const [w,h]=map.size;
  if(x<1||y<1||x>=w-1||y>=h-1)return true;
  for(const p of map.placements){
    const[px,py]=p.tile,[fw,fh]=p.footprint;
    if(x>=px&&x<px+fw&&y>=py&&y<py+fh)return true;
  }
  return false;
}
function draw(){
  cx.setTransform(1,0,0,1,0,0);
  cx.clearRect(0,0,cv.width,cv.height);
  cx.translate(-cam.x*T,-cam.y*T);
  const x0=cam.x,y0=cam.y,x1=Math.min(map.size[0],cam.x+VW),y1=Math.min(map.size[1],cam.y+VH);
  for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++)
    cx.drawImage(IMG.tileset,tileAt(x,y)*32,0,32,32,x*T,y*T,T,T);
  if(overlays){
    if(map.amrLane){const[a,b]=map.amrLane;for(let x=a[0];x<=b[0];x++)cx.drawImage(IMG.tileset,2*32,0,32,32,x*T,a[1]*T,T,T);}
    for(const[zx,zy]of map.powerDrops){cx.fillStyle="#e8b93b";cx.fillRect(zx*T+12,zy*T+12,8,8);cx.strokeStyle="#000";cx.strokeRect(zx*T+12,zy*T+12,8,8);}
    if(map.netLane){const[a,b]=map.netLane;cx.strokeStyle="#4a9fd4";cx.setLineDash([6,4]);cx.beginPath();cx.moveTo(a[0]*T,a[1]*T+6);cx.lineTo((b[0]+1)*T,b[1]*T+6);cx.stroke();cx.setLineDash([]);}
    cx.fillStyle="rgba(74,159,212,.14)";const zr=map.zones.receiving;cx.fillRect(zr[0][0]*T,zr[0][1]*T,(zr[1][0]-zr[0][0]+1)*T,(zr[1][1]-zr[0][1]+1)*T);
    cx.fillStyle="rgba(232,73,29,.14)";const zs=map.zones.shipping;cx.fillRect(zs[0][0]*T,zs[0][1]*T,(zs[1][0]-zs[0][0]+1)*T,(zs[1][1]-zs[0][1]+1)*T);
  }
  const items=[...map.placements].sort((a,b)=>(a.tile[1]+a.footprint[1])-(b.tile[1]+b.footprint[1]));
  let pd=false;
  for(const p of items){
    const a=ATLAS[p.sprite]; if(!a)continue;
    if(!pd&&P.y+1<=p.tile[1]+p.footprint[1]){drawP();pd=true;}
    let fi=0; if(running&&a.frames>1)fi=frame%2;
    cx.drawImage(IMG[p.sprite],fi*a.fw,0,a.fw,a.fh,p.tile[0]*T,p.tile[1]*T+(p.footprint[1]*T-a.fh),a.fw,a.fh);
    if(overlays&&p.label){cx.font="13px VT323, monospace";
      cx.strokeStyle="#000";cx.lineWidth=3;cx.strokeText(p.label,p.tile[0]*T+1,p.tile[1]*T-3);
      cx.fillStyle="#e8b93b";cx.fillText(p.label,p.tile[0]*T+1,p.tile[1]*T-3);}
  }
  if(!pd)drawP();
}
function drawP(){
  const a=ATLAS["av_m_01"];
  cx.fillStyle="rgba(0,0,0,.3)";cx.fillRect(P.x*T+4,P.y*T+26,24,5);
  cx.drawImage(IMG["av_m_01"],(P.step%2)*a.fw,0,a.fw,a.fh,P.x*T,P.y*T-16,32,48);
}
function checkNear(){
  for(const p of map.placements){
    const[px,py]=p.tile,[fw,fh]=p.footprint;
    if(P.x>=px-1&&P.x<=px+fw&&P.y>=py-1&&P.y<=py+fh){
      const m=MSG[p.sprite];if(m)say(m[0],m[1]);
      mission(p.sprite);return;
    }
  }
}
function move(dx,dy){
  const nx=P.x+dx,ny=P.y+dy;
  if(!blocked(nx,ny)){P.x=nx;P.y=ny;P.step++;clampCam();checkNear();}
}
document.addEventListener("keydown",e=>{
  const k=e.key.toLowerCase();
  if(["arrowup","w"].includes(k)){e.preventDefault();move(0,-1);}
  if(["arrowdown","s"].includes(k)){e.preventDefault();move(0,1);}
  if(["arrowleft","a"].includes(k)){e.preventDefault();move(-1,0);}
  if(["arrowright","d"].includes(k)){e.preventDefault();move(1,0);}
});
const DIRS={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]};
let holdT=null;
document.querySelectorAll("#pad b[data-d]").forEach(el=>{
  const d=el.dataset.d;
  const fire=()=>{ if(d==="act"){checkNear();} else {const[dx,dy]=DIRS[d];move(dx,dy);} };
  const start_=(e)=>{e.preventDefault();fire();clearInterval(holdT);holdT=setInterval(fire,170);};
  const stop_=()=>clearInterval(holdT);
  el.addEventListener("touchstart",start_,{passive:false});
  el.addEventListener("touchend",stop_); el.addEventListener("touchcancel",stop_);
  el.addEventListener("mousedown",start_); el.addEventListener("mouseup",stop_); el.addEventListener("mouseleave",stop_);
});
cv.addEventListener("click",e=>{
  const r=cv.getBoundingClientRect();
  const tx=cam.x+Math.floor((e.clientX-r.left)/(r.width/VW));
  const ty=cam.y+Math.floor((e.clientY-r.top)/(r.height/VH));
  const dx=Math.sign(tx-P.x), dy=Math.sign(ty-P.y);
  if(Math.abs(tx-P.x)>=Math.abs(ty-P.y)&&dx)move(dx,0); else if(dy)move(0,dy); else if(dx)move(dx,0);
});
document.getElementById("b1").onclick=()=>{setMap("bay_01");sel("b1");};
document.getElementById("b2").onclick=()=>{setMap("bay_02");sel("b2");};
function sel(id){for(const b of["b1","b2"])document.getElementById(b).classList.toggle("on",b===id);}
document.getElementById("brun").onclick=function(){running=!running;this.textContent=running?"⏸ STOP":"▶ RUN";this.classList.toggle("on",running);};
document.getElementById("bover").onclick=function(){overlays=!overlays;this.classList.toggle("on",overlays);};
function start(){setMap("bay_01");setInterval(()=>{frame++;draw();},260);}
</script></body></html>
"""
html = (html.replace("__SPRITES__", json.dumps(sprites))
            .replace("__ATLAS__", json.dumps(atlas))
            .replace("__MAPS__", json.dumps(maps)))
out = "/mnt/user-data/outputs/shop-floor-viewer.html"
with open(out, "w") as f: f.write(html)
print("wrote", out, len(html)//1024, "KB")
