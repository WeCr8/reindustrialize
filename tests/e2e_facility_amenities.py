"""Validate later-chapter amenity placement and safe maintenance-event rules."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
events = json.loads((ROOT / "data/facility-amenity-events.json").read_text())
bay = json.loads((ROOT / "data/maps/bay_02.json").read_text())
roster = json.loads((ROOT / "data/hiring-roster.json").read_text())
facilities = json.loads((ROOT / "data/facilities.json").read_text())["facilities"]

station = next(item for item in events["stations"] if item["id"] == "restroom_station")
location = next(item for item in bay["facilityAmenities"] if item["id"] == station["id"])
incident = next(item for item in events["events"] if item["id"] == "clogged_restroom")

assert station["firstFacility"] == "job_shop" and station["orientationOnly"] is False
assert location["status"] == "playable"
assert any(p["sprite"] == "restroom_station" for p in bay["placements"])
x, y = location["tile"]
w, h = location["footprint"]
assert x >= 0 and y >= 0 and x + w <= bay["size"][0] and y + h <= bay["size"][1]

assert incident["minimumChapter"] == 2
assert "garage_bay" not in incident["eligibleFacilities"]
assert incident["eligibleFacilities"] == [f["id"] for f in facilities if f["chapter"] >= 2]
assert incident["rarity"]["class"] == "rare"
assert 0 < incident["rarity"]["chancePerEligibleShift"] <= 0.02
assert incident["rarity"]["minimumShiftsBetweenOccurrences"] >= 20

expected = ["isolate", "post_sign", "clear", "sanitize", "reopen"]
assert [step["action"] for step in incident["responseSequence"]] == expected
assert [step["order"] for step in incident["responseSequence"]] == list(range(1, 6))
assert incident["requiredWorker"]["qualification"] == station["id"]
qualified = [c for c in roster["candidates"] if c["role"] in incident["requiredWorker"]["rolesAnyOf"] and station["id"] in c["qualifications"]]
assert qualified, "At least one Job Shop worker must be qualified for the amenity response"
assert all(c["unlocksAtFacility"] != "garage_bay" for c in qualified)

consequences = incident["consequences"]
assert consequences["onTrigger"]["stationAvailability"] == "unavailable"
assert consequences["resolvedCorrectly"]["stationAvailability"] == "available"
assert consequences["resolvedWithoutQualifiedWorker"]["allowed"] is False
assert consequences["ignoredForOneShift"]["cashCost"] > consequences["resolvedCorrectly"]["cashCost"]
assert consequences["ignoredForOneShift"]["morale"] < consequences["onTrigger"]["morale"] < 0
assert len(incident["completionEvidence"]) == len(expected)

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
      setMap('bay_02');state.jobsShipped=8;coins=10000;addCoins(0);openRestroomTask();
    }""")
    assert page.locator("#restroomTaskView").is_visible()
    page.locator("#reportRestroomIssue").click()
    assert "STEP 1 OF 5" in page.locator("#tcontrols").inner_text()
    page.locator("#advanceFacilityRepair").click()
    page.locator("#advanceFacilityRepair").click()
    assert page.locator("#hireFacilityTech").is_visible()
    page.evaluate("""() => {const candidate=HIRE_ROSTER.candidates.find(c=>c.id==='taylor_morgan');hired.add(candidate.id);workers.push({id:candidate.id,candidate,x:P.x,y:P.y,assignment:'restroom_station',status:'WORKING',nextMove:0,workPulse:0});openRestroomTask();}""")
    before = page.evaluate("coins")
    page.locator("#advanceFacilityRepair").click()
    assert page.evaluate("coins") == before - 450
    page.locator("#advanceFacilityRepair").click()
    page.locator("#advanceFacilityRepair").click()
    assert page.evaluate("restroomState().status") == "available"
    assert page.evaluate("JSON.parse(localStorage.getItem(SAVE_KEY)).state.facilityAmenities.restroom.status") == "available"
    assert not errors, errors
    browser.close()

print("PASS: playable Job Shop restroom -> rare incident -> qualified five-step repair -> exact cost/morale/saved availability")
