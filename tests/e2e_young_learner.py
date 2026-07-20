"""A first-time young learner can reach the shop through three forgiving lessons."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL=(Path(__file__).resolve().parents[1]/"apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={"width":1024,"height":768});errors=[]
    page.on("pageerror",lambda error:errors.append(str(error)))
    page.add_init_script("localStorage.setItem('reindustrialize.learnerMode','on')")
    page.goto(URL);page.wait_for_function("loaded===total")
    assert "GUIDED LEARNER HELP: ON" in page.locator("#learnerMode").inner_text()
    for _ in range(4): page.locator("#preFounderNext").click()
    page.locator("#newGame").click()
    for _ in range(3): page.locator("#introNext").click()
    page.locator("#tourNext").wait_for(timeout=10000)
    assert page.evaluate("tourIndex") == 2
    expected=["tour_material","tour_saw","tour_vmc"]
    for stop_id in expected:
        assert page.locator("#task").get_attribute("data-tour-stop")==stop_id
        page.locator("#tourNext").click();page.locator("#tourNext").click()
        page.wait_for_function("document.querySelector('#task').dataset.tourPhase==='practice'")
        wrong=page.evaluate("(ONBOARDING_PRACTICE[SHOP_TOUR.stops[tourIndex].id][tourPracticeStep].correct+1)%3")
        page.locator(".practiceChoice").nth(wrong).click()
        assert page.locator(".practiceChoice.answerHint").count()==1
        for _ in range(2):
            correct=page.evaluate("ONBOARDING_PRACTICE[SHOP_TOUR.stops[tourIndex].id][tourPracticeStep].correct")
            page.locator(".practiceChoice").nth(correct).click();page.wait_for_timeout(650)
    assert page.locator("#task").get_attribute("data-tour-phase")=="complete"
    page.locator("#openEquipmentMarket").click(force=True)
    assert "SHIP 2 JOBS TO REVEAL" in page.locator("#equipmentMarketBody").inner_text()
    assert not errors,errors
    browser.close()
print("PASS: guided young learner completes 3-stop starter route with recovery hints and staged equipment store")
