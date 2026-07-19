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
#task{position:fixed;inset:0;background:rgba(5,6,9,.92);z-index:50;display:none;
flex-direction:column;align-items:center;justify-content:flex-start;gap:8px;padding:10px;overflow:auto;}
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
  body{gap:6px;padding:6px;} h1{font-size:20px;}
  #layout{display:flex;flex-direction:column;align-items:center;gap:6px;width:100%;}
  #sideL,#sideR{display:none;} #mini{display:flex;}
  #dlg{width:100%;padding:6px 8px;} #dport{width:56px;height:56px;} #dtext{font-size:19px;}
  .hint{display:none;} #bar button{font-size:15px;padding:2px 8px;}
}
@media (pointer:coarse){ #pad{display:grid;} body{padding-bottom:196px;} }
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
#campaign{position:fixed;inset:0;background:rgba(5,6,9,.96);z-index:155;display:none;place-items:center;padding:12px;overflow:auto}#campaign.open{display:grid}#campaignPanel{width:min(1120px,97vw)}#campaignGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}.chapterCard{background:#0a1017;border:3px solid #434b55;padding:11px;min-height:190px}.chapterCard.playable{border-color:var(--green)}.chapterCard.development{border-color:var(--gold)}.chapterCard.locked{opacity:.72}.chapterCard h3{color:#fff;font-size:25px}.chapterStatus{display:inline-block;padding:2px 7px;background:#161c23;color:#aeb7c0}.playable .chapterStatus{background:#123a29;color:var(--green)}.development .chapterStatus{background:#433613;color:var(--gold)}.chapterFacility{color:var(--sky);font-size:21px}.chapterTime{color:#fff}.chapterGate{font-size:17px;color:#aeb7c0;margin-top:6px}@media(max-width:760px){#campaignGrid{grid-template-columns:1fr}.chapterCard{min-height:0}}
#customers{position:fixed;inset:0;background:rgba(5,6,9,.96);z-index:160;display:none;place-items:center;padding:12px;overflow:auto}#customers.open{display:grid}#customerPanel{width:min(1080px,97vw)}#customerTabs,#customerActions{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}.customerGrid{display:grid;grid-template-columns:220px 1fr;gap:12px}.customerPortrait{height:250px;background-repeat:no-repeat;background-size:400% 100%;background-color:#081019;border:3px solid var(--gold)}.companyImage{height:235px;background-repeat:no-repeat;background-size:400% 100%;border:3px solid var(--sky)}.customerMeta{color:var(--green)}.rfq{background:#08151d;border:2px solid var(--sky);padding:10px;margin-top:8px}.rfq ul{margin:5px 0 5px 22px}.mailBadge{display:inline-block;background:var(--alert);color:#fff;padding:0 6px;border-radius:8px}.contractAccepted{color:var(--green);font-size:23px}.customerCard.locked{opacity:.65}.commProps{display:flex;gap:8px}.commProp{width:100px;height:76px;background-repeat:no-repeat;background-size:200% 100%;border:2px solid var(--green);image-rendering:pixelated}.commProp.phone{background-position:0 50%}.commProp.computer{background-position:100% 50%}@media(max-width:700px){.customerGrid{grid-template-columns:1fr}.customerPortrait{height:220px}.companyImage{height:180px}}
@media(max-width:600px){#introCopy{position:relative;left:auto;right:auto;bottom:auto;}#introTitle{font-size:27px}#introText{font-size:19px}}
</style></head><body>
<div id="preFounder"><div id="preFounderCard"><img id="preFounderArt" alt="Zach introduces the manufacturing journey before founder selection"><div id="preFounderCopy"><div id="preFounderKicker"></div><div id="preFounderText"></div><button id="preFounderNext" class="grn">CONTINUE ▸</button></div></div></div>
<div id="titleScreen"><div id="titleShade"></div><div id="titleUi"><div id="gameLogo">REINDUSTRIALIZE</div><div id="tagline">CREATE YOUR FOUNDER. BUILD AN INDUSTRIAL POWERHOUSE.</div><div class="founderSetup"><div class="hint">CHOOSE YOUR FOUNDER</div><div class="avatarChoices"><button class="avatarChoice selected" data-avatar="av_m_01"><canvas width="64" height="96"></canvas><span>MALE 01</span></button><button class="avatarChoice" data-avatar="av_m_founder_02_hd"><canvas width="64" height="96"></canvas><span>MALE 02</span></button><button class="avatarChoice" data-avatar="av_f_founder_hd"><canvas width="64" height="96"></canvas><span>FEMALE 01</span></button><button class="avatarChoice" data-avatar="av_f_founder_02_hd"><canvas width="64" height="96"></canvas><span>FEMALE 02</span></button><button class="avatarChoice" data-avatar="av_m_blonde_hd"><canvas width="64" height="96"></canvas><span>BLONDE M</span></button><button class="avatarChoice" data-avatar="av_f_blonde_hd"><canvas width="64" height="96"></canvas><span>BLONDE F</span></button><button class="avatarChoice" data-avatar="av_m_middle_eastern_hd"><canvas width="64" height="96"></canvas><span>M.E. M</span></button><button class="avatarChoice" data-avatar="av_f_middle_eastern_hd"><canvas width="64" height="96"></canvas><span>M.E. F</span></button><button class="avatarChoice" data-avatar="av_m_indian_hd"><canvas width="64" height="96"></canvas><span>INDIAN M</span></button><button class="avatarChoice" data-avatar="av_f_indian_hd"><canvas width="64" height="96"></canvas><span>INDIAN F</span></button></div><input id="founderName" maxlength="24" value="ALEX MORGAN" aria-label="Name your founder"><div class="hint">FOUNDER NAME</div></div><input id="companyName" maxlength="32" value="AMERICAN FORGE WORKS" aria-label="Name your manufacturing company"><div class="hint">MANUFACTURING COMPANY NAME</div><div class="controlSelect"><div class="hint">CHOOSE HOW YOU WILL PLAY</div><div class="controlChoices"><button class="controlChoice selected" data-control="auto"><b>✦ AUTO</b><span>Use any connected control</span></button><button class="controlChoice" data-control="keyboard"><b>⌨ KEYBOARD</b><span>WASD / arrows · Shift · E</span></button><button class="controlChoice" data-control="gamepad"><b>🎮 XBOX</b><span>Stick / D-pad · RT · A</span></button><button class="controlChoice" data-control="phone"><b>▦ PHONE QR</b><span>Scan to pair your phone</span></button></div><div id="selectedControlStatus" aria-live="polite">ALL INPUTS ACTIVE</div></div><div class="titleMenu"><button id="newGame" class="grn">▶ LAUNCH COMPANY</button><button id="continueGame" disabled>CONTINUE</button><button id="titleSettings">ADVANCED CONTROLS & PHONE QR</button><button id="credits">CREDITS</button></div><div class="build">FIRST PLAYABLE · BUILD 0.7</div></div></div>
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
      <div style="color:#9aa1ab;font-size:18px">▸ PROFILE<br>&nbsp;&nbsp;SKILLS<br>&nbsp;&nbsp;PROJECTS<br>&nbsp;&nbsp;GEAR<br>&nbsp;&nbsp;OPTIONS</div>
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
      <button id="tclose">✕ LEAVE</button></span></div>
    <div id="tjob"></div>
    <div id="tsceneWrap"><img id="tview" alt="Opened equipment view"><canvas id="tscene" width="480" height="260"></canvas></div>
    <div id="tcontrols"></div>
    <div id="tzach"><div id="tzport"><img id="tzportimg"></div><div id="tztext"></div></div>
  </div>
</div>

<div id="taskGuideModal"><div id="taskGuidePanel" class="panel"><div class="ttl" id="taskGuideTitle"></div><div id="taskGuideStatus"></div><img id="taskGuideImage" alt="Active production task tutorial"><div id="taskGuideNarration"></div><div><b>PREREQUISITES:</b> <span id="taskGuidePrereq"></span></div><ol id="taskGuideSteps"></ol><div><b>SUCCESS:</b> <span id="taskGuideSuccess"></span></div><button id="taskGuideClose" class="grn">RETURN TO TASK</button></div></div>
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
const TOOL_ART=__TOOL_ART__;
const HIRE_ROSTER=__HIRE_ROSTER__,HIRE_IMAGES=__HIRE_IMAGES__,FOUNDER_PROFILES=__FOUNDER_PROFILES__,WORKFORCE_CONVERSATIONS=__WORKFORCE_CONVERSATIONS__;const hired=new Set(),workers=[];
const MENTOR=__MENTOR__;
const CUSTOMER_CONTRACTS=__CUSTOMER_CONTRACTS__,CUSTOMER_ART=__CUSTOMER_ART__;
const REUSABLE_ZACH=__REUSABLE_ZACH__;
const ZACH_VOICE=__ZACH_VOICE__;let zachAudio=null,voiceEnabled=localStorage.getItem("reindustrialize.voice")!=="off",voiceVolume=Number(localStorage.getItem("reindustrialize.voiceVolume")||"1");
const SFX_AUDIO=__SFX_AUDIO__;let sfxLoop=null,sfxEnabled=localStorage.getItem("reindustrialize.sfx")!=="off",sfxVolume=Number(localStorage.getItem("reindustrialize.sfxVolume")||"0.7");
let ambienceAudio=null,ambienceId=null,ambienceEnabled=localStorage.getItem("reindustrialize.ambience")!=="off",ambienceVolume=Number(localStorage.getItem("reindustrialize.ambienceVolume")||"0.16");
const assetUrl=(value,mime="image/png")=>value.startsWith("/")?value:"data:"+mime+";base64,"+value;
function playSfx(id,{loop=false,volume=1}={}){if(!sfxEnabled||!SFX_AUDIO[id])return null;const audio=new Audio(assetUrl(SFX_AUDIO[id],"audio/mpeg"));audio.loop=loop;audio.volume=Math.max(0,Math.min(1,sfxVolume*volume));audio.play().catch(()=>{});if(loop){stopSfxLoop();sfxLoop=audio;}return audio;}
function stopSfxLoop(){if(sfxLoop){sfxLoop.pause();sfxLoop.currentTime=0;sfxLoop=null;}}
function updateSfxButton(){const b=document.getElementById("bsfx");b.textContent=sfxEnabled?"🔊 MACHINES ON":"🔇 MACHINES OFF";b.classList.toggle("on",sfxEnabled);}
function ambienceForMap(){return map?.id==="bay_02"?"job_shop_ambience":"shop_ambience_small";}
function setAmbienceLevel(ducked=false){if(ambienceAudio)ambienceAudio.volume=Math.max(0,Math.min(.3,ambienceVolume*(ducked ? .38 : 1)));}
function startAmbience(id=ambienceForMap()){if(!ambienceEnabled||!SFX_AUDIO[id])return;if(ambienceAudio&&ambienceId===id){setAmbienceLevel(false);ambienceAudio.play().catch(()=>{});return;}if(ambienceAudio)ambienceAudio.pause();ambienceId=id;ambienceAudio=new Audio(assetUrl(SFX_AUDIO[id],"audio/mpeg"));ambienceAudio.loop=true;setAmbienceLevel(false);ambienceAudio.play().catch(()=>{});}
function stopAmbience(){if(ambienceAudio){ambienceAudio.pause();ambienceAudio.currentTime=0;}}
function updateAmbienceButton(){const b=document.getElementById("bambience");b.textContent=ambienceEnabled?"◉ AMBIENCE ON":"○ AMBIENCE OFF";b.classList.toggle("on",ambienceEnabled);}
function toolArt(kind){const setup=kind==="probe"||kind==="chamfer",key=setup?"setup-tools-atlas-v1":"core-cutters-atlas-v1";return '<span class="toolArt '+(setup?'setup ':'core ')+kind+'" style="background-image:url('+assetUrl(TOOL_ART[key])+')" aria-hidden="true"></span>';}
function audioStatus(text,bad=false){const el=document.getElementById("audioState");if(el){el.textContent=text;el.style.color=bad?"#ff8075":"var(--green)";}}
function updateVoiceButton(){const b=document.getElementById("bvoice");if(!b)return;b.textContent=voiceEnabled?"🔊 VOICE ON":"🔇 VOICE OFF";b.classList.toggle("on",voiceEnabled);audioStatus(voiceEnabled?"VOICE: READY":"VOICE: MUTED");}
function playZach(id){if(!id)return Promise.resolve(false);if(!ZACH_VOICE[id]){audioStatus("VOICE: CLIP MISSING",true);return Promise.resolve(false);}if(!voiceEnabled){audioStatus("VOICE: MUTED — PRESS VOICE ON",true);return Promise.resolve(false);}if(zachAudio)zachAudio.pause();zachAudio=new Audio(assetUrl(ZACH_VOICE[id],"audio/mpeg"));zachAudio.volume=Math.max(0,Math.min(1,voiceVolume));zachAudio.onplaying=()=>{audioStatus("VOICE: ZACH SPEAKING");setAmbienceLevel(true);};zachAudio.onended=()=>{audioStatus("VOICE: READY");setAmbienceLevel(false);};zachAudio.onerror=()=>{audioStatus("VOICE: AUDIO ERROR — PRESS TEST ZACH",true);setAmbienceLevel(false);};return zachAudio.play().then(()=>true).catch(()=>{audioStatus("VOICE: BLOCKED — PRESS TEST ZACH",true);setAmbienceLevel(false);return false;});}
let preFounderStep=0,preFounderStarted=false;const preFounderBeats=STORY_PRODUCTION.sequences.pre_founder;
function renderPreFounder(play=false){const beat=preFounderBeats[preFounderStep];document.getElementById("preFounderArt").src=assetUrl(PRE_FOUNDER_ART[beat.id.replace("pre_founder_","")]);document.getElementById("preFounderKicker").textContent=beat.kicker;document.getElementById("preFounderText").textContent=beat.text;document.getElementById("preFounderNext").textContent=!preFounderStarted?"▶ PLAY ZACH'S INTRO":preFounderStep===preFounderBeats.length-1?"CHOOSE YOUR FOUNDER ▸":"CONTINUE ▸";if(play)playZach(beat.voice);}
document.getElementById("preFounderNext").onclick=()=>{if(!preFounderStarted){preFounderStarted=true;renderPreFounder(true);return;}preFounderStep++;if(preFounderStep<preFounderBeats.length){renderPreFounder(true);return;}if(zachAudio)zachAudio.pause();document.getElementById("preFounder").classList.add("closed");};renderPreFounder(false);
const IMG={}; let loaded=0, total=Object.keys(SPRITES).length;
for(const k in SPRITES){const im=new Image();im.onload=()=>{if(++loaded===total)start();};
im.src=assetUrl(SPRITES[k]);IMG[k]=im;}
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
function renderFounderProfile(){let root=document.getElementById("founderProfile");if(!root){root=document.createElement("div");root.id="founderProfile";document.getElementById("founderName").before(root);}const p=FOUNDER_PROFILES.profiles.find(x=>x.avatar===selectedAvatar);const stats=Object.entries(p.stats).map(([k,v])=>'<span>'+k.toUpperCase()+' '+"■".repeat(v)+"□".repeat(5-v)+'</span>').join('');root.innerHTML='<div class="atlasPortrait" style="'+atlasStyle(FOUNDER_PROFILES.portraitAtlas,p.atlasCell)+'"></div><div><b>'+p.displayName+' · '+p.specialty.toUpperCase()+'</b><div class="founderStats">'+stats+'</div><div class="founderAbility">'+p.ability.name+': '+p.ability.effect+'</div><div class="hint">UPGRADES: '+p.upgradePath.join(' → ')+'</div></div>';}
function renderFounderPreview(){document.querySelectorAll(".avatarChoice").forEach((b,i)=>{b.querySelector("span").textContent="FOUNDER "+String.fromCharCode(65+i);drawFounder(b.querySelector("canvas"),b.dataset.avatar);});drawFounder(document.querySelector("#sceneFounderBadge canvas"),selectedAvatar);document.getElementById("sceneFounderBadge").dataset.founderAvatar=selectedAvatar;renderFounderProfile();}
document.querySelectorAll(".avatarChoice").forEach(b=>b.onclick=()=>{selectedAvatar=b.dataset.avatar;document.querySelectorAll(".avatarChoice").forEach(x=>x.classList.toggle("selected",x===b));renderFounderPreview();setTitleArt();setStoryArt("opening");});
document.getElementById("newGame").onclick=()=>{companyName=document.getElementById("companyName").value.trim().toUpperCase()||"AMERICAN FORGE WORKS";playerName=document.getElementById("founderName").value.trim().toUpperCase()||"ALEX MORGAN";document.getElementById("playerName").textContent=playerName;document.getElementById("playerNameM").textContent=playerName;startAmbience("shop_ambience_small");introSequence="opening";setStoryArt("opening");introPages=makePrologue();introStep=0;renderIntro();document.getElementById("titleScreen").classList.add("closed");};
document.getElementById("titleSettings").onclick=()=>document.getElementById("connect").classList.add("open");
document.getElementById("bvoice").onclick=()=>{voiceEnabled=!voiceEnabled;localStorage.setItem("reindustrialize.voice",voiceEnabled?"on":"off");if(!voiceEnabled&&zachAudio)zachAudio.pause();updateVoiceButton();if(voiceEnabled)playZach("zach_welcome");};
document.getElementById("bsfx").onclick=()=>{sfxEnabled=!sfxEnabled;localStorage.setItem("reindustrialize.sfx",sfxEnabled?"on":"off");if(!sfxEnabled)stopSfxLoop();updateSfxButton();if(sfxEnabled)playSfx("machine_power_on",{volume:.65});};updateSfxButton();
document.getElementById("bambience").onclick=()=>{ambienceEnabled=!ambienceEnabled;localStorage.setItem("reindustrialize.ambience",ambienceEnabled?"on":"off");if(ambienceEnabled)startAmbience();else stopAmbience();updateAmbienceButton();};updateAmbienceButton();
document.getElementById("testVoice").onclick=()=>{voiceEnabled=true;voiceVolume=1;localStorage.setItem("reindustrialize.voice","on");localStorage.setItem("reindustrialize.voiceVolume","1");updateVoiceButton();playZach("zach_welcome");};
updateVoiceButton();
document.getElementById("credits").onclick=()=>alert("REINDUSTRIALIZE\nA manufacturing RPG by WeCr8 Solutions\nZach is the mentor. You build the shop.");
let hireIndex=0;
function workerFor(id){return workers.find(w=>w.id===id)}
function assignmentOptions(h){return '<option value="">UNASSIGNED · MEANDER</option>'+h.qualifications.map(q=>'<option value="'+q+'">'+(STATION_NAMES[q]||q.replaceAll('_',' ').toUpperCase())+'</option>').join('')}
function assignWorker(h,value){const w=workerFor(h.id);if(!w||(!h.qualifications.includes(value)&&value))return;w.assignment=value||null;w.status=w.assignment?'TRAVELING TO '+(STATION_NAMES[w.assignment]||w.assignment.toUpperCase()):'MEANDERING';renderHires();}
function hireCandidate(h){if(hired.has(h.id))return;if(coins<h.hireCost)return alert("Not enough coins.");coins-=h.hireCost;hired.add(h.id);workers.push({id:h.id,candidate:h,x:P.x+1,y:P.y,assignment:null,status:'MEANDERING',nextMove:0,workPulse:0});addCoins(0);renderHires();}
function renderHires(){const h=HIRE_ROSTER.candidates[hireIndex],root=document.getElementById("hireCard");document.getElementById("hireCount").textContent=(hireIndex+1)+" / "+HIRE_ROSTER.candidates.length;root.innerHTML='<div class="hireCard panel"><img src="data:image/png;base64,'+HIRE_IMAGES[hireKey(h)]+'"><h3>'+h.name+'</h3><div class="role">'+h.title+' · '+h.shift.toUpperCase()+' SHIFT</div><div>'+h.strength+'</div><div>HIRE '+h.hireCost+' · WAGE '+h.wagePerShift+'/SHIFT</div><div class="hireActions"><button id="viewProfile">VIEW PROFILE</button><button id="hireNow" '+(hired.has(h.id)?'disabled':'')+'>'+(hired.has(h.id)?'HIRED':'HIRE')+'</button></div></div>';document.getElementById("viewProfile").onclick=()=>showProfile(h);document.getElementById("hireNow").onclick=()=>hireCandidate(h);}
function showProfile(h){const p=document.getElementById("profile");document.getElementById("roster").style.display="none";p.className="open panel";const skills=Object.entries(h.skills).map(([k,v])=>'<div class="skillRow"><span>'+k.replaceAll("_"," ").toUpperCase()+'</span><span>'+"■".repeat(v)+"□".repeat(5-v)+'</span></div>').join("");p.innerHTML='<div class="profileGrid"><img src="data:image/png;base64,'+HIRE_IMAGES[hireKey(h)]+'"><div><div class="ttl">CANDIDATE PROFILE</div><h2>'+h.name+'</h2><div class="role">'+h.title+' · '+h.shift.toUpperCase()+' SHIFT</div>'+skills+'<p><b>STRENGTH:</b> '+h.strength+'</p><p><b>GROWTH:</b> '+h.growthTo.replaceAll("_"," ").toUpperCase()+'</p><p><b>WATCH:</b> '+h.flaw+'</p><p class="qual"><b>QUALIFIED:</b> '+h.qualifications.join(" · ")+'</p><p>HIRE '+h.hireCost+' · WAGE '+h.wagePerShift+'/SHIFT</p><button id="profileBack">◀ BACK TO CANDIDATES</button> <button id="profileHire" '+(hired.has(h.id)?'disabled':'')+'>'+(hired.has(h.id)?'HIRED':'HIRE '+h.name.toUpperCase())+'</button></div></div>';document.getElementById("profileBack").onclick=()=>{p.className="";document.getElementById("roster").style.display="block";renderHires();};document.getElementById("profileHire").onclick=()=>{hireCandidate(h);showProfile(h);};}
document.getElementById("hirePrev").onclick=()=>{hireIndex=(hireIndex-1+HIRE_ROSTER.candidates.length)%HIRE_ROSTER.candidates.length;renderHires();};document.getElementById("hireNext").onclick=()=>{hireIndex=(hireIndex+1)%HIRE_ROSTER.candidates.length;renderHires();};document.getElementById("bteam").onclick=()=>{hireIndex=0;renderHires();document.getElementById("hire").classList.add("open");};document.getElementById("hireClose").onclick=()=>document.getElementById("hire").classList.remove("open");
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
const state={ toolReady:false, tool:null, stickout:0, toolsSet:[], rawStockReady:false, job:null, materialOrders:[], jobsShipped:0, grades:[],pendingContract:null,contracts:[],reputation:CUSTOMER_CONTRACTS.reputationRules.starting,founder:{level:1,xp:0,upgradePoints:0,stats:null} };
const CHAPTER_ONE_TARGET=5;
let phoneSocket=null,phoneRun=false;
let inputMode=localStorage.getItem("reindustrialize.inputMode")||"auto";const accepts=kind=>inputMode==="auto"||inputMode===kind;
function renderControlSelection(){document.getElementById("inputMode").value=inputMode;document.querySelectorAll(".controlChoice").forEach(b=>b.classList.toggle("selected",b.dataset.control===inputMode));const labels={keyboard:"KEYBOARD SELECTED",gamepad:"XBOX / GAMEPAD SELECTED",phone:"PHONE QR CONTROL SELECTED",touch:"TOUCHSCREEN SELECTED",auto:"ALL INPUTS ACTIVE"};document.getElementById("selectedControlStatus").textContent=labels[inputMode]||"CONTROL SELECTED";}
function selectControl(mode){inputMode=mode;localStorage.setItem("reindustrialize.inputMode",mode);renderControlSelection();if(mode==="phone"){document.getElementById("connect").classList.add("open");if(!document.getElementById("pairQr").getAttribute("src"))createPhoneSession();}}
document.querySelectorAll(".controlChoice").forEach(b=>b.onclick=()=>selectControl(b.dataset.control));
document.getElementById("inputMode").onchange=e=>selectControl(e.target.value);renderControlSelection();
function phoneInput(key){if(!accepts("phone"))return;const d=DIRS[key];if(d)move(d[0],d[1],false,phoneRun);else if(key==="run")phoneRun=!phoneRun;else if(key==="action")interact();else if(key==="menu")document.getElementById("connect").classList.add("open");}
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
function makePrologue(){return sequencePages("opening");}
let introPages=makePrologue();
let introStep=0,introSequence="opening";
function renderIntro(){const s=introPages[introStep];setStoryArt(s[3]);document.getElementById("introKicker").textContent=s[0];document.getElementById("introText").textContent=s[1];document.getElementById("intro").dataset.storyBeat=s[4];document.getElementById("introNext").textContent=introStep===introPages.length-1?(introSequence==="opening"?"OPEN THE SHOP ▸":"ENTER THE JOB SHOP ▸"):"CONTINUE ▸";if(s[2])playZach(s[2]);else{if(zachAudio)zachAudio.pause();audioStatus("VOICE: NARRATION PAUSED");}}
document.getElementById("introNext").onclick=()=>{introStep++;if(introStep<introPages.length){renderIntro();return;}document.getElementById("intro").classList.add("closed");if(introSequence==="opening"){mission("meet_zach");say(companyName+" is open.","Zach will tour the floor before your first material order.");setTimeout(()=>startShopTour(true),100);}else{setMap("bay_02");sel("b2");say(companyName+" has entered the Job Shop chapter.","Hire a team, control flow, and earn the next facility.");}};
function showExpansion(){
  document.getElementById("b2").disabled=false;document.getElementById("b2").textContent="BAY 02";
  setStoryArt("expansion");
  introSequence="job_shop_expansion";introPages=sequencePages(introSequence);
  introStep=0;renderIntro();document.getElementById("intro").classList.remove("closed");
}
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
function setMap(id){cancelMove();map=MAPS[id]; P.x=map.spawn[0]; P.y=map.spawn[1];P.rx=P.x;P.ry=P.y;P.fromX=P.x;P.fromY=P.y; fit(); clampCam();
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
    cx.drawImage(IMG.bay_01_hd_bg,0,0,map.size[0]*T,map.size[1]*T);
  }else{
    for(let y=cam.y;y<Math.min(map.size[1],cam.y+VH);y++)
      for(let x=cam.x;x<Math.min(map.size[0],cam.x+VW);x++)
        cx.drawImage(IMG.tileset,tileAt(x,y)*32,0,32,32,x*T,y*T,T,T);
  }
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
    const dw=p.footprint[0]*T,dh=Math.min(p.footprint[1]*T,a.fh*(dw/a.fw));
    cx.drawImage(IMG[p.sprite],fi*a.fw,0,a.fw,a.fh,p.tile[0]*T,p.tile[1]*T+(p.footprint[1]*T-dh),dw,dh);
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
function drawP(){ const a=ATLAS[selectedAvatar];cv.dataset.playerAvatar=selectedAvatar;const moving=performance.now()-P.moveAt<P.moveDuration,run=moving&&P.running,walkFrame=moving?Math.floor(performance.now()/(run?48:90))%2:0;cv.dataset.motion=run?"running":moving?"walking":"idle";
  const now=performance.now(),stride=run?Math.sin(now/38):Math.sin(now/62),bob=moving?Math.abs(stride)*(run?5:2):0;
  cx.fillStyle=run?"rgba(0,0,0,.22)":"rgba(0,0,0,.3)";cx.beginPath();cx.ellipse(P.rx*T+32,P.ry*T+57,run?28:24,run?5:6,0,0,Math.PI*2);cx.fill();
  if(run){const trail=P.facing==="left"?1:P.facing==="right"?-1:0;cx.save();cx.strokeStyle="rgba(226,235,239,.42)";cx.lineWidth=3;for(let i=0;i<3;i++){const yy=P.ry*T+23+i*11;cx.beginPath();cx.moveTo(P.rx*T+32+trail*20,yy);cx.lineTo(P.rx*T+32+trail*(34+i*5),yy);cx.stroke();}cx.fillStyle="rgba(190,176,145,.42)";cx.beginPath();cx.arc(P.rx*T+22-stride*8,P.ry*T+58,3+Math.abs(stride)*3,0,Math.PI*2);cx.fill();}
  const py=P.ry*T-32-bob;cx.save();cx.translate(P.rx*T+32,P.ry*T+18);cx.rotate(run?(P.facing==="left"?-.09:P.facing==="right"?.09:stride*.025):0);cx.scale(1+(run?Math.abs(stride)*.025:0),1-(run?Math.abs(stride)*.018:0));cx.translate(-(P.rx*T+32),-(P.ry*T+18));if(P.facing==="left"){cx.translate(P.rx*T+64,0);cx.scale(-1,1);cx.drawImage(IMG[selectedAvatar],walkFrame*a.fw,0,a.fw,a.fh,0,py,64,96);}else cx.drawImage(IMG[selectedAvatar],walkFrame*a.fw,0,a.fw,a.fh,P.rx*T,py,64,96);cx.restore();}
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
  if(o){document.getElementById("objectiveStep").textContent=o.step;document.getElementById("objectiveHow").textContent=o.how;const atTarget=near&&near.sprite===o.sprite;action.disabled=false;action.textContent=atTarget?"OPEN "+(STATION_NAMES[o.sprite]||"STATION"):"GO TO & OPEN "+(STATION_NAMES[o.sprite]||"TARGET");}else{document.getElementById("objectiveStep").textContent="Garage mastery complete — graduate to the Job Shop";document.getElementById("objectiveHow").textContent="Five customer jobs shipped. Review the expansion scene and move your company.";action.disabled=true;action.textContent="CHAPTER COMPLETE";}
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
function acceptCustomerContract(c){const o=c.offer;state.pendingContract={...o,customerId:c.id,customer:c.company,contact:c.contact};state.contracts.push({offerId:o.id,customerId:c.id,status:"accepted"});playSfx("handoff_confirm");say(c.company+" hired "+companyName+".","JobLine work order "+o.id+" created. Open PLANNING to release the traveler.");renderCustomer();updateGuide();}
document.getElementById("bcustomerphone").onclick=()=>openCustomers("shop_phone");document.getElementById("bmail").onclick=()=>openCustomers("jobline_email");document.getElementById("customerClose").onclick=()=>document.getElementById("customers").classList.remove("open");
document.getElementById("shopPhoneProp").style.backgroundImage="url("+assetUrl(CUSTOMER_ART["shop-communications-v1"])+")";document.getElementById("shopComputerProp").style.backgroundImage="url("+assetUrl(CUSTOMER_ART["shop-communications-v1"])+")";document.getElementById("shopPhoneProp").onclick=()=>{customerChannel="shop_phone";playSfx("phone_answer");renderCustomer();};document.getElementById("shopComputerProp").onclick=()=>{customerChannel="jobline_email";playSfx("terminal_wake");renderCustomer();};
let lastNearSprite=null;function checkNear(){const p=nearStation();if(p&&p.sprite!==lastNearSprite){const m=MSG[p.sprite];if(m)say(m[0],m[1]);if(p.sprite==="chalkboard")mission("chalkboard");}lastNearSprite=p?.sprite||null;updateGuide();}
function cancelMove(){if(moveTimer)clearInterval(moveTimer);moveTimer=null;moveTarget=null;P.running=false;}
function move(dx,dy,fromPath=false,run=false){if(!fromPath)cancelMove();const nx=P.x+dx,ny=P.y+dy;P.facing=dx<0?"left":dx>0?"right":dy<0?"up":"down";P.running=!!run;P.moveDuration=P.running?82:145;
  if(!blocked(nx,ny)){P.fromX=P.rx;P.fromY=P.ry;P.x=nx;P.y=ny;P.step++;P.moveAt=performance.now();cv.dataset.moveResult="moved";cv.dataset.moveSpeed=P.running?"run":"walk";clampCam();checkNear();return true;}P.running=false;cv.dataset.moveResult="blocked";updateGuide();return false;}
function pathToTile(goalX,goalY){if(blocked(goalX,goalY))return[];const q=[[P.x,P.y]],prev=new Map([[P.x+','+P.y,null]]),dirs=[[1,0],[-1,0],[0,1],[0,-1]],goal=goalX+','+goalY;while(q.length){const[x,y]=q.shift(),key=x+','+y;if(key===goal)break;for(const[dX,dY]of dirs){const nx=x+dX,ny=y+dY,k=nx+','+ny;if(!prev.has(k)&&!blocked(nx,ny)){prev.set(k,key);q.push([nx,ny]);}}}if(!prev.has(goal))return[];const path=[];let end=goal;while(prev.get(end)!==null){const[x,y]=end.split(',').map(Number),[px,py]=prev.get(end).split(',').map(Number);path.push([x-px,y-py]);end=prev.get(end);}return path.reverse();}
function pathToStation(sprite){const target=map.placements.find(p=>p.sprite===sprite);if(!target)return[];const goals=new Set(),[tx0,ty0]=target.tile,[fw,fh]=target.footprint;for(let y=ty0-1;y<=ty0+fh;y++)for(let x=tx0-1;x<=tx0+fw;x++){const dx=Math.max(tx0-x,0,x-(tx0+fw-1)),dy=Math.max(ty0-y,0,y-(ty0+fh-1));if(dx+dy<=1&&!blocked(x,y))goals.add(x+','+y);}const q=[[P.x,P.y]],prev=new Map([[P.x+','+P.y,null]]),dirs=[[1,0],[-1,0],[0,1],[0,-1]];let end=null;while(q.length){const [x,y]=q.shift(),key=x+','+y;if(goals.has(key)){end=key;break;}for(const[dX,dY]of dirs){const nx=x+dX,ny=y+dY,k=nx+','+ny;if(!prev.has(k)&&!blocked(nx,ny)){prev.set(k,key);q.push([nx,ny]);}}}if(!end)return[];const path=[];while(prev.get(end)!==null){const [x,y]=end.split(',').map(Number),[px,py]=prev.get(end).split(',').map(Number);path.push([x-px,y-py]);end=prev.get(end);}return path.reverse();}
function followPath(path,openWhenThere=false,run=true){cancelMove();if(!path.length){if(openWhenThere)interact();return;}let i=0,pace=run?82:145;moveTarget={x:P.x+path.reduce((n,d)=>n+d[0],0),y:P.y+path.reduce((n,d)=>n+d[1],0)};moveTimer=setInterval(()=>{if(i>=path.length){cancelMove();if(openWhenThere)setTimeout(interact,100);return;}move(path[i][0],path[i][1],true,run);i++;},pace);}
function walkToStation(sprite,openWhenThere=false){followPath(pathToStation(sprite),openWhenThere);}

/* ================= INTERACT -> TASKS ================= */
const STATION_SFX={nox_terminal:"terminal_wake",saw_t1:"bandsaw_vise_clamp",tool_cart:"tool_drawer_open",presetter_t4:"probe_touch",toolcrib_rfid_t4:"rfid_tool_scan",vmc_t2:"machine_vise_clamp",lathe_cnc_t2:"lathe_chuck_clamp",planning_desk:"planning_paperwork",chalkboard:"chalk_marker",mill_manual_t1:"manual_mill_run",bench_deburr_t1:"deburr_tool",network_node_t3:"network_connect",handoff_terminal_t4:"handoff_confirm",nox_pallet:"pallet_delivery",whiteboard:"mission_board_update",amr_t5:"amr_drive",cobot_t5:"cobot_motion"};
function interact(){
  const worker=nearWorker();if(worker){talkWorker(worker);return;}
  const p=nearStation(); if(!p){cv.dataset.interaction="too-far";say("Move beside a station before using it.","Follow the pulsing objective or click a machine to walk into interaction range.");return;}
  cv.dataset.interaction=p.sprite;
  if(STATION_SFX[p.sprite])playSfx(STATION_SFX[p.sprite]);
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
  document.getElementById("tjob").textContent=jobCard;
  task.classList.add("open"); hintI=0; attempts=0;}
function clearCycleTimers(){cycleTimers.forEach(clearTimeout);cycleTimers=[];}
function closeOverlay(){task.classList.remove("open");cancelAnimationFrame(taskAnim);taskAnim=null;clearCycleTimers();stopSfxLoop();machineMotionMode=null;tctrl.innerHTML="";updateGuide();}
function showEquipmentView(id){const im=document.getElementById("tview");im.src=assetUrl(EQUIPMENT_VIEWS[id]);im.style.display="block";tscene.style.display="none";}
function showNoxMaterialsView(){const im=document.getElementById("tview");im.src=assetUrl(NOX_MATERIALS_ART);im.style.display="block";tscene.style.display="none";}
function showTaskCanvas(){document.getElementById("tview").style.display="none";tscene.style.display="block";}
let tourIndex=0,tourPhase=0,tourActive=false;
function renderTourStop(){const stop=SHOP_TOUR.stops[tourIndex],walk=STATION_WALKTHROUGHS[stop.id],detail=tourPhase===0?{label:"WHAT & WHY",text:stop.text,voice:stop.voice}:{label:"HOW TO OPERATE",text:walk.text,voice:walk.voice},placement=map.placements.find(p=>p.sprite===stop.sprite);tourActive=true;openOverlay(stop.title,`STOP ${tourIndex+1} OF ${SHOP_TOUR.stops.length} · ${detail.label} · ${stop.location}`);task.dataset.tourStop=stop.id;task.dataset.tourPhase=tourPhase===0?"overview":"walkthrough";const im=document.getElementById("tview");im.style.display="block";tscene.style.display="none";im.style.objectFit="contain";im.style.background="#080b10";im.src=stop.imageType==="equipment"?"data:image/png;base64,"+EQUIPMENT_VIEWS[stop.image]:stop.imageType==="nox"?"data:image/png;base64,"+NOX_MATERIALS_ART:"data:image/png;base64,"+SPRITES[stop.image];curHints=[stop.operation];tz("ZACH: "+detail.text);playZach(detail.voice);const last=tourIndex===SHOP_TOUR.stops.length-1;tctrl.innerHTML='<div class="ttl">WHERE: '+stop.location+'</div><div style="color:#fff">'+detail.label+': '+(tourPhase===0?stop.operation:walk.text)+'</div><button id="tourPrev" '+(tourIndex===0&&tourPhase===0?'disabled':'')+'>◀ PREVIOUS</button><button id="tourLocate">SHOW ON FLOOR</button><button id="tourNext" class="grn">'+(tourPhase===0?'OPERATING STEPS ▶':last?'FINISH TOUR':'NEXT STATION ▶')+'</button><button id="tourSkip">SKIP TOUR</button>';document.getElementById("tourPrev").onclick=()=>{if(tourPhase===1)tourPhase=0;else{tourIndex--;tourPhase=1;}renderTourStop();};document.getElementById("tourLocate").onclick=()=>{const id=stop.sprite;closeOverlay();tourActive=false;walkToStation(id,false);say("Tour location: "+stop.title,stop.location+" · Use SHOP TOUR to resume.");};document.getElementById("tourNext").onclick=()=>{if(tourPhase===0){tourPhase=1;renderTourStop();return;}if(last){finishTour();return;}tourIndex++;tourPhase=0;renderTourStop();};document.getElementById("tourSkip").onclick=finishTour;if(placement)cv.dataset.tourTarget=stop.sprite;}
function startShopTour(reset=false){if(reset){tourIndex=0;tourPhase=0;}renderTourStop();}
function finishTour(){tourActive=false;task.dataset.tourStop="complete";closeOverlay();cv.dataset.tourTarget="";say("Shop tour complete.","Your first achievable step is the NOX material terminal. You can replay the tour any time.","zach_response_next_step");updateGuide();}
document.getElementById("btour").onclick=()=>startShopTour(true);
document.getElementById("tclose").onclick=closeOverlay;
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
  const rows=NOX_CATALOG.map((m,i)=>'<button class="toolbtn noxOrder" data-i="'+i+'"><b>'+m.name+'</b><span>'+m.detail+'</span><strong>'+m.cost+' COINS</strong></button>').join('');
  tctrl.innerHTML='<div class="ttl">LIVE DETROIT INVENTORY</div><div class="tools">'+rows+'</div><div id="noxStatus" class="hint">ALLOY · CONDITION · DIMENSIONS · QUANTITY</div>';
  document.querySelectorAll('.noxOrder').forEach(b=>b.onclick=()=>placeNoxOrder(NOX_CATALOG[Number(b.dataset.i)]));
  tz("ZACH: Raw stock is the first operation. Buy the right alloy, condition, and size — then protect the cert chain.");
}
function placeNoxOrder(item){
  const status=document.getElementById("noxStatus");
  if(coins<item.cost){status.textContent="ORDER DECLINED — NOT ENOUGH COINS";return;}
  playSfx("terminal_confirm");setTimeout(()=>playSfx("pallet_delivery",{volume:.75}),500);coins-=item.cost;addCoins(0);state.materialOrders.push({sku:item.sku,qty:1,status:"NEXT-DAY DELIVERY"});
  status.textContent="ORDER CONFIRMED · "+item.sku+" · NEXT-DAY DELIVERY TO RECEIVING";
  say("NOX order confirmed: "+item.name,"Material will arrive at receiving with certification.");
  updateGuide();
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
  tctrl.innerHTML='<input type="range" id="cutLength" min="3" max="6.5" step="0.05" value="3"><span id="cutLengthValue" style="color:#e8b93b;font-size:22px"></span><button id="cutStock" class="grn">CLAMP & CUT ▸</button>';
  const sl=document.getElementById("cutLength"),value=document.getElementById("cutLengthValue");const render=()=>{const v=Number(sl.value);value.textContent=v.toFixed(2)+' in';drawSawCut(v,J.stockLength);};sl.oninput=render;render();
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
    b.onclick=()=>{ if(kind===J.tool){playSfx("toolholder_load");state.tool=kind;stepStickout();}
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
  tctrl.innerHTML='<div class="toolMeasure">'+toolArt(J.tool)+'<div><b>MEASURE HOLDER FACE TO CUTTING TIP</b><br><span class="hint">Short for rigidity · long enough for clearance</span></div></div><input type="range" id="stick" min="0.5" max="2.2" step="0.05" value="0.6">'+
    '<span id="stickval" style="color:#e8b93b;font-size:22px">0.60"</span>'+
    '<button id="lockin" class="grn">LOCK IN ▸</button>';
  const sl=document.getElementById("stick"), sv=document.getElementById("stickval");
  const render=()=>{ const v=parseFloat(sl.value); sv.textContent=v.toFixed(2)+'"'; sceneStick(v); };
  sl.oninput=render; render();
  document.getElementById("lockin").onclick=()=>{
    const v=parseFloat(sl.value), J=state.job;
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
  document.getElementById("installKit").onclick=()=>{state.toolReady=true;mission("task_tool");closeOverlay();say("Three tools gauged and installed: cutter, probe, chamfer.","Stock and tool kit are ready. Open the VMC for the G/M-code proof.");};}

/* ================= TASK 2: VMC G/M + RUN ================= */
function openVmcTask(){
  activeTaskTutorialId="prove_gcode";
  playZach("zach_gcode_intro");
  const J=state.job; curHints=J.hints.g; hintI=0;
  openOverlay("VMC — "+J.gtitle, J.card);showEquipmentView("vmc-open-v1");playSfx("machine_power_on",{volume:.7});
  tz("ZACH: Program's missing three words. Offset, spindle, coolant. Fill them and press CYCLE START.");
  // program with inputs
  let progHtml='<div class="gcode">';
  for(const ln of J.prog){
    progHtml+=ln.replace(/{{(\w)}}/g,(m,k)=>'<input maxlength="2" data-b="'+k+'" placeholder="__">')+"<br>";
  }
  progHtml+="</div>";
  tctrl.innerHTML=progHtml+
    '<div class="gline"><button id="cycst" class="grn">▶ CYCLE START</button></div><details><summary class="ttl">TRUE G & M CODE · READ THE MODAL SEQUENCE</summary><div class="hint">M06 TOOL CHANGE → G90 ABSOLUTE → G54 WORK OFFSET → G00 RAPID CLEAR → M03 SPINDLE CW → G43 H TOOL LENGTH → M08 COOLANT → G01/G81 CONTROLLED CUT → G80 CANCEL CYCLE → G00 RETRACT → M09 COOLANT OFF → M05 SPINDLE STOP → G28 RETURN → M30 END/REWIND</div></details>';
  sceneVmcIdle();
  document.getElementById("cycst").onclick=()=>{
    let allOk=true;
    document.querySelectorAll('#tcontrols input[data-b]').forEach(inp=>{
      const key=inp.dataset.b, val=inp.value.trim();
      const ok=J.blanks[key].ans.includes(val);
      inp.className=ok?"ok":"bad"; if(!ok)allOk=false;
    });
    if(!allOk){attempts++;tz("ZACH: Red ones are wrong. "+(attempts>=2?"Hit ASK ZACH if you're stuck.":"Think: where's the part, spin it, cool it."));return;}
    tz("ZACH: Program's good. Doors closed. Watch the path — this is your setup running.");
    runAnim(J);
  };
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
  addCoins(pay); mission("task_vmc");state.toolReady=false;state.rawStockReady=false;state.toolsSet=[];state.jobsShipped++;state.grades.push({A:5,B:4,C:3,D:2,F:1}[g]);awardFounderXp(60+({A:5,B:4,C:3,D:2,F:1}[g])*10);if(J.contract){const r=state.contracts.find(x=>x.offerId===J.contract.id);if(r)r.status="delivered · grade "+g;state.reputation=Math.max(0,Math.min(100,state.reputation+({A:6,B:4,C:2,D:-1,F:-4}[g])));}jobIdx++; state.job=null;updateGuide();
  tz("ZACH: "+(g==="A"?"First-try clean. THAT'S craftsmanship — "+pay+" coins.":g<="C"?"Shipped at grade "+g+". Review the misses at Shop Class and the next one's an A. +"+pay+" coins.":"It shipped, barely. Shop Class. Tonight. +"+pay+" coins."));
  tctrl.innerHTML='<button id="tdone" class="grn">BACK TO THE FLOOR ▸</button>';
  document.getElementById("tdone").onclick=()=>{playSfx("machine_power_off",{volume:.7});closeOverlay();
    say("Grade "+g+" recorded. "+state.jobsShipped+" of "+CHAPTER_ONE_TARGET+" Garage jobs shipped.",state.jobsShipped<CHAPTER_ONE_TARGET?"Return to planning for the next customer order.":"Garage mastery proven. Prepare to move your company.");
    if(state.jobsShipped>=CHAPTER_ONE_TARGET&&gradeAverage()>=3)showExpansion();};
}

/* ================= INPUT ================= */
document.addEventListener("keydown",e=>{
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
addEventListener("gamepadconnected",e=>document.getElementById("gamepadState").textContent="GAMEPAD: "+e.gamepad.id);
addEventListener("gamepaddisconnected",()=>document.getElementById("gamepadState").textContent="GAMEPAD: NOT CONNECTED");
function pollGamepad(now){
  const gp=[...(navigator.getGamepads?.()||[])].find(Boolean);
  if(gp&&accepts("gamepad")){
    document.getElementById("gamepadState").textContent="GAMEPAD: "+gp.id;
    const pressed=i=>!!gp.buttons[i]?.pressed,edge=i=>pressed(i)&&!gpPrev[i];
    if(edge(0)){if(!document.getElementById("preFounder").classList.contains("closed"))document.getElementById("preFounderNext").click();else if(!document.getElementById("titleScreen").classList.contains("closed"))document.getElementById("newGame").click();else if(!task.classList.contains("open"))interact();}
    if(edge(1)){if(task.classList.contains("open"))closeOverlay();else document.getElementById("connect").classList.remove("open");}
    if(edge(9))document.getElementById("connect").classList.toggle("open");
    const sprint=pressed(7)||pressed(10);
    if(now-gpLastMove>(sprint?92:165)&&!task.classList.contains("open")&&document.getElementById("titleScreen").classList.contains("closed")&&document.getElementById("intro").classList.contains("closed")){
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
function start(){renderFounderPreview();setTitleArt();setStoryArt("opening");setMap("bay_01");let lastFrame=0;const animate=now=>{const t=Math.min(1,(now-P.moveAt)/P.moveDuration),ease=1-Math.pow(1-t,3);P.rx=P.fromX+(P.x-P.fromX)*ease;P.ry=P.fromY+(P.y-P.fromY)*ease;if(now-lastFrame>130){frame++;lastFrame=now;}if(!task.classList.contains("open"))draw();requestAnimationFrame(animate);};requestAnimationFrame(animate);}
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
out = os.path.join(ROOT, "apps", "wecr8-info", "prototypes", "shop-floor-viewer.html")
with open(out, "w", encoding="utf-8") as f: f.write(html)
print("wrote", out, len(html)//1024, "KB")
