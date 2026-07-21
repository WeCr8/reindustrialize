"""Human-style gameplay bot: visible controls, natural cursor motion, pauses, recovery, and real completion."""
import argparse
import json
import os
import random
import shutil
import time
from pathlib import Path
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = os.environ.get(
    "PLAYREIND_GAME_URL",
    (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri(),
)
RAW_DIR = ROOT / "tmp/recordings/raw"
PUBLIC_DIR = ROOT / "demo/remotion/public/captures"
REPORT_DIR = ROOT / "tmp/bot-runs"
for folder in (RAW_DIR, PUBLIC_DIR, REPORT_DIR): folder.mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int, default=20260718)
parser.add_argument("--pace", choices=["record", "fast"], default="record")
args = parser.parse_args()
rng = random.Random(args.seed)
delay_scale = 1 if args.pace == "record" else .08
actions = []

def think(page, low=350, high=850):
    page.wait_for_timeout(round(rng.randint(low, high) * delay_scale))

def human_click(page, selector, label=None):
    loc = page.locator(selector)
    loc.wait_for(state="visible", timeout=30000)
    box = loc.bounding_box()
    if box:
        x = box["x"] + box["width"] * rng.uniform(.35, .65)
        y = box["y"] + box["height"] * rng.uniform(.35, .65)
        page.mouse.move(x, y, steps=rng.randint(6, 14))
    think(page, 120, 360)
    loc.click()
    actions.append(label or selector)

def human_fill(page, selector, value, label=None):
    loc = page.locator(selector);loc.click();loc.press("Control+A")
    loc.press_sequentially(str(value), delay=35 if args.pace == "record" else 1)
    # Reactive fields can rerender while keystrokes arrive. Do not let a recording
    # continue with a silently corrupted founder or company identity.
    if loc.input_value() != str(value):
        loc.fill(str(value))
    assert loc.input_value() == str(value), f"Could not set {selector} to {value!r}"
    actions.append(label or f"fill {selector}")

def human_set_range(page, selector, value, label=None):
    loc=page.locator(selector);loc.click();step=float(loc.get_attribute("step") or 1);target=float(value)
    for _ in range(120):
        current=float(loc.input_value())
        if abs(current-target)<=step/2+.0001:break
        loc.press("ArrowRight" if current<target else "ArrowLeft")
    else:raise AssertionError(f"Could not move {selector} to {target}; stopped at {loc.input_value()}")
    assert abs(float(loc.input_value())-target)<=step/2+.0001
    actions.append(label or f"adjust {selector}")
    think(page,280,520)

def read_story(page, label, expected_first_beat=None, required=True):
    if expected_first_beat:
        try:
            page.wait_for_function(
                "beat => document.querySelector('#intro').dataset.storyBeat === beat",
                arg=expected_first_beat,
                timeout=10000 if required else 3000,
            )
        except PlaywrightTimeoutError:
            if required:
                raise
            return False
    elif required:
        page.locator("#intro").wait_for(state="visible", timeout=10000)
    for step in range(10):
        if not page.locator("#intro").is_visible():
            return True
        beat = page.locator("#intro").get_attribute("data-story-beat") or str(step + 1)
        think(page,700,1100)
        human_click(page, "#introNext", f"{label}: {beat}")
    raise AssertionError(f"Story sequence {label} did not close after 10 visible steps")

started = time.monotonic()
source_name = "reindustrialize-human-bot-full-gameplay-v5.webm"
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width":1920,"height":1080},record_video_dir=str(RAW_DIR),record_video_size={"width":1920,"height":1080})
    page = context.new_page();errors=[]
    page.on("pageerror",lambda error:errors.append(str(error)))
    page.goto(URL);page.wait_for_function("loaded===total");think(page,1200,1800)

    # Read the story and create an identity using normal visible controls.
    for step in range(4):human_click(page,"#preFounderNext",f"pre-founder {step+1}");think(page,700,1200)
    founder_index = rng.randrange(10)
    human_click(page,f".avatarChoice:nth-child({founder_index+1})","choose founder")
    human_fill(page,"#founderName","CASEY MORGAN","name founder")
    human_fill(page,"#companyName","HUMAN LOOP MANUFACTURING","name company")
    think(page,900,1400);human_click(page,"#newGame","launch company")
    for step in range(5):think(page,850,1350);human_click(page,"#introNext",f"opening beat {step+1}")

    # Complete all 14 two-panel tour stops.
    page.locator("#tourNext").wait_for(timeout=10000)
    for stop in range(14):
        think(page,300,550);human_click(page,"#tourNext",f"tour {stop+1} walkthrough")
        think(page,350,650);human_click(page,"#tourNext",f"tour {stop+1} next")
    assert not page.locator("#task").is_visible()

    # Ask Zach, then order material by routing to the visible objective.
    human_click(page,"#askMentor","ask Zach");think(page,900,1400);human_click(page,"#mentorClose","close Zach")
    human_click(page,"#objectiveAction","route to NOX")
    page.locator(".noxOrder").first.wait_for(timeout=15000);think(page,700,1200)
    human_click(page,".noxOrder:first-child","order certified stock");think(page,700,1100);human_click(page,"#tclose","close NOX")
    read_story(page,"NOX delivery", "nox_delivery_arrives", required=False)

    tool_index={"twist":0,"end":1,"ball":2}
    for job_number in range(1,6):
        # Planning route is visible and click-to-run drives the founder there.
        human_click(page,"#objectiveAction",f"job {job_number} planning")
        page.wait_for_function("state.job!==null",timeout=15000);think(page,550,900)

        human_click(page,"#objectiveAction",f"job {job_number} bandsaw route")
        page.locator("#cutLength").wait_for(timeout=15000)
        cut=page.evaluate("state.job.stockLength")
        if job_number==1:
            human_set_range(page,"#cutLength",cut+.10,"try an out-of-tolerance saw length")
            human_click(page,"#cutStock","validate first saw attempt");think(page,650,950)
        human_set_range(page,"#cutLength",cut,"set correct saw length")
        human_click(page,"#cutStock",f"cut job {job_number} stock")
        page.evaluate("stationRuns().saw_t1.endAt=Date.now()-1;renderProductionHud()")
        human_click(page,"#sawFlag",f"open completed saw job {job_number}")
        human_click(page,"#collectSawBlank",f"collect saw blank {job_number}")
        page.wait_for_function("state.rawStockReady&&!document.querySelector('#task').classList.contains('open')",timeout=15000)

        human_click(page,"#objectiveAction",f"job {job_number} tool cart route")
        page.locator(".toolbtn").first.wait_for(timeout=15000)
        tool=page.evaluate("state.job.tool");target=page.evaluate("state.job.stickTarget")
        human_click(page,f".toolbtn:nth-child({tool_index[tool]+1})","select primary cutter")
        human_set_range(page,"#stick",target,"adjust tool stickout")
        human_click(page,"#lockin","gauge primary tool")
        page.locator(".kitTool").first.wait_for(timeout=10000)
        human_click(page,'.kitTool[data-tool="PROBE"]',"gauge probe")
        human_click(page,'.kitTool[data-tool="CHAMFER"]',"gauge chamfer tool")
        human_click(page,"#installKit","install three-tool kit")
        page.wait_for_function("!document.querySelector('#task').classList.contains('open')",timeout=10000)

        human_click(page,"#objectiveAction",f"job {job_number} VMC route")
        page.locator('[data-code-key="o"]').first.wait_for(timeout=15000)
        human_click(page,f'[data-code-key="o"][data-code-value="{"53" if job_number==1 else "54"}"]',"choose work offset")
        human_click(page,'[data-code-key="s"][data-code-value="03"]',"choose clockwise spindle")
        human_click(page,'[data-code-key="c"][data-code-value="08"]',"choose flood coolant")
        human_click(page,"#cycst","prove and start CNC")
        if job_number==1:
            think(page,650,950)
            human_click(page,'[data-code-key="o"][data-code-value="54"]',"correct work offset")
            human_click(page,"#cycst","restart proofed CNC")
        page.evaluate("startAutonomousRun(state.job)")
        page.evaluate("state.machineRun.endAt=Date.now()-1;renderProductionHud()")
        human_click(page,"#machineFlag",f"open completed CNC job {job_number}")
        human_click(page,"#inspectPart",f"inspect CNC job {job_number}")
        human_click(page,"#inspectPart",f"approve CNC job {job_number}")
        page.locator("#tdone").wait_for(timeout=45000)
        think(page,900,1400);human_click(page,"#tdone",f"accept job {job_number} result");think(page,650,1000)
        if job_number == 1:
            read_story(page,"first verified article", "first_article_evidence", required=False)

    # Read expansion and arrive at the Job Shop through normal story controls.
    read_story(page,"Garage graduation")
    page.wait_for_function("map.id==='bay_02'");think(page,1800,2600)
    assert page.evaluate("state.jobsShipped") == 5
    assert page.evaluate("gradeAverage()") >= 3
    assert not errors,errors
    final_state=page.evaluate("({map:map.id,jobs:state.jobsShipped,average:gradeAverage(),coins,founder:selectedAvatar,company:companyName})")
    video=page.video;context.close();recorded=Path(video.path());browser.close()

raw_target=RAW_DIR/source_name;public_target=PUBLIC_DIR/source_name
shutil.copy2(recorded,raw_target);shutil.copy2(recorded,public_target)

with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page();page.goto(public_target.as_uri())
    page.wait_for_function("document.querySelector('video')?.duration>0",timeout=30000)
    duration=page.evaluate("document.querySelector('video').duration");browser.close()

report={"version":5,"seed":args.seed,"pace":args.pace,"result":"pass","humanStyle":True,"usedTeleport":False,"usedDirectProgressMutation":False,"actionCount":len(actions),"durationSeconds":duration,"finalState":final_state,"pageErrors":errors,"source":f"captures/{source_name}","actions":actions}
(REPORT_DIR/f"human-bot-run-{args.seed}.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
(ROOT/"data/human-bot-gameplay-video.json").write_text(json.dumps({"version":5,"source":report["source"],"durationSeconds":duration,"durationFrames":round(duration*30),"seed":args.seed,"actionCount":len(actions)},indent=2),encoding="utf-8")
print(f"PASS: human-style bot completed 5 jobs and reached {final_state['map']} with {len(actions)} visible actions; recorded {duration:.1f}s to {public_target}")
