import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
market = json.loads((ROOT / "data/equipment-market.json").read_text(encoding="utf-8"))
damage = json.loads((ROOT / "data/equipment-damage-states.json").read_text(encoding="utf-8"))
expected = {item["id"] for item in market["items"]}
states = {item["equipment"]: item for item in damage["states"]}
assert set(states) == expected
for key, atlas in damage["atlases"].items():
    path = ROOT / "packages/assets/equipment" / f"{atlas['asset']}.png"
    assert path.exists() and path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", (key, path)
for item in states.values():
    atlas = damage["atlases"][item["atlas"]]
    assert 0 <= item["cell"] < atlas["columns"] * atlas["rows"]
    assert item["fault"] and item["qualifiedRoles"]

url = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(url)
    page.wait_for_function("loaded===total")
    page.evaluate("""() => {
      gameStarted=true;document.getElementById('preFounder').classList.add('closed');document.getElementById('titleScreen').classList.add('closed');document.getElementById('intro').classList.add('closed');
      state.job=JOBS[0];state.rawStockReady=true;state.toolReady=true;state.toolsSet=['end','probe','chamfer'];maintenanceState().condition=15;openVmcTask();
    }""")
    view = page.locator("#equipmentDamageView")
    assert view.is_visible()
    assert "vmc damaged state" in view.get_attribute("aria-label")
    assert page.evaluate("document.getElementById('equipmentDamageView').style.backgroundImage.includes(assetUrl(EQUIPMENT_VIEWS['garage-equipment-damaged-atlas-v1']))")
    assert not errors, errors
    browser.close()

print("PASS: all 17 store equipment types map to repairable damage art; live VMC lockout renders its damaged state")
