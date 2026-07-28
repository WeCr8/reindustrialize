import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
market = json.loads((ROOT / "data/equipment-market.json").read_text(encoding="utf-8"))
operating = json.loads((ROOT / "data/equipment-operating-profiles.json").read_text(encoding="utf-8"))
robotics = json.loads((ROOT / "data/robotics-sprite-profiles.json").read_text(encoding="utf-8"))
assert {item["id"] for item in market["items"]} == {profile["equipment"] for profile in operating["profiles"]}
for profile in operating["profiles"]:
    assert profile["realSetup"] and profile["realCycle"] and profile["capacity"]
    assert 0 < profile["gameCycleSeconds"][0] <= profile["gameCycleSeconds"][1]
    assert set(profile["stats"]) >= {"speed", "precision", "flexibility", "spaceEfficiency", "maintenanceComplexity"}
    assert all(1 <= value <= 5 for value in profile["stats"].values())
    assert len(profile["dependencies"]) >= 3
for profile in robotics["platforms"]:
    assert profile["fps"] == 8 and profile["frames"]
    sprite = ROOT / "packages/assets/sprites" / f"{profile['spriteAtlas']}.png"
    assert sprite.exists() and sprite.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
profile_image = ROOT / "packages/assets/equipment/humanoid-assistant-profile-v1.png"
assert profile_image.exists() and profile_image.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"

url = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(url)
    page.wait_for_function("loaded===total")
    page.evaluate("gameStarted=true;state.jobsShipped=60;coins=1000000;openEquipmentMarket()")
    assert page.locator(".operatingProfileButton").count() == 17
    page.locator('[data-equipment="saw"] .operatingProfileButton').click()
    assert "REAL SETUP" in page.locator("#operatingProfileBody").inner_text()
    assert "8–16 SECONDS" in page.locator("#operatingProfileBody").inner_text()
    page.locator("#operatingProfileClose").click()
    assert page.locator('[data-robot="starter_tugger_agv"]').is_visible()
    assert page.locator('[data-robot="amr_wip_fleet"]').is_visible()
    assert page.locator('[data-robot="humanoid_factory_assistant"]').is_visible()
    first_position = page.locator('[data-robot="humanoid_factory_assistant"]').evaluate("node => node.style.backgroundPosition")
    page.wait_for_timeout(160)
    second_position = page.locator('[data-robot="humanoid_factory_assistant"]').evaluate("node => node.style.backgroundPosition")
    assert first_position != second_position
    page.get_by_text("VIEW SUPERVISED HUMANOID ASSISTANT PROFILE").click()
    assert page.locator('#robotProfile img[alt="Supervised Humanoid Assistant profile"]').is_visible()
    assert "NOT APPROVED" in page.locator("#robotProfileBody").inner_text()
    assert not errors, errors
    browser.close()

print("PASS: all 17 store assets expose stats/capacity/real+game cycle time; AGV/AMR/humanoid previews animate at 8 FPS")
