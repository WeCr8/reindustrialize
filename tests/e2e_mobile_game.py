"""Mobile-only E2E: responsive layout, touch controls, and the first production flow."""
import os
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = [
    ("small-portrait", 360, 800),
    ("modern-portrait", 390, 844),
    ("phone-landscape", 844, 390),
]
OUT = ROOT / "tmp" / "mobile-qa"
OUT.mkdir(parents=True, exist_ok=True)


def assert_no_horizontal_overflow(page, stage):
    overflow = page.evaluate(
        """() => ({
          viewport: innerWidth,
          root: document.documentElement.scrollWidth,
          body: document.body.scrollWidth,
          offenders: [...document.querySelectorAll('body *')]
            .filter(el => {
              const r = el.getBoundingClientRect();
              const s = getComputedStyle(el);
              return s.display !== 'none' && r.width > 0 && (r.left < -1 || r.right > innerWidth + 1);
            })
            .slice(0, 8)
            .map(el => ({id: el.id, cls: el.className, tag: el.tagName, rect: el.getBoundingClientRect().toJSON()}))
        })"""
    )
    assert overflow["root"] <= overflow["viewport"] + 1, f"{stage}: horizontal overflow {overflow}"
    assert overflow["body"] <= overflow["viewport"] + 1, f"{stage}: body overflow {overflow}"


def assert_action_in_viewport(page, selector, stage):
    result = page.locator(selector).evaluate(
        """el => {
          const r = el.getBoundingClientRect();
          return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height,
            viewportWidth:innerWidth,viewportHeight:innerHeight};
        }"""
    )
    assert result["width"] > 0 and result["height"] > 0, f"{stage}: action has no size {result}"
    assert result["top"] >= -1 and result["bottom"] <= result["viewportHeight"] + 1, f"{stage}: action below/above viewport {result}"
    assert result["left"] >= -1 and result["right"] <= result["viewportWidth"] + 1, f"{stage}: action outside viewport {result}"


def assert_gameplay_uses_viewport(page, stage):
    layout = page.evaluate(
        """() => {
          const rect = selector => document.querySelector(selector).getBoundingClientRect().toJSON();
          const intersects = (a,b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
          const dialogue=rect('#dlg'), objective=rect('#objectiveGuide');
          const prompt=document.querySelector('#stationPrompt').classList.contains('open') ? rect('#stationPrompt') : null;
          const controls=[...document.querySelectorAll('#pad b[data-d]')].map(el=>el.getBoundingClientRect().toJSON());
          return {
            viewport:{width:innerWidth,height:innerHeight},
            bodyHeight:document.body.scrollHeight,
            rootHeight:document.documentElement.scrollHeight,
            toolbar:rect('#bar'), canvas:rect('#cv'), dialogue, objective, prompt, controls,
            controlDialogueOverlap:controls.some(control=>intersects(control,dialogue)),
            objectiveDialogueOverlap:intersects(objective,dialogue)
          };
        }"""
    )
    height = layout["viewport"]["height"]
    minimum_canvas_ratio = 0.48 if layout["viewport"]["width"] > height else 0.42
    assert layout["rootHeight"] <= height + 1 and layout["bodyHeight"] <= height + 1, f"{stage}: game shell scrolls {layout}"
    assert layout["toolbar"]["height"] <= 42, f"{stage}: toolbar consumes playfield {layout}"
    assert layout["canvas"]["height"] >= height * minimum_canvas_ratio, f"{stage}: playfield is too small {layout}"
    assert layout["dialogue"]["height"] <= 94, f"{stage}: Zach text tray is too tall {layout}"
    assert layout["objective"]["height"] <= 64, f"{stage}: objective tray is too tall {layout}"
    assert not layout["prompt"] or layout["prompt"]["height"] <= 58, f"{stage}: station prompt covers too much playfield {layout}"
    assert not layout["controlDialogueOverlap"], f"{stage}: a thumb control covers Zach text {layout}"
    assert not layout["objectiveDialogueOverlap"], f"{stage}: objective and Zach text overlap {layout}"


def close_opening(page, name):
    for _ in range(4):
        assert_action_in_viewport(page, "#preFounderNext", f"{name}/prefounder-action")
        page.locator("#preFounderNext").tap()
    page.locator('[data-avatar="av_f_blonde_hd"]').tap()
    page.locator("#founderName").fill("MOBILE FOUNDER")
    page.locator("#companyName").fill("POCKET WORKS")
    page.locator('[data-control="auto"]').tap()
    page.locator("#newGame").tap()
    for _ in range(3):
        assert_action_in_viewport(page, "#introNext", f"{name}/intro-action")
        page.locator("#introNext").tap()
    page.locator("#btour").tap()
    page.locator("#tourNext").wait_for(timeout=10_000)
    for stop_number in range(3):
        assert_action_in_viewport(page, "#tourNext", f"{name}/tour-overview-action")
        if stop_number == 0:
            page.screenshot(path=OUT / f"{name}-tour-overview.png")
        page.locator("#tourNext").tap()
        assert_action_in_viewport(page, "#tourNext", f"{name}/tour-walkthrough-action")
        page.locator("#tourNext").tap()
        page.wait_for_function("document.querySelector('#task').dataset.tourPhase==='practice'")
        for _ in range(2):
            correct=page.evaluate("ONBOARDING_PRACTICE[SHOP_TOUR.stops[tourIndex].id][tourPracticeStep].correct")
            assert_action_in_viewport(page, f'.practiceChoice[data-choice="{correct}"]', f"{name}/tour-practice-action")
            if stop_number == 0 and page.evaluate("tourPracticeStep") == 0:
                page.screenshot(path=OUT / f"{name}-tour-practice.png")
            page.locator(".practiceChoice").nth(correct).tap();page.wait_for_timeout(650)
    page.evaluate("finishTour()")


env = dict(os.environ, PORT="8811")
server = subprocess.Popen(["node", "src/dev-server.js"], cwd=ROOT / "server", env=env)
try:
    time.sleep(0.8)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        results = []
        for name, width, height in VIEWPORTS:
            page = browser.new_page(
                viewport={"width": width, "height": height},
                is_mobile=True,
                has_touch=True,
                device_scale_factor=1,
            )
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.add_init_script("localStorage.setItem('reindustrialize.learnerMode','on')")
            page.goto("http://127.0.0.1:8811/game", wait_until="domcontentloaded")
            page.wait_for_function("typeof loaded !== 'undefined' && loaded === total")
            assert_no_horizontal_overflow(page, f"{name}/prefounder")
            close_opening(page, name)
            assert_no_horizontal_overflow(page, f"{name}/shop")
            assert_gameplay_uses_viewport(page, f"{name}/shop")
            assert page.locator("#pad").is_visible(), f"{name}: touch pad hidden"

            before = page.evaluate("P.x+','+P.y")
            direction = page.evaluate("Object.entries(DIRS).find(([k,d])=>!blocked(P.x+d[0],P.y+d[1]))[0]")
            page.locator(f'#pad [data-d="{direction}"]').dispatch_event("touchstart")
            page.locator(f'#pad [data-d="{direction}"]').dispatch_event("touchend")
            page.wait_for_function(f"P.x+','+P.y !== '{before}'")

            page.locator("#objectiveAction").tap()
            page.locator("#customers").wait_for(timeout=10_000)
            assert_no_horizontal_overflow(page, f"{name}/customer-intake")
            page.locator("#acceptContract").tap()
            page.locator("#introNext").wait_for(timeout=10_000)
            page.locator("#introNext").tap()
            page.locator("#introNext").tap()
            page.wait_for_function("document.querySelector('#intro').classList.contains('closed')")

            page.locator("#objectiveAction").tap()
            page.locator(".noxOrder").first.wait_for(timeout=10_000)
            assert_no_horizontal_overflow(page, f"{name}/material-order")
            page.locator(".noxOrder").first.tap()
            page.locator("#tclose").tap()
            page.locator("#introNext").wait_for(timeout=10_000)
            page.locator("#introNext").tap()
            page.wait_for_function("document.querySelector('#intro').classList.contains('closed')")

            page.evaluate("walkToStation('planning_desk')")
            page.wait_for_function("document.querySelector('#cv').dataset.nearStation === 'planning_desk'")
            page.locator("#stationOpen").tap()
            assert_no_horizontal_overflow(page, f"{name}/job-card")
            assert_gameplay_uses_viewport(page, f"{name}/station-open")
            page.screenshot(path=OUT / f"{name}-viewport.png")
            page.screenshot(path=OUT / f"{name}-full.png", full_page=True)
            assert not errors, f"{name}: page errors: {errors}"
            results.append(f"{name} {width}x{height}: touch movement + material order + station open")
            page.close()
        browser.close()
finally:
    server.terminate()
    server.wait(timeout=5)

print("PASS: " + " | ".join(results))
