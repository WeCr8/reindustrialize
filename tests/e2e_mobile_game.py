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


def close_opening(page):
    for _ in range(4):
        page.locator("#preFounderNext").tap()
    page.locator('[data-avatar="av_f_blonde_hd"]').tap()
    page.locator("#founderName").fill("MOBILE FOUNDER")
    page.locator("#companyName").fill("POCKET WORKS")
    page.locator('[data-control="auto"]').tap()
    page.locator("#newGame").tap()
    for _ in range(3):
        page.locator("#introNext").tap()
    page.locator("#tourNext").wait_for(timeout=10_000)
    for _ in range(3):
        page.locator("#tourNext").tap();page.locator("#tourNext").tap()
        page.wait_for_function("document.querySelector('#task').dataset.tourPhase==='practice'")
        for _ in range(2):
            correct=page.evaluate("ONBOARDING_PRACTICE[SHOP_TOUR.stops[tourIndex].id][tourPracticeStep].correct")
            page.locator(".practiceChoice").nth(correct).tap();page.wait_for_timeout(650)


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
            close_opening(page)
            assert_no_horizontal_overflow(page, f"{name}/shop")
            assert page.locator("#pad").is_visible(), f"{name}: touch pad hidden"

            before = page.evaluate("P.x+','+P.y")
            direction = page.evaluate("Object.entries(DIRS).find(([k,d])=>!blocked(P.x+d[0],P.y+d[1]))[0]")
            page.locator(f'#pad [data-d="{direction}"]').dispatch_event("touchstart")
            page.locator(f'#pad [data-d="{direction}"]').dispatch_event("touchend")
            page.wait_for_function(f"P.x+','+P.y !== '{before}'")

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
            controls_clear_dialogue = page.evaluate(
                """() => {
                  const a = document.querySelector('#pad').getBoundingClientRect();
                  const b = document.querySelector('#dlg').getBoundingClientRect();
                  return a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom;
                }"""
            )
            assert controls_clear_dialogue, f"{name}: touch controls overlap Zach's dialogue"
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
