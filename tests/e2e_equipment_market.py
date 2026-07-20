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
    assert cards.count() == 13
    for equipment in ["vmc", "cnc_lathe", "five_axis_vmc", "tig_manual", "robotic_tig", "surface_grinder", "polymer_print_farm", "metal_additive", "cmm", "xray"]:
        assert page.locator(f'[data-equipment="{equipment}"]').count() == 1
    assert page.locator(".equipmentProductArt").count() == 10
    assert "ORIENTATION · WORKFLOW ARRIVES WITH CHAPTER" in page.locator('[data-equipment="xray"]').inner_text()
    assert "SHIP 35 JOBS" in page.locator('[data-equipment="xray"]').inner_text()

    page.evaluate("state.jobsShipped=5;coins=100000;openEquipmentMarket()")
    page.locator('[data-equipment="tig_manual"] [data-buy-equipment]').click()
    assert page.evaluate("state.equipment.tig_manual") == 1
    assert "OWNED 1" in page.locator('[data-equipment="tig_manual"]').inner_text()
    page.set_viewport_size({"width": 390, "height": 844})
    page.evaluate("openEquipmentMarket()")
    assert page.locator("#storeCoach").is_visible()
    assert page.locator("#storeLessonNext").is_visible()
    assert page.locator("#equipmentMarket").evaluate("e=>e.scrollWidth<=innerWidth")
    assert not errors, errors
    browser.close()

print("PASS: portrait-scale founder selection -> 13-item aerospace equipment ladder -> gated purchase")
