"""E2E: click-to-walk, equipment approach/open, and manual cancellation."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto(URL)
    page.wait_for_function("loaded === total")
    for _ in range(4): page.locator("#preFounderNext").click()
    page.locator("#newGame").click()
    for _ in range(3):
        page.locator("#introNext").click()

    # Clicking a distant walkable floor tile follows a complete path, not one step.
    box = page.locator("#cv").bounding_box()
    cam = page.evaluate("({x:cam.x,y:cam.y,vw:VW,vh:VH})")
    floor_x, floor_y = 12, 9
    page.locator("#cv").click(position={
        "x": (floor_x - cam["x"] + 0.5) * box["width"] / cam["vw"],
        "y": (floor_y - cam["y"] + 0.5) * box["height"] / cam["vh"],
    })
    page.wait_for_function("P.x === 12 && P.y === 9 && moveTimer === null", timeout=10000)

    # Manual directional input takes control immediately and clears a queued route.
    page.evaluate("followPath(pathToTile(4, 8))")
    page.wait_for_timeout(180)
    page.keyboard.press("ArrowRight")
    assert page.evaluate("moveTimer === null && moveTarget === null")

    # Clicking the NOX equipment itself routes to a valid side and opens ordering.
    page.evaluate("walkToStation('nox_terminal', true)")
    page.locator(".noxOrder").first.wait_for(timeout=10000)
    assert page.locator("#ttitle").inner_text() == "NOX METALS — MATERIAL ORDERING"
    browser.close()

print("PASS: distant click-to-walk -> cancelable path -> equipment approach -> station opens")
