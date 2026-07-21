"""Focused catalog/E2E gate for safe, facility-driven robotics progression."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
market = json.loads((ROOT / "data/equipment-market.json").read_text(encoding="utf-8"))
facilities = json.loads((ROOT / "data/facilities.json").read_text(encoding="utf-8"))["facilities"]
roster = json.loads((ROOT / "data/hiring-roster.json").read_text(encoding="utf-8"))["candidates"]

robot_ids = [
    "starter_tugger_agv",
    "amr_wip_fleet",
    "heavy_mobile_robot_platform",
    "humanoid_factory_assistant",
]
robots = [next(item for item in market["items"] if item["id"] == robot_id) for robot_id in robot_ids]
facility_by_chapter = {facility["chapter"]: facility for facility in facilities}
roster_roles = {candidate["role"] for candidate in roster}

assert [robot["chapter"] for robot in robots] == [2, 3, 4, 6]
assert [robot["unlockJobs"] for robot in robots] == sorted(robot["unlockJobs"] for robot in robots)
assert [robot["cost"] for robot in robots] == sorted(robot["cost"] for robot in robots)
assert [robot["maxOwned"] for robot in robots] == [1, 3, 4, 2]
for robot in robots:
    facility = facility_by_chapter[robot["minimumFacilityChapter"]]
    assert robot["facility"] == facility["name"].removeprefix("The ")
    assert set(robot["requiredDepartments"]) <= set(facility["departments"])
    assert robot["installSpaceSqFt"] * robot["maxOwned"] <= facility["robotLogisticsSpaceSqFt"]
    assert set(robot["requiredRoleIds"]) <= roster_roles
    assert robot["requiredSafety"]
    assert robot["requiresMaintenance"] is True
    assert len(robot["kidSummary"].split()) <= 24
    assert robot["status"] == "orientation"

assert "fixed marked path" in robots[0]["effect"]
assert all(department in robots[1]["requiredDepartments"] for department in [
    "receiving", "material_prep", "machining", "fabrication", "inspection", "assembly", "shipping"
])
assert "never replaces a qualified operator" in robots[-1]["effect"]
assert "supervised" in robots[-1]["spec"].lower()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded===total")
    page.evaluate("openEquipmentMarket()")
    assert page.locator("[data-equipment]").count() == 17
    for robot in robots:
        card = page.locator(f'[data-equipment="{robot["id"]}"]')
        assert card.count() == 1
        text = card.inner_text()
        assert robot["name"] in text
        assert robot["effect"] in text
        assert robot["spec"] in text
        assert f"CHAPTER {robot['chapter']}" in text
        assert "ORIENTATION" in text
        assert f"SHIP {robot['unlockJobs']} JOBS" in text
    assert not errors, errors
    browser.close()

print("PASS: facility growth -> capped AGV/AMR/platform/humanoid catalog -> realistic roles, routes, space, safety, maintenance, and prices")
