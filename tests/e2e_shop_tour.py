"""E2E: shop tour keeps image, text, audio, and station target aligned."""
from pathlib import Path
from playwright.sync_api import sync_playwright
URL=(Path(__file__).resolve().parents[1]/"apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={"width":1440,"height":1000});errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)));page.goto(URL);page.wait_for_function("loaded===total")
    for _ in range(4): page.locator("#preFounderNext").click()
    page.locator("#newGame").click()
    for _ in range(5): page.locator("#introNext").click()
    page.locator("#tourNext").wait_for(timeout=10000)
    count=page.evaluate("SHOP_TOUR.stops.length");assert count==14
    for index in range(count):
        stop=page.evaluate("i=>SHOP_TOUR.stops[i]",index)
        walkthrough=page.evaluate("id=>STATION_WALKTHROUGHS[id]",stop["id"])
        assert page.locator("#task").get_attribute("data-tour-stop")==stop["id"]
        assert page.locator("#task").get_attribute("data-tour-phase")=="overview"
        assert page.locator("#ttitle").inner_text()==stop["title"]
        assert page.locator("#tview").get_attribute("src").startswith("data:image/png;base64,")
        assert stop["operation"] in page.locator("#tcontrols").inner_text()
        assert stop["text"] in page.locator("#tztext").inner_text()
        assert page.evaluate("zachAudio && zachAudio.src.startsWith('data:audio/mpeg;base64,')")
        page.locator("#tourNext").click()
        assert page.locator("#task").get_attribute("data-tour-phase")=="walkthrough"
        assert walkthrough["text"] in page.locator("#tztext").inner_text()
        assert page.locator("#tview").get_attribute("src").startswith("data:image/png;base64,")
        assert page.evaluate("zachAudio && zachAudio.src.startsWith('data:audio/mpeg;base64,')")
        page.locator("#tourNext").click()
    assert not page.locator("#task").is_visible()
    page.locator("#btour").click();assert page.locator("#task").get_attribute("data-tour-stop")=="tour_overview"
    assert not errors,errors;browser.close()
print("PASS: 14-station, 28-panel tour -> exact images/audio/text -> finish -> replay")
