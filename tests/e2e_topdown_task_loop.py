"""Validate the original proximity-task loop and control readability."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded===total")
    for _ in range(4): page.locator("#preFounderNext").click()
    page.locator("#newGame").click()
    for _ in range(5): page.locator("#introNext").click()
    page.locator("#tourSkip").wait_for(timeout=10000)
    page.locator("#tourSkip").click()

    page.keyboard.press("Space")
    assert page.locator("#cv").get_attribute("data-interaction") == "too-far"
    assert "open" not in (page.locator("#task").get_attribute("class") or "")

    page.evaluate("P.x=1;P.y=1;P.rx=1;P.ry=1;P.fromX=1;P.fromY=1;move(-1,0)")
    assert page.locator("#cv").get_attribute("data-move-result") == "blocked"
    assert page.evaluate("[P.x,P.y]") == [1, 1]

    # Running has a distinct state, faster interpolation, and two-frame founder cadence.
    page.evaluate("setMap('bay_01'); const d=pathToStation('nox_terminal')[0]; move(d[0],d[1],false,true)")
    assert page.locator("#cv").get_attribute("data-move-speed") == "run"
    assert page.evaluate("P.running && P.moveDuration===82")
    page.wait_for_function("document.querySelector('#cv').dataset.motion==='running'", timeout=2000)
    assert page.evaluate("Object.values(SCENE_MANIFEST.founders).length===10 && Object.keys(SCENE_MANIFEST.founders).every(id=>ATLAS[id].frames>=2)")

    page.evaluate("walkToStation('nox_terminal')")
    page.wait_for_function("document.querySelector('#cv').dataset.nearStation==='nox_terminal'", timeout=10000)
    assert page.locator("#stationPrompt").is_visible()
    assert "USE" in page.locator("#stationPromptText").inner_text()
    page.keyboard.press("Space")
    page.locator(".noxOrder").first.wait_for(timeout=10000)
    assert page.locator("#cv").get_attribute("data-interaction") == "nox_terminal"
    assert "MATERIAL ORDERING" in page.locator("#ttitle").inner_text()
    assert not errors, errors
    browser.close()

print("PASS: top-down movement -> collision -> proximity highlight -> USE action -> station task")
