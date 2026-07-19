"""Deterministic screenshot source for the Remotion gameplay demo."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v2"
OUT = ROOT / "tmp" / "demo" / VERSION / "screens"
PUBLIC = ROOT / "demo" / "remotion" / "public" / "screens" / VERSION
OUT.mkdir(parents=True, exist_ok=True)
PUBLIC.mkdir(parents=True, exist_ok=True)
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

def shot(page, order, name):
    filename = f"{order:02d}-{name}-{VERSION}.png"
    page.screenshot(path=OUT / filename)
    page.screenshot(path=PUBLIC / filename)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded === total")
    for _ in range(4): page.locator("#preFounderNext").click()
    shot(page, 1, "title-and-company-creation")
    page.locator('[data-avatar="av_f_middle_eastern_hd"]').click()
    page.locator("#founderName").fill("YOUR FOUNDER")
    page.locator("#companyName").fill("YOUR FACTORY")
    shot(page, 2, "ten-founder-selection")
    page.locator("#newGame").click()
    shot(page, 3, "zach-founding-story")
    for _ in range(5): page.locator("#introNext").click()
    page.locator("#tourSkip").wait_for(timeout=10000)
    page.locator("#tourSkip").click()
    page.evaluate("const d=pathToStation('nox_terminal')[0];move(d[0],d[1],false,true)")
    page.wait_for_function("document.querySelector('#cv').dataset.motion==='running'")
    shot(page, 4, "founder-running-shop-floor")
    page.evaluate("walkToStation('nox_terminal')")
    page.wait_for_function("document.querySelector('#cv').dataset.nearStation==='nox_terminal'", timeout=10000)
    shot(page, 5, "playable-shop-objectives")
    page.evaluate("openNoxOrder()")
    shot(page, 6, "nox-material-ordering")
    page.locator("#tclose").click()
    page.evaluate("openOverlay('EQUIPMENT VIEW — CNC MILL', 'OPEN STATIONS TO RUN REAL TASKS');showEquipmentView('vmc-t2-open-v1')")
    shot(page, 7, "cnc-equipment-view")
    page.locator("#tclose").click()
    page.locator("#bteam").click()
    shot(page, 8, "hire-your-team")
    page.locator("#hireClose").click()
    page.evaluate("showExpansion()")
    shot(page, 9, "factory-expansion")
    assert not errors, errors
    browser.close()
print(f"PASS: captured 9 versioned demo screenshots in {OUT} and {PUBLIC}")
