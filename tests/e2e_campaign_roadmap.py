"""Campaign screen must show honest chapter availability and final growth scale."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL=(Path(__file__).resolve().parents[1]/"apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={"width":1440,"height":1000});errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)));page.goto(URL);page.wait_for_function("loaded===total")
    for _ in range(4):page.locator("#preFounderNext").click()
    page.locator("#newGame").click()
    for _ in range(3):page.locator("#introNext").click()
    page.locator("#tourNext").wait_for(timeout=10000);page.evaluate("tourMandatory=false;finishTour()")
    page.locator("#bcampaign").click()
    cards=page.locator(".chapterCard")
    assert cards.count()==6
    assert "PLAYABLE" in cards.nth(0).inner_text()
    assert "IN DEVELOPMENT" in cards.nth(1).inner_text()
    for index in range(2,6):assert "LOCKED" in cards.nth(index).inner_text()
    assert "2,400 SQ FT" in cards.nth(0).inner_text()
    assert "1,000,000 SQ FT" in cards.nth(5).inner_text()
    assert page.evaluate("CHAPTER_PROGRESSION.campaignTime.mainStoryPlayerHours.join('-')") == "25-35"
    assert page.evaluate("CHAPTER_PROGRESSION.campaignTime.completionistPlayerHours.join('-')") == "40-55"
    assert "family-friendly" in page.evaluate("CHAPTER_PROGRESSION.audienceDifficultyRule.chapters1To2")
    assert page.evaluate("CHAPTER_PROGRESSION.easterEggs.total") == 24
    assert not errors,errors;browser.close()
print("PASS: campaign screen -> 6 chapters -> honest playable/development/locked states -> final scale")
