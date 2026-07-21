"""Record the complete current Garage-to-Job-Shop campaign as a deterministic browser video."""
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "tmp/recordings/raw"
PUBLIC_DIR = ROOT / "demo/remotion/public/captures"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
RAW_NAME = "reindustrialize-full-gameplay-garage-to-job-shop-v3.webm"

def pause(page, ms=900):
    page.wait_for_timeout(ms)

def stand_by(page, sprite):
    page.evaluate("""sprite => {
      const p=map.placements.find(x=>x.sprite===sprite);
      P.x=p.tile[0];P.y=p.tile[1]+p.footprint[1];P.rx=P.x;P.ry=P.y;
      P.fromX=P.x;P.fromY=P.y;clampCam();updateGuide();draw();
    }""", sprite)
    pause(page, 650)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=str(RAW_DIR),
        record_video_size={"width": 1920, "height": 1080},
    )
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded===total")
    pause(page, 1800)

    # Full introduction and founder/company setup.
    for _ in range(4):
        page.locator("#preFounderNext").click(); pause(page, 1300)
    page.locator('[data-avatar="av_f_blonde_hd"]').click()
    page.locator("#founderName").fill("YOUR FOUNDER")
    page.locator("#companyName").fill("YOUR FACTORY")
    pause(page, 1800)
    page.locator("#newGame").click()
    for _ in range(5):
        pause(page, 1500); page.locator("#introNext").click()

    # Show every ordered shop-tour panel at an edited walkthrough pace.
    page.locator("#tourNext").wait_for(timeout=10000)
    pause(page, 1200)
    for _ in range(page.evaluate("SHOP_TOUR.stops.length")):
        page.locator("#tourNext").click(); pause(page, 420)
        page.locator("#tourNext").click(); pause(page, 420)
    assert not page.locator("#task").is_visible()

    # Movement, running, proximity, Zach guidance, and the first material purchase.
    page.locator("#askMentor").click(); pause(page, 1700)
    page.locator("#mentorClose").click()
    page.evaluate("walkToStation('nox_terminal')")
    page.wait_for_function("document.querySelector('#cv').dataset.nearStation==='nox_terminal'", timeout=10000)
    pause(page, 900); page.keyboard.press("Space"); pause(page, 1500)
    page.locator(".noxOrder").first.click(); pause(page, 1300); page.locator("#tclose").click()

    # Briefly demonstrate team review without changing the required production route.
    page.locator("#bteam").click(); pause(page, 1200)
    page.locator("#hireNext").click(); pause(page, 700)
    page.locator("#viewProfile").click(); pause(page, 1200)
    page.locator("#profileBack").click(); page.locator("#hireClose").click()

    tool_index = {"twist": 0, "end": 1, "ball": 2}
    for job_number in range(1, 6):
        stand_by(page, "planning_desk")
        page.locator("#objectiveAction").click(); pause(page, 1100)

        cut_length = page.evaluate("state.job.stockLength")
        stand_by(page, "saw_t1")
        page.locator("#objectiveAction").click(); pause(page, 850)
        page.locator("#cutLength").evaluate("(e,v)=>{e.value=String(v);e.dispatchEvent(new Event('input'))}", cut_length)
        pause(page, 600); page.locator("#cutStock").click()
        page.evaluate("stationRuns().saw_t1.endAt=Date.now()-1;renderProductionHud()")
        page.locator("#sawFlag").click(); page.locator("#collectSawBlank").click()
        page.wait_for_function("state.rawStockReady && !document.querySelector('#task').classList.contains('open')")

        tool = page.evaluate("state.job.tool")
        target = page.evaluate("state.job.stickTarget")
        stand_by(page, "tool_cart")
        page.locator("#stationOpen").click(); pause(page, 850)
        page.locator(".toolbtn").nth(tool_index[tool]).click()
        page.locator("#stick").evaluate("(e,v)=>{e.value=String(v);e.dispatchEvent(new Event('input'))}", target)
        pause(page, 600); page.locator("#lockin").click()
        page.locator(".kitTool").first.wait_for()
        page.locator(".kitTool").first.click(); page.locator(".kitTool").nth(1).click(); pause(page, 700)
        page.locator("#installKit").click()
        page.wait_for_function("!document.querySelector('#task').classList.contains('open')")

        stand_by(page, "vmc_t2")
        page.locator("#objectiveAction").click(); pause(page, 950)
        for key, value in {"o": "54", "s": "03", "c": "08"}.items():
            page.locator(f'[data-code-key="{key}"][data-code-value="{value}"]').click(); pause(page, 300)
        page.locator("#cycst").click(); pause(page, 1300)
        page.evaluate("startAutonomousRun(state.job)")
        page.evaluate("state.machineRun.endAt=Date.now()-1;renderProductionHud()")
        page.locator("#machineFlag").click(); page.locator("#inspectPart").click(); page.locator("#inspectPart").click()
        page.locator("#tdone").wait_for(timeout=25000)
        pause(page, 1200); page.locator("#tdone").click(); pause(page, 1200)

    # Complete the expansion story and end on the larger Job Shop floor.
    for _ in range(3):
        pause(page, 1600); page.locator("#introNext").click()
    assert page.evaluate("map.id") == "bay_02"
    pause(page, 3500)
    assert not errors, errors

    video = page.video
    context.close()
    recorded = Path(video.path())
    browser.close()

raw_target = RAW_DIR / RAW_NAME
public_target = PUBLIC_DIR / RAW_NAME
shutil.copy2(recorded, raw_target)
shutil.copy2(recorded, public_target)

# Direct file navigation lets Chromium report the real recorded duration.
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(public_target.as_uri())
    page.wait_for_function("document.querySelector('video')?.duration > 0", timeout=30000)
    duration = page.evaluate("document.querySelector('video').duration")
    browser.close()

metadata = {"version": 3, "source": f"captures/{RAW_NAME}", "durationSeconds": duration, "durationFrames": round(duration * 30), "campaignScope": "Garage Bay through Job Shop expansion"}
(ROOT / "data/full-gameplay-video.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
print(f"PASS: recorded full current campaign to {public_target} ({duration:.1f} seconds)")
