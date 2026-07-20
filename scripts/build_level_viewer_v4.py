#!/usr/bin/env python3
"""Viewer v4 — playable station tasks:
Tool Setup (pick twist drill / end mill / ball mill + set stickout to the line)
-> CNC Run at the VMC (solve easy G/M blanks -> animated toolpath scene).
Zach explains every step; ASK ZACH gives progressive hints. Grades A-F feed coins/XP."""
import base64, json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
SPR = os.path.join(ROOT, "packages", "assets", "sprites")
sprites = {f[:-4]: base64.b64encode(open(os.path.join(SPR, f), "rb").read()).decode()
           for f in os.listdir(SPR) if f.endswith(".png")}
atlas = json.load(open(os.path.join(SPR, "atlas.json")))
maps = {m: json.load(open(os.path.join(ROOT, "data", "maps", m + ".json")))
        for m in ["bay_01", "bay_02"]}
opening = base64.b64encode(open(os.path.join(ROOT, "packages", "assets", "opening-shop-zach-v2.png"), "rb").read()).decode()
expansion = base64.b64encode(open(os.path.join(ROOT, "packages", "assets", "job-shop-expansion-zach-v2.png"), "rb").read()).decode()
scene_manifest = json.load(open(os.path.join(ROOT, "data", "player-scene-manifest.json")))
story_production = json.load(open(os.path.join(ROOT, "data", "story-production.json")))
shop_tour = json.load(open(os.path.join(ROOT, "data", "shop-tour.json")))
station_walkthroughs = json.load(open(os.path.join(ROOT, "data", "station-walkthroughs.json")))
production_task_tutorials = json.load(open(os.path.join(ROOT, "data", "production-task-tutorials.json")))
chapter_progression = json.load(open(os.path.join(ROOT, "data", "chapter-progression.json")))
facilities = json.load(open(os.path.join(ROOT, "data", "facilities.json")))
equipment_market = json.load(open(os.path.join(ROOT, "data", "equipment-market.json")))
scene_files = sorted({n for s in scene_manifest["scenes"].values() if s.get("active") for n in s["assets"].values()})
story_scenes = {n[:-4]: base64.b64encode(open(os.path.join(ROOT, "packages", "assets", n), "rb").read()).decode() for n in scene_files}
pre_founder_art = {n.replace("story-pre-founder-", "").replace("-v1.png", ""): base64.b64encode(open(os.path.join(ROOT, "packages", "assets", n), "rb").read()).decode() for n in ["story-pre-founder-welcome-v1.png", "story-pre-founder-path-v1.png", "story-pre-founder-choice-v1.png"]}
title_art = base64.b64encode(open(os.path.join(ROOT, "packages", "assets", "title-screen-zach-v2.png"), "rb").read()).decode()
nox_materials_art = base64.b64encode(open(os.path.join(ROOT, "packages", "assets", "materials", "nox-metals-exterior-v1.png"), "rb").read()).decode()
equipment_views = {n[:-4]: base64.b64encode(open(os.path.join(ROOT, "packages", "assets", "equipment", n), "rb").read()).decode() for n in os.listdir(os.path.join(ROOT, "packages", "assets", "equipment")) if n.endswith(".png")}
tool_art_dir = os.path.join(ROOT, "packages", "assets", "tools")
tool_art = {n[:-4]: base64.b64encode(open(os.path.join(tool_art_dir, n), "rb").read()).decode()
            for n in os.listdir(tool_art_dir) if n.endswith(".png") and not n.endswith("-source.png")}
hire_roster = json.load(open(os.path.join(ROOT, "data", "hiring-roster.json")))
founder_profiles = json.load(open(os.path.join(ROOT, "data", "founder-profiles.json")))
workforce_conversations = json.load(open(os.path.join(ROOT, "data", "workforce-conversations.json")))
mentor_conversations = json.load(open(os.path.join(ROOT, "data", "zach-mentor-conversations.json")))
customer_contracts = json.load(open(os.path.join(ROOT, "data", "customer-contracts.json")))
reusable_voice = json.load(open(os.path.join(ROOT, "data", "zach-reusable-voice-clips.json")))
hire_images = {n[:-4]: base64.b64encode(open(os.path.join(ROOT, "packages", "assets", "hires", n), "rb").read()).decode() for n in os.listdir(os.path.join(ROOT, "packages", "assets", "hires")) if n.endswith(".png")}
voice_dir = os.path.join(ROOT, "packages", "assets", "audio", "zach")
zach_voice = {n[:-4]: base64.b64encode(open(os.path.join(voice_dir, n), "rb").read()).decode() for n in os.listdir(voice_dir) if n.endswith(".mp3")}
sfx_dir = os.path.join(ROOT, "packages", "assets", "audio", "sfx")
sfx_audio = {n[:-4]: base64.b64encode(open(os.path.join(sfx_dir, n), "rb").read()).decode() for n in os.listdir(sfx_dir) if n.endswith(".mp3")}
customer_art_dir = os.path.join(ROOT, "packages", "assets", "customers")
customer_art = {n[:-4]: base64.b64encode(open(os.path.join(customer_art_dir, n), "rb").read()).decode() for n in os.listdir(customer_art_dir) if n.endswith(".png")}

html = r"""<!DOCTYPE html>
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
button.gld{color:var(--gold);border-color:var(--gold);}
button.grn{color:var(--green);border-color:var(--green);}
#bvoice,#testVoice,#audioState{position:fixed;z-index:150;top:10px}#bvoice{right:154px}#testVoice{right:10px}#audioState{right:10px;top:52px;background:rgba(5,8,12,.94);border:1px solid #3fd08a;padding:3px 8px;color:var(--green)}
button:disabled{opacity:.4;}
#connect{position:fixed;inset:0;background:rgba(5,6,9,.9);z-index:130;display:none;place-items:center;padding:14px}#connect.open{display:grid}
#connectPanel{width:min(560px,96vw);text-align:center}#pairQr{width:256px;max-width:70vw;background:#fff;border:8px solid #fff;margin:10px}#pairUrl{color:var(--green);overflow-wrap:anywhere}#pairState{color:var(--gold);font-size:24px}
#resumeSummary{max-width:620px;margin:6px auto;padding:7px;border:2px solid var(--green);background:#07100ddd;color:#fff}#resumeSummary:empty{display:none}#founderProgress{position:fixed;inset:0;z-index:180;background:#05070aef;display:none;place-items:center;padding:12px}#founderProgress.open{display:grid}#founderProgressPanel{width:min(760px,96vw);max-height:94dvh;overflow:auto}.progressStat{display:grid;grid-template-columns:1fr auto auto;gap:8px;align-items:center;padding:8px;border-bottom:1px solid #39434d}.progressStat button{min-width:90px}
#learnerMode{margin-top:6px;width:100%;border-color:var(--sky)}.kidWord{display:inline-block;padding:2px 5px;margin:2px;background:#142334;border:1px solid var(--sky);color:#fff}.practiceChoice.answerHint{outline:4px solid var(--gold);animation:pulse 1s infinite}
#layout{display:grid;grid-template-columns:200px auto 230px;gap:10px;align-items:start;}
#cwrap{position:relative;border:3px solid var(--gold);outline:2px solid #000;background:#000;
box-shadow:4px 4px 0 rgba(0,0,0,.45);line-height:0;}
#stationPrompt{display:none;position:absolute;left:50%;bottom:12px;transform:translateX(-50%);z-index:8;line-height:1.2;white-space:nowrap;background:rgba(8,11,16,.96);border:3px solid var(--green);outline:2px solid #000;color:#fff;padding:7px 12px;text-align:center}#stationPrompt.open{display:block;animation:useReady .7s steps(2,end) infinite}#stationPrompt button{margin-left:8px;color:#07140f;background:var(--green);border-color:#fff}@keyframes useReady{50%{border-color:#fff;transform:translateX(-50%) translateY(-2px)}}
canvas{display:block;touch-action:manipulation;}
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
#objectiveGuide{margin-top:8px;padding:7px;background:#0a1721;border:2px solid var(--sky)}#objectiveStep{color:#fff;font-size:19px}#objectiveHow{color:var(--gold);font-size:16px;margin:4px 0}#objectiveAction{width:100%;padding:5px;font-size:19px}
#qbar{height:14px;background:#23262d;border:2px solid #000;margin-top:6px;position:relative;}
#qbar i{position:absolute;inset:0;width:0%;background:linear-gradient(#7fe08a,#2f9a4a);border-right:2px solid #000;transition:width .3s;}
#qpct{color:var(--gold);text-align:right;font-size:18px;}
#dlg{display:flex;gap:10px;width:min(1120px,96vw);align-items:flex-start;}
#dport{width:72px;height:72px;flex:none;border:3px solid var(--gold);outline:2px solid #000;background:#0e1826;}
#dport img{width:100%;height:100%;}
#dtext{flex:1;color:#e6e6e6;font-size:21px;} #dname{color:var(--gold);font-size:18px;}
.hint{color:#8a919c;font-size:15px;}
kbd{background:#23262d;border:1px solid #4a4f58;padding:0 5px;border-radius:3px;}
#mini{display:none;width:100%;max-width:96vw;justify-content:space-between;align-items:center;
gap:8px;padding:5px 10px;font-size:19px;}
#mini .nm{color:#fff;} #mini .q{color:var(--green);}
#pad{display:none;position:fixed;left:12px;bottom:12px;z-index:30;
grid-template-columns:repeat(3,54px);grid-template-rows:repeat(3,54px);gap:4px;opacity:.93;}
#pad b{background:var(--panel);border:3px solid var(--gold);outline:2px solid #000;
display:flex;align-items:center;justify-content:center;font-size:24px;color:var(--gold);
user-select:none;-webkit-user-select:none;touch-action:manipulation;}
#pad b:active{background:var(--gold);color:#000;} #pad b.x{visibility:hidden;}
/* ---------- TASK OVERLAY ---------- */
#task{position:fixed;inset:0;background:rgba(5,6,9,.92);z-index:170;display:none;
flex-direction:column;align-items:center;justify-content:flex-start;gap:8px;padding:max(10px,env(safe-area-inset-top)) max(10px,env(safe-area-inset-right)) max(10px,env(safe-area-inset-bottom)) max(10px,env(safe-area-inset-left));overflow:auto;}
#task.open{display:flex;}
#tpanel{width:min(700px,96vw);}
#thead{display:flex;justify-content:space-between;align-items:center;gap:8px;}
#ttitle{color:var(--gold);font-size:22px;letter-spacing:1px;}
#tjob{color:#fff;background:#1a2e44;border:2px solid #000;padding:3px 8px;font-size:18px;margin:6px 0;}
#tsceneWrap{border:3px solid var(--gold);outline:2px solid #000;background:#0a0d12;line-height:0;margin:6px 0;}
#tscene{width:100%;}#tview{display:none;width:100%;aspect-ratio:16/9;object-fit:cover;image-rendering:auto}
#tcontrols{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:6px 0;}
.toolbtn{display:flex;flex-direction:column;align-items:center;gap:2px;background:var(--panel);
border:3px solid #4a4f58;outline:2px solid #000;padding:6px 10px;cursor:pointer;color:#c4c9d0;font-size:16px;}
.toolbtn:active{border-color:var(--gold);}
.toolbtn canvas{width:48px;height:96px;}
.toolArt{display:inline-block;width:96px;height:156px;background-repeat:no-repeat;background-color:#080b10;border:2px solid #2c3540;image-rendering:pixelated;}
.toolArt.core{background-size:300% 100%;}.toolArt.setup{background-size:200% 100%;}
.toolArt.twist{background-position:0% 50%;}.toolArt.end{background-position:50% 50%;}.toolArt.ball{background-position:100% 50%;}
.toolArt.probe{background-position:0% 50%;}.toolArt.chamfer{background-position:100% 50%;}
.toolMeasure{display:flex;align-items:center;gap:10px;background:#080b10;border:2px solid #2c3540;padding:4px 10px;}
.kitTool{display:flex;align-items:center;gap:8px}.kitTool .toolArt{width:42px;height:68px;border:0;pointer-events:none}
#stick{width:min(300px,60vw);}
input[type=range]{accent-color:var(--gold);height:30px;}
.gline{display:flex;gap:6px;flex-wrap:wrap;font-size:20px;align-items:center;}
.gline input{font-family:inherit;font-size:19px;background:#062017;color:var(--green);
border:2px solid #1d7a4f;width:64px;padding:1px 6px;text-align:center;}
.gline input.ok{border-color:var(--green);background:#0a2f1e;}
.gline input.bad{border-color:var(--alert);color:#ffb0ab;}
.gcode{color:#3fd08a;background:#03130b;border:2px solid #1d7a4f;padding:8px;font-size:19px;line-height:1.5;}
#tzach{display:flex;gap:10px;align-items:flex-start;}
#tzport{width:56px;height:56px;flex:none;border:3px solid var(--gold);outline:2px solid #000;background:#0e1826;}
#tzport img{width:100%;height:100%;}
#tztext{flex:1;font-size:20px;color:#e6e6e6;min-height:44px;}
.stamp{display:inline-block;border:3px solid var(--gold);color:var(--gold);padding:2px 12px;font-size:30px;
transform:rotate(-4deg);animation:stampin .25s ease-out;}
@keyframes stampin{from{transform:rotate(-14deg) scale(2.2);opacity:0}to{transform:rotate(-4deg) scale(1);opacity:1}}
@media (max-width: 900px), (pointer:coarse) and (max-width: 1100px){
  body{gap:6px;padding:max(6px,env(safe-area-inset-top)) max(6px,env(safe-area-inset-right)) max(6px,env(safe-area-inset-bottom)) max(6px,env(safe-area-inset-left));} h1{font-size:20px;}
  #layout{display:flex;flex-direction:column;align-items:center;gap:6px;width:100%;}
  #sideL{display:none;} #mini{display:flex;}
  #sideR{display:block;width:min(100%,720px);order:2}#sideR>.panel:first-child{display:none}#sideR>.panel:nth-child(2){margin-top:0!important;padding:6px 8px}#sideR>.panel:nth-child(2)>.ttl,#sideR>.panel:nth-child(2)>div[style],#missions,#chapterProgress,#qbar,#qpct{display:none}#objectiveGuide{margin-top:0}#objectiveHow{font-size:17px}#objectiveAction{min-height:44px}
  #stationPrompt{width:calc(100% - 16px);max-width:420px;white-space:normal;padding:6px 8px}#stationPrompt button{display:block;min-height:42px;margin:5px auto 0}
  #dlg{width:100%;padding:6px 8px;} #dport{width:56px;height:56px;} #dtext{font-size:19px;}
  .hint{display:none;} #bar button{font-size:15px;padding:2px 8px;}#bvoice,#testVoice,#audioState{position:static}#testVoice,#audioState{display:none}
}
@media (pointer:coarse){#pad{display:grid;left:max(12px,env(safe-area-inset-left));bottom:max(12px,env(safe-area-inset-bottom));grid-template-columns:repeat(3,44px);grid-template-rows:repeat(3,44px);gap:3px}#pad b{font-size:20px}body{padding-bottom:max(154px,calc(142px + env(safe-area-inset-bottom)))}#dlg{margin-left:150px;width:calc(100% - 156px)}}
@media (pointer:coarse) and (max-height:480px){#dlg{font-size:16px}#dport{width:44px;height:44px}#dtext{font-size:17px}}
#intro{position:fixed;inset:0;z-index:100;background:#050609;display:flex;align-items:center;justify-content:center;padding:16px;}
#preFounder{position:fixed;inset:0;z-index:145;background:#050609;display:grid;place-items:center;padding:16px}#preFounder.closed{display:none}#preFounderCard{position:relative;width:min(1280px,96vw);height:min(760px,92vh);overflow:hidden;border:4px solid var(--gold);outline:3px solid #000;background:#080b10}#preFounderArt{width:100%;height:100%;object-fit:cover;image-rendering:auto}#preFounderCopy{position:absolute;left:3%;right:3%;bottom:3%;background:rgba(5,8,12,.96);border:3px solid var(--gold);outline:2px solid #000;padding:14px 18px;box-shadow:7px 7px 0 #000}#preFounderKicker{color:var(--gold);font-size:25px}#preFounderText{color:#fff;font-size:27px;line-height:1.15;margin:7px 0}#preFounderNext{font-size:24px;padding:6px 18px}
#titleScreen{position:fixed;inset:0;z-index:120;background:#050609 center/cover no-repeat;display:grid;place-items:center;text-align:center}#titleScreen.closed{display:none}
#titleShade{position:absolute;inset:0;background:linear-gradient(rgba(3,8,15,.22),rgba(3,8,15,.1) 45%,rgba(3,8,15,.8))}#titleUi{position:relative;width:min(820px,96vw);margin-top:1vh;max-height:98vh;overflow:auto;padding:4px}#companyName,#founderName{font-family:inherit;font-size:20px;text-align:center;text-transform:uppercase;background:rgba(8,11,16,.94);color:#fff;border:3px solid var(--gold);outline:2px solid #000;padding:5px;width:min(420px,90%);margin:4px auto}.founderSetup{margin:4px auto}.avatarChoices{display:grid;grid-template-columns:repeat(5,minmax(78px,1fr));gap:5px;max-width:610px;margin:4px auto 6px}.avatarChoice{display:flex;flex-direction:column;align-items:center;gap:1px;padding:3px 2px;font-size:17px}.avatarChoice canvas{width:40px;height:60px;image-rendering:pixelated;background:#101820;border:1px solid #53606b}.avatarChoice.selected{color:var(--green);border-color:var(--green);background:#0a251b}.avatarChoice.selected canvas{border-color:var(--green)}.controlSelect{max-width:760px;margin:6px auto}.controlChoices{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}.controlChoice{min-height:64px;padding:5px;background:rgba(8,11,16,.94);border:2px solid #66717d;color:#fff}.controlChoice b{display:block;color:var(--gold);font-size:20px}.controlChoice span{display:block;color:#c2c9d0;font-size:15px;line-height:1}.controlChoice.selected{border-color:var(--green);background:#0a251b;box-shadow:0 0 0 2px #000}.controlChoice.selected b{color:var(--green)}#selectedControlStatus{color:var(--green);font-size:17px;margin-top:3px}@media(max-width:600px){.avatarChoices{display:flex;overflow-x:auto;max-width:94vw;justify-content:flex-start}.avatarChoice{min-width:82px}.avatarChoice canvas{width:36px;height:54px}#titleUi{margin-top:1vh}.controlChoices{grid-template-columns:repeat(2,1fr)}.controlChoice b{font-size:17px}.controlChoice span{font-size:13px}}
#gameLogo{font-size:clamp(42px,7vw,88px);color:var(--gold);letter-spacing:5px;text-shadow:4px 4px #000,-2px -2px #1a2e44}#tagline{color:var(--green);font-size:clamp(18px,2.4vw,28px);letter-spacing:2px;margin-bottom:28px}.titleMenu{display:grid;gap:8px;width:min(330px,80vw);margin:auto}.titleMenu button{font-size:25px;padding:8px}.build{margin-top:16px;color:#8a919c;font-size:14px}
#intro.closed{display:none;} #introCard{width:min(1180px,96vw);position:relative;overflow:hidden;padding:0;}
#introArt{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;image-rendering:auto;filter:saturate(.88) contrast(1.06);}
#sceneFounderBadge{position:absolute;right:3%;top:3%;width:82px;height:118px;background:rgba(8,11,16,.9);border:3px solid var(--green);outline:2px solid #000;z-index:2;image-rendering:pixelated}#sceneFounderBadge canvas{width:64px;height:96px;margin:7px;image-rendering:pixelated}
#introCopy{position:absolute;left:3%;right:3%;bottom:4%;background:rgba(8,11,16,.94);border:3px solid var(--gold);outline:2px solid #000;padding:14px 18px;box-shadow:6px 6px 0 #000;}
#introKicker{color:var(--green);letter-spacing:2px;} #introTitle{color:#fff;font-size:34px;line-height:1.05;margin:4px 0;}
#introText{font-size:23px;max-width:780px;} #introNext{float:right;margin-top:8px;}
#hire{position:fixed;inset:0;background:rgba(5,6,9,.94);z-index:125;display:none;place-items:center;padding:12px;overflow:auto}#hire.open{display:grid}#hirePanel{width:min(900px,96vw)}#hireBrowser{display:grid;grid-template-columns:56px minmax(240px,520px) 56px;gap:10px;align-items:center;justify-content:center;margin:12px 0}.atlasPortrait{height:330px;background-repeat:no-repeat;background-color:#091017;image-rendering:pixelated}.hireCard h3{color:var(--gold);font-size:28px}.hireCard .role{color:var(--green)}.navHire{height:80px;font-size:30px}.hireActions{display:flex;gap:8px;justify-content:center;margin-top:8px}#hireCount{text-align:center;color:var(--gold)}#profile{display:none}#profile.open{display:block}.profileGrid{display:grid;grid-template-columns:minmax(220px,38%) 1fr;gap:14px}.profileGrid .atlasPortrait{height:520px}.skillRow{display:flex;justify-content:space-between;border-bottom:1px solid #30343c;padding:3px}.qual{color:var(--green)}.assignSelect{width:100%;padding:6px;background:#0b1118;color:#fff;border:2px solid var(--green)}#founderProfile{max-width:610px;margin:5px auto;padding:7px;display:grid;grid-template-columns:92px 1fr;gap:9px;text-align:left;background:rgba(7,10,14,.93);border:2px solid var(--green)}#founderProfile .atlasPortrait{height:100px}.founderStats{display:grid;grid-template-columns:repeat(5,1fr);gap:3px;font-size:14px}.founderAbility{color:var(--gold);font-size:16px}@media(max-width:600px){#hireBrowser{grid-template-columns:40px 1fr 40px}.atlasPortrait{height:280px}.profileGrid{grid-template-columns:1fr}#founderProfile{grid-template-columns:70px 1fr}.founderStats{grid-template-columns:repeat(3,1fr)}}
#mentor{position:fixed;inset:0;background:rgba(5,6,9,.94);z-index:140;display:none;place-items:center;padding:12px;overflow:auto}#mentor.open{display:grid}#mentorPanel{width:min(980px,96vw)}#mentorHead{display:flex;gap:14px;align-items:center;border-bottom:3px solid var(--gold);padding-bottom:8px}#mentorHead img{width:96px;height:96px;image-rendering:pixelated;border:3px solid var(--gold)}#mentorTabs,#mentorQuestions{display:flex;flex-wrap:wrap;gap:7px;margin:10px 0}.mentorTab.on{border-color:var(--green);color:var(--green)}.mentorQuestion{text-align:left}.mentorAnswer{display:grid;grid-template-columns:96px 1fr;gap:12px;background:#0a1721;border:2px solid var(--sky);padding:12px;min-height:130px}.mentorAnswer img{width:96px;height:96px;image-rendering:pixelated}.mentorAnswer h3{color:var(--gold);margin-bottom:5px}@media(max-width:600px){.mentorAnswer{grid-template-columns:64px 1fr}.mentorAnswer img{width:64px;height:64px}}
#taskGuideModal{position:fixed;inset:0;background:rgba(5,6,9,.96);z-index:165;display:none;place-items:center;padding:12px;overflow:auto}#taskGuideModal.open{display:grid}#taskGuidePanel{width:min(900px,96vw)}#taskGuideImage{width:100%;height:min(420px,44vh);object-fit:contain;background:#080b10;border:3px solid var(--gold)}#taskGuideNarration{color:#fff;background:#0a1721;border:2px solid var(--sky);padding:10px;margin:8px 0}#taskGuideSteps{color:#fff;padding-left:26px}#taskGuideStatus{color:var(--green)}
#pauseMenu{position:fixed;inset:0;background:rgba(3,5,8,.94);z-index:210;display:none;place-items:center;padding:12px}#pauseMenu.open{display:grid}#pausePanel{width:min(680px,96vw)}.settingsGrid{display:grid;grid-template-columns:1fr 1fr;gap:8px 16px;margin:12px 0}.settingsGrid label{display:grid;gap:3px;color:#d4dae0}.settingsGrid input,.settingsGrid select{width:100%}.pauseActions{display:flex;flex-wrap:wrap;gap:8px}.pauseActions button{flex:1;min-width:180px}#saveStatus{color:var(--green);min-height:24px}#debugHud{position:fixed;z-index:205;right:8px;top:8px;display:none;white-space:pre;background:rgba(0,0,0,.88);border:2px solid var(--green);color:#aef5cf;padding:8px;font:14px Consolas,monospace;pointer-events:none}#debugHud.open{display:block}.reducedMotion *,body.reducedMotion *{animation-duration:.001ms!important;transition-duration:.001ms!important;scroll-behavior:auto!important}@media(max-width:620px){.settingsGrid{grid-template-columns:1fr}}
#campaign{position:fixed;inset:0;background:rgba(5,6,9,.96);z-index:155;display:none;place-items:center;padding:12px;overflow:auto}#campaign.open{display:grid}#campaignPanel{width:min(1120px,97vw)}#campaignGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}.chapterCard{background:#0a1017;border:3px solid #434b55;padding:11px;min-height:190px}.chapterCard.playable{border-color:var(--green)}.chapterCard.development{border-color:var(--gold)}.chapterCard.locked{opacity:.72}.chapterCard h3{color:#fff;font-size:25px}.chapterStatus{display:inline-block;padding:2px 7px;background:#161c23;color:#aeb7c0}.playable .chapterStatus{background:#123a29;color:var(--green)}.development .chapterStatus{background:#433613;color:var(--gold)}.chapterFacility{color:var(--sky);font-size:21px}.chapterTime{color:#fff}.chapterGate{font-size:17px;color:#aeb7c0;margin-top:6px}@media(max-width:760px){#campaignGrid{grid-template-columns:1fr}.chapterCard{min-height:0}}
#customers{position:fixed;inset:0;background:rgba(5,6,9,.96);z-index:160;display:none;place-items:center;padding:12px;overflow:auto}#customers.open{display:grid}#customerPanel{width:min(1080px,97vw)}#customerTabs,#customerActions{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}.customerGrid{display:grid;grid-template-columns:220px 1fr;gap:12px}.customerPortrait{height:250px;background-repeat:no-repeat;background-size:400% 100%;background-color:#081019;border:3px solid var(--gold)}.companyImage{height:235px;background-repeat:no-repeat;background-size:400% 100%;border:3px solid var(--sky)}.customerMeta{color:var(--green)}.rfq{background:#08151d;border:2px solid var(--sky);padding:10px;margin-top:8px}.rfq ul{margin:5px 0 5px 22px}.mailBadge{display:inline-block;background:var(--alert);color:#fff;padding:0 6px;border-radius:8px}.contractAccepted{color:var(--green);font-size:23px}.customerCard.locked{opacity:.65}.commProps{display:flex;gap:8px}.commProp{width:100px;height:76px;background-repeat:no-repeat;background-size:200% 100%;border:2px solid var(--green);image-rendering:pixelated}.commProp.phone{background-position:0 50%}.commProp.computer{background-position:100% 50%}@media(max-width:700px){.customerGrid{grid-template-columns:1fr}.customerPortrait{height:220px}.companyImage{height:180px}}
@media(max-width:600px){#introCopy{position:relative;left:auto;right:auto;bottom:auto;}#introTitle{font-size:27px}#introText{font-size:19px}}
#titleUi{width:min(1180px,97vw)}.avatarChoices{grid-template-columns:repeat(5,minmax(112px,1fr));max-width:680px;gap:7px}.avatarChoice{position:relative;min-height:202px;padding:5px;justify-content:flex-end;overflow:hidden}.avatarChoice .founderCardPortrait{position:absolute;top:5px;left:50%;width:112px;height:149px;transform:translateX(-50%);background-repeat:no-repeat;background-color:#091017;image-rendering:auto}.avatarChoice canvas{display:none}.avatarChoice span{position:relative;z-index:3;width:100%;padding:4px 2px;background:#05090de8;color:#fff;font-size:17px}.avatarChoice small{position:relative;z-index:3;display:block;width:100%;color:var(--gold);font-size:13px;line-height:1.05;min-height:26px}.avatarChoice.selected{outline:3px solid var(--green);box-shadow:0 0 18px #48e39a66}.avatarChoice:focus-visible{outline:4px solid #fff}#founderProfile{max-width:880px;grid-template-columns:210px 1fr;gap:16px;padding:12px;min-height:300px}#founderProfile .atlasPortrait{width:210px;height:280px}.founderProfileTitle{color:#fff;font-size:27px}.founderSpecialty{color:var(--green);font-size:20px}.founderStats{grid-template-columns:repeat(5,1fr);gap:7px;margin:8px 0}.founderStat{background:#101820;padding:6px;border:1px solid #384854}.founderStat b{display:block;color:#fff;font-size:14px}.founderStat i{color:var(--gold);font-style:normal;white-space:nowrap}.founderAbility{padding:8px;background:#17220e;border-left:4px solid var(--gold);font-size:18px}.founderTradeoff{margin-top:6px;color:#d4dde2}.founderRules{margin-top:6px;color:#9fadb5;font-size:14px}#founderSelectionStatus{min-height:22px;color:var(--green);font-size:16px}.equipmentMarketGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.equipmentProduct{display:grid;grid-template-columns:150px 1fr;gap:10px;margin:0}.equipmentProductArt{width:150px;height:150px;background-repeat:no-repeat;background-color:#081019;border:2px solid #3d5262}.equipmentMeta{color:var(--sky)}.equipmentStatus{display:inline-block;padding:2px 6px;border:1px solid var(--gold);color:var(--gold)}@media(max-width:700px){#titleUi{width:96vw}.avatarChoices{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;max-width:94vw;padding:4px 2px}.avatarChoice{min-width:142px;min-height:225px;scroll-snap-align:center}.avatarChoice .founderCardPortrait{width:132px;height:176px}#founderProfile{grid-template-columns:112px 1fr;max-width:94vw;min-height:0}#founderProfile .atlasPortrait{width:108px;height:144px}.founderProfileTitle{font-size:21px}.founderSpecialty{font-size:16px}.founderStats{grid-template-columns:repeat(2,1fr)}.founderStat{padding:4px}.founderAbility{font-size:16px}.founderRules{display:none}.equipmentMarketGrid{grid-template-columns:1fr}.equipmentProduct{grid-template-columns:108px 1fr}.equipmentProductArt{width:108px;height:108px}}
@media(max-width:700px){#titleScreen:not(.closed)~#bvoice,#titleScreen:not(.closed)~#testVoice,#titleScreen:not(.closed)~#audioState{display:none}}
#titleScreen .titleMenu{position:sticky;z-index:12;bottom:0;width:min(760px,96vw);grid-template-columns:2fr 1fr 1.5fr 1fr;gap:6px;padding:8px;background:rgba(5,9,13,.97);border:2px solid var(--gold);box-shadow:0 -8px 25px #000}#titleScreen .titleMenu button{font-size:19px;padding:7px 5px}@media(max-width:700px){#titleUi{max-height:100dvh;padding-bottom:0}#titleScreen .titleMenu{grid-template-columns:2fr 1fr;bottom:0}#titleScreen .titleMenu button{font-size:16px;min-height:46px}#titleSettings,#credits{font-size:13px!important}.build{display:none}}
#titleScreen .titleMenu{position:fixed;left:50%;transform:translateX(-50%)}#titleUi{padding-bottom:88px}@media(max-width:700px){#titleUi{padding-bottom:118px}}
</style></head><body>
<div id="preFounder"><div id="preFounderCard"><img id="preFounderArt" alt="Zach introduces the manufacturing journey before founder selection"><div id="preFounderCopy"><div id="preFounderKicker"></div><div id="preFounderText"></div><button id="preFounderNext" class="grn">CONTINUE ▸</button></div></div></div>
<div id="titleScreen"><div id="titleShade"></div><div id="titleUi"><div id="gameLogo">REINDUSTRIALIZE</div><div id="tagline">CREATE YOUR FOUNDER. BUILD AN INDUSTRIAL POWERHOUSE.</div><div class="founderSetup"><div class="hint">CHOOSE YOUR FOUNDER</div><div class="avatarChoices"><button class="avatarChoice selected" data-avatar="av_m_01"><canvas width="64" height="96"></canvas><span>FOUNDER A</span></button><button class="avatarChoice" data-avatar="av_m_founder_02_hd"><canvas width="64" height="96"></canvas><span>FOUNDER B</span></button><button class="avatarChoice" data-avatar="av_f_founder_hd"><canvas width="64" height="96"></canvas><span>FOUNDER C</span></button><button class="avatarChoice" data-avatar="av_f_founder_02_hd"><canvas width="64" height="96"></canvas><span>FOUNDER D</span></button><button class="avatarChoice" data-avatar="av_m_blonde_hd"><canvas width="64" height="96"></canvas><span>FOUNDER E</span></button><button class="avatarChoice" data-avatar="av_f_blonde_hd"><canvas width="64" height="96"></canvas><span>FOUNDER F</span></button><button class="avatarChoice" data-avatar="av_m_middle_eastern_hd"><canvas width="64" height="96"></canvas><span>FOUNDER G</span></button><button class="avatarChoice" data-avatar="av_f_middle_eastern_hd"><canvas width="64" height="96"></canvas><span>FOUNDER H</span></button><button class="avatarChoice" data-avatar="av_m_indian_hd"><canvas width="64" height="96"></canvas><span>FOUNDER I</span></button><button class="avatarChoice" data-avatar="av_f_indian_hd"><canvas width="64" height="96"></canvas><span>FOUNDER J</span></button></div><input id="founderName" maxlength="24" value="ALEX MORGAN" aria-label="Name your founder"><div class="hint">FOUNDER NAME</div></div><input id="companyName" maxlength="32" value="AMERICAN FORGE WORKS" aria-label="Name your manufacturing company"><div class="hint">MANUFACTURING COMPANY NAME</div><div class="controlSelect"><div class="hint">CHOOSE HOW YOU WILL PLAY</div><div class="controlChoices"><button class="controlChoice selected" data-control="auto"><b>✦ AUTO</b><span>Use any connected control</span></button><button class="controlChoice" data-control="keyboard"><b>⌨ KEYBOARD</b><span>WASD / arrows · Shift · E</span></button><button class="controlChoice" data-control="gamepad"><b>🎮 XBOX</b><span>Stick / D-pad · RT · A</span></button><button class="controlChoice" data-control="phone"><b>▦ PHONE QR</b><span>Scan to pair your phone</span></button></div><div id="selectedControlStatus" aria-live="polite">ALL INPUTS ACTIVE</div></div><div class="titleMenu"><button id="newGame" class="grn">▶ LAUNCH COMPANY</button><button id="continueGame" disabled>CONTINUE</button><button id="titleSettings">ADVANCED CONTROLS & PHONE QR</button><button id="credits">CREDITS</button></div><div class="build">FIRST PLAYABLE · BUILD 0.7</div></div></div>
<div id="intro"><div id="introCard" class="panel"><img id="introArt" alt="A new manufacturing founder arrives at their first shop"><div id="sceneFounderBadge"><canvas width="64" height="96" aria-label="Selected founder in this scene"></canvas></div><div id="introCopy"><div id="introKicker">PROLOGUE · FOUNDING DAY</div><div id="introTitle">BUILD YOUR COMPANY</div><div id="introText"></div><button id="introNext" class="grn">CONTINUE ▸</button></div></div></div>
<h1>REINDUSTRIALIZE</h1>
<div id="bar">
  <button id="b1" class="on">BAY 01</button>
  <button id="b2" disabled title="Complete First Chips to unlock">BAY 02 🔒</button>
  <button id="brun">▶ RUN</button>
  <button id="bover" class="on">LAYERS</button>
  <button id="bphone">PHONE CTRL</button>
  <button id="bteam">HIRE TEAM</button>
  <button id="bcustomerphone">☎ SHOP PHONE <span class="mailBadge">4</span></button>
  <button id="bmail">▣ JOBLINE MAIL</button>
  <button id="bcampaign">CAMPAIGN</button>
  <button id="btour">SHOP TOUR</button>
  <button id="btaskguide">TASK GUIDE</button>
  <button id="bpause">Ⅱ PAUSE</button>
  <button id="bvoice" class="on">🔊 VOICE ON</button>
  <button id="bsfx" class="on">🔊 MACHINES ON</button>
  <button id="bambience" class="on">◉ AMBIENCE ON</button>
  <button id="testVoice">TEST ZACH</button>
  <span id="audioState" class="hint" aria-live="polite">VOICE: READY</span>
  <span class="hint"><kbd>←↑↓→</kbd> walk · <kbd>E</kbd>/<kbd>ENTER</kbd> open station · tap ● on mobile</span>
</div>
<div id="connect"><div id="connectPanel" class="panel"><div class="ttl">CONTROL SETTINGS</div><label>INPUT MODE <select id="inputMode"><option value="auto">AUTO · ALL INPUTS</option><option value="keyboard">KEYBOARD</option><option value="gamepad">XBOX / GAMEPAD</option><option value="touch">TOUCHSCREEN</option><option value="phone">QR PHONE</option></select></label><div id="gamepadState">GAMEPAD: NOT CONNECTED</div><div style="color:#9aa1ab">Keyboard: WASD/arrows + Shift to run + E/Space · Xbox: stick/D-pad + RT to run + A · Phone: scan below</div><hr><div class="ttl">PHONE CONTROLLER</div><div id="pairState">READY TO PAIR</div><img id="pairQr" alt="Phone controller QR code"><div id="pairUrl"></div><p>Scan on a phone connected to the same network.</p><button id="pairStart" class="grn">CREATE SESSION</button> <button id="pairClose">CLOSE</button></div></div>
<div id="hire"><div id="hirePanel" class="panel"><div id="roster"><div class="ttl">BUILD YOUR TEAM</div><div>Browse candidates, review qualifications, assign stations, and talk with your employees.</div><div id="hireCount"></div><div id="hireBrowser"><button id="hirePrev" class="navHire">◀</button><div id="hireCard"></div><button id="hireNext" class="navHire">▶</button></div><button id="talkHire" class="grn">TALK WITH EMPLOYEE</button> <button id="hireClose">CLOSE</button></div><div id="profile"></div></div></div>
<div id="mentor"><div id="mentorPanel" class="panel"><div id="mentorHead"><img id="mentorPortrait" alt="Zach"><div><div class="ttl">ASK ZACH · SHOP TEACHER & BUSINESS MENTOR</div><div>Ask about the next step, the machining reason, quality, people, or growing the company.</div></div></div><div id="mentorTabs"></div><div id="mentorQuestions"></div><div id="mentorAnswer"></div><button id="mentorClose">RETURN TO SHOP</button></div></div>
<div id="campaign"><div id="campaignPanel" class="panel"><div class="ttl">YOUR ROAD TO AN INDUSTRIAL POWERHOUSE</div><div>Six chapters · 30 levels · 10–12 hour main campaign · 24 hidden discoveries</div><div id="campaignGrid"></div><button id="campaignClose" class="grn">RETURN TO SHOP</button></div></div>
<div id="customers"><div id="customerPanel" class="panel"><div class="ttl">CUSTOMERS · CALLS, EMAILS & JOBLINE WORK ORDERS</div><div class="commProps"><button class="commProp phone" id="shopPhoneProp" aria-label="Answer shop phone"></button><button class="commProp computer" id="shopComputerProp" aria-label="Open JobLine email computer"></button></div><div id="customerHeader"></div><div id="customerTabs"></div><div id="customerBody"></div><div id="customerActions"></div><button id="customerClose">RETURN TO SHOP</button></div></div>
<div id="mini" class="panel">
  <span class="nm"><span id="playerNameM">ALEX MORGAN</span> <span style="color:var(--gold)">L1</span></span>
  <span class="coin">COINS <span id="coinsM">8250</span></span>
  <span class="q">QUEST <span id="qpctM">0%</span></span>
</div>
<div id="layout">
  <div id="sideL">
    <div class="panel" id="pp">
      <div class="nm" id="playerName">ALEX MORGAN</div>
      <div><span class="lvl">LVL 1</span> SHOP APPRENTICE</div>
      <div style="font-size:16px;color:#9aa1ab">HP</div><div class="bar hp"><i></i></div>
      <div style="font-size:16px;color:#9aa1ab">XP 0/100</div><div class="bar xp"><i style="width:0%"></i></div>
      <div class="coin">COINS <span id="coins">8250</span></div>
    </div>
    <div class="panel" style="margin-top:10px">
      <div class="ttl">MENU</div>
      <button id="openFounderProgress">FOUNDER PROFILE & UPGRADES</button><div style="color:#9aa1ab;font-size:16px">PROJECTS · GEAR · OPTIONS</div>
    </div>
  </div>
  <div id="cwrap"><canvas id="cv"></canvas><div id="stationPrompt"><span id="stationPromptText"></span><button id="stationOpen">USE / OPEN</button></div></div>
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
      <div style="color:#fff">FIRST CHIPS</div>
      <div id="missions">
        <div data-m="meet_zach">MEET ZACH AT THE BAY</div>
        <div data-m="planning_desk">ACCEPT JOB 1042</div>
        <div data-m="task_tool">SET UP A TOOL ★</div>
        <div data-m="task_vmc">RUN THE VMC ★</div>
      </div>
      <div id="chapterProgress" style="margin-top:7px;color:#fff">GARAGE GRADUATION<br><span id="shipProgress">JOBS SHIPPED 0 / 5</span><br><span id="gradeProgress">QUALITY: NOT YET GRADED</span></div>
      <div id="objectiveGuide"><div class="ttl">NEXT ACHIEVABLE STEP</div><div id="objectiveStep"></div><div id="objectiveHow"></div><button id="objectiveAction" class="grn" disabled>MOVE TO TARGET</button></div>
      <div id="qbar"><i></i></div><div id="qpct">0%</div>
    </div>
  </div>
</div>
<div id="dlg" class="panel">
  <div id="dport"><img id="dportimg" alt="Zach"></div>
  <div><div id="dname">ZACH — LVL 34 CNC SPECIALIST</div><div id="dtext"></div><div class="hint" id="dhint"></div><button id="askMentor" class="gld">? TALK WITH ZACH</button></div>
</div>
<div id="pad">
  <b data-d="run">RUN</b><b data-d="up">▲</b><b class="x"></b>
  <b data-d="left">◀</b><b data-d="act">●</b><b data-d="right">▶</b>
  <b class="x"></b><b data-d="down">▼</b><b class="x"></b>
</div>

<!-- ============ TASK OVERLAY ============ -->
<div id="task">
  <div id="tpanel" class="panel">
    <div id="thead"><span id="ttitle"></span>
      <span><button id="askzach" class="gld">? ASK ZACH</button><button id="taskGuideButton">TASK GUIDE</button>
      <button id="tclose">BACK TO SHOP · PROGRESS SAVED</button></span></div>
    <div id="tjob"></div>
    <div id="tsceneWrap"><img id="tview" alt="Opened equipment view"><canvas id="tscene" width="480" height="260"></canvas></div>
    <div id="tcontrols"></div>
    <div id="tzach"><div id="tzport"><img id="tzportimg"></div><div id="tztext"></div></div>
  </div>
</div>

<div id="taskGuideModal"><div id="taskGuidePanel" class="panel"><div class="ttl" id="taskGuideTitle"></div><div id="taskGuideStatus"></div><img id="taskGuideImage" alt="Active production task tutorial"><div id="taskGuideNarration"></div><div><b>PREREQUISITES:</b> <span id="taskGuidePrereq"></span></div><ol id="taskGuideSteps"></ol><div><b>SUCCESS:</b> <span id="taskGuideSuccess"></span></div><button id="taskGuideClose" class="grn">RETURN TO TASK</button></div></div>
<div id="pauseMenu" role="dialog" aria-modal="true" aria-labelledby="pauseTitle"><div id="pausePanel" class="panel"><div class="ttl" id="pauseTitle">GAME PAUSED · SETTINGS</div><div id="saveStatus" aria-live="polite"></div><div class="settingsGrid"><label>MASTER VOLUME<input id="masterVolume" type="range" min="0" max="1" step="0.05" value="1"></label><label>ZACH / VOICE<input id="voiceVolumeSetting" type="range" min="0" max="1" step="0.05" value="1"></label><label>MACHINE SFX<input id="sfxVolumeSetting" type="range" min="0" max="1" step="0.05" value="0.7"></label><label>SHOP AMBIENCE<input id="ambienceVolumeSetting" type="range" min="0" max="0.3" step="0.01" value="0.16"></label><label><span>ACCESSIBILITY</span><span><input id="reducedMotion" type="checkbox"> REDUCED MOTION</span></label><label>UI SCALE<select id="uiScale"><option value="1">100%</option><option value="1.15">115%</option><option value="1.3">130%</option></select></label></div><div class="pauseActions"><button id="resumeGame" class="grn">▶ RESUME</button><button id="saveNow">SAVE NOW</button><button id="fullscreenGame">FULLSCREEN</button><button id="returnTitle">RETURN TO TITLE</button></div><div class="hint">ESC / XBOX MENU toggles pause · F3 toggles developer diagnostics</div></div></div>
<div id="debugHud" aria-hidden="true"></div>
<script>
const SPRITES=__SPRITES__, ATLAS=__ATLAS__, MAPS=__MAPS__;
const OPENING="__OPENING__";
const EXPANSION="__EXPANSION__";
const STORY_SCENES=__STORY_SCENES__;
const SCENE_MANIFEST=__SCENE_MANIFEST__;
const STORY_PRODUCTION=__STORY_PRODUCTION__,PRE_FOUNDER_ART=__PRE_FOUNDER_ART__;
const SHOP_TOUR=__SHOP_TOUR__;
const STATION_WALKTHROUGHS=__STATION_WALKTHROUGHS__.walkthroughs;
const PRODUCTION_TASK_TUTORIALS=__PRODUCTION_TASK_TUTORIALS__.tasks;
const CHAPTER_PROGRESSION=__CHAPTER_PROGRESSION__,FACILITIES=__FACILITIES__.facilities;
const TITLE_ART="__TITLE_ART__";
const NOX_MATERIALS_ART="__NOX_MATERIALS_ART__";
const EQUIPMENT_VIEWS=__EQUIPMENT_VIEWS__;
const EQUIPMENT_MARKET=__EQUIPMENT_MARKET__;
const TOOL_ART=__TOOL_ART__;
const HIRE_ROSTER=__HIRE_ROSTER__,HIRE_IMAGES=__HIRE_IMAGES__,FOUNDER_PROFILES=__FOUNDER_PROFILES__,WORKFORCE_CONVERSATIONS=__WORKFORCE_CONVERSATIONS__;const hired=new Set(),workers=[];
const MENTOR=__MENTOR__;
const CUSTOMER_CONTRACTS=__CUSTOMER_CONTRACTS__,CUSTOMER_ART=__CUSTOMER_ART__;
const REUSABLE_ZACH=__REUSABLE_ZACH__;
const ZACH_VOICE=__ZACH_VOICE__;let zachAudio=null,masterVolume=Number(localStorage.getItem("reindustrialize.masterVolume")||"1"),voiceEnabled=localStorage.getItem("reindustrialize.voice")!=="off",voiceVolume=Number(localStorage.getItem("reindustrialize.voiceVolume")||"1");
const SFX_AUDIO=__SFX_AUDIO__;let sfxLoop=null,sfxEnabled=localStorage.getItem("reindustrialize.sfx")!=="off",sfxVolume=Number(localStorage.getItem("reindustrialize.sfxVolume")||"0.7");
let ambienceAudio=null,ambienceId=null,ambienceEnabled=localStorage.getItem("reindustrialize.ambience")!=="off",ambienceVolume=Number(localStorage.getItem("reindustrialize.ambienceVolume")||"0.16");
const assetUrl=(value,mime="image/png")=>value.startsWith("/")?value:"data:"+mime+";base64,"+value;
function playSfx(id,{loop=false,volume=1}={}){if(!sfxEnabled||!SFX_AUDIO[id])return null;const audio=new Audio(assetUrl(SFX_AUDIO[id],"audio/mpeg"));audio.loop=loop;audio.volume=Math.max(0,Math.min(1,masterVolume*sfxVolume*volume));audio.play().catch(()=>{});if(loop){stopSfxLoop();sfxLoop=audio;}return audio;}
function stopSfxLoop(){if(sfxLoop){sfxLoop.pause();sfxLoop.currentTime=0;sfxLoop=null;}}
function updateSfxButton(){const b=document.getElementById("bsfx");b.textContent=sfxEnabled?"🔊 MACHINES ON":"🔇 MACHINES OFF";b.classList.toggle("on",sfxEnabled);}
function ambienceForMap(){return map?.id==="bay_02"?"job_shop_ambience":"shop_ambience_small";}
function setAmbienceLevel(ducked=false){if(ambienceAudio)ambienceAudio.volume=Math.max(0,Math.min(.3,masterVolume*ambienceVolume*(ducked ? .38 : 1)));}
function startAmbience(id=ambienceForMap()){if(!ambienceEnabled||!SFX_AUDIO[id])return;if(ambienceAudio&&ambienceId===id){setAmbienceLevel(false);ambienceAudio.play().catch(()=>{});return;}if(ambienceAudio)ambienceAudio.pause();ambienceId=id;ambienceAudio=new Audio(assetUrl(SFX_AUDIO[id],"audio/mpeg"));ambienceAudio.loop=true;setAmbienceLevel(false);ambienceAudio.play().catch(()=>{});}
function stopAmbience(){if(ambienceAudio){ambienceAudio.pause();ambienceAudio.currentTime=0;}}
function updateAmbienceButton(){const b=document.getElementById("bambience");b.textContent=ambienceEnabled?"◉ AMBIENCE ON":"○ AMBIENCE OFF";b.classList.toggle("on",ambienceEnabled);}
function toolArt(kind){const setup=kind==="probe"||kind==="chamfer",key=setup?"setup-tools-atlas-v1":"core-cutters-atlas-v1";return '<span class="toolArt '+(setup?'setup ':'core ')+kind+'" style="background-image:url('+assetUrl(TOOL_ART[key])+')" aria-hidden="true"></span>';}
function audioStatus(text,bad=false){const el=document.getElementById("audioState");if(el){el.textContent=text;el.style.color=bad?"#ff8075":"var(--green)";}}
function updateVoiceButton(){const b=document.getElementById("bvoice");if(!b)return;b.textContent=voiceEnabled?"🔊 VOICE ON":"🔇 VOICE OFF";b.classList.toggle("on",voiceEnabled);audioStatus(voiceEnabled?"VOICE: READY":"VOICE: MUTED");}
function stopZach(status="VOICE: READY"){if(zachAudio){zachAudio.pause();zachAudio.currentTime=0;}setAmbienceLevel(false);audioStatus(status);}
function playZach(id){if(!id)return Promise.resolve(false);if(!ZACH_VOICE[id]){audioStatus("VOICE: CLIP MISSING",true);return Promise.resolve(false);}if(!voiceEnabled){audioStatus("VOICE: MUTED — PRESS VOICE ON",true);setAmbienceLevel(false);return Promise.resolve(false);}if(zachAudio)stopZach();zachAudio=new Audio(assetUrl(ZACH_VOICE[id],"audio/mpeg"));zachAudio.volume=Math.max(0,Math.min(1,masterVolume*voiceVolume));zachAudio.onplaying=()=>{audioStatus("VOICE: ZACH SPEAKING");setAmbienceLevel(true);};zachAudio.onended=()=>{audioStatus("VOICE: READY");setAmbienceLevel(false);};zachAudio.onerror=()=>{audioStatus("VOICE: AUDIO ERROR — PRESS TEST ZACH",true);setAmbienceLevel(false);};return zachAudio.play().then(()=>true).catch(()=>{audioStatus("VOICE: BLOCKED — PRESS TEST ZACH",true);setAmbienceLevel(false);return false;});}
let preFounderStep=0,preFounderStarted=false;const preFounderBeats=STORY_PRODUCTION.sequences.pre_founder;
function renderPreFounder(play=false){const beat=preFounderBeats[preFounderStep];document.getElementById("preFounderArt").src=assetUrl(PRE_FOUNDER_ART[beat.id.replace("pre_founder_","")]);document.getElementById("preFounderKicker").textContent=beat.kicker;document.getElementById("preFounderText").textContent=beat.text;document.getElementById("preFounderNext").textContent=!preFounderStarted?"▶ PLAY ZACH'S INTRO":preFounderStep===preFounderBeats.length-1?"CHOOSE YOUR FOUNDER ▸":"CONTINUE ▸";if(play)playZach(beat.voice);}
document.getElementById("preFounderNext").onclick=()=>{if(!preFounderStarted){preFounderStarted=true;renderPreFounder(true);return;}preFounderStep++;if(preFounderStep<preFounderBeats.length){renderPreFounder(true);return;}if(zachAudio)zachAudio.pause();document.getElementById("preFounder").classList.add("closed");};renderPreFounder(false);
const IMG={};
const CORE_SPRITES=new Set(["tileset","bay_01_hd_bg","zach_portrait",...Object.keys(SCENE_MANIFEST.founders),...MAPS.bay_01.placements.map(p=>p.sprite)]);
let loaded=0,total=CORE_SPRITES.size;
function loadSprite(key,priority="auto"){
  if(!SPRITES[key])return Promise.resolve(null);
  if(IMG[key])return IMG[key]._ready||Promise.resolve(IMG[key]);
  const im=new Image();IMG[key]=im;im.decoding="async";im.fetchPriority=priority;
  im._ready=new Promise(resolve=>{im.onload=()=>{if(map)draw();resolve(im)};im.onerror=()=>resolve(null)});
  im.src=assetUrl(SPRITES[key]);return im._ready;
}
function ensureMapSprites(nextMap){return Promise.all(["tileset",nextMap.id==="bay_01"?"bay_01_hd_bg":null,...nextMap.placements.map(p=>p.sprite),selectedAvatar].filter(Boolean).map(k=>loadSprite(k,k===selectedAvatar?"high":"auto")));}
Promise.all([...CORE_SPRITES].map(k=>loadSprite(k,"high"))).then(()=>{loaded=total;start();});
document.getElementById("dportimg").src=assetUrl(SPRITES["zach_portrait"]);
document.getElementById("tzportimg").src=assetUrl(SPRITES["zach_portrait"]);
document.getElementById("introArt").src=assetUrl(OPENING);
document.getElementById("titleScreen").style.backgroundImage="url("+assetUrl(TITLE_ART)+")";
let companyName="AMERICAN FORGE WORKS",playerName="ALEX MORGAN",selectedAvatar="av_m_01";
const FOUNDER_OPTIONS=SCENE_MANIFEST.founders;
const storyVariant=()=>FOUNDER_OPTIONS[selectedAvatar]?.family||"male";
function sceneAsset(scene,variant){const file=SCENE_MANIFEST.scenes[scene]?.assets?.[variant];if(!file)throw new Error(`Missing ${variant} art for active scene ${scene}`);return file.replace(/\.png$/,'');}
function setTitleArt(){const variant=storyVariant(),key=sceneAsset("title",variant),screen=document.getElementById("titleScreen");screen.style.backgroundImage="url("+assetUrl(STORY_SCENES[key])+")";screen.dataset.variant="title-"+variant;}
function setStoryArt(scene){const variant=storyVariant(),key=sceneAsset(scene,variant),im=document.getElementById("introArt");im.src=assetUrl(STORY_SCENES[key]);im.dataset.variant=scene+"-"+variant;}
function drawFounder(c,id){const g=c.getContext("2d"),a=ATLAS[id],im=IMG[id];g.clearRect(0,0,c.width,c.height);if(im?.complete)g.drawImage(im,0,0,a.fw,a.fh,0,0,64,96);}
function atlasStyle(name,cell){const x=cell%5,y=Math.floor(cell/5);return 'background-image:url('+assetUrl(SPRITES[name])+');background-size:500% 200%;background-position:'+(x*25)+'% '+(y*100)+'%;'}
const FOUNDER_GUIDANCE={"Machining Craft":["Hands-on first-part and setup specialist","Lower starting business skill"],"Shop Operations":["Keeps work moving between stations","Less focused on early innovation"],"Customer Growth":["Builds repeat business and customer value","Needs technical development"],"Quality Systems":["Finds risk before scrap reaches the customer","Balanced rather than commercially specialized"],"Industrial Software":["Earns more from machine-data objectives","Needs stronger leadership growth"],"Finance & Reinvestment":["Stretches capital when expanding the shop","Starts with less technical depth"],"Supply Chain":["Gets certified material ready sooner","Needs innovation development"],"People Leadership":["Develops assigned employees faster","Needs technical and operations growth"],"Automation":["Recovers automation prove-outs safely","Needs business and leadership growth"],"Product & Process Design":["Exposes manufacturability risks before setup","Needs operations and business growth"]};
function renderFounderProfile(){let root=document.getElementById("founderProfile");if(!root){root=document.createElement("div");root.id="founderProfile";root.setAttribute("aria-live","polite");document.getElementById("founderName").before(root);}const p=FOUNDER_PROFILES.profiles.find(x=>x.avatar===selectedAvatar),guide=FOUNDER_GUIDANCE[p.specialty];const stats=Object.entries(p.stats).map(([k,v])=>'<span class="founderStat"><b>'+k.replaceAll('_',' ').toUpperCase()+'</b><i aria-label="'+v+' out of 5">'+"■".repeat(v)+"□".repeat(5-v)+'</i></span>').join('');root.innerHTML='<div class="atlasPortrait" role="img" aria-label="Portrait of '+p.displayName+'" style="'+atlasStyle(FOUNDER_PROFILES.portraitAtlas,p.atlasCell)+'"></div><div><div class="founderProfileTitle">'+p.displayName+'</div><div class="founderSpecialty">'+p.specialty.toUpperCase()+'</div><div class="founderStats" aria-label="Starting skills">'+stats+'</div><div class="founderAbility"><b>SIGNATURE SKILL · '+p.ability.name+'</b><br>'+p.ability.effect+'</div><div class="founderTradeoff"><b>PLAY STYLE:</b> '+guide[0]+' · <b>GROWTH AREA:</b> '+guide[1]+'</div><div class="hint">UPGRADES: '+p.upgradePath.join(' → ')+'</div><div class="founderRules">All founders start with equal total skill points. Choose the strategy you want, then improve every skill through play.</div></div>';}
function renderFounderPreview(){let status=document.getElementById("founderSelectionStatus");if(!status){status=document.createElement("div");status.id="founderSelectionStatus";status.setAttribute("aria-live","polite");document.querySelector(".avatarChoices").before(status);}document.querySelector(".avatarChoices").setAttribute("role","listbox");document.querySelectorAll(".avatarChoice").forEach(b=>{const p=FOUNDER_PROFILES.profiles.find(x=>x.avatar===b.dataset.avatar);let portrait=b.querySelector(".founderCardPortrait"),detail=b.querySelector("small");if(!portrait){portrait=document.createElement("div");portrait.className="founderCardPortrait";b.prepend(portrait)}portrait.setAttribute("style",atlasStyle(FOUNDER_PROFILES.portraitAtlas,p.atlasCell));portrait.setAttribute("role","img");portrait.setAttribute("aria-label",p.displayName+' portrait');b.querySelector("span").textContent=p.displayName;if(!detail){detail=document.createElement("small");b.append(detail)}detail.textContent=p.specialty;b.setAttribute("role","option");b.setAttribute("aria-selected",String(b.dataset.avatar===selectedAvatar));b.setAttribute("aria-label",p.displayName+', '+p.specialty);drawFounder(b.querySelector("canvas"),b.dataset.avatar);});const active=FOUNDER_PROFILES.profiles.find(x=>x.avatar===selectedAvatar);status.textContent=active.displayName+' selected · '+active.specialty+' · '+active.ability.name;drawFounder(document.querySelector("#sceneFounderBadge canvas"),selectedAvatar);document.getElementById("sceneFounderBadge").dataset.founderAvatar=selectedAvatar;renderFounderProfile();}
function selectFounderButton(b){selectedAvatar=b.dataset.avatar;document.querySelectorAll(".avatarChoice").forEach(x=>x.classList.toggle("selected",x===b));renderFounderPreview();setTitleArt();setStoryArt("opening");b.scrollIntoView({block:"nearest",inline:"center"});}
document.querySelectorAll(".avatarChoice").forEach(b=>{b.onclick=()=>selectFounderButton(b);b.onkeydown=event=>{if(!["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"].includes(event.key))return;event.preventDefault();const cards=[...document.querySelectorAll(".avatarChoice")],current=cards.indexOf(b),delta=event.key==="ArrowLeft"?-1:event.key==="ArrowRight"?1:event.key==="ArrowUp"?-5:5,next=cards[(current+delta+cards.length)%cards.length];next.focus();selectFounderButton(next);};});
document.getElementById("newGame").onclick=()=>{if([SAVE_KEY,SAVE_TEMP_KEY,SAVE_BACKUP_KEY].some(key=>localStorage.getItem(key))&&!confirm("Start a new company and replace the current local save?"))return;[SAVE_KEY,SAVE_TEMP_KEY,SAVE_BACKUP_KEY].forEach(key=>localStorage.removeItem(key));gameStarted=true;companyName=document.getElementById("companyName").value.trim().toUpperCase()||"AMERICAN FORGE WORKS";playerName=document.getElementById("founderName").value.trim().toUpperCase()||"ALEX MORGAN";document.getElementById("playerName").textContent=playerName;document.getElementById("playerNameM").textContent=playerName;startAmbience("shop_ambience_small");introSequence="opening";setStoryArt("opening");introPages=makePrologue();introStep=0;renderIntro();document.getElementById("titleScreen").classList.add("closed");};
document.getElementById("newGame").addEventListener("click",()=>setTimeout(()=>saveGame("COMPANY LAUNCH"),0));
document.getElementById("titleSettings").onclick=()=>document.getElementById("connect").classList.add("open");
document.getElementById("bvoice").onclick=()=>{voiceEnabled=!voiceEnabled;localStorage.setItem("reindustrialize.voice",voiceEnabled?"on":"off");if(!voiceEnabled)stopZach("VOICE: MUTED");updateVoiceButton();if(voiceEnabled)playZach("zach_welcome");};
document.getElementById("bsfx").onclick=()=>{sfxEnabled=!sfxEnabled;localStorage.setItem("reindustrialize.sfx",sfxEnabled?"on":"off");if(!sfxEnabled)stopSfxLoop();updateSfxButton();if(sfxEnabled)playSfx("machine_power_on",{volume:.65});};updateSfxButton();
document.getElementById("bambience").onclick=()=>{ambienceEnabled=!ambienceEnabled;localStorage.setItem("reindustrialize.ambience",ambienceEnabled?"on":"off");if(ambienceEnabled)startAmbience();else stopAmbience();updateAmbienceButton();};updateAmbienceButton();
document.getElementById("testVoice").onclick=()=>{voiceEnabled=true;voiceVolume=1;localStorage.setItem("reindustrialize.voice","on");localStorage.setItem("reindustrialize.voiceVolume","1");updateVoiceButton();playZach("zach_welcome");};
updateVoiceButton();
document.getElementById("credits").onclick=()=>alert("REINDUSTRIALIZE\nA manufacturing RPG by WeCr8 Solutions\nZach is the mentor. You build the shop.");
let hireIndex=0;
function workerFor(id){return workers.find(w=>w.id===id)}
function assignmentOptions(h){return '<option value="">UNASSIGNED · MEANDER</option>'+h.qualifications.map(q=>'<option value="'+q+'">'+(STATION_NAMES[q]||q.replaceAll('_',' ').toUpperCase())+'</option>').join('')}
function assignWorker(h,value){const w=workerFor(h.id);if(!w||(!h.qualifications.includes(value)&&value))return;w.assignment=value||null;w.status=w.assignment?'TRAVELING TO '+(STATION_NAMES[w.assignment]||w.assignment.toUpperCase()):'MEANDERING';renderHires();}
function hireCandidate(h){if(hired.has(h.id))return;if(coins<h.hireCost)return alert("Not enough coins.");const returnToProfile=document.getElementById("profile").classList.contains("open");coins-=h.hireCost;hired.add(h.id);workers.push({id:h.id,candidate:h,x:P.x+1,y:P.y,assignment:null,status:'MEANDERING',nextMove:0,workPulse:0});addCoins(0);renderHires();if(!storySeen("first_hire")){document.getElementById("hire").classList.remove("open");setTimeout(()=>showStorySequence("first_hire",()=>{document.getElementById("hire").classList.add("open");if(returnToProfile)showProfileV2(h);else renderHires();}),100);}}
function renderHires(){const h=HIRE_ROSTER.candidates[hireIndex],root=document.getElementById("hireCard");document.getElementById("hireCount").textContent=(hireIndex+1)+" / "+HIRE_ROSTER.candidates.length;root.innerHTML='<div class="hireCard panel"><img src="data:image/png;base64,'+HIRE_IMAGES[hireKey(h)]+'"><h3>'+h.name+'</h3><div class="role">'+h.title+' · '+h.shift.toUpperCase()+' SHIFT</div><div>'+h.strength+'</div><div>HIRE '+h.hireCost+' · WAGE '+h.wagePerShift+'/SHIFT</div><div class="hireActions"><button id="viewProfile">VIEW PROFILE</button><button id="hireNow" '+(hired.has(h.id)?'disabled':'')+'>'+(hired.has(h.id)?'HIRED':'HIRE')+'</button></div></div>';document.getElementById("viewProfile").onclick=()=>showProfile(h);document.getElementById("hireNow").onclick=()=>hireCandidate(h);}
function showProfile(h){const p=document.getElementById("profile");document.getElementById("roster").style.display="none";p.className="open panel";const skills=Object.entries(h.skills).map(([k,v])=>'<div class="skillRow"><span>'+k.replaceAll("_"," ").toUpperCase()+'</span><span>'+"■".repeat(v)+"□".repeat(5-v)+'</span></div>').join("");p.innerHTML='<div class="profileGrid"><img src="data:image/png;base64,'+HIRE_IMAGES[hireKey(h)]+'"><div><div class="ttl">CANDIDATE PROFILE</div><h2>'+h.name+'</h2><div class="role">'+h.title+' · '+h.shift.toUpperCase()+' SHIFT</div>'+skills+'<p><b>STRENGTH:</b> '+h.strength+'</p><p><b>GROWTH:</b> '+h.growthTo.replaceAll("_"," ").toUpperCase()+'</p><p><b>WATCH:</b> '+h.flaw+'</p><p class="qual"><b>QUALIFIED:</b> '+h.qualifications.join(" · ")+'</p><p>HIRE '+h.hireCost+' · WAGE '+h.wagePerShift+'/SHIFT</p><button id="profileBack">◀ BACK TO CANDIDATES</button> <button id="profileHire" '+(hired.has(h.id)?'disabled':'')+'>'+(hired.has(h.id)?'HIRED':'HIRE '+h.name.toUpperCase())+'</button></div></div>';document.getElementById("profileBack").onclick=()=>{p.className="";document.getElementById("roster").style.display="block";renderHires();};document.getElementById("profileHire").onclick=()=>{hireCandidate(h);showProfile(h);};}
document.getElementById("hirePrev").onclick=()=>{hireIndex=(hireIndex-1+HIRE_ROSTER.candidates.length)%HIRE_ROSTER.candidates.length;renderHires();};document.getElementById("hireNext").onclick=()=>{hireIndex=(hireIndex+1)%HIRE_ROSTER.candidates.length;renderHires();};document.getElementById("bteam").onclick=()=>{loadSprite(HIRE_ROSTER.spriteAtlas);loadSprite(HIRE_ROSTER.profileAtlas);hireIndex=0;renderHires();document.getElementById("hire").classList.add("open");};document.getElementById("hireClose").onclick=()=>document.getElementById("hire").classList.remove("open");
document.getElementById("talkHire").onclick=()=>{const h=HIRE_ROSTER.candidates[hireIndex],w=workerFor(h.id);if(w)talkWorker(w);else say('Hire '+h.name+' before starting an employee conversation.','Review qualifications, wage, strength, and growth path first.');};
function renderCampaign(){const root=document.getElementById("campaignGrid");root.innerHTML=CHAPTER_PROGRESSION.chapters.map((chapter,index)=>{const facility=FACILITIES.find(x=>x.id===chapter.facility),state=index===0?"playable":index===1?"development":"locked",label=index===0?"PLAYABLE OPENING CHAPTER":index===1?"IN DEVELOPMENT":"LOCKED · FUTURE CHAPTER",gate=Object.entries(chapter.gate).slice(0,3).map(([k,v])=>k.replaceAll(/([A-Z])/g," $1").toUpperCase()+": "+v).join(" · ");return '<article class="chapterCard '+state+'" data-chapter="'+chapter.chapter+'"><span class="chapterStatus">'+label+'</span><h3>CHAPTER '+chapter.chapter+' · '+chapter.title.toUpperCase()+'</h3><div class="chapterFacility">'+facility.name.toUpperCase()+' · '+facility.floorAreaSqFt.toLocaleString()+' SQ FT</div><div class="chapterTime">TARGET '+chapter.targetHours[0]+'–'+chapter.targetHours[1]+' HOURS</div><p>'+facility.fantasy+'</p><div class="chapterGate">GRADUATION: '+gate+'</div></article>'}).join("");}
document.getElementById("bcampaign").onclick=()=>{renderCampaign();document.getElementById("campaign").classList.add("open");};document.getElementById("campaignClose").onclick=()=>document.getElementById("campaign").classList.remove("open");

function renderHires(){const h=HIRE_ROSTER.candidates[hireIndex],root=document.getElementById("hireCard"),w=workerFor(h.id);document.getElementById("hireCount").textContent=(hireIndex+1)+" / "+HIRE_ROSTER.candidates.length+' · TEAM '+workers.length;root.innerHTML='<div class="hireCard panel"><div class="atlasPortrait" style="'+atlasStyle(HIRE_ROSTER.profileAtlas,h.atlasCell)+'"></div><h3>'+h.name+'</h3><div class="role">'+h.title+' · '+h.shift.toUpperCase()+' SHIFT</div><div>'+h.strength+'</div><div>HIRE '+h.hireCost+' · WAGE '+h.wagePerShift+'/SHIFT</div>'+(w?'<div class="qual">STATUS: '+w.status+'</div><select id="quickAssign" class="assignSelect">'+assignmentOptions(h)+'</select>':'')+'<div class="hireActions"><button id="viewProfile">VIEW PROFILE</button><button id="hireNow" '+(hired.has(h.id)?'disabled':'')+'>'+(hired.has(h.id)?'HIRED':'HIRE')+'</button></div></div>';document.getElementById("viewProfile").onclick=()=>showProfileV2(h);document.getElementById("hireNow").onclick=()=>hireCandidate(h);if(w){const s=document.getElementById('quickAssign');s.value=w.assignment||'';s.onchange=()=>assignWorker(h,s.value)}}
function showProfileV2(h){const p=document.getElementById("profile"),w=workerFor(h.id);document.getElementById("roster").style.display="none";p.className="open panel";const skills=Object.entries(h.skills).map(([k,v])=>'<div class="skillRow"><span>'+k.replaceAll("_"," ").toUpperCase()+'</span><span>'+"■".repeat(v)+"□".repeat(5-v)+'</span></div>').join("");p.innerHTML='<div class="profileGrid"><div class="atlasPortrait" style="'+atlasStyle(HIRE_ROSTER.profileAtlas,h.atlasCell)+'"></div><div><div class="ttl">CANDIDATE PROFILE</div><h2>'+h.name+'</h2><div class="role">'+h.title+' · '+h.shift.toUpperCase()+' SHIFT</div>'+skills+'<p><b>STRENGTH:</b> '+h.strength+'</p><p><b>GROWTH:</b> '+h.growthTo.replaceAll("_"," ").toUpperCase()+'</p><p><b>WATCH:</b> '+h.flaw+'</p><p class="qual"><b>QUALIFIED:</b> '+h.qualifications.join(" · ")+'</p>'+(w?'<p><b>ASSIGN TO:</b></p><select id="profileAssign" class="assignSelect">'+assignmentOptions(h)+'</select>':'')+'<p>HIRE '+h.hireCost+' · WAGE '+h.wagePerShift+'/SHIFT</p><button id="profileBack">◀ BACK TO CANDIDATES</button> <button id="profileHire" '+(hired.has(h.id)?'disabled':'')+'>'+(hired.has(h.id)?'HIRED':'HIRE '+h.name.toUpperCase())+'</button></div></div>';document.getElementById("profileBack").onclick=()=>{p.className="";document.getElementById("roster").style.display="block";renderHires();};document.getElementById("profileHire").onclick=()=>{hireCandidate(h);showProfileV2(h);};if(w){const s=document.getElementById('profileAssign');s.value=w.assignment||'';s.onchange=()=>{assignWorker(h,s.value);showProfileV2(h)}}}
const cv=document.getElementById("cv"), cx=cv.getContext("2d");
const T=64;
let map, running=false, overlays=true, frame=0;
let P={x:9,y:7,step:0,rx:9,ry:7,fromX:9,fromY:7,moveAt:0,facing:"down",running:false,moveDuration:145},moveTimer=null,moveTarget=null;
let cam={x:0,y:0}, VW=20, VH=14;
const done=new Set(); let coins=8250;
const state={ toolReady:false, tool:null, stickout:0, toolsSet:[], rawStockReady:false, job:null, materialOrders:[], jobsShipped:0, grades:[],pendingContract:null,contracts:[],storySequences:[],reputation:CUSTOMER_CONTRACTS.reputationRules.starting,founder:{level:1,xp:0,upgradePoints:0,stats:null},machineRun:null,equipment:{vmc:1,saw:1,inspection:1},equipmentCooldownUntil:0 };let paused=false,gameStarted=false,debugOpen=false;
function founderState(){const profile=activeFounderProfile(),f=state.founder||(state.founder={level:1,xp:0,upgradePoints:0,stats:null});if(!f.stats)f.stats={...profile.stats};return f;}
function openFounderProgress(){const f=founderState(),profile=activeFounderProfile();let modal=document.getElementById("founderProgress");if(!modal){modal=document.createElement("div");modal.id="founderProgress";modal.innerHTML='<div id="founderProgressPanel" class="panel"><div class="ttl">FOUNDER DEVELOPMENT</div><div id="founderProgressBody"></div><button id="closeFounderProgress">RETURN TO SHOP</button></div>';document.body.append(modal);document.getElementById("closeFounderProgress").onclick=()=>modal.classList.remove("open");}document.getElementById("founderProgressBody").innerHTML='<h2>'+playerName+'</h2><div class="founderSpecialty">'+profile.specialty+'</div><p>LEVEL '+f.level+' · XP '+f.xp+'/'+(f.level*100)+' · UPGRADE POINTS '+f.upgradePoints+'</p><div>'+Object.entries(f.stats).map(([key,value])=>'<div class="progressStat"><b>'+key.replaceAll("_"," ").toUpperCase()+'</b><span>'+"■".repeat(value)+"□".repeat(5-value)+'</span><button data-upgrade="'+key+'" '+(f.upgradePoints<1||value>=5?'disabled':'')+'>UPGRADE</button></div>').join('')+'</div><p class="founderAbility"><b>'+profile.ability.name+'</b> · '+profile.ability.effect+'</p>';document.querySelectorAll('[data-upgrade]').forEach(button=>button.onclick=()=>{const key=button.dataset.upgrade;if(f.upgradePoints<1||f.stats[key]>=5)return;f.stats[key]++;f.upgradePoints--;saveGame("FOUNDER UPGRADE");openFounderProgress();});modal.classList.add("open");}
document.getElementById("openFounderProgress").onclick=openFounderProgress;
function equipmentState(){return state.equipment||(state.equipment={vmc:1,saw:1,inspection:1});}
function marketAtlasStyle(cell){if(cell===undefined)return '';const x=cell%3,y=Math.floor(cell/3);return 'background-image:url('+assetUrl(EQUIPMENT_VIEWS[EQUIPMENT_MARKET.atlas])+');background-size:300% 300%;background-position:'+(x*50)+'% '+(y*50)+'%;';}
let storeLesson=0;
function renderStoreCoach(){const lesson=EQUIPMENT_MARKET.walkthrough[storeLesson],average=gradeAverage(),next=map?.id==='bay_02'?FACILITIES[2]:FACILITIES[1],garageReady=state.jobsShipped>=5&&average>=3,pressure=state.jobsShipped<2?'KEEP LEARNING · CURRENT EQUIPMENT IS ENOUGH':state.jobsShipped<5?'WATCH QUEUES · BUY ONLY WHEN A WAIT BLOCKS GOOD WORK':'REVIEW THE NEXT FACILITY · GARAGE PRODUCTION IS PROVEN';document.getElementById('storeCoach').innerHTML='<div class="ttl">ZACH\'S STORE WALKTHROUGH · '+lesson.title+'</div><p>'+lesson.text+'</p><div class="panel"><b>GROWTH CHECK:</b> '+pressure+'<br><span class="hint">JOBS '+state.jobsShipped+'/5 · QUALITY '+(average||0).toFixed(1)+'/3.0 · TEAM '+workers.length+' · CASH '+coins+' · NEXT '+next.name.toUpperCase()+' '+next.floorAreaSqFt.toLocaleString()+' SQ FT</span><br><span class="equipmentStatus">'+(garageReady?'CHAPTER PRODUCTION GATE READY':'KEEP BUILDING CAPABILITY')+'</span></div><button id="storeLessonPrev" '+(storeLesson===0?'disabled':'')+'>◀ PREVIOUS</button><button id="storeLessonNext" class="grn">'+(storeLesson===EQUIPMENT_MARKET.walkthrough.length-1?'RESTART WALKTHROUGH':'NEXT LESSON ▶')+'</button><button id="storeFacilityRoadmap">VIEW FACILITY ROADMAP</button>';document.getElementById('storeLessonPrev').onclick=()=>{storeLesson=Math.max(0,storeLesson-1);renderStoreCoach()};document.getElementById('storeLessonNext').onclick=()=>{storeLesson=(storeLesson+1)%EQUIPMENT_MARKET.walkthrough.length;renderStoreCoach();playZach('zach_response_next_step')};document.getElementById('storeFacilityRoadmap').onclick=()=>{document.getElementById('equipmentMarket').style.display='none';renderCampaign();document.getElementById('campaign').classList.add('open')};}
function openEquipmentMarket(){let modal=document.getElementById("equipmentMarket");if(!modal){modal=document.createElement("div");modal.id="equipmentMarket";modal.style.cssText="position:fixed;inset:0;z-index:181;background:#05070aef;display:none;place-items:center;padding:12px";modal.innerHTML='<div class="panel" style="width:min(1100px,96vw);max-height:94dvh;overflow:auto"><div class="ttl">FACTORY EQUIPMENT MARKET · AEROSPACE GROWTH PATH</div><p>'+EQUIPMENT_MARKET.progressionRule+'</p><div id="equipmentMarketBody" class="equipmentMarketGrid"></div><button id="equipmentMarketClose">RETURN TO SHOP</button></div>';document.body.append(modal);document.getElementById("equipmentMarketClose").onclick=()=>modal.style.display="none";}const owned=equipmentState();document.getElementById("equipmentMarketBody").innerHTML=EQUIPMENT_MARKET.items.map(item=>{const locked=state.jobsShipped<item.unlockJobs,count=owned[item.id]||0,price=item.cost*Math.max(1,count),art=item.atlasCell===undefined?'':'<div class="equipmentProductArt" role="img" aria-label="'+item.name+' equipment preview" style="'+marketAtlasStyle(item.atlasCell)+'"></div>';return '<article class="panel equipmentProduct" data-equipment="'+item.id+'">'+art+'<div><div class="equipmentMeta">'+item.category+' · CHAPTER '+item.chapter+' · '+item.facility+'</div><h3>'+item.name+' · OWNED '+count+'</h3><p>'+item.effect+'</p><p class="hint">'+item.spec+'</p><span class="equipmentStatus">'+(item.status==='playable'?'PLAYABLE CAPACITY':'ORIENTATION · WORKFLOW ARRIVES WITH CHAPTER')+'</span>'+(locked?'<div class="hint">LOCKED · SHIP '+item.unlockJobs+' JOBS TO REVEAL</div>':'<button data-buy-equipment="'+item.id+'" data-price="'+price+'" '+(coins<price?'disabled':'')+'>BUY FOR '+price+' COINS</button>')+'</div></article>';}).join('');document.querySelectorAll('[data-buy-equipment]').forEach(button=>button.onclick=()=>{const id=button.dataset.buyEquipment,price=Number(button.dataset.price);if(coins<price)return;coins-=price;owned[id]=(owned[id]||0)+1;addCoins(0);saveGame("EQUIPMENT PURCHASE");playSfx("terminal_confirm");openEquipmentMarket();});modal.style.display="grid";}
const openEquipmentMarketBase=openEquipmentMarket;openEquipmentMarket=function(){openEquipmentMarketBase();if(!document.getElementById('storeCoach')){const coach=document.createElement('section');coach.id='storeCoach';coach.className='panel';coach.setAttribute('aria-live','polite');document.getElementById('equipmentMarketBody').before(coach)}renderStoreCoach();};
{const marketButton=document.createElement("button");marketButton.id="openEquipmentMarket";marketButton.textContent="EQUIPMENT MARKET";marketButton.style.cssText="position:fixed;left:10px;bottom:64px;z-index:35";document.getElementById("openFounderProgress").after(marketButton);marketButton.onclick=openEquipmentMarket;}
const CHAPTER_ONE_TARGET=5;
let phoneSocket=null,phoneRun=false;
let inputMode=localStorage.getItem("reindustrialize.inputMode")||"auto";const accepts=kind=>!paused&&(inputMode==="auto"||inputMode===kind);
function renderControlSelection(){document.getElementById("inputMode").value=inputMode;document.querySelectorAll(".controlChoice").forEach(b=>b.classList.toggle("selected",b.dataset.control===inputMode));const labels={keyboard:"KEYBOARD SELECTED",gamepad:"XBOX / GAMEPAD SELECTED",phone:"PHONE QR CONTROL SELECTED",touch:"TOUCHSCREEN SELECTED",auto:"ALL INPUTS ACTIVE"};document.getElementById("selectedControlStatus").textContent=labels[inputMode]||"CONTROL SELECTED";}
function selectControl(mode){inputMode=mode;localStorage.setItem("reindustrialize.inputMode",mode);renderControlSelection();if(mode==="phone"){document.getElementById("connect").classList.add("open");if(!document.getElementById("pairQr").getAttribute("src"))createPhoneSession();}}
document.querySelectorAll(".controlChoice").forEach(b=>b.onclick=()=>selectControl(b.dataset.control));
document.getElementById("inputMode").onchange=e=>selectControl(e.target.value);renderControlSelection();
let learnerMode=localStorage.getItem("reindustrialize.learnerMode")!=="off";
function renderLearnerMode(){let button=document.getElementById("learnerMode");if(!button){button=document.createElement("button");button.id="learnerMode";document.querySelector(".controlSelect").append(button);button.onclick=()=>{learnerMode=!learnerMode;localStorage.setItem("reindustrialize.learnerMode",learnerMode?"on":"off");renderLearnerMode();};}button.textContent=learnerMode?"★ GUIDED LEARNER HELP: ON · BIG HINTS + EASIER FIRST JOBS":"GUIDED LEARNER HELP: OFF";button.setAttribute("aria-pressed",String(learnerMode));}
renderLearnerMode();
const kidExplain=text=>learnerMode?text.replaceAll("traveler","job instruction card").replaceAll("certification","proof of the exact metal type").replaceAll("work offset","saved part starting point").replaceAll("protrusion","tool length outside the holder").replaceAll("first article","first finished part"):text;
function phoneInput(key){if(key==="menu"&&gameStarted){togglePause();return}if(!accepts("phone"))return;const d=DIRS[key];if(d)move(d[0],d[1],false,phoneRun);else if(key==="run")phoneRun=!phoneRun;else if(key==="action")interact();}
async function createPhoneSession(){
  const stateEl=document.getElementById("pairState");stateEl.textContent="CREATING SESSION…";
  try{const response=await fetch("/api/controller-session",{method:"POST"});if(!response.ok)throw new Error("Launch through the game server first.");const data=await response.json();
    document.getElementById("pairQr").src=data.qr;document.getElementById("pairUrl").textContent=data.controllerUrl;stateEl.textContent="WAITING FOR PHONE";
    const protocol=location.protocol==="https:"?"wss":"ws";phoneSocket=new WebSocket(protocol+"://"+location.host+"/pair?token="+data.token+"&role=host");
    phoneSocket.onmessage=e=>{const msg=JSON.parse(e.data);if(msg.type==="status")stateEl.textContent=msg.connected?"PHONE CONNECTED":"WAITING FOR PHONE";if(msg.type==="input"&&msg.state)phoneInput(msg.key);};
    phoneSocket.onclose=()=>stateEl.textContent="SESSION ENDED";
  }catch(error){stateEl.textContent=error.message;}
}
document.getElementById("bphone").onclick=()=>document.getElementById("connect").classList.add("open");
document.getElementById("pairClose").onclick=()=>document.getElementById("connect").classList.remove("open");
document.getElementById("pairStart").onclick=createPhoneSession;
function storyText(text){return text.replaceAll("{playerName}",playerName).replaceAll("{companyName}",companyName);}
function sequencePages(id){return STORY_PRODUCTION.sequences[id].map(b=>[b.kicker,storyText(b.text),b.voice,b.visual,b.id]);}
function makePrologue(){const pages=sequencePages("opening");return learnerMode?pages.slice(0,3):pages;}
let introPages=makePrologue();
let introStep=0,introSequence="opening",introComplete=null;
function renderIntro(){const s=introPages[introStep];setStoryArt(s[3]);document.getElementById("introKicker").textContent=s[0];document.getElementById("introText").textContent=s[1];document.getElementById("intro").dataset.storyBeat=s[4];document.getElementById("introNext").textContent=introStep===introPages.length-1?(introSequence==="opening"?"OPEN THE SHOP ▸":"ENTER THE JOB SHOP ▸"):"CONTINUE ▸";if(s[2])playZach(s[2]);else stopZach("VOICE: NARRATION PAUSED");}
document.getElementById("introNext").onclick=()=>{introStep++;if(introStep<introPages.length){renderIntro();return;}document.getElementById("intro").classList.add("closed");const complete=introComplete;introComplete=null;if(complete){complete();return;}if(introSequence==="opening"){mission("meet_zach");say(companyName+" is open.","Zach will coach you through a hands-on shift at every Garage Bay station.");setTimeout(()=>startShopTour(true,true),100);}};
function storySeen(id){return (state.storySequences||[]).includes(id);}
function markStorySeen(ids){if(!state.storySequences)state.storySequences=[];for(const id of ids)if(!state.storySequences.includes(id))state.storySequences.push(id);cv.dataset.storySequences=state.storySequences.join(",");}
function showStorySequence(id,onComplete=null){if(storySeen(id)){if(onComplete)onComplete();return false;}markStorySeen([id]);introSequence=id;introPages=sequencePages(id);introStep=0;introComplete=onComplete;renderIntro();document.getElementById("intro").classList.remove("closed");saveGame("STORY");return true;}
function showExpansion(){
  document.getElementById("b2").disabled=false;document.getElementById("b2").textContent="BAY 02";
  setStoryArt("expansion");
  if(storySeen("garage_graduation")){enterJobShop();return;}
  markStorySeen(["garage_graduation","job_shop_expansion"]);introSequence="garage_graduation";introPages=[...sequencePages("garage_graduation"),...sequencePages("job_shop_expansion")];
  introStep=0;introComplete=enterJobShop;renderIntro();document.getElementById("intro").classList.remove("closed");saveGame("CHAPTER");
}
function enterJobShop(){setMap("bay_02");sel("b2");say(companyName+" has entered the Job Shop chapter.","Hire a team, control flow, and earn the next facility.");}
renderIntro();

/* ================= JOBS (rotate) ================= */
const JOBS=[
 {id:"drill", card:"JOB 1042 — DRILL 4 HOLES Ø0.257, 0.55 DEEP — 6061-T6", stockLength:4.25,
  tool:"twist", stickTarget:1.1, stickTol:0.15, stickWhy:"hole depth 0.55 + clamp clearance — set to the line",
  gtitle:"DRILL CYCLE", anim:"drill",
  prog:["T1 M06 (0.257 TWIST DRILL)","G90 G{{o}} G00 X0.6 Y0.7","S3500 M{{s}}","G43 H01 Z1.0 M{{c}}","G81 G99 Z-0.55 R0.1 F8.","X1.2 / X1.8 / X2.4","G80 G00 Z1.0 M09","M05","G28 G91 Z0.","M30"],
  blanks:{o:{ans:["54"],label:"G__ work offset"}, s:{ans:["03","3"],label:"M__ spindle CW"}, c:{ans:["08","8"],label:"M__ coolant on"}},
  hints:{tool:["The print says HOLES.","Drills make holes. Flat or ball endmills don't start holes well.","Pick the twist drill — the pointed one."],
         stick:["Enough to reach depth, no more.","Short = crash into the clamp. Long = wander and snap.","Put the tool tip right on the gold line."],
         g:["Work offset is where the part lives. Spindle needs a direction. Chips need coolant.","G54 is the classic first offset. M03 is clockwise. M08 is flood on.","G54 / M03 / M08."]}},
 {id:"pocket", card:"JOB 1043 — ROUGH SQUARE POCKET 2.0 x 1.4, 0.375 DEEP — 6061-T6", stockLength:5.50,
  tool:"end", stickTarget:1.4, stickTol:0.15, stickWhy:"pocket depth + holder clearance — set to the line",
  gtitle:"POCKET ROUGHING", anim:"pocket",
  prog:["T2 M06 (1/2 END MILL)","G90 G{{o}} G00 X0. Y0.","S6100 M{{s}}","G43 H02 Z1.0 M{{c}}","G01 Z-0.375 F12.","G01 (SPIRAL POCKET PATH)","G00 Z1.0 M09","M05","G28 G91 Z0.","M30"],
  blanks:{o:{ans:["54"],label:"G__ work offset"}, s:{ans:["03","3"],label:"M__ spindle CW"}, c:{ans:["08","8"],label:"M__ coolant on"}},
  hints:{tool:["Square pocket, flat floor.","A flat-bottom cutter leaves a flat floor. Drills can't drive sideways.","Pick the end mill — flat tip with flutes."],
         stick:["Reach the floor of the pocket plus a little.","Too much stickout on an end mill = chatter marks all over your wall.","Tip on the gold line. That's the number."],
         g:["Offset, spindle, coolant. Same three every day.","G54 / M03 / M08.","G54 / M03 / M08 — burn it in."]}},
 {id:"dome", card:"JOB 1044 — FINISH 3D DOME SURFACE R0.75 — 6061-T6", stockLength:3.75,
  tool:"ball", stickTarget:1.3, stickTol:0.15, stickWhy:"curve depth + clearance — set to the line",
  gtitle:"3D FINISHING", anim:"dome",
  prog:["T3 M06 (3/8 BALL MILL)","G90 G{{o}} G00 X-1.0 Y0.","S8000 M{{s}}","G43 H03 Z1.0 M{{c}}","G01 (3D CONTOUR PASSES)","G00 Z1.0 M09","M05","G28 G91 Z0.","M30"],
  blanks:{o:{ans:["54"],label:"G__ work offset"}, s:{ans:["03","3"],label:"M__ spindle CW"}, c:{ans:["08","8"],label:"M__ coolant on"}},
  hints:{tool:["Curved surface. Which tip matches a curve?","A ball nose blends 3D surfaces smooth. Flat tools leave steps.","Pick the ball mill — round tip."],
         stick:["Reach the low point of the dome.","Finishing hates vibration — don't hang it out further than the line.","Tip on the gold line."],
         g:["Same trio: where's the part, spin it, cool it.","G54 / M03 / M08.","G54 / M03 / M08."]}}
];
let jobIdx=0;
const SAVE_KEY="reindustrialize.save.v1",SAVE_BACKUP_KEY="reindustrialize.save.backup.v1",SAVE_TEMP_KEY="reindustrialize.save.pending.v1",SAVE_VERSION=1;
function renderRecoverySummary(){let box=document.getElementById("resumeSummary");if(!box){box=document.createElement("div");box.id="resumeSummary";box.setAttribute("aria-live","polite");document.querySelector(".titleMenu").before(box);}let save=null;for(const key of [SAVE_KEY,SAVE_TEMP_KEY,SAVE_BACKUP_KEY]){try{const candidate=JSON.parse(localStorage.getItem(key)||"null");if(candidate&&candidate.v===SAVE_VERSION){save=candidate;break;}}catch{}}if(!save){box.textContent="";document.getElementById("continueGame").textContent="CONTINUE";return;}const chapter=(save.state?.jobsShipped||0)>=5?"JOB SHOP EXPANSION":"GARAGE BAY";box.innerHTML='<b>FACTORY READY TO RESUME</b><br>'+save.companyName+' · '+save.playerName+' · '+chapter+' · '+(save.state?.jobsShipped||0)+' JOBS SHIPPED<br><span class="hint">CHECKPOINT '+new Date(save.savedAt).toLocaleString()+'</span>';document.getElementById("continueGame").textContent="CONTINUE FACTORY";}
function saveSnapshot(){return{v:SAVE_VERSION,savedAt:new Date().toISOString(),companyName,playerName,selectedAvatar,mapId:map?.id||"bay_01",player:{x:P.x,y:P.y},coins,done:[...done],jobIdx,state:JSON.parse(JSON.stringify(state)),hired:[...hired],workers:workers.map(w=>({id:w.id,x:w.x,y:w.y,assignment:w.assignment,status:w.status})),flow:{introOpen:!document.getElementById("intro").classList.contains("closed"),introSequence,introStep,onboarding:{active:tourActive,index:tourIndex,phase:tourPhase,practiceStep:tourPracticeStep,mandatory:tourMandatory,completed:[...completedTourStops]}}};}
function saveGame(reason="MANUAL"){if(!gameStarted)return false;try{const next=JSON.stringify(saveSnapshot()),current=localStorage.getItem(SAVE_KEY);if(current)localStorage.setItem(SAVE_BACKUP_KEY,current);localStorage.setItem(SAVE_TEMP_KEY,next);localStorage.setItem(SAVE_KEY,next);localStorage.removeItem(SAVE_TEMP_KEY);document.getElementById("continueGame").disabled=false;renderRecoverySummary();const status=document.getElementById("saveStatus");status.textContent=reason+" SAVE · "+new Date().toLocaleTimeString();cv.dataset.saveStatus="saved";return true}catch(error){document.getElementById("saveStatus").textContent="SAVE FAILED · "+error.message;cv.dataset.saveStatus="failed";return false;}}
function validateSaveSnapshot(save){
  const fail=message=>{throw new Error("Corrupt save: "+message)};
  if(!save||typeof save!=="object"||save.v!==SAVE_VERSION)fail("missing or unsupported version");
  if(typeof save.companyName!=="string"||!save.companyName.trim()||save.companyName.length>80)fail("invalid company name");
  if(typeof save.playerName!=="string"||!save.playerName.trim()||save.playerName.length>80)fail("invalid founder name");
  if(!FOUNDER_PROFILES.profiles.some(profile=>profile.avatar===save.selectedAvatar))fail("unknown founder avatar");
  if(!(save.mapId in MAPS))fail("unknown facility map");
  if(!Number.isSafeInteger(save.jobIdx)||save.jobIdx<0||!Number.isSafeInteger(save.coins)||save.coins<0)fail("invalid economy values");
  if(!save.player||!Number.isInteger(save.player.x)||!Number.isInteger(save.player.y))fail("invalid player position");
  const [width,height]=MAPS[save.mapId].size;if(save.player.x<0||save.player.y<0||save.player.x>=width||save.player.y>=height)fail("player outside facility");
  if(!Array.isArray(save.done)||!save.done.every(x=>typeof x==="string")||!Array.isArray(save.hired)||!save.hired.every(x=>typeof x==="string"))fail("invalid progression lists");
  if(!Array.isArray(save.workers)||!save.workers.every(w=>w&&typeof w.id==="string"&&Number.isInteger(w.x)&&Number.isInteger(w.y)))fail("invalid workforce");
  const s=save.state;if(!s||typeof s!=="object"||!Array.isArray(s.toolsSet)||!Array.isArray(s.materialOrders)||!Array.isArray(s.grades)||!Array.isArray(s.contracts)||!Array.isArray(s.storySequences)||!Number.isSafeInteger(s.jobsShipped)||s.jobsShipped<0||!Number.isFinite(s.reputation)||s.reputation<0||s.reputation>100)fail("invalid game progression");
  return save;
}
function quarantineBrokenSave(raw){try{if(raw&&raw.length<1000000)localStorage.setItem("reindustrialize.save.recovery",raw);localStorage.removeItem(SAVE_KEY)}catch{}document.getElementById("continueGame").disabled=true;}
function restoreGame(){const raw=localStorage.getItem(SAVE_KEY);try{const save=validateSaveSnapshot(JSON.parse(raw||"null"));gameStarted=true;companyName=save.companyName;playerName=save.playerName;selectedAvatar=save.selectedAvatar;jobIdx=save.jobIdx;coins=save.coins;Object.assign(state,save.state);done.clear();save.done.forEach(x=>done.add(x));hired.clear();workers.length=0;save.hired.forEach(x=>hired.add(x));save.workers.forEach(w=>{const candidate=HIRE_ROSTER.candidates.find(c=>c.id===w.id);if(candidate)workers.push({...w,candidate,nextMove:0,workPulse:0})});document.getElementById("companyName").value=companyName;document.getElementById("founderName").value=playerName;document.getElementById("playerName").textContent=playerName;document.getElementById("playerNameM").textContent=playerName;document.querySelectorAll(".avatarChoice").forEach(b=>b.classList.toggle("selected",b.dataset.avatar===selectedAvatar));renderFounderPreview();const mapId=save.mapId;if(mapId==="bay_02"){document.getElementById("b2").disabled=false;document.getElementById("b2").textContent="BAY 02"}setMap(mapId);P.x=save.player.x;P.y=save.player.y;P.rx=P.x;P.ry=P.y;P.fromX=P.x;P.fromY=P.y;document.querySelectorAll("#missions [data-m]").forEach(el=>el.classList.toggle("done",done.has(el.dataset.m)));const pct=Math.round(done.size/4*100);document.querySelector("#qbar i").style.width=pct+"%";document.getElementById("qpct").textContent=pct+"%";document.getElementById("qpctM").textContent=pct+"%";addCoins(0);updateGuide();document.getElementById("preFounder").classList.add("closed");document.getElementById("titleScreen").classList.add("closed");document.getElementById("intro").classList.add("closed");startAmbience();say(companyName+" restored.","Local save loaded · "+new Date(save.savedAt).toLocaleString());return true}catch(error){gameStarted=false;quarantineBrokenSave(raw);alert("Unable to load this save: "+error.message+" A recovery copy was kept on this device and you can safely start a new game.");return false;}}
function applyRuntimeSettings(){document.getElementById("masterVolume").value=masterVolume;document.getElementById("voiceVolumeSetting").value=voiceVolume;document.getElementById("sfxVolumeSetting").value=sfxVolume;document.getElementById("ambienceVolumeSetting").value=ambienceVolume;const reduced=localStorage.getItem("reindustrialize.reducedMotion")==="on",scale=localStorage.getItem("reindustrialize.uiScale")||"1";document.getElementById("reducedMotion").checked=reduced;document.getElementById("uiScale").value=scale;document.body.classList.toggle("reducedMotion",reduced);document.body.style.zoom=scale;setAmbienceLevel(false);if(zachAudio)zachAudio.volume=masterVolume*voiceVolume;if(sfxLoop)sfxLoop.volume=masterVolume*sfxVolume;}
function openPause(){if(!gameStarted)return;paused=true;document.getElementById("pauseMenu").classList.add("open");document.getElementById("resumeGame").focus();applyRuntimeSettings();}
function closePause(){paused=false;document.getElementById("pauseMenu").classList.remove("open");document.getElementById("bpause").focus();}
function togglePause(){paused?closePause():openPause();}
function restoreGameResilient(){let selected=null;for(const key of [SAVE_KEY,SAVE_TEMP_KEY,SAVE_BACKUP_KEY]){const raw=localStorage.getItem(key);if(!raw)continue;try{const parsed=validateSaveSnapshot(JSON.parse(raw));selected={raw,parsed,key};break}catch{}}if(!selected){alert("No valid local recovery checkpoint was found.");return false;}localStorage.setItem(SAVE_KEY,selected.raw);const ok=restoreGame();if(!ok)return false;const flow=selected.parsed.flow;if(flow?.introOpen&&!flow?.onboarding?.active){introSequence=flow.introSequence||"opening";introPages=introSequence==="opening"?makePrologue():sequencePages(introSequence);introStep=Math.max(0,Math.min(Number(flow.introStep)||0,introPages.length-1));renderIntro();document.getElementById("intro").classList.remove("closed");}const onboarding=flow?.onboarding;if(onboarding?.active){tourIndex=Math.max(0,Math.min(Number(onboarding.index)||0,SHOP_TOUR.stops.length-1));tourPhase=Math.max(0,Math.min(Number(onboarding.phase)||0,2));tourPracticeStep=Math.max(0,Number(onboarding.practiceStep)||0);tourMandatory=!!onboarding.mandatory;tourActive=true;completedTourStops.clear();(onboarding.completed||[]).forEach(id=>completedTourStops.add(id));setTimeout(()=>tourPhase===2?renderTourPractice():renderTourStop(),100);}saveGame("RECOVERY");say(companyName+" recovered.",selected.key===SAVE_KEY?"Restored from the latest automatic checkpoint.":"The latest save was incomplete, so the previous safe checkpoint was restored.");return true;}
document.getElementById("continueGame").disabled=![SAVE_KEY,SAVE_TEMP_KEY,SAVE_BACKUP_KEY].some(key=>localStorage.getItem(key));renderRecoverySummary();document.getElementById("continueGame").onclick=restoreGameResilient;document.getElementById("bpause").onclick=openPause;document.getElementById("resumeGame").onclick=closePause;document.getElementById("saveNow").onclick=()=>saveGame("MANUAL");document.getElementById("fullscreenGame").onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen().catch(()=>{});document.getElementById("returnTitle").onclick=()=>{saveGame("RETURN");location.reload()};
[["masterVolume",v=>masterVolume=v,"reindustrialize.masterVolume"],["voiceVolumeSetting",v=>voiceVolume=v,"reindustrialize.voiceVolume"],["sfxVolumeSetting",v=>sfxVolume=v,"reindustrialize.sfxVolume"],["ambienceVolumeSetting",v=>ambienceVolume=v,"reindustrialize.ambienceVolume"]].forEach(([id,set,key])=>document.getElementById(id).oninput=e=>{set(Number(e.target.value));localStorage.setItem(key,e.target.value);applyRuntimeSettings()});document.getElementById("reducedMotion").onchange=e=>{localStorage.setItem("reindustrialize.reducedMotion",e.target.checked?"on":"off");applyRuntimeSettings()};document.getElementById("uiScale").onchange=e=>{localStorage.setItem("reindustrialize.uiScale",e.target.value);applyRuntimeSettings()};applyRuntimeSettings();
setInterval(()=>saveGame("AUTO"),10000);document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="hidden")saveGame("BACKGROUND")});addEventListener("pagehide",()=>saveGame("PAGE HIDE"));addEventListener("beforeunload",()=>saveGame("EXIT"));

/* ================= FLOOR (same engine as v3) ================= */
const MSG={
 "planning_desk":["Planning desk. New job card is here.","Press E / ● to read today's job."],
 "nox_terminal":["NOX-NET terminal. Metal on your dock next day.",""],
 "chalkboard":["Shop Class. The formulas behind every task live here.",""],
 "whiteboard":["Today's missions. Set up a tool. Run the VMC.",""],
 "tool_cart":["Tool cart. Press E / ● to open TOOL SETUP.","Pick the right tool and set stickout to the line."],
 "presetter_t4":["Presetter. Press E / ● to open TOOL SETUP.","Measure offline, cut sooner."],
 "saw_t1":["Bandsaw. Square stock, square parts.",""],
 "mill_manual_t1":["Knee mill. Every machinist starts here.",""],
 "bench_deburr_t1":["Deburr bench. Break every edge.",""],
 "vmc_t2":["The VMC. Press E / ● to load your program.","Needs a tool set up first."],
 "lathe_cnc_t2":["CNC lathe. Constant surface speed thinking.",""],
 "network_node_t3":["MTConnect node. See the truth about uptime.",""],
 "handoff_terminal_t4":["JobLine handoff terminal.",""],
 "toolcrib_rfid_t4":["RFID tool crib. Tag it or hunt for it.",""],
 "cobot_t5":["Cobot. Runs your process faster — good or bad.",""],
 "amr_t5":["AMR pallet bot. Stay out of its lane.",""],
 "nox_pallet":["Certed NOX aluminum.",""]
};
function say(a,b,voiceId){document.getElementById("dtext").textContent=a;document.getElementById("dhint").textContent=b||"";playZach(voiceId);}
function mission(id){
  const el=document.querySelector('#missions div[data-m="'+id+'"]');
  if(el&&!el.classList.contains("done")){
    el.classList.add("done"); done.add(id); addCoins(250);
    const pct=Math.round(done.size/4*100);
    document.querySelector("#qbar i").style.width=pct+"%";
    document.getElementById("qpct").textContent=pct+"%";
    document.getElementById("qpctM").textContent=pct+"%";
    if(pct===100)say(companyName+" shipped its first paid order.","Reinvest the profit. Grow the team. Earn a larger facility.");
  }
  updateGuide();
  if(gameStarted)saveGame("CHECKPOINT");
}
function addCoins(n){coins+=n;document.getElementById("coins").textContent=coins;document.getElementById("coinsM").textContent=coins;}

function fit(){
  const availW=Math.min(document.documentElement.clientWidth-16, 1120);
  const mobile=availW<900;
  if(map){
    VW=mobile?Math.min(map.size[0], Math.max(9, Math.floor(availW/(availW<420?34:36)))):map.size[0];
    VH=mobile?Math.min(map.size[1], 11):map.size[1];
  }
  cv.width=VW*T; cv.height=VH*T;
  let s=availW/(VW*T); if(s>=2)s=2; else if(s>=1.5&&!mobile)s=1.5;
  cv.style.width=Math.floor(VW*T*s)+"px"; cv.style.height=Math.floor(VH*T*s)+"px";
  clampCam(); if(loaded===total&&map)draw();
}
addEventListener("resize",fit); addEventListener("orientationchange",()=>setTimeout(fit,100));
function clampCam(){ if(!map)return;
  cam.x=Math.max(0,Math.min(P.x-Math.floor(VW/2), map.size[0]-VW));
  cam.y=Math.max(0,Math.min(P.y-Math.floor(VH/2), map.size[1]-VH));}
function setMap(id){cancelMove();map=MAPS[id];ensureMapSprites(map).then(draw); P.x=map.spawn[0]; P.y=map.spawn[1];P.rx=P.x;P.ry=P.y;P.fromX=P.x;P.fromY=P.y; fit(); clampCam();
  if(ambienceAudio)startAmbience(ambienceForMap());
  say("Job card's on the planning desk. Then hit the tool cart, then the VMC.","Follow NEXT ACHIEVABLE STEP. The pulsing gold box marks your target.");updateGuide();}
function tileAt(x,y){ const [w,h]=map.size;
  if(x===0||y===0||x===w-1||y===h-1){
    const z=map.zones, inZ=zn=>z[zn]&&x>=z[zn][0][0]&&x<=z[zn][1][0]&&y>=z[zn][0][1]&&y<=z[zn][1][1];
    if(inZ("receiving")&&x===0)return 4; if(inZ("shipping")&&x===w-1)return 4; return 3;}
  return (x*7+y*13)%9===0?1:0;}
function blocked(x,y){ const [w,h]=map.size;
  if(x<1||y<1||x>=w-1||y>=h-1)return true;
  for(const p of map.placements){const[px,py]=p.tile,[fw,fh]=p.footprint;
    if(x>=px&&x<px+fw&&y>=py&&y<py+fh)return true;} return false;}
function draw(){
  cx.setTransform(1,0,0,1,0,0); cx.clearRect(0,0,cv.width,cv.height);
  cx.translate(-cam.x*T,-cam.y*T);
  if(map.id==="bay_01"){
    if(IMG.bay_01_hd_bg?.complete)cx.drawImage(IMG.bay_01_hd_bg,0,0,map.size[0]*T,map.size[1]*T);else{cx.fillStyle="#111923";cx.fillRect(0,0,map.size[0]*T,map.size[1]*T);}
  }else{
    for(let y=cam.y;y<Math.min(map.size[1],cam.y+VH);y++)
      for(let x=cam.x;x<Math.min(map.size[0],cam.x+VW);x++)
        if(IMG.tileset?.complete)cx.drawImage(IMG.tileset,tileAt(x,y)*32,0,32,32,x*T,y*T,T,T);
  }
  if(overlays){
    if(map.amrLane&&IMG.tileset?.complete){const[a,b]=map.amrLane;for(let x=a[0];x<=b[0];x++)cx.drawImage(IMG.tileset,2*32,0,32,32,x*T,a[1]*T,T,T);}
    for(const[zx,zy]of map.powerDrops){cx.fillStyle="#e8b93b";cx.fillRect(zx*T+12,zy*T+12,8,8);cx.strokeStyle="#000";cx.strokeRect(zx*T+12,zy*T+12,8,8);}
    if(map.netLane){const[a,b]=map.netLane;cx.strokeStyle="#4a9fd4";cx.setLineDash([6,4]);cx.beginPath();cx.moveTo(a[0]*T,a[1]*T+6);cx.lineTo((b[0]+1)*T,b[1]*T+6);cx.stroke();cx.setLineDash([]);}
    cx.fillStyle="rgba(74,159,212,.14)";const zr=map.zones.receiving;cx.fillRect(zr[0][0]*T,zr[0][1]*T,(zr[1][0]-zr[0][0]+1)*T,(zr[1][1]-zr[0][1]+1)*T);
    cx.fillStyle="rgba(232,73,29,.14)";const zs=map.zones.shipping;cx.fillRect(zs[0][0]*T,zs[0][1]*T,(zs[1][0]-zs[0][0]+1)*T,(zs[1][1]-zs[0][1]+1)*T);
  }
  const items=[...map.placements].sort((a,b)=>(a.tile[1]+a.footprint[1])-(b.tile[1]+b.footprint[1]));
  let pd=false;
  for(const p of items){
    const a=ATLAS[p.sprite],spriteImage=IMG[p.sprite]; if(!a||!spriteImage?.complete)continue;
    if(!pd&&P.y+1<=p.tile[1]+p.footprint[1]){drawP();pd=true;}
    let fi=0; if(running&&a.frames>1)fi=frame%2;
    const dw=p.footprint[0]*T,dh=Math.min(p.footprint[1]*T,a.fh*(dw/a.fw));
    cx.drawImage(spriteImage,fi*a.fw,0,a.fw,a.fh,p.tile[0]*T,p.tile[1]*T+(p.footprint[1]*T-dh),dw,dh);
    if(overlays&&p.label){cx.font="13px VT323, monospace";
      cx.strokeStyle="#000";cx.lineWidth=3;cx.strokeText(p.label,p.tile[0]*T+1,p.tile[1]*T-3);
      cx.fillStyle="#e8b93b";cx.fillText(p.label,p.tile[0]*T+1,p.tile[1]*T-3);}
  }
  drawWorkers();if(!pd)drawP();
  const usable=nearStation();
  if(usable){const pulse=.65+.35*Math.sin(Date.now()/105);cx.save();cx.strokeStyle=`rgba(63,208,138,${pulse})`;cx.fillStyle=`rgba(63,208,138,${.08+.08*pulse})`;cx.lineWidth=4;cx.setLineDash([8,5]);cx.fillRect(usable.tile[0]*T-4,usable.tile[1]*T-4,usable.footprint[0]*T+8,usable.footprint[1]*T+8);cx.strokeRect(usable.tile[0]*T-4,usable.tile[1]*T-4,usable.footprint[0]*T+8,usable.footprint[1]*T+8);cx.setLineDash([]);cx.font="bold 18px VT323, monospace";cx.textAlign="center";cx.strokeStyle="#000";cx.lineWidth=4;const ux=(usable.tile[0]+usable.footprint[0]/2)*T,uy=usable.tile[1]*T-10;cx.strokeText("USE",ux,uy);cx.fillStyle="#fff";cx.fillText("USE",ux,uy);cx.restore();}
  const objective=currentObjective(),target=objective&&map.placements.find(p=>p.sprite===objective.sprite);
  if(target){const pulse=.55+.35*Math.sin(Date.now()/180);cx.save();cx.strokeStyle=`rgba(232,185,59,${pulse})`;cx.lineWidth=5;cx.setLineDash([12,7]);cx.strokeRect(target.tile[0]*T-5,target.tile[1]*T-5,target.footprint[0]*T+10,target.footprint[1]*T+10);cx.restore();}
  if(moveTarget){const pulse=.55+.35*Math.sin(Date.now()/120);cx.save();cx.strokeStyle=`rgba(63,208,138,${pulse})`;cx.lineWidth=3;cx.beginPath();cx.arc(moveTarget.x*T+T/2,moveTarget.y*T+T/2,10+4*pulse,0,Math.PI*2);cx.stroke();cx.beginPath();cx.moveTo(moveTarget.x*T+18,moveTarget.y*T+32);cx.lineTo(moveTarget.x*T+46,moveTarget.y*T+32);cx.moveTo(moveTarget.x*T+32,moveTarget.y*T+18);cx.lineTo(moveTarget.x*T+32,moveTarget.y*T+46);cx.stroke();cx.restore();}
  const glow=cx.createLinearGradient(0,0,0,map.size[1]*T);glow.addColorStop(0,"rgba(5,10,16,.18)");glow.addColorStop(.55,"rgba(0,0,0,0)");glow.addColorStop(1,"rgba(3,6,10,.18)");cx.fillStyle=glow;cx.fillRect(cam.x*T,cam.y*T,VW*T,VH*T);
}
function drawP(){ const a=ATLAS[selectedAvatar],playerImage=IMG[selectedAvatar];if(!a||!playerImage?.complete){loadSprite(selectedAvatar,"high");return}cv.dataset.playerAvatar=selectedAvatar;const moving=performance.now()-P.moveAt<P.moveDuration,run=moving&&P.running,walkFrame=moving?Math.floor(performance.now()/(run?48:90))%2:0;cv.dataset.motion=run?"running":moving?"walking":"idle";
  const now=performance.now(),stride=run?Math.sin(now/38):Math.sin(now/62),bob=moving?Math.abs(stride)*(run?5:2):0;
  cx.fillStyle=run?"rgba(0,0,0,.22)":"rgba(0,0,0,.3)";cx.beginPath();cx.ellipse(P.rx*T+32,P.ry*T+57,run?28:24,run?5:6,0,0,Math.PI*2);cx.fill();
  if(run){const trail=P.facing==="left"?1:P.facing==="right"?-1:0;cx.save();cx.strokeStyle="rgba(226,235,239,.42)";cx.lineWidth=3;for(let i=0;i<3;i++){const yy=P.ry*T+23+i*11;cx.beginPath();cx.moveTo(P.rx*T+32+trail*20,yy);cx.lineTo(P.rx*T+32+trail*(34+i*5),yy);cx.stroke();}cx.fillStyle="rgba(190,176,145,.42)";cx.beginPath();cx.arc(P.rx*T+22-stride*8,P.ry*T+58,3+Math.abs(stride)*3,0,Math.PI*2);cx.fill();}
  const py=P.ry*T-32-bob;cx.save();cx.translate(P.rx*T+32,P.ry*T+18);cx.rotate(run?(P.facing==="left"?-.09:P.facing==="right"?.09:stride*.025):0);cx.scale(1+(run?Math.abs(stride)*.025:0),1-(run?Math.abs(stride)*.018:0));cx.translate(-(P.rx*T+32),-(P.ry*T+18));if(P.facing==="left"){cx.translate(P.rx*T+64,0);cx.scale(-1,1);cx.drawImage(playerImage,walkFrame*a.fw,0,a.fw,a.fh,0,py,64,96);}else cx.drawImage(playerImage,walkFrame*a.fw,0,a.fw,a.fh,P.rx*T,py,64,96);cx.restore();}
function nearStation(){let best=null,bestD=Infinity;
  for(const p of map.placements){const[px,py]=p.tile,[fw,fh]=p.footprint;
    const dx=Math.max(px-P.x,0,P.x-(px+fw-1)),dy=Math.max(py-P.y,0,P.y-(py+fh-1)),d=dx+dy;
    if(d<=1&&d<bestD){best=p;bestD=d;}}return best;}
function drawWorkers(){const im=IMG[HIRE_ROSTER.spriteAtlas];if(!im?.complete)return;const sw=im.naturalWidth/5,sh=im.naturalHeight/2;for(const w of workers){const cell=w.candidate.atlasCell,sx=(cell%5)*sw,sy=Math.floor(cell/5)*sh,bob=w.status.startsWith('WORKING')?Math.sin(Date.now()/120)*2:0;cx.fillStyle='rgba(0,0,0,.28)';cx.beginPath();cx.ellipse(w.x*T+32,w.y*T+57,21,5,0,0,Math.PI*2);cx.fill();cx.drawImage(im,sx,sy,sw,sh,w.x*T+8,w.y*T-22+bob,48,72);cx.font='13px VT323, monospace';cx.textAlign='center';cx.strokeStyle='#000';cx.lineWidth=3;cx.strokeText(w.candidate.name,w.x*T+32,w.y*T-25);cx.fillStyle='#fff';cx.fillText(w.candidate.name,w.x*T+32,w.y*T-25);}}
function updateWorkers(){if(!map)return;const now=Date.now();for(const w of workers){if(now<w.nextMove)continue;w.nextMove=now+700+Math.random()*900;let target=null;if(w.assignment)target=map.placements.find(p=>p.sprite===w.assignment);if(target){const tx=Math.max(1,target.tile[0]-1),ty=target.tile[1]+target.footprint[1]-1,d=Math.abs(tx-w.x)+Math.abs(ty-w.y);if(d<=1){w.status='WORKING · '+(STATION_NAMES[w.assignment]||w.assignment.toUpperCase());continue}w.status='TRAVELING · '+(STATION_NAMES[w.assignment]||w.assignment.toUpperCase());const dx=Math.sign(tx-w.x),dy=Math.sign(ty-w.y);if(dx&&!blocked(w.x+dx,w.y))w.x+=dx;else if(dy&&!blocked(w.x,w.y+dy))w.y+=dy}else{w.status='MEANDERING';const dirs=[[1,0],[-1,0],[0,1],[0,-1],[0,0]],q=dirs[Math.floor(Math.random()*dirs.length)];if(!blocked(w.x+q[0],w.y+q[1])){w.x+=q[0];w.y+=q[1]}}}cv.dataset.workerCount=workers.length;cv.dataset.assignedWorkers=workers.filter(w=>w.assignment).length;}
function nearWorker(){return workers.find(w=>Math.abs(w.x-P.x)+Math.abs(w.y-P.y)<=2)||null}
function talkWorker(w){const c=WORKFORCE_CONVERSATIONS.employees[w.id];if(!c)return;w.dialogueStep=((w.dialogueStep??-1)+1)%4;const lines=[c.greeting,w.assignment?c.assigned:c.idle,c.question,c.answer],labels=['GREETING',w.assignment?'ASSIGNMENT UPDATE':'IDLE UPDATE','PLAYER QUESTION','ROLE GUIDANCE'],speaker=w.candidate.name+': '+lines[w.dialogueStep],hint=labels[w.dialogueStep]+' · Talk again for the next response.';say(speaker,hint);let panel=document.getElementById('npcConversation');if(!panel){panel=document.createElement('div');panel.id='npcConversation';panel.className='panel';document.getElementById('hirePanel').append(panel);}panel.innerHTML='<div class="ttl">'+labels[w.dialogueStep]+' · '+w.candidate.title.toUpperCase()+'</div><b>'+speaker+'</b><div>'+hint+'</div>';panel.style.display=document.getElementById('hire').classList.contains('open')?'block':'none';cv.dataset.lastNpcConversation=w.id;cv.dataset.lastNpcDialogue=labels[w.dialogueStep];}
setInterval(updateWorkers,450);
const STATION_NAMES={planning_desk:"PLANNING DESK",tool_cart:"TOOL CART",vmc_t2:"VMC",nox_terminal:"NOX MATERIAL TERMINAL",lathe_cnc_t2:"CNC LATHE",saw_t1:"BANDSAW",mill_manual_t1:"MANUAL MILL",bench_deburr_t1:"DEBURR BENCH",network_node_t3:"MTCONNECT NODE",handoff_terminal_t4:"HANDOFF TERMINAL",nox_pallet:"RECEIVING",whiteboard:"MISSION BOARD",cobot_t5:"COBOT",amr_t5:"AMR"};
function activeFounderProfile(){return FOUNDER_PROFILES.profiles.find(x=>x.avatar===selectedAvatar)}
function awardFounderXp(amount){const f=state.founder,p=activeFounderProfile();if(!f.stats)f.stats={...p.stats};f.xp+=amount;const needed=f.level*100;while(f.xp>=needed){f.xp-=needed;f.level++;f.upgradePoints++;const lowest=Object.entries(f.stats).sort((a,b)=>a[1]-b[1])[0][0];f.stats[lowest]=Math.min(5,f.stats[lowest]+1);say(playerName+' reached Founder Level '+f.level+'.',lowest.replaceAll('_',' ').toUpperCase()+' improved. Signature abilities evolve at levels 5, 10, and 20.');}cv.dataset.founderLevel=f.level;cv.dataset.founderXp=f.xp;cv.dataset.founderAbility=p.ability.name;}
function gradeAverage(){return state.grades.length?state.grades.reduce((a,b)=>a+b,0)/state.grades.length:0;}
function currentObjective(){
  if(state.machineRun)return{sprite:"vmc_t2",step:state.machineRun.status==="running"?"The VMC is making your part":"Your part is ready to check",how:state.machineRun.status==="running"?"Explore the shop or watch the VMC timer flag.":"Open the green VMC flag and check the finished part."};
  if(!state.materialOrders.length)return{sprite:"nox_terminal",step:"1. Order certified stock for production",how:"Open the pulsing NOX terminal and order 6061-T6 plate."};
  if(state.jobsShipped>=CHAPTER_ONE_TARGET&&gradeAverage()>=3)return null;
  const n=state.jobsShipped+1;
  const countLabel=state.jobsShipped>=CHAPTER_ONE_TARGET?"QUALITY RECOVERY JOB":("JOB "+n+" OF "+CHAPTER_ONE_TARGET);
  if(!state.job)return{sprite:"planning_desk",step:countLabel+": Accept the next customer order",how:"Open the pulsing PLANNING DESK. Each job introduces a different challenge."};
  if(!state.rawStockReady)return{sprite:"saw_t1",step:countLabel+": Cut raw stock to saw length",how:"Open the pulsing BANDSAW. Read the cut length and hold the tolerance."};
  if(!state.toolReady)return{sprite:"tool_cart",step:countLabel+": Set the three-tool CNC kit",how:"Gauge the primary cutting tool, probe, and chamfer tool at the pulsing TOOL CART."};
  return{sprite:"vmc_t2",step:countLabel+": Prove the program and ship the part",how:"Open the pulsing VMC. Complete the G-code checks and run the cycle."};
}
function updateGuide(){if(!map)return;const o=currentObjective(),near=nearStation(),prompt=document.getElementById("stationPrompt"),action=document.getElementById("objectiveAction");
  cv.dataset.nearStation=near?.sprite||"";
  const avg=state.grades.length?state.grades.reduce((a,b)=>a+b,0)/state.grades.length:null;document.getElementById("shipProgress").textContent="JOBS SHIPPED "+state.jobsShipped+" / "+CHAPTER_ONE_TARGET;document.getElementById("gradeProgress").textContent=avg===null?"QUALITY: NOT YET GRADED":"QUALITY SCORE "+avg.toFixed(1)+" / 5 · 3.0 REQUIRED";
  if(o){document.getElementById("objectiveStep").textContent=o.step;document.getElementById("objectiveHow").textContent=kidExplain(o.how);const atTarget=near&&near.sprite===o.sprite;action.disabled=false;action.textContent=atTarget?"OPEN "+(STATION_NAMES[o.sprite]||"STATION"):"GO TO & OPEN "+(STATION_NAMES[o.sprite]||"TARGET");}else{document.getElementById("objectiveStep").textContent="Garage mastery complete — graduate to the Job Shop";document.getElementById("objectiveHow").textContent="Five customer jobs shipped. Review the expansion scene and move your company.";action.disabled=true;action.textContent="CHAPTER COMPLETE";}
  if(near){prompt.classList.add("open");document.getElementById("stationPromptText").textContent="USE · "+(STATION_NAMES[near.sprite]||near.label||"STATION")+" · E / SPACE / XBOX A / PHONE ●";}else prompt.classList.remove("open");}
document.getElementById("objectiveAction").onclick=()=>{const o=currentObjective(),near=nearStation();if(o&&(!near||near.sprite!==o.sprite))walkToStation(o.sprite,true);else interact();};document.getElementById("stationOpen").onclick=interact;
let mentorCategory="context";
function mentorReply(question,answer,voice){const root=document.getElementById("mentorAnswer");root.innerHTML='<div class="mentorAnswer"><img alt="Zach teaching" src="'+assetUrl(SPRITES.zach_portrait)+'"><div><h3>'+question+'</h3><div>'+answer+'</div></div></div>';playZach(voice);}
function contextAnswer(){const o=currentObjective();if(!o)return {question:"What should I improve next?",answer:"Your immediate garage gate is complete. Review quality, cash, team capacity, and flow before committing to the next facility.",voice:"zach_response_next_step"};return {question:"What should I do next?",answer:o.step+" "+o.how+" I will explain the reason at the station, but you make the setup and business decision.",voice:"zach_response_next_step"};}
function renderMentor(category="context"){mentorCategory=category;const tabs=document.getElementById("mentorTabs"),questions=document.getElementById("mentorQuestions");tabs.innerHTML='<button class="mentorTab '+(category==="context"?'on':'')+'" data-c="context">WHAT NEXT?</button>'+MENTOR.categories.map(c=>'<button class="mentorTab '+(category===c.id?'on':'')+'" data-c="'+c.id+'">'+c.label+'</button>').join('');document.querySelectorAll('.mentorTab').forEach(b=>b.onclick=()=>renderMentor(b.dataset.c));if(category==="context"){const x=contextAnswer();questions.innerHTML='<button class="mentorQuestion grn">'+x.question+'</button>';questions.firstElementChild.onclick=()=>mentorReply(x.question,x.answer,x.voice);mentorReply(x.question,x.answer,x.voice);return;}const group=MENTOR.categories.find(c=>c.id===category);questions.innerHTML=group.questions.map(q=>'<button class="mentorQuestion" data-q="'+q.id+'">'+q.question+'</button>').join('');document.querySelectorAll('.mentorQuestion').forEach(b=>b.onclick=()=>{const q=group.questions.find(x=>x.id===b.dataset.q);mentorReply(q.question,q.answer,q.voice);});const q=group.questions[0];mentorReply(q.question,q.answer,q.voice);}
function openMentor(){document.getElementById("mentorPortrait").src=assetUrl(SPRITES.zach_portrait);renderMentor("context");document.getElementById("mentor").classList.add("open");}
document.getElementById("askMentor").onclick=openMentor;document.getElementById("mentorClose").onclick=()=>document.getElementById("mentor").classList.remove("open");
let customerIndex=0,customerChannel="shop_phone";
function customerAtlasStyle(asset,cell){return 'background-image:url('+assetUrl(CUSTOMER_ART[asset])+');background-position:'+(cell*33.333)+'% 50%;';}
function renderCustomer(){const c=CUSTOMER_CONTRACTS.customers[customerIndex],o=c.offer,min=o.minimumReputation||0,locked=state.reputation<min,record=state.contracts.find(x=>x.offerId===o.id),channel=customerChannel==="shop_phone"?"INCOMING SHOP CALL":customerChannel==="jobline_email"?"JOBLINE EMAIL INBOX":"JOBLINE MOBILE";document.getElementById("customerHeader").innerHTML='<b>'+channel+'</b> · REPUTATION '+state.reputation+' / 100 · '+(customerIndex+1)+' OF '+CUSTOMER_CONTRACTS.customers.length;document.getElementById("customerTabs").innerHTML=CUSTOMER_CONTRACTS.customers.map((x,i)=>'<button class="'+(i===customerIndex?'on':'')+'" data-customer="'+i+'">'+x.company+'</button>').join('');document.querySelectorAll('[data-customer]').forEach(b=>b.onclick=()=>{customerIndex=Number(b.dataset.customer);renderCustomer();});document.getElementById("customerBody").innerHTML='<div class="customerCard '+(locked?'locked':'')+'"><div class="customerGrid"><div><div class="customerPortrait" style="'+customerAtlasStyle("customer-profiles-v1",c.atlasCell)+'"></div><div class="customerMeta">'+c.contact+' · '+c.title+'</div></div><div><div class="companyImage" style="'+customerAtlasStyle("customer-companies-v1",c.atlasCell)+'"></div><h2>'+c.company+'</h2><div class="customerMeta">'+c.industry+' · '+c.relationship+'</div><p>'+c.description+'</p></div></div><div class="rfq"><h3>'+o.subject+'</h3><p>“'+o.message+'”</p><b>'+o.quantity+' PIECES · '+o.material+' · '+o.dueShifts+' SHIFTS · '+o.unitPrice+' COINS EACH</b><ul>'+o.requirements.map(x=>'<li>'+x+'</li>').join('')+'</ul>'+(locked?'<div class="hint">LOCKED · REPUTATION '+min+' REQUIRED</div>':'')+(record?'<div class="contractAccepted">'+record.status.toUpperCase()+'</div>':'')+'</div></div>';document.getElementById("customerActions").innerHTML='<button id="customerPrev">◀ PREVIOUS</button><button id="customerNext">NEXT ▶</button><button id="acceptContract" class="grn" '+(locked||record||state.pendingContract?'disabled':'')+'>ACCEPT & CREATE JOBLINE WORK ORDER</button><button id="declineContract" '+(record?'disabled':'')+'>DECLINE</button><button id="mobileMail">OPEN ON SHOP PHONE</button>';document.getElementById("customerPrev").onclick=()=>{customerIndex=(customerIndex+CUSTOMER_CONTRACTS.customers.length-1)%CUSTOMER_CONTRACTS.customers.length;renderCustomer();};document.getElementById("customerNext").onclick=()=>{customerIndex=(customerIndex+1)%CUSTOMER_CONTRACTS.customers.length;renderCustomer();};document.getElementById("mobileMail").onclick=()=>{customerChannel="mobile_jobline";renderCustomer();};document.getElementById("acceptContract").onclick=()=>acceptCustomerContract(c);document.getElementById("declineContract").onclick=()=>{state.contracts.push({offerId:o.id,customerId:c.id,status:"declined"});playSfx("terminal_confirm");renderCustomer();};}
function openCustomers(channel="jobline_email"){customerChannel=channel;document.getElementById("customers").classList.add("open");playSfx(channel==="shop_phone"?"phone_ring":"terminal_wake");renderCustomer();}
function acceptCustomerContract(c){const o=c.offer;state.pendingContract={...o,customerId:c.id,customer:c.company,contact:c.contact};state.contracts.push({offerId:o.id,customerId:c.id,status:"accepted"});playSfx("handoff_confirm");say(c.company+" hired "+companyName+".","JobLine work order "+o.id+" created. Open PLANNING to release the traveler.");renderCustomer();updateGuide();if(!storySeen("first_customer")){document.getElementById("customers").classList.remove("open");setTimeout(()=>showStorySequence("first_customer"),100);}}
document.getElementById("bcustomerphone").onclick=()=>openCustomers("shop_phone");document.getElementById("bmail").onclick=()=>openCustomers("jobline_email");document.getElementById("customerClose").onclick=()=>document.getElementById("customers").classList.remove("open");
document.getElementById("shopPhoneProp").style.backgroundImage="url("+assetUrl(CUSTOMER_ART["shop-communications-v1"])+")";document.getElementById("shopComputerProp").style.backgroundImage="url("+assetUrl(CUSTOMER_ART["shop-communications-v1"])+")";document.getElementById("shopPhoneProp").onclick=()=>{customerChannel="shop_phone";playSfx("phone_answer");renderCustomer();};document.getElementById("shopComputerProp").onclick=()=>{customerChannel="jobline_email";playSfx("terminal_wake");renderCustomer();};
let lastNearSprite=null;function checkNear(){const p=nearStation();if(p&&p.sprite!==lastNearSprite){const m=MSG[p.sprite];if(m)say(m[0],m[1]);if(p.sprite==="chalkboard")mission("chalkboard");}lastNearSprite=p?.sprite||null;updateGuide();}
function cancelMove(){if(moveTimer)clearInterval(moveTimer);moveTimer=null;moveTarget=null;P.running=false;}
function move(dx,dy,fromPath=false,run=false){if(!fromPath)cancelMove();const nx=P.x+dx,ny=P.y+dy;P.facing=dx<0?"left":dx>0?"right":dy<0?"up":"down";P.running=!!run;P.moveDuration=P.running?82:145;
  if(!blocked(nx,ny)){P.fromX=P.rx;P.fromY=P.ry;P.x=nx;P.y=ny;P.step++;P.moveAt=performance.now();cv.dataset.moveResult="moved";cv.dataset.moveSpeed=P.running?"run":"walk";clampCam();checkNear();if(gameStarted&&P.step%8===0)saveGame("POSITION");return true;}P.running=false;cv.dataset.moveResult="blocked";updateGuide();return false;}
function pathToTile(goalX,goalY){if(blocked(goalX,goalY))return[];const q=[[P.x,P.y]],prev=new Map([[P.x+','+P.y,null]]),dirs=[[1,0],[-1,0],[0,1],[0,-1]],goal=goalX+','+goalY;while(q.length){const[x,y]=q.shift(),key=x+','+y;if(key===goal)break;for(const[dX,dY]of dirs){const nx=x+dX,ny=y+dY,k=nx+','+ny;if(!prev.has(k)&&!blocked(nx,ny)){prev.set(k,key);q.push([nx,ny]);}}}if(!prev.has(goal))return[];const path=[];let end=goal;while(prev.get(end)!==null){const[x,y]=end.split(',').map(Number),[px,py]=prev.get(end).split(',').map(Number);path.push([x-px,y-py]);end=prev.get(end);}return path.reverse();}
function pathToStation(sprite){const target=map.placements.find(p=>p.sprite===sprite);if(!target)return[];const goals=new Set(),[tx0,ty0]=target.tile,[fw,fh]=target.footprint;for(let y=ty0-1;y<=ty0+fh;y++)for(let x=tx0-1;x<=tx0+fw;x++){const dx=Math.max(tx0-x,0,x-(tx0+fw-1)),dy=Math.max(ty0-y,0,y-(ty0+fh-1));if(dx+dy<=1&&!blocked(x,y))goals.add(x+','+y);}const q=[[P.x,P.y]],prev=new Map([[P.x+','+P.y,null]]),dirs=[[1,0],[-1,0],[0,1],[0,-1]];let end=null;while(q.length){const [x,y]=q.shift(),key=x+','+y;if(goals.has(key)){end=key;break;}for(const[dX,dY]of dirs){const nx=x+dX,ny=y+dY,k=nx+','+ny;if(!prev.has(k)&&!blocked(nx,ny)){prev.set(k,key);q.push([nx,ny]);}}}if(!end)return[];const path=[];while(prev.get(end)!==null){const [x,y]=end.split(',').map(Number),[px,py]=prev.get(end).split(',').map(Number);path.push([x-px,y-py]);end=prev.get(end);}return path.reverse();}
function followPath(path,openWhenThere=false,run=true){cancelMove();const openTarget=()=>tourActive&&tourPhase===2?renderTourPractice():interact();if(!path.length){if(openWhenThere)openTarget();return;}let i=0,pace=run?82:145;moveTarget={x:P.x+path.reduce((n,d)=>n+d[0],0),y:P.y+path.reduce((n,d)=>n+d[1],0)};moveTimer=setInterval(()=>{if(i>=path.length){cancelMove();if(openWhenThere)setTimeout(openTarget,100);return;}move(path[i][0],path[i][1],true,run);i++;},pace);}
function walkToStation(sprite,openWhenThere=false){const path=pathToStation(sprite),exists=map.placements.some(p=>p.sprite===sprite),orientationOnly=["zach_npc","mission_board"].includes(sprite);if(openWhenThere&&(!exists||orientationOnly)){setTimeout(renderTourPractice,100);return;}followPath(path,openWhenThere);}

/* ================= INTERACT -> TASKS ================= */
const STATION_SFX={nox_terminal:"terminal_wake",saw_t1:"bandsaw_vise_clamp",tool_cart:"tool_drawer_open",presetter_t4:"probe_touch",toolcrib_rfid_t4:"rfid_tool_scan",vmc_t2:"machine_vise_clamp",lathe_cnc_t2:"lathe_chuck_clamp",planning_desk:"planning_paperwork",chalkboard:"chalk_marker",mill_manual_t1:"manual_mill_run",bench_deburr_t1:"deburr_tool",network_node_t3:"network_connect",handoff_terminal_t4:"handoff_confirm",nox_pallet:"pallet_delivery",whiteboard:"mission_board_update",amr_t5:"amr_drive",cobot_t5:"cobot_motion"};
function interact(){
  const worker=nearWorker();if(worker){talkWorker(worker);return;}
  const p=nearStation(); if(!p){cv.dataset.interaction="too-far";say("Move beside a station before using it.","Follow the pulsing objective or click a machine to walk into interaction range.");return;}
  cv.dataset.interaction=p.sprite;
  if(STATION_SFX[p.sprite])playSfx(STATION_SFX[p.sprite]);
  if(tourActive&&tourPhase===2){const stop=SHOP_TOUR.stops[tourIndex];if(p.sprite===stop.sprite){renderTourPractice();return;}say("This is not the assigned training station.","Follow the highlighted route to "+stop.title+".");return;}
  if(p.sprite==="nox_terminal"){openNoxOrder();return;}
  if(p.sprite==="saw_t1"){if(!state.job){say("No traveler, no cut length.","Accept a customer job at planning first.");return;}openSawTask();return;}
  if(p.sprite==="tool_cart"||p.sprite==="presetter_t4"){openToolTask();return;}
  if(p.sprite==="vmc_t2"){
    if(!state.rawStockReady){say("The vise is empty — raw stock has not been cut.","Cut the blank at the BANDSAW first.");return;}
    if(!state.toolReady||state.toolsSet.length<3){say("The setup sheet calls for three gauged tools.","Finish the full tool kit at the TOOL CART.");return;}
    openVmcTask();return;}
  if(p.sprite==="lathe_cnc_t2"){openOverlay("CNC LATHE — EQUIPMENT VIEW","Inspect the workholding, stock, turret, tailstock, and control before setup.");showEquipmentView("lathe-open-v1");setTimeout(()=>playSfx("lathe_turret_index"),700);tctrl.innerHTML='<button id="latheClose" class="grn">INSPECTION COMPLETE ▸</button>';document.getElementById("latheClose").onclick=closeOverlay;tz("ZACH: Chuck pressure, stickout, tool clearance. A lathe remembers every shortcut.");return;}
  if(p.sprite==="planning_desk"){const contract=state.pendingContract;state.job=contract?JOBS.find(j=>j.id===contract.jobFamily):JOBS[jobIdx%JOBS.length];state.rawStockReady=false;state.toolReady=false;state.toolsSet=[];if(contract){state.job={...state.job,contract};state.pendingContract=null;const r=state.contracts.find(x=>x.offerId===contract.id);if(r)r.status="released to production";}
    say(contract?contract.customer+" work order released: "+state.job.card:"Job card: "+state.job.card,contract?"JobLine traveler created for "+contract.quantity+" pieces. First operation: cut the raw blank.":"First operation: cut the raw blank at the bandsaw.");mission("planning_desk");updateGuide();return;}
  checkNear();
}

/* ================= TASK OVERLAY CORE ================= */
const task=document.getElementById("task"), tscene=document.getElementById("tscene"), tx=tscene.getContext("2d");
const tctrl=document.getElementById("tcontrols");
let taskAnim=null, hintI=0, attempts=0, curHints=[],cycleTimers=[],machineMotionMode=null;
let activeTaskTutorialId=null;
function contextTaskTutorialId(){if(task.classList.contains("open")&&activeTaskTutorialId)return activeTaskTutorialId;if(!state.materialOrders.length)return"order_material";if(!state.job)return"accept_job";if(!state.rawStockReady)return"cut_raw_stock";if(!state.tool)return"select_primary_tool";if(!state.stickout)return"set_stickout";if(!state.toolReady)return"complete_tool_kit";return"prove_gcode";}
function showTaskGuide(id=contextTaskTutorialId()){const guide=PRODUCTION_TASK_TUTORIALS.find(x=>x.id===id)||PRODUCTION_TASK_TUTORIALS[0];document.getElementById("taskGuideTitle").textContent=guide.id.replaceAll("_"," ").toUpperCase()+" · "+guide.location;document.getElementById("taskGuideStatus").textContent="VALIDATION STATUS: "+guide.status.toUpperCase();const im=document.getElementById("taskGuideImage");im.src=guide.imageType==="equipment"?assetUrl(EQUIPMENT_VIEWS[guide.image]):guide.imageType==="nox"?assetUrl(NOX_MATERIALS_ART):assetUrl(SPRITES[guide.image]);document.getElementById("taskGuideNarration").textContent="ZACH: "+guide.text;document.getElementById("taskGuidePrereq").textContent=guide.prerequisites;document.getElementById("taskGuideSteps").innerHTML=guide.instructions.map(x=>"<li>"+x+"</li>").join("");document.getElementById("taskGuideSuccess").textContent=guide.success;document.getElementById("taskGuideModal").dataset.taskTutorial=guide.id;document.getElementById("taskGuideModal").classList.add("open");playZach(guide.voice);}
document.getElementById("btaskguide").onclick=()=>showTaskGuide();document.getElementById("taskGuideButton").onclick=()=>showTaskGuide();document.getElementById("taskGuideClose").onclick=()=>document.getElementById("taskGuideModal").classList.remove("open");
function tz(msg){document.getElementById("tztext").textContent=msg;}
function openOverlay(title,jobCard){document.getElementById("ttitle").textContent=title;
  if(learnerMode&&tourMandatory&&String(jobCard).startsWith("HANDS-ON STOP")){const beginner=[2,3,5],step=Math.max(0,beginner.indexOf(tourIndex))+1;jobCard=String(jobCard).replace(/HANDS-ON STOP \d+ OF \d+/,"STARTER STEP "+step+" OF 3");}document.getElementById("tjob").textContent=jobCard;
  document.getElementById("tclose").style.display=tourActive&&tourMandatory?"none":"";task.classList.add("open"); hintI=0; attempts=0;}
function clearCycleTimers(){cycleTimers.forEach(clearTimeout);cycleTimers=[];}
function closeOverlay(){task.classList.remove("open");cancelAnimationFrame(taskAnim);taskAnim=null;clearCycleTimers();stopSfxLoop();machineMotionMode=null;tctrl.innerHTML="";updateGuide();}
function showEquipmentView(id){const im=document.getElementById("tview");im.src=assetUrl(EQUIPMENT_VIEWS[id]);im.style.display="block";tscene.style.display="none";}
function showNoxMaterialsView(){const im=document.getElementById("tview");im.src=assetUrl(NOX_MATERIALS_ART);im.style.display="block";tscene.style.display="none";}
function showTaskCanvas(){document.getElementById("tview").style.display="none";tscene.style.display="block";}
const ONBOARDING_PRACTICE={
 tour_overview:[{prompt:"Put the production route in the correct starting order.",options:["Material → preparation → machining","Machining → material → planning","Inspection → machining → material"],correct:0,success:"Material must be verified before preparation or machining."},{prompt:"A step is unclear. What should you use?",options:["Guess and continue","The pulsing objective or Go To & Open","Skip the operation"],correct:1,success:"Routing help keeps the work in sequence."}],
 tour_planning:[{prompt:"What do you check before accepting the work?",options:["Only the payout","Material, dimensions, tolerance, quantity, and due date","Only the customer name"],correct:1,success:"You read the traveler before promising the job."},{prompt:"The required material is unavailable. What is the correct decision?",options:["Accept silently","Substitute any alloy","Confirm supply or renegotiate before release"],correct:2,success:"A responsible promise begins with real capacity and supply."}],
 tour_material:[{prompt:"The traveler calls for 6061-T6. Which stock passes?",options:["6061-T6 with dimensions and certification","Any aluminum without paperwork","Unmarked remnant stock"],correct:0,success:"Alloy, size, and certification match the traveler."},{prompt:"Before confirming the purchase, what else must you verify?",options:["Color only","Cost, quantity, dimensions, and delivery","Machine spindle speed"],correct:1,success:"The material order now supports the job and the cash plan."}],
 tour_saw:[{prompt:"The finished blank is 4.00 inches. Which saw target preserves finish allowance?",options:["3.90 in","4.00 in exactly","4.25 in as specified by the traveler"],correct:2,success:"The blank retains controlled finishing allowance."},{prompt:"Before cutting, what must be secured?",options:["Stock in the vise with hands clear","Only the coolant hose","The finished-part inspection report"],correct:0,success:"The stock is clamped and the cut zone is clear."}],
 tour_tooling:[{prompt:"Choose the primary tool for a square pocket with a flat floor.",options:["Twist drill","Flat end mill","Ball end mill"],correct:1,success:"A flat end mill supports the specified pocket floor."},{prompt:"How should tool stickout be set?",options:["As long as possible","Only long enough for depth and clearance","Flush inside the holder"],correct:1,success:"Controlled stickout reduces chatter and breakage."}],
 tour_vmc:[{prompt:"Which sequence is safe before Cycle Start?",options:["Run first, then inspect","Blank → workholding → tools → offset → program check","Open the door and start the spindle"],correct:1,success:"The setup is proven before motion begins."},{prompt:"Which codes command clockwise spindle and coolant on?",options:["M03 and M08","M05 and M09","G00 and G80"],correct:0,success:"M03 starts clockwise rotation; M08 enables coolant."}],
 tour_shop_class:[{prompt:"A result does not make sense. What should you do here?",options:["Repeat it unchanged","Review the principle, calculate, and answer the check","Hide the result"],correct:1,success:"Understanding the cause prevents repeated process errors."},{prompt:"What is the purpose of speeds-and-feeds math?",options:["Decoration","Protect the tool, machine, and surface result","Replace inspection"],correct:1,success:"The math connects material, tool, speed, feed, and outcome."}],
 tour_manual_mill:[{prompt:"Before manual spindle motion, what comes first?",options:["Secure workholding and establish position","Maximum feed","Hold the part by hand"],correct:0,success:"The part is restrained and the reference is understood."},{prompt:"This station is orientation-only today. What can you still validate?",options:["Safe stop, controls, workholding, and clearance","A completed production batch","Automatic inspection results"],correct:0,success:"You completed a real safety and setup inspection without pretending production is enabled."}],
 tour_deburr:[{prompt:"Which result passes the edge check?",options:["Sharp burr remains","Consistent edge break without feature damage","Rounded critical dimension"],correct:1,success:"The edge is safe while the finished feature remains protected."},{prompt:"Before handing the part to inspection, what do you verify?",options:["Every required edge is safe and clean","Only one corner","The machine is still running"],correct:0,success:"The part is safe to handle and ready for measurement."}],
 tour_lathe:[{prompt:"Excessive stock stickout creates what risk?",options:["Better rigidity","Deflection and unsafe rotation","Automatic tool correction"],correct:1,success:"You identified unsafe stickout before spindle motion."},{prompt:"What must clear the chuck and stock?",options:["Turret, tools, and planned motion","Only the coolant","The operator's paperwork"],correct:0,success:"Chuck pressure, stickout, turret, and tool clearance pass inspection."}],
 tour_mtconnect:[{prompt:"Which machine state should the node distinguish?",options:["Running, idle, faulted, and stopped","Only paint color","Employee payroll"],correct:0,success:"Machine states can now support honest uptime analysis."},{prompt:"A machine reports running but produces no cycles. What should you do?",options:["Ignore it","Investigate the signal and actual process state","Increase the reported count"],correct:1,success:"Connected data must agree with physical production."}],
 tour_handoff:[{prompt:"What must a useful shift handoff contain?",options:["Job status, completed work, next action, and concerns","Only the employee name","A blank note"],correct:0,success:"The next operator receives enough context to act safely."},{prompt:"An unusual vibration occurred. Where does it go?",options:["Nowhere","In the handoff concern with the affected operation","Only in memory"],correct:1,success:"The abnormal condition is preserved for the next decision."}],
 tour_receiving:[{prompt:"The packing slip says 6061-T6, but the stock has no certification. What do you do?",options:["Send it to the saw","Quarantine it and resolve the missing record","Relabel it yourself"],correct:1,success:"Unverified stock is contained before production."},{prompt:"What four items must agree?",options:["Alloy, dimensions, quantity, and certification","Color, price, weather, and shift","Spindle, coolant, probe, and vise"],correct:0,success:"The incoming material matches the purchase and traveler."}],
 tour_missions:[{prompt:"What does the mission board show?",options:["Current objective, requirements, progress, and quality gate","Only total coins","Only the map name"],correct:0,success:"You can read the current chapter and its achievable next step."},{prompt:"When should a chapter advance?",options:["Whenever the player clicks Next","After required jobs, operations, and quality gates are proven","Before the first task"],correct:1,success:"Progression follows demonstrated capability."}]
};
let tourIndex=0,tourPhase=0,tourPracticeStep=0,tourActive=false,tourMandatory=false;const completedTourStops=new Set();
function tourImage(stop){return stop.imageType==="equipment"?assetUrl(EQUIPMENT_VIEWS[stop.image]):stop.imageType==="nox"?assetUrl(NOX_MATERIALS_ART):assetUrl(SPRITES[stop.image]);}
function renderTourStop(){const stop=SHOP_TOUR.stops[tourIndex],walk=STATION_WALKTHROUGHS[stop.id],overview=tourPhase===0,detail=overview?{label:"WHY THIS STATION MATTERS",text:stop.text,voice:stop.voice}:{label:"OPERATING STEPS",text:walk.text,voice:walk.voice};tourActive=true;openOverlay(stop.title,`HANDS-ON STOP ${tourIndex+1} OF ${SHOP_TOUR.stops.length} · ${detail.label} · ${stop.location}`);task.dataset.tourStop=stop.id;task.dataset.tourPhase=overview?"overview":"walkthrough";document.getElementById("tview").src=tourImage(stop);document.getElementById("tview").style.display="block";tscene.style.display="none";curHints=[stop.operation,walk.text];tz("ZACH: "+detail.text);playZach(detail.voice);tctrl.innerHTML='<div class="ttl">WHERE: '+stop.location+'</div><div style="color:#fff">'+detail.label+': '+(overview?stop.operation:walk.text)+'</div><div class="hint">'+(stop.status==="orientation"?'ORIENTATION-ONLY PRODUCTION · HANDS-ON SAFETY/SETUP CHECK REQUIRED':'PLAYABLE TRAINING · STATION ACTION REQUIRED')+'</div><button id="tourPrev" '+(tourIndex===0&&tourPhase===0?'disabled':'')+'>◀ PREVIOUS</button><button id="tourNext" class="grn">'+(overview?'SHOW OPERATING STEPS ▶':'GO TO STATION & PRACTICE ▶')+'</button>'+(tourMandatory?'':'<button id="tourSkip">EXIT REPLAY</button>');document.getElementById("tourPrev").onclick=()=>{if(tourPhase===1)tourPhase=0;else{tourIndex=Math.max(0,tourIndex-1);tourPhase=1;}renderTourStop();};document.getElementById("tourNext").onclick=()=>{if(tourPhase===0){tourPhase=1;renderTourStop();return;}tourPhase=2;tourPracticeStep=0;closeOverlay();cv.dataset.tourTarget=stop.sprite;walkToStation(stop.sprite,true);};const skip=document.getElementById("tourSkip");if(skip)skip.onclick=finishTour;}
function renderTourPractice(){const stop=SHOP_TOUR.stops[tourIndex],steps=ONBOARDING_PRACTICE[stop.id],step=steps[tourPracticeStep];openOverlay(stop.title,`AT STATION · REQUIRED ACTION ${tourPracticeStep+1} OF ${steps.length}`);task.dataset.tourPhase="practice";document.getElementById("tview").src=tourImage(stop);document.getElementById("tview").style.display="block";tscene.style.display="none";tz("ZACH: "+kidExplain(step.prompt));curHints=[step.success];tctrl.innerHTML='<div class="ttl">TRY ONE SMALL STEP · '+kidExplain(step.prompt)+'</div><div id="practiceChoices">'+step.options.map((option,index)=>'<button class="practiceChoice" data-choice="'+index+'">'+String.fromCharCode(65+index)+' · '+kidExplain(option)+'</button>').join('')+'</div><div id="practiceValidation" aria-live="polite">PICK THE SAFEST ANSWER · YOU CAN TRY AGAIN</div>';document.querySelectorAll(".practiceChoice").forEach(button=>button.onclick=()=>{const choice=Number(button.dataset.choice),status=document.getElementById("practiceValidation");if(choice!==step.correct){button.classList.add("bad");if(learnerMode)document.querySelector('.practiceChoice[data-choice="'+step.correct+'"]').classList.add("answerHint");status.textContent=learnerMode?"GOOD TRY · THE GOLD OUTLINE SHOWS THE SAFEST ANSWER":"NOT YET · REVIEW THE OPERATING STEPS AND TRY AGAIN";playSfx("terminal_error");tz("ZACH: Good try. "+kidExplain(STATION_WALKTHROUGHS[stop.id].text));return;}button.classList.add("ok");document.querySelectorAll(".practiceChoice").forEach(x=>x.disabled=true);status.textContent="GREAT JOB · "+kidExplain(step.success);playSfx("terminal_confirm");setTimeout(()=>{tourPracticeStep++;if(tourPracticeStep<steps.length){renderTourPractice();return;}completeTourStop();},550);});}
function completeTourStop(){const stop=SHOP_TOUR.stops[tourIndex];completedTourStops.add(stop.id);task.dataset.completedTourStops=[...completedTourStops].join(",");say(stop.title+" training complete.",kidExplain(ONBOARDING_PRACTICE[stop.id].at(-1).success));if(tourMandatory&&learnerMode){const beginner=[2,3,5],position=beginner.indexOf(tourIndex);if(position===beginner.length-1){finishTour();return;}tourIndex=beginner[position+1];}else{if(tourIndex===SHOP_TOUR.stops.length-1){finishTour();return;}tourIndex++;}tourPhase=0;tourPracticeStep=0;renderTourStop();}
function startShopTour(reset=false,mandatory=false){if(reset){tourIndex=mandatory&&learnerMode?2:0;tourPhase=0;tourPracticeStep=0;completedTourStops.clear();}tourMandatory=mandatory;renderTourStop();}
function finishTour(){const required=tourMandatory&&learnerMode?3:SHOP_TOUR.stops.length;if(tourMandatory&&completedTourStops.size<required){tz("ZACH: Finish these "+required+" small practice stops first.");return;}tourActive=false;tourMandatory=false;task.dataset.tourStop="complete";task.dataset.tourPhase="complete";closeOverlay();cv.dataset.tourTarget="";say("Starter training complete.",learnerMode?"You practiced metal, cutting, and the CNC. I will teach each new station when you need it.":"You operated or inspected every Garage Bay station. Your first production step is the NOX material terminal.","zach_response_next_step");updateGuide();}
document.getElementById("btour").onclick=()=>startShopTour(true,false);
tctrl.addEventListener("click",()=>{if(gameStarted&&tourActive)setTimeout(()=>saveGame("ONBOARDING"),0);});
document.getElementById("tclose").onclick=()=>{if(tourActive&&tourMandatory){tz("ZACH: Complete this hands-on onboarding stop before opening production.");return;}closeOverlay();};
document.getElementById("askzach").onclick=()=>{ if(!curHints.length)return;
  tz("ZACH: "+curHints[Math.min(hintI,curHints.length-1)]);playZach(hintI===0?"zach_response_explain_why":"zach_response_slow_down");hintI++; attempts+=0.5; };
function grade(){ return attempts<=0?"A":attempts<=1?"B":attempts<=2?"C":attempts<=3?"D":"F"; }

const NOX_CATALOG=[
  {sku:"6061-T6-PLATE",name:'6061-T6 ALUMINUM PLATE',detail:'12 × 12 × 0.75 in · cert included',cost:420},
  {sku:"7075-T651-PLATE",name:'7075-T651 ALUMINUM PLATE',detail:'12 × 12 × 0.75 in · aerospace cert',cost:690},
  {sku:"6061-T6-BAR",name:'6061-T6 ALUMINUM BAR',detail:'2 × 2 × 24 in · cert included',cost:285}
];
function openNoxOrder(){
  activeTaskTutorialId="order_material";
  playZach("zach_order_stock");
  openOverlay("NOX METALS — MATERIAL ORDERING","Select production-ready stock for the active job. Landed price includes next-day delivery.");
  showNoxMaterialsView();curHints=["Match the alloy on the job card before comparing price.","Job 1042 calls for 6061-T6. Certs preserve material traceability.","Order 6061-T6 plate for the current job."];
  const rows=NOX_CATALOG.map((m,i)=>'<button class="toolbtn noxOrder '+(learnerMode&&m.sku==="6061-T6-PLATE"?'answerHint':'')+'" data-i="'+i+'"><b>'+m.name+'</b><span>'+m.detail+'</span><strong>'+m.cost+' COINS</strong></button>').join('');
  tctrl.innerHTML='<div class="ttl">LIVE DETROIT INVENTORY</div><div class="tools">'+rows+'</div><div id="noxStatus" class="hint">ALLOY · CONDITION · DIMENSIONS · QUANTITY</div>';
  document.querySelectorAll('.noxOrder').forEach(b=>b.onclick=()=>placeNoxOrder(NOX_CATALOG[Number(b.dataset.i)]));
  tz("ZACH: Raw stock is the first operation. Buy the right alloy, condition, and size — then protect the cert chain.");
}
function placeNoxOrder(item){
  const status=document.getElementById("noxStatus");
  if(item.sku!=="6061-T6-PLATE"){status.textContent=learnerMode?"NOT THIS ONE · THIS JOB NEEDS THE FLAT 6061-T6 PLATE":"MATERIAL MISMATCH · JOB REQUIRES 6061-T6 PLATE";playSfx("terminal_error");tz("ZACH: This is not the right shape. Pick the flat 6061-T6 plate card.");return;}
  if(coins<item.cost){status.textContent="ORDER DECLINED — NOT ENOUGH COINS";return;}
  playSfx("terminal_confirm");setTimeout(()=>playSfx("pallet_delivery",{volume:.75}),500);coins-=item.cost;addCoins(0);state.materialOrders.push({sku:item.sku,qty:1,status:"NEXT-DAY DELIVERY"});
  status.textContent="ORDER CONFIRMED · "+item.sku+" · NEXT-DAY DELIVERY TO RECEIVING";
  say("NOX order confirmed: "+item.name,"Material will arrive at receiving with certification.");
  updateGuide();if(!storySeen("nox_delivery"))setTimeout(()=>{closeOverlay();showStorySequence("nox_delivery");},450);
}

/* draw a tool: kind twist|end|ball, at x, holderY; stick = inches beyond holder; ppi px/inch */
function drawTool(g,kind,x0,holderBot,stick,ppi,shank=10){
  const len=stick*ppi;
  g.fillStyle="#9aa1ab"; g.fillRect(x0-shank/2,holderBot,shank,len-8);
  g.strokeStyle="#000"; g.strokeRect(x0-shank/2,holderBot,shank,len-8);
  const tipY=holderBot+len;
  g.fillStyle="#c4c9d0";
  if(kind==="twist"){ // fluted + point
    for(let i=0;i<Math.floor((len-14)/6);i++){g.strokeStyle="#6e747f";
      g.beginPath();g.moveTo(x0-shank/2+1,holderBot+6+i*6);g.lineTo(x0+shank/2-1,holderBot+10+i*6);g.stroke();}
    g.fillStyle="#c4c9d0";g.beginPath();g.moveTo(x0-shank/2,tipY-8);g.lineTo(x0+shank/2,tipY-8);g.lineTo(x0,tipY);g.closePath();g.fill();g.strokeStyle="#000";g.stroke();
  }else if(kind==="end"){ // flat with flutes
    g.fillRect(x0-shank/2,tipY-10,shank,10);
    g.strokeStyle="#6e747f";for(let i=0;i<3;i++){g.beginPath();g.moveTo(x0-shank/2+2+i*3,tipY-10);g.lineTo(x0-shank/2+2+i*3,tipY);g.stroke();}
    g.strokeStyle="#000";g.strokeRect(x0-shank/2,tipY-10,shank,10);
  }else{ // ball
    g.beginPath();g.arc(x0,tipY-shank/2,shank/2,0,Math.PI*2);g.fill();g.strokeStyle="#000";g.stroke();
    g.strokeStyle="#6e747f";g.beginPath();g.arc(x0,tipY-shank/2,shank/4,0,Math.PI*2);g.stroke();
  }
}
function drawHolder(g,x0,y0){ g.fillStyle="#2b2f36"; g.fillRect(x0-16,y0-28,32,20);
  g.fillStyle="#4a4f58"; g.fillRect(x0-12,y0-8,24,8);
  g.strokeStyle="#000"; g.strokeRect(x0-16,y0-28,32,20); g.strokeRect(x0-12,y0-8,24,8);
  g.fillStyle="#e8b93b"; g.fillRect(x0-16,y0-28,32,3); }

/* ================= RAW STOCK: BANDSAW ================= */
function openSawTask(){const J=state.job;openOverlay("BANDSAW — CUT RAW STOCK",J.card);showTaskCanvas();playSfx("bandsaw_power_on");curHints=["Saw blanks need finish allowance.","Set the stop to the traveler length, not the final print length.","The gold line is the required saw length: "+J.stockLength.toFixed(2)+' inches.'];
playZach("zach_cut_stock");
  tz("ZACH: Every CNC job starts as raw stock. Set the stop, cut the blank, and leave the finish allowance.");
  tctrl.innerHTML='<label>COARSE MATERIAL STOP <input type="range" id="cutLength" min="3" max="6.5" step="0.01" value="3"></label><label>FINE LENGTH <input type="number" id="cutLengthFine" min="3" max="6.5" step="0.01" value="3.00"> in</label><span id="cutLengthValue" style="color:#e8b93b;font-size:22px"></span><div class="hint">'+(learnerMode?'Move the marker to the gold line. Close is okay!':'Approach with the slider, then set hundredths with the fine control.')+'</div>'+(learnerMode?'<button id="kidSetCut">1 · MOVE TO GOLD LINE</button>':'')+'<button id="cutStock" class="grn">'+(learnerMode?'2 · CUT THE METAL':'CLAMP & CUT ▸')+'</button>';
  const sl=document.getElementById("cutLength"),fine=document.getElementById("cutLengthFine"),value=document.getElementById("cutLengthValue");if(learnerMode){sl.min=J.stockLength-.4;sl.max=J.stockLength+.4;sl.value=J.stockLength-.2;fine.min=sl.min;fine.max=sl.max;fine.value=sl.value;}const render=source=>{if(source===sl)fine.value=sl.value;else sl.value=fine.value;let v=Number(fine.value);if(learnerMode&&Math.abs(v-J.stockLength)<=.12){v=J.stockLength;sl.value=v;fine.value=v;}value.textContent=v.toFixed(2)+' in · '+(learnerMode?(Math.abs(v-J.stockLength)<=.12?'IN THE GREEN ZONE':'MOVE TOWARD THE GOLD LINE'):'ERROR '+Math.abs(v-J.stockLength).toFixed(2)+' in');drawSawCut(v,J.stockLength);};sl.oninput=()=>render(sl);fine.oninput=()=>render(fine);render(sl);
  const kidSetCut=document.getElementById("kidSetCut");if(kidSetCut)kidSetCut.onclick=()=>{sl.value=J.stockLength;render(sl);playSfx("terminal_confirm");tz("ZACH: Gold line matched. Extra metal gives the CNC room to finish the part.");};
  document.getElementById("cutStock").onclick=()=>{const v=Number(sl.value);if(Math.abs(v-J.stockLength)>.08){attempts++;tz("ZACH: That blank misses the traveler length. Reset the stop before cutting.");return;}playSfx("bandsaw_cut");state.rawStockReady=true;drawSawCut(v,J.stockLength,true);tz("ZACH: Blank cut, labeled, and ready for CNC setup.");setTimeout(()=>{playSfx("bandsaw_power_off");closeOverlay();say("Raw blank ready at "+v.toFixed(2)+' inches.',"Next: gauge the full CNC tool kit.");},700);};}
function drawSawCut(v,target,done=false){tx.fillStyle="#0e1826";tx.fillRect(0,0,480,260);tx.fillStyle="#b9c2cb";tx.fillRect(75,105,330,58);tx.fillStyle="#76818c";tx.fillRect(75+v/6.5*330,95,8,78);const x=75+target/6.5*330;tx.strokeStyle="#e8b93b";tx.lineWidth=3;tx.beginPath();tx.moveTo(x,70);tx.lineTo(x,190);tx.stroke();tx.fillStyle="#e8b93b";tx.font="20px VT323, monospace";tx.fillText("CUT "+target.toFixed(2)+' in',x-42,55);tx.fillStyle=done?"#3fd08a":"#9aa1ab";tx.fillText(done?"✔ STOCK READY":"SET THE MATERIAL STOP",150,225);}

/* ================= TASK 1: TOOL SETUP ================= */
function openToolTask(){
  activeTaskTutorialId=null;
  playZach("zach_tool_setup");
  if(!state.job){state.job=JOBS[jobIdx%JOBS.length];}
  const J=state.job;
  openOverlay("TOOL SETUP — "+(J.gtitle),J.card);showEquipmentView("tool-cart-open-v1");
  curHints=J.hints.tool;
  tz("ZACH: Read the job card. Which tool does this work want? Pick one.");
  // step 1: pick tool
  tctrl.innerHTML="";
  [["twist","TWIST DRILL"],["end","END MILL"],["ball","BALL MILL"]].forEach(([kind,label])=>{
    const b=document.createElement("div");b.className="toolbtn";
    b.innerHTML=toolArt(kind)+'<span>'+label+'</span><small>'+(kind==="twist"?'POINTED · HOLES':kind==="end"?'FLAT · POCKETS':'ROUND · CONTOURS')+'</small>';
    if(learnerMode&&kind===J.tool)b.classList.add("answerHint");b.onclick=()=>{ if(kind===J.tool){playSfx("toolholder_load");state.tool=kind;stepStickout();}
      else{attempts++;tz("ZACH: "+wrongToolMsg(kind,J));playZach("zach_response_try_again");} };
    tctrl.appendChild(b);
  });
  sceneToolIdle();
}
function wrongToolMsg(kind,J){
  if(J.tool==="twist")return kind==="end"?"An end mill won't self-center in a hole. Drills drill.":"A ball nose in a hole? That's a bad day. Drills drill.";
  if(J.tool==="end")return kind==="twist"?"A drill can't cut sideways — pockets need an end mill.":"Ball nose leaves a round floor. This pocket wants FLAT.";
  return kind==="twist"?"A drill on a 3D surface? Nope. Curves want a ball nose.":"Flat end mill will stair-step that dome. Ball nose blends it.";
}
function sceneToolIdle(){
  cancelAnimationFrame(taskAnim);
  tx.fillStyle="#0e1826";tx.fillRect(0,0,480,260);
  tx.fillStyle="#e8b93b";tx.font="20px VT323, monospace";
  tx.fillText("PICK THE TOOL FOR THE JOB",130,40);
  tx.fillStyle="#9aa1ab";tx.font="16px VT323, monospace";
  tx.fillText("wrong picks cost grade — ASK ZACH if unsure",110,64);
}
function stepStickout(){
  showTaskCanvas();
  const J=state.job; curHints=J.hints.stick; hintI=0;
  tz("ZACH: Right tool. Now stick it out to the GOLD LINE — "+J.stickWhy+".");
  tctrl.innerHTML='<div class="toolMeasure">'+toolArt(J.tool)+'<div><b>MEASURE HOLDER FACE TO CUTTING TIP</b><br><span class="hint">Short for rigidity · long enough for clearance</span></div></div><label>COARSE PROTRUSION <input type="range" id="stick" min="0.5" max="2.2" step="0.01" value="0.6"></label><label>FINE PROTRUSION <input type="number" id="stickFine" min="0.5" max="2.2" step="0.01" value="0.60"> in</label>'+
    '<span id="stickval" style="color:#e8b93b;font-size:22px">0.60"</span>'+
    (learnerMode?'<button id="kidSetStick">1 · SLIDE TIP TO GOLD LINE</button>':'')+'<button id="lockin" class="grn">'+(learnerMode?'2 · LOCK SAFE LENGTH':'LOCK IN ▸')+'</button>';
const sl=document.getElementById("stick"),fine=document.getElementById("stickFine"), sv=document.getElementById("stickval");if(learnerMode){sl.value=J.stickTarget-.1;fine.value=sl.value;}
  const render=source=>{if(source===sl)fine.value=sl.value;else sl.value=fine.value;const v=parseFloat(fine.value);sv.textContent=v.toFixed(2)+'" · TARGET '+J.stickTarget.toFixed(2)+'"';sceneStick(v);};
  sl.oninput=()=>render(sl);fine.oninput=()=>render(fine);render(sl);
  const kidSetStick=document.getElementById("kidSetStick");if(kidSetStick)kidSetStick.onclick=()=>{sl.value=J.stickTarget;render(sl);playSfx("terminal_confirm");tz("ZACH: The tip is on the gold line. Short tools stay steadier.");};
  document.getElementById("lockin").onclick=()=>{
    const v=parseFloat(fine.value), J=state.job;
    if(Math.abs(v-J.stickTarget)<=J.stickTol){
      playSfx("tool_torque_click");state.stickout=v;state.toolsSet=["PRIMARY"];
      tz("ZACH: Primary tool is on the line. A CNC setup needs more than one tool — finish the kit.");
      sceneStick(v,true);
      setTimeout(stepToolKit,500);
    }else{
      attempts++;
      tz("ZACH: "+(v<J.stickTarget?"Too short — you'll bury the holder before you hit depth.":"Hanging way out — that'll chatter or snap. Bring it to the line."));
    }
  };
}
function sceneStick(v,locked=false){
  const J=state.job, ppi=90, x0=200, hb=70;
  tx.fillStyle="#0e1826";tx.fillRect(0,0,480,260);
  // gauge column
  tx.strokeStyle="#4a4f58";tx.beginPath();tx.moveTo(320,40);tx.lineTo(320,250);tx.stroke();
  for(let i=0;i<=8;i++){const y=hb+i*0.25*ppi;if(y>250)break;
    tx.strokeStyle="#4a4f58";tx.beginPath();tx.moveTo(312,y);tx.lineTo(328,y);tx.stroke();
    tx.fillStyle="#6e747f";tx.font="13px VT323, monospace";tx.fillText((i*0.25).toFixed(2),334,y+4);}
  // tolerance band + target line
  const ty=hb+J.stickTarget*ppi, tol=J.stickTol*ppi;
  tx.fillStyle="rgba(232,185,59,.15)";tx.fillRect(120,ty-tol,240,tol*2);
  tx.strokeStyle="#e8b93b";tx.lineWidth=2;tx.beginPath();tx.moveTo(120,ty);tx.lineTo(360,ty);tx.stroke();tx.lineWidth=1;
  tx.fillStyle="#e8b93b";tx.font="15px VT323, monospace";tx.fillText("SET TIP TO LINE — "+J.stickTarget.toFixed(2)+'"',126,ty-tol-6);
  drawHolder(tx,x0,hb); drawTool(tx,J.tool,x0,hb,v,ppi);
  if(locked){tx.fillStyle="#3fd08a";tx.font="22px VT323, monospace";tx.fillText("✔ GAUGED",70,120);}
}
function stepToolKit(){showEquipmentView("tool-cart-open-v1");curHints=["The probe establishes where the stock is.","The chamfer tool breaks sharp edges before inspection.","A complete kit is primary cutter, probe, and chamfer tool."];tz("ZACH: Gauge the probe and chamfer tool before loading the machine.");
  tctrl.innerHTML='<div class="ttl">SETUP SHEET · 1 / 3 TOOLS READY</div><button class="kitTool" data-tool="PROBE">'+toolArt("probe")+'<span>GAUGE T90 · TOUCH PROBE</span></button><button class="kitTool" data-tool="CHAMFER">'+toolArt("chamfer")+'<span>GAUGE T4 · CHAMFER MILL</span></button><button id="installKit" class="grn" disabled>INSTALL 3-TOOL KIT ▸</button>';
  document.querySelectorAll(".kitTool").forEach(b=>b.onclick=()=>{playSfx(b.dataset.tool==="PROBE"?"probe_touch":"toolholder_load");if(!state.toolsSet.includes(b.dataset.tool))state.toolsSet.push(b.dataset.tool);b.textContent="✔ "+b.textContent;b.disabled=true;document.querySelector("#tcontrols .ttl").textContent="SETUP SHEET · "+state.toolsSet.length+" / 3 TOOLS READY";document.getElementById("installKit").disabled=state.toolsSet.length<3;});
  if(learnerMode){const helper=document.createElement("button");helper.id="kidLoadKit";helper.textContent="1 · LOAD THE TWO GLOWING TOOLS";document.getElementById("installKit").before(helper);document.getElementById("installKit").textContent="2 · INSTALL TOOL KIT";helper.onclick=()=>{document.querySelectorAll(".kitTool:not(:disabled)").forEach(button=>button.click());helper.disabled=true;tz("ZACH: Probe finds the part. Chamfer tool smooths sharp edges. The kit is ready.");};}
  document.getElementById("installKit").onclick=()=>{state.toolReady=true;mission("task_tool");closeOverlay();say("Three tools gauged and installed: cutter, probe, chamfer.","Stock and tool kit are ready. Open the VMC for the G/M-code proof.");};}

/* ================= TASK 2: VMC G/M + RUN ================= */
function machineFlag(){let flag=document.getElementById("machineFlag");if(!flag){flag=document.createElement("button");flag.id="machineFlag";flag.style.cssText="position:absolute;right:10px;top:10px;z-index:12;border:3px solid #e8b93b;background:#081018;color:#fff;padding:8px;display:none";document.getElementById("cwrap").append(flag);flag.onclick=()=>walkToStation("vmc_t2",true);}return flag;}
function refreshMachineRun(){const run=state.machineRun,flag=machineFlag();if(!run){flag.style.display="none";return;}if(run.status==="running"&&Date.now()>=run.endAt){run.status="inspection";stopSfxLoop();playSfx("coolant_off");setTimeout(()=>playSfx("spindle_stop"),300);saveGame("MACHINE COMPLETE");}flag.style.display="block";if(run.status==="inspection"){flag.textContent="⚑ VMC COMPLETE · INSPECT PART";flag.style.borderColor="#3fd08a";}else{flag.textContent="⚙ VMC RUNNING · "+Math.max(0,Math.ceil((run.endAt-Date.now())/1000))+"s REMAINING";flag.style.borderColor="#e8b93b";}cv.dataset.machineStatus=run.status;}
function startAutonomousRun(J){const duration=learnerMode?12000:Math.max(8000,20000-(equipmentState().vmc-1)*4000);state.machineRun={jobId:J.id,status:"running",startedAt:Date.now(),endAt:Date.now()+duration};playSfx("cnc_door_close");setTimeout(()=>playSfx("spindle_start"),500);setTimeout(()=>playSfx(J.tool==="twist"?"drill_cut_aluminum":J.tool==="ball"?"ball_mill_cut_aluminum":"end_mill_cut_aluminum",{loop:true}),1400);closeOverlay();say("Verified VMC cycle running autonomously.","The station flag shows remaining time. Return anytime to review it; inspection is still required before shipment.");refreshMachineRun();saveGame("AUTO CYCLE");}
setInterval(refreshMachineRun,500);
function openVmcTask(){
  if(!state.machineRun&&Date.now()<(state.equipmentCooldownUntil||0)){const seconds=Math.ceil((state.equipmentCooldownUntil-Date.now())/1000);openOverlay("VMC — COOLING DOWN","This machine cannot start another job yet.");showEquipmentView("vmc-open-v1");tz("ZACH: Machines need recovery time too. Use these "+seconds+" seconds to plan, inspect, buy capacity, or help another station.");tctrl.innerHTML='<div class="ttl">AVAILABLE IN '+seconds+' SECONDS</div><button id="cooldownClose">USE ANOTHER STATION</button>';document.getElementById("cooldownClose").onclick=closeOverlay;return;}
  if(state.machineRun){const run=state.machineRun,J=state.job||JOBS.find(x=>x.id===run.jobId);refreshMachineRun();if(run.status==="inspection"){openOverlay("VMC — CHECK THE FINISHED PART","The machine is done, but the job is not shipped until you check it.");showEquipmentView("vmc-open-v1");tz("ZACH: Compare the finished part with the job picture. Check the shape, holes, and clean edges.");tctrl.innerHTML='<button id="inspectPart" class="grn">COMPARE PART TO JOB PICTURE</button><div id="inspectionStatus" class="hint">PART NOT SHIPPED YET</div>';document.getElementById("inspectPart").onclick=()=>{document.getElementById("inspectionStatus").textContent="✔ SHAPE · HOLES · EDGES MATCH";document.getElementById("inspectPart").textContent="APPROVE CHECK & SHIP PART";document.getElementById("inspectPart").onclick=()=>{state.machineRun=null;showTaskCanvas();finishRun(J);};};return;}openOverlay("VMC — AUTONOMOUS CYCLE",J.card);showEquipmentView("vmc-open-v1");tz("ZACH: The verified cycle is running. Stay clear of the enclosure and review the remaining time.");tctrl.innerHTML='<div class="ttl">CYCLE IN PROGRESS · CHECK THE FLOOR FLAG FOR TIME</div><button id="leaveRunning" class="grn">RETURN TO FLOOR · KEEP RUNNING</button>';document.getElementById("leaveRunning").onclick=closeOverlay;return;}
  activeTaskTutorialId="prove_gcode";
  playZach("zach_gcode_intro");
  const J=state.job; curHints=J.hints.g; hintI=0;
  openOverlay("VMC — "+J.gtitle, J.card);showEquipmentView("vmc-open-v1");playSfx("machine_power_on",{volume:.7});
  const guided=state.jobsShipped<2,autonomyReady=learnerMode||state.jobsShipped>=3&&gradeAverage()>=4;
  tz(guided?"ZACH: We will read each blank together. Choose A, B, C, or D, then study what the code controls.":"ZACH: Program's missing three words. Offset, spindle, coolant. Fill them and press CYCLE START.");
  // program with inputs
  const choices={o:[["53","A · G53 MACHINE COORDINATE"],["54","B · G54 WORK OFFSET"],["90","C · G90 ABSOLUTE MODE"],["00","D · G00 RAPID"]],s:[["03","A · M03 SPINDLE CLOCKWISE"],["04","B · M04 COUNTERCLOCKWISE"],["05","C · M05 SPINDLE STOP"],["06","D · M06 TOOL CHANGE"]],c:[["08","A · M08 COOLANT ON"],["09","B · M09 COOLANT OFF"],["30","C · M30 END PROGRAM"],["01","D · M01 OPTIONAL STOP"]]};
  let progHtml='<div class="gcode">';
  for(const ln of J.prog){
    progHtml+=ln.replace(/{{(\w)}}/g,(m,k)=>guided?'<select data-b="'+k+'"><option value="">CHOOSE A–D</option>'+choices[k].map(choice=>'<option value="'+choice[0]+'">'+choice[1]+'</option>').join('')+'</select>':'<input maxlength="2" data-b="'+k+'" placeholder="__">')+"<br>";
  }
  progHtml+="</div>";
  tctrl.innerHTML=progHtml+
    '<div class="gline"><button id="cycst" class="grn">▶ CYCLE START</button>'+(autonomyReady?'<button id="verifiedSetup">LOAD VERIFIED REPEAT SETUP</button><button id="autonomousRun">START AUTO CYCLE & RETURN TO FLOOR</button>':'')+'</div><details open><summary class="ttl">TRUE G & M CODE · READ THE MODAL SEQUENCE</summary><div class="hint"><b>G54</b> selects the stored part origin · <b>M03</b> commands spindle clockwise · <b>M08</b> turns flood coolant on.<br>M06 TOOL CHANGE → G90 ABSOLUTE → G54 WORK OFFSET → G00 RAPID CLEAR → M03 SPINDLE CW → G43 H TOOL LENGTH → M08 COOLANT → G01/G81 CONTROLLED CUT → G80 CANCEL CYCLE → G00 RETRACT → M09 COOLANT OFF → M05 SPINDLE STOP → G28 RETURN → M30 END/REWIND</div></details>';
  sceneVmcIdle();
  if(learnerMode){const helper=document.createElement("button");helper.id="kidLoadCodes";helper.textContent="1 · LEARN & LOAD THE 3 CODES";document.getElementById("cycst").before(helper);document.getElementById("autonomousRun").textContent="2 · START MACHINE & RETURN TO SHOP";helper.onclick=()=>{document.querySelectorAll('[data-b]').forEach(field=>{field.value=J.blanks[field.dataset.b].ans[0];field.dispatchEvent(new Event("change"));});helper.disabled=true;tz("ZACH: G54 finds the part. M03 spins right. M08 turns coolant on.");playSfx("terminal_confirm");};}
  const refreshCycleReady=()=>{const fields=[...document.querySelectorAll('#tcontrols [data-b]')],ready=fields.length===3&&fields.every(field=>J.blanks[field.dataset.b].ans.includes(field.value.trim()));const auto=document.getElementById("autonomousRun");if(auto)auto.disabled=!ready;task.dataset.programReady=String(ready);};document.querySelectorAll('#tcontrols [data-b]').forEach(field=>field.addEventListener("change",refreshCycleReady));refreshCycleReady();
  document.getElementById("cycst").onclick=()=>{
    let allOk=true;
    document.querySelectorAll('#tcontrols [data-b]').forEach(inp=>{
      const key=inp.dataset.b, val=inp.value.trim();
      const ok=J.blanks[key].ans.includes(val);
      inp.className=ok?"ok":"bad"; if(!ok)allOk=false;
    });
    if(!allOk){attempts++;tz("ZACH: Red ones are wrong. "+(attempts>=2?"Hit ASK ZACH if you're stuck.":"Think: where's the part, spin it, cool it."));return;}
    tz("ZACH: Program's good. Doors closed. Watch the path — this is your setup running.");
    runAnim(J);
  };
  const verified=document.getElementById("verifiedSetup");if(verified)verified.onclick=()=>{document.querySelectorAll('[data-b]').forEach(inp=>inp.value=J.blanks[inp.dataset.b].ans[0]);tz("ZACH: This repeat setup earned assisted loading through three good jobs. You still verify stock, workholding, offsets, tools, and first article.");document.getElementById("cycst").click();};
  const auto=document.getElementById("autonomousRun");if(auto)auto.onclick=()=>{if(auto.disabled)return;startAutonomousRun(J);};
}
function sceneVmcIdle(){
  if(document.getElementById("tview").style.display==="block")return;
  cancelAnimationFrame(taskAnim);
  tx.fillStyle="#0a0d12";tx.fillRect(0,0,480,260);
  tx.fillStyle="#e8b93b";tx.font="20px VT323, monospace";tx.fillText("MACHINE READY — FILL THE BLANKS",96,130);
}
/* animated run scenes */
function runAnim(J){
  showTaskCanvas();
  cancelAnimationFrame(taskAnim);
  clearCycleTimers();machineMotionMode=null;tscene.dataset.motionCode="STARTUP";
  playSfx("cnc_door_close");
  cycleTimers.push(setTimeout(()=>playSfx("cnc_tool_change"),700));
  cycleTimers.push(setTimeout(()=>playSfx("spindle_start"),1800));
  cycleTimers.push(setTimeout(()=>playSfx("coolant_on"),4200));
  let t=0; const chips=[];
  const pathPts=buildPath(J);
  let seg=0, segT=0, cut=[];
  const cuttingSfx=J.tool==="twist"?"drill_cut_aluminum":J.tool==="ball"?"ball_mill_cut_aluminum":"end_mill_cut_aluminum";
  function setMachineMotion(mode){if(machineMotionMode===mode)return;machineMotionMode=mode;tscene.dataset.motionCode=mode;if(mode==="G0")playSfx("cnc_rapid_traverse",{loop:true});else playSfx(cuttingSfx,{loop:true});}
  function frame_(){
    t++;
    tx.fillStyle="#0a0d12";tx.fillRect(0,0,480,260);
    // machine interior
    tx.fillStyle="#14161c";tx.fillRect(0,0,480,30);
    tx.fillStyle="#e8b93b";tx.font="15px VT323, monospace";tx.fillText(J.gtitle+" — CYCLE RUNNING",10,20);
    tx.fillStyle=(t>>4)%2?"#d0433f":"#7a2a28";tx.fillRect(455,8,14,14);tx.strokeStyle="#000";tx.strokeRect(455,8,14,14);
    const nextPoint=pathPts[Math.min(seg+1,pathPts.length-1)];setMachineMotion(nextPoint?.rapid?"G0":"G1");
    if(J.anim==="drill"||J.anim==="dome"){ sideScene(J,pathPts,seg,segT,cut,chips,t); }
    else { topScene(J,pathPts,seg,segT,cut,chips,t); }
    // advance along path
    segT+=nextPoint?.rapid?0.10:0.035;
    if(segT>=1){segT=0;seg++;}
    if(seg>=pathPts.length-1){ finishRun(J); return; }
    taskAnim=requestAnimationFrame(frame_);
  }
  cycleTimers.push(setTimeout(()=>{tscene.dataset.motionCode="G0";taskAnim=requestAnimationFrame(frame_);},5000));
}
function lerp(a,b,t){return a+(b-a)*t;}
function buildPath(J){
  if(J.anim==="drill"){
    const pts=[{x:60,y:50}]; const holes=[120,200,280,360]; const topY=70,botY=190;
    let first=true;
    for(const hx of holes){
      pts.push({x:hx,y:60,rapid:true});
      pts.push({x:hx,y:botY});           // feed down
      pts.push({x:hx,y:topY,rapid:true}); // retract
      first=false;
    }
    pts.push({x:400,y:50,rapid:true});
    return pts;
  }
  if(J.anim==="pocket"){
    const pts=[{x:70,y:40},{x:240,y:130,rapid:true}];
    let l=170,r=310,tp=90,b=170;
    for(let i=0;i<3;i++){
      pts.push({x:l,y:tp});pts.push({x:r,y:tp});pts.push({x:r,y:b});pts.push({x:l,y:b});pts.push({x:l,y:tp});
      l+=18;r-=18;tp+=14;b-=14;
    }
    pts.push({x:240,y:40,rapid:true});
    return pts;
  }
  // dome: side-view arc passes
  const pts=[{x:60,y:40},{x:80,y:60,rapid:true}];
  for(let p=0;p<3;p++){
    const dir=p%2===0;
    for(let i=0;i<=20;i++){
      const xx=dir? 100+i*14 : 380-i*14;
      const yy=190-Math.sqrt(Math.max(0,1-Math.pow((xx-240)/140,2)))*70 - p*0;
      pts.push({x:xx,y:yy-6+p*3});
    }
  }
  pts.push({x:400,y:50,rapid:true});
  return pts;
}
function sideScene(J,pts,seg,segT,cut,chips,t){
  // stock
  tx.fillStyle="#8a6a48";tx.fillRect(80,150,320,70);tx.strokeStyle="#000";tx.strokeRect(80,150,320,70);
  tx.fillStyle="#b08a5e";tx.fillRect(80,150,320,6);
  if(J.anim==="dome"){ // dome profile carved
    tx.fillStyle="#0a0d12";tx.beginPath();tx.moveTo(100,150);
    for(let xx=100;xx<=380;xx+=8){const yy=150+ (30-Math.sqrt(Math.max(0,1-Math.pow((xx-240)/140,2)))*30);tx.lineTo(xx,Math.min(yy, 150+ (cutProgress(cut,xx)?0:0)+ 999)); }
    // simpler: draw carved dome as arc mask progressive
    tx.closePath();
  }
  const a=pts[seg]||pts[pts.length-1], b=pts[Math.min(seg+1,pts.length-1)];
  const X=lerp(a.x,b.x,segT), Y=lerp(a.y,b.y,segT);
  // carved holes record
  if(!b.rapid){cut.push({x:X,y:Y});}
  tx.fillStyle="#0a0d12";
  for(const c of cut){ if(J.anim==="drill"){tx.fillRect(c.x-5,150,10,Math.max(0,c.y-150));} else {tx.fillRect(c.x-6,c.y,12,220-c.y);} }
  // coolant + chips while feeding
  if(!b.rapid&&Y>140){
    for(let i=0;i<2;i++)chips.push({x:X+(Math.random()*20-10),y:Y,vy:-2-Math.random()*2,vx:Math.random()*3-1.5,c:Math.random()<.5?"#b08a5e":"#4a9fd4"});
  }
  chips.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=0.25;tx.fillStyle=p.c;tx.fillRect(p.x,p.y,3,3);});
  while(chips.length>60)chips.shift();
  // spindle + tool
  tx.fillStyle="#4a4f58";tx.fillRect(X-10,0,20,Math.max(10,Y-70));tx.strokeStyle="#000";tx.strokeRect(X-10,0,20,Math.max(10,Y-70));
  drawHolder(tx,X,Y-42); drawTool(tx,state.tool||J.tool,X,Y-42,0.5,84,8);
  // path preview
  tx.strokeStyle="rgba(63,208,138,.35)";tx.setLineDash([4,4]);tx.beginPath();
  pts.forEach((p,i)=>{i?tx.lineTo(p.x,p.y):tx.moveTo(p.x,p.y);});tx.stroke();tx.setLineDash([]);
}
function cutProgress(){return 0;}
function topScene(J,pts,seg,segT,cut,chips,t){
  // stock top view
  tx.fillStyle="#b08a5e";tx.fillRect(140,70,200,120);tx.strokeStyle="#000";tx.strokeRect(140,70,200,120);
  const a=pts[seg]||pts[pts.length-1], b=pts[Math.min(seg+1,pts.length-1)];
  const X=lerp(a.x,b.x,segT), Y=lerp(a.y,b.y,segT);
  if(!b.rapid)cut.push({x:X,y:Y});
  // cut trail (pocket floor)
  tx.fillStyle="#7a5a3a";
  for(const c of cut){tx.beginPath();tx.arc(c.x,c.y,9,0,Math.PI*2);tx.fill();}
  tx.strokeStyle="rgba(63,208,138,.4)";tx.setLineDash([4,4]);tx.beginPath();
  pts.forEach((p,i)=>{i?tx.lineTo(p.x,p.y):tx.moveTo(p.x,p.y);});tx.stroke();tx.setLineDash([]);
  if(!b.rapid){for(let i=0;i<2;i++)chips.push({x:X+(Math.random()*16-8),y:Y+(Math.random()*16-8),vx:Math.random()*4-2,vy:Math.random()*4-2,c:"#d6b484"});}
  chips.forEach(p=>{p.x+=p.vx;p.y+=p.vy;tx.fillStyle=p.c;tx.fillRect(p.x,p.y,2,2);});
  while(chips.length>80)chips.shift();
  // tool (circle w/ rotation tick)
  tx.fillStyle="#c4c9d0";tx.beginPath();tx.arc(X,Y,8,0,Math.PI*2);tx.fill();tx.strokeStyle="#000";tx.stroke();
  tx.strokeStyle="#6e747f";tx.beginPath();tx.moveTo(X,Y);tx.lineTo(X+Math.cos(t/2)*8,Y+Math.sin(t/2)*8);tx.stroke();
}
function finishRun(J){
  activeTaskTutorialId="review_quality_result";
  cancelAnimationFrame(taskAnim);
  clearCycleTimers();stopSfxLoop();machineMotionMode=null;tscene.dataset.motionCode="M30";playSfx("coolant_off");setTimeout(()=>playSfx("spindle_stop"),350);setTimeout(()=>playSfx("cnc_door_open"),3500);
  const g=grade();
  tx.fillStyle="rgba(5,6,9,.6)";tx.fillRect(0,0,480,260);
  tx.fillStyle="#e8b93b";tx.font="34px VT323, monospace";tx.fillText("PART COMPLETE",130,110);
  tx.font="28px VT323, monospace";tx.fillText("GRADE: "+g,190,150);
  const basePay=g==="A"?600:g==="B"?450:g==="C"?300:150,pay=J.contract?Math.round(J.contract.quantity*J.contract.unitPrice*({A:1,B:.9,C:.75,D:.5,F:.25}[g])):basePay;
  addCoins(pay); mission("task_vmc");state.equipmentCooldownUntil=Date.now()+Math.max(3000,10000-(equipmentState().vmc-1)*2500);state.toolReady=false;state.rawStockReady=false;state.toolsSet=[];state.jobsShipped++;state.grades.push({A:5,B:4,C:3,D:2,F:1}[g]);awardFounderXp(60+({A:5,B:4,C:3,D:2,F:1}[g])*10);if(J.contract){const r=state.contracts.find(x=>x.offerId===J.contract.id);if(r)r.status="delivered · grade "+g;state.reputation=Math.max(0,Math.min(100,state.reputation+({A:6,B:4,C:2,D:-1,F:-4}[g])));}jobIdx++; state.job=null;updateGuide();
  tz("ZACH: "+(g==="A"?"First-try clean. THAT'S craftsmanship — "+pay+" coins.":g<="C"?"Shipped at grade "+g+". Review the misses at Shop Class and the next one's an A. +"+pay+" coins.":"It shipped, barely. Shop Class. Tonight. +"+pay+" coins."));
  tctrl.innerHTML='<button id="tdone" class="grn">BACK TO THE FLOOR ▸</button>';
  document.getElementById("tdone").onclick=()=>{playSfx("machine_power_off",{volume:.7});closeOverlay();
    say("Grade "+g+" recorded. "+state.jobsShipped+" of "+CHAPTER_ONE_TARGET+" Garage jobs shipped.",state.jobsShipped<CHAPTER_ONE_TARGET?"Return to planning for the next customer order.":"Garage mastery proven. Prepare to move your company.");
    const advance=()=>{if(state.jobsShipped>=CHAPTER_ONE_TARGET&&gradeAverage()>=3)showExpansion();};if(!storySeen("first_verified_article"))showStorySequence("first_verified_article",advance);else advance();};
}

/* ================= INPUT ================= */
document.addEventListener("keydown",e=>{
  if(e.key==="F3"){e.preventDefault();debugOpen=!debugOpen;document.getElementById("debugHud").classList.toggle("open",debugOpen);return;}
  if(e.key==="Escape"&&gameStarted&&!task.classList.contains("open")){e.preventDefault();togglePause();return;}
  if(!accepts("keyboard"))return;
  if(task.classList.contains("open")){ if(e.key==="Escape")closeOverlay(); return; }
  const k=e.key.toLowerCase();
  if(["arrowup","w"].includes(k)){e.preventDefault();move(0,-1,false,e.shiftKey);}
  if(["arrowdown","s"].includes(k)){e.preventDefault();move(0,1,false,e.shiftKey);}
  if(["arrowleft","a"].includes(k)){e.preventDefault();move(-1,0,false,e.shiftKey);}
  if(["arrowright","d"].includes(k)){e.preventDefault();move(1,0,false,e.shiftKey);}
  if(k==="e"||k==="enter"||k===" "){e.preventDefault();interact();}
});
const DIRS={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]};
let holdT=null,touchRun=false;
document.querySelectorAll("#pad b[data-d]").forEach(el=>{
  const d=el.dataset.d;
  const fire=()=>{ if(!accepts("touch")||task.classList.contains("open"))return;
    if(d==="act"){interact();}else if(d==="run"){touchRun=!touchRun;el.classList.toggle("on",touchRun);el.textContent=touchRun?"RUN!":"RUN";}else {const[dx,dy]=DIRS[d];move(dx,dy,false,touchRun);} };
  const start_=(e)=>{e.preventDefault();fire();clearInterval(holdT);if(d!=="act"&&d!=="run")holdT=setInterval(fire,touchRun?95:170);};
  const stop_=()=>clearInterval(holdT);
  el.addEventListener("touchstart",start_,{passive:false});
  el.addEventListener("touchend",stop_); el.addEventListener("touchcancel",stop_);
  el.addEventListener("mousedown",start_); el.addEventListener("mouseup",stop_); el.addEventListener("mouseleave",stop_);
});
/* Standard Gamepad mapping: Xbox left stick/D-pad, A interact, B back, Menu controls. */
let gpLastMove=0,gpPrev=[];
let gpFounderIndex=0;
addEventListener("gamepadconnected",e=>document.getElementById("gamepadState").textContent="GAMEPAD: "+e.gamepad.id);
addEventListener("gamepaddisconnected",()=>document.getElementById("gamepadState").textContent="GAMEPAD: NOT CONNECTED");
function pollGamepad(now){
  const gp=[...(navigator.getGamepads?.()||[])].find(Boolean);
  if(gp&&(inputMode==="auto"||inputMode==="gamepad")){
    document.getElementById("gamepadState").textContent="GAMEPAD: "+gp.id;
    const pressed=i=>!!gp.buttons[i]?.pressed,edge=i=>pressed(i)&&!gpPrev[i];
    const founderScreenOpen=document.getElementById("preFounder").classList.contains("closed")&&!document.getElementById("titleScreen").classList.contains("closed");
    if(founderScreenOpen&&(edge(14)||edge(12)||edge(15)||edge(13))){const cards=[...document.querySelectorAll(".avatarChoice")],back=edge(14)||edge(12);gpFounderIndex=(cards.findIndex(x=>x.dataset.avatar===selectedAvatar)+(back?-1:1)+cards.length)%cards.length;selectFounderButton(cards[gpFounderIndex]);cards[gpFounderIndex].focus();}
    if(!paused&&edge(0)){if(!document.getElementById("preFounder").classList.contains("closed"))document.getElementById("preFounderNext").click();else if(founderScreenOpen)document.getElementById("newGame").click();else if(!task.classList.contains("open"))interact();}
    if(edge(1)){if(task.classList.contains("open"))closeOverlay();else document.getElementById("connect").classList.remove("open");}
    if(edge(9)){if(gameStarted)togglePause();else document.getElementById("connect").classList.toggle("open");}
    const sprint=pressed(7)||pressed(10);
    if(!paused&&now-gpLastMove>(sprint?92:165)&&!task.classList.contains("open")&&document.getElementById("titleScreen").classList.contains("closed")&&document.getElementById("intro").classList.contains("closed")){
      const x=gp.axes[0]||0,y=gp.axes[1]||0;let d=null;
      if(pressed(12)||y<-.45)d=[0,-1];else if(pressed(13)||y>.45)d=[0,1];else if(pressed(14)||x<-.45)d=[-1,0];else if(pressed(15)||x>.45)d=[1,0];
      if(d){move(d[0],d[1],false,sprint);gpLastMove=now;}
    }
    gpPrev=gp.buttons.map(b=>b.pressed);
  }else gpPrev=[];
  requestAnimationFrame(pollGamepad);
}
requestAnimationFrame(pollGamepad);
cv.addEventListener("click",e=>{
  if(!accepts("touch")&&!accepts("keyboard"))return;
  const r=cv.getBoundingClientRect();
  const txx=cam.x+Math.floor((e.clientX-r.left)/(r.width/VW));
  const tyy=cam.y+Math.floor((e.clientY-r.top)/(r.height/VH));
  const worker=workers.find(w=>Math.abs(w.x-txx)<=1&&Math.abs(w.y-tyy)<=1);if(worker){const d=Math.abs(worker.x-P.x)+Math.abs(worker.y-P.y);if(d<=2)talkWorker(worker);else{const goals=[[worker.x-1,worker.y],[worker.x+1,worker.y],[worker.x,worker.y-1],[worker.x,worker.y+1]].filter(q=>!blocked(q[0],q[1]));if(goals.length)followPath(pathToTile(goals[0][0],goals[0][1]));say('Walking to '+worker.candidate.name+'.','Click the employee or press E when you arrive.');}return;}
  const equipment=map.placements.find(p=>txx>=p.tile[0]&&txx<p.tile[0]+p.footprint[0]&&tyy>=p.tile[1]&&tyy<p.tile[1]+p.footprint[1]);
  if(equipment){walkToStation(equipment.sprite,true);return;}
  if(!blocked(txx,tyy))followPath(pathToTile(txx,tyy));
});
document.getElementById("b1").onclick=()=>{setMap("bay_01");sel("b1");};
document.getElementById("b2").onclick=()=>{if(!document.getElementById("b2").disabled){setMap("bay_02");sel("b2");}};
function sel(id){for(const b of["b1","b2"])document.getElementById(b).classList.toggle("on",b===id);}
document.getElementById("brun").onclick=function(){running=!running;this.textContent=running?"⏸ STOP":"▶ RUN";this.classList.toggle("on",running);};
document.getElementById("bover").onclick=function(){overlays=!overlays;this.classList.toggle("on",overlays);};
function start(){renderFounderPreview();setTitleArt();setStoryArt("opening");setMap("bay_01");let lastFrame=0,lastDebug=0,frames=0,fps=0;const animate=now=>{frames++;if(now-lastDebug>=1000){fps=Math.round(frames*1000/(now-lastDebug||1000));frames=0;lastDebug=now;if(debugOpen){const mem=performance.memory?Math.round(performance.memory.usedJSHeapSize/1048576)+" MB":"n/a";document.getElementById("debugHud").textContent=`REIND DEV HUD · F3\nFPS ${fps} · HEAP ${mem}\nMAP ${map?.id||"none"} · POS ${P.x},${P.y}\nSPRITES ${Object.keys(IMG).length}/${Object.keys(SPRITES).length}\nINPUT ${inputMode} · PAUSED ${paused}\nJOBS ${state.jobsShipped} · TEAM ${workers.length}\nSAVE ${cv.dataset.saveStatus||"none"}`;}}if(!paused){const t=Math.min(1,(now-P.moveAt)/P.moveDuration),ease=1-Math.pow(1-t,3);P.rx=P.fromX+(P.x-P.fromX)*ease;P.ry=P.fromY+(P.y-P.fromY)*ease;if(now-lastFrame>130){frame++;lastFrame=now;}if(!task.classList.contains("open"))draw();}requestAnimationFrame(animate);};requestAnimationFrame(animate);}
const runtimeErrors=[];function recordRuntimeError(kind,message){runtimeErrors.push({at:new Date().toISOString(),kind,message:String(message).slice(0,500)});while(runtimeErrors.length>20)runtimeErrors.shift();cv.dataset.runtimeErrors=runtimeErrors.length;if(debugOpen)document.getElementById("debugHud").textContent+="\nLAST ERROR "+kind+": "+String(message).slice(0,100)}addEventListener("error",e=>recordRuntimeError("ERROR",e.message));addEventListener("unhandledrejection",e=>recordRuntimeError("PROMISE",e.reason));
</script></body></html>
"""
html = (html.replace("__SPRITES__", json.dumps(sprites))
            .replace("__ATLAS__", json.dumps(atlas))
            .replace("__MAPS__", json.dumps(maps))
            .replace("__OPENING__", opening)
            .replace("__EXPANSION__", expansion)
            .replace("__STORY_SCENES__", json.dumps(story_scenes))
            .replace("__SCENE_MANIFEST__", json.dumps(scene_manifest))
            .replace("__STORY_PRODUCTION__", json.dumps(story_production))
            .replace("__PRE_FOUNDER_ART__", json.dumps(pre_founder_art))
            .replace("__SHOP_TOUR__", json.dumps(shop_tour))
            .replace("__STATION_WALKTHROUGHS__", json.dumps(station_walkthroughs))
            .replace("__PRODUCTION_TASK_TUTORIALS__", json.dumps(production_task_tutorials))
            .replace("__CHAPTER_PROGRESSION__", json.dumps(chapter_progression))
            .replace("__FACILITIES__", json.dumps(facilities))
            .replace("__TITLE_ART__", title_art)
            .replace("__NOX_MATERIALS_ART__", nox_materials_art)
            .replace("__EQUIPMENT_VIEWS__", json.dumps(equipment_views))
            .replace("__EQUIPMENT_MARKET__", json.dumps(equipment_market))
            .replace("__TOOL_ART__", json.dumps(tool_art))
            .replace("__HIRE_ROSTER__", json.dumps(hire_roster))
            .replace("__HIRE_IMAGES__", json.dumps(hire_images))
            .replace("__FOUNDER_PROFILES__", json.dumps(founder_profiles))
            .replace("__WORKFORCE_CONVERSATIONS__", json.dumps(workforce_conversations))
            .replace("__MENTOR__", json.dumps(mentor_conversations))
            .replace("__CUSTOMER_CONTRACTS__", json.dumps(customer_contracts))
            .replace("__CUSTOMER_ART__", json.dumps(customer_art))
            .replace("__REUSABLE_ZACH__", json.dumps(reusable_voice))
            .replace("__ZACH_VOICE__", json.dumps(zach_voice))
            .replace("__SFX_AUDIO__", json.dumps(sfx_audio)))
for broken, clean in {"Â·":"·","â€”":"—","â–¶":"▶","â—€":"◀","âœ”":"✔","â˜‘":"☑","â˜":"☐","â€œ":"“","â€":"”","Ã—":"×","Ã˜":"Ø","â†’":"→"}.items():
    html = html.replace(broken, clean)
for broken, clean in {r"\u00c2\u00b7":r"\u00b7",r"\u00e2\u20ac\u201d":r"\u2014",r"\u00c3\u02dc":r"\u00d8",r"\u00c3\u2014":r"\u00d7"}.items():
    html = html.replace(broken, clean)
out = os.path.join(ROOT, "apps", "wecr8-info", "prototypes", "shop-floor-viewer.html")
with open(out, "w", encoding="utf-8") as f: f.write(html)
print("wrote", out, len(html)//1024, "KB")
