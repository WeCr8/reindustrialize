"""Equipment store exposes a truthful aerospace progression and profile-scale founder art."""
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

    assert page.locator(".founderCardPortrait").count() == 10
    card_box = page.locator(".founderCardPortrait").first.bounding_box()
    assert card_box["height"] > card_box["width"]
    assert page.locator(".avatarChoice canvas").first.evaluate("e=>getComputedStyle(e).display") == "none"
    profile_box = page.locator("#founderProfile .atlasPortrait").bounding_box()
    assert profile_box["height"] >= 1.3 * profile_box["width"]

    page.evaluate("openEquipmentMarket()")
    assert "ZACH'S STORE WALKTHROUGH" in page.locator("#storeCoach").inner_text()
    assert "FIND THE BOTTLENECK" in page.locator("#storeCoach").inner_text()
    for lesson in ["CHECK THE WHOLE COST", "PROVE THE PROCESS", "MOVE AT THE RIGHT TIME"]:
        page.locator("#storeLessonNext").click()
        assert lesson in page.locator("#storeCoach").inner_text()
    assert "NEXT THE JOB SHOP 12,000 SQ FT" in page.locator("#storeCoach").inner_text()
    page.locator("#storeFacilityRoadmap").click()
    assert page.locator("#campaign").is_visible()
    assert page.locator(".chapterCard").count() == 6
    page.locator("#campaignClose").click()
    page.evaluate("openEquipmentMarket()")
    cards = page.locator("[data-equipment]")
    assert cards.count() == 17
    for equipment in ["vmc", "cnc_lathe", "five_axis_vmc", "tig_manual", "robotic_tig", "surface_grinder", "polymer_print_farm", "metal_additive", "cmm", "xray", "starter_tugger_agv", "amr_wip_fleet", "heavy_mobile_robot_platform", "humanoid_factory_assistant"]:
        assert page.locator(f'[data-equipment="{equipment}"]').count() == 1
    assert page.locator(".equipmentProductArt").count() == 17
    assert "ORIENTATION · WORKFLOW ARRIVES WITH CHAPTER" in page.locator('[data-equipment="xray"]').inner_text()
    assert "SHIP 35 JOBS" in page.locator('[data-equipment="xray"]').inner_text()
    assert "MAINTENANCE TECHNICIAN REQUIRED" in page.locator('[data-equipment="xray"]').inner_text()

    page.evaluate("gameStarted=true;setMap('bay_02');state.jobsShipped=5;coins=100000;openEquipmentMarket()")
    assert page.locator('[data-equipment="tig_manual"] [data-buy-equipment]').is_disabled()
    assert "HIRE 3 MORE EMPLOYEES" in page.locator('[data-equipment="tig_manual"]').inner_text()
    assert page.evaluate("coins") == 100000
    page.evaluate("workers.push(...HIRE_ROSTER.candidates.slice(0,3).map((candidate,index)=>({id:candidate.id,candidate,x:index,y:0,assignment:null,status:'MEANDERING'})));openEquipmentMarket()")
    assert page.locator('[data-equipment="tig_manual"] [data-buy-equipment]').inner_text() == "BUY FOR 6500 COINS"
    page.locator('[data-equipment="tig_manual"] [data-buy-equipment]').click()
    assert page.evaluate("state.equipment.tig_manual") == 1
    assert page.evaluate("coins") == 93500
    assert "OWNED 1" in page.locator('[data-equipment="tig_manual"]').inner_text()
    assert page.locator('[data-equipment="tig_manual"] [data-buy-equipment]').inner_text() == "BUY FOR 13000 COINS"
    page.locator('[data-equipment="tig_manual"] [data-buy-equipment]').click()
    assert page.evaluate("state.equipment.tig_manual") == 2
    assert page.evaluate("coins") == 80500
    assert page.evaluate("JSON.parse(localStorage.getItem('reindustrialize.save.v1')).state.equipment.tig_manual") == 2
    page.set_viewport_size({"width": 390, "height": 844})
    page.evaluate("openEquipmentMarket()")
    assert page.locator("#storeCoach").is_visible()
    assert page.locator("#storeLessonNext").is_visible()
    assert page.locator("#equipmentMarket").evaluate("e=>e.scrollWidth<=innerWidth")
    assert not errors, errors
    browser.close()

print("PASS: portraits -> 17-item store -> staffing locks -> exact escalating spend -> saved ownership")
