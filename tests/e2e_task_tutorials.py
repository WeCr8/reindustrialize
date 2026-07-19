from pathlib import Path
from playwright.sync_api import sync_playwright
URL=(Path(__file__).resolve().parents[1]/"apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={"width":1440,"height":1000});errors=[];page.on("pageerror",lambda e:errors.append(str(e)));page.goto(URL);page.wait_for_function("loaded===total")
    for _ in range(4):page.locator("#preFounderNext").click()
    count=page.evaluate("PRODUCTION_TASK_TUTORIALS.length");assert count==9
    for index in range(count):
        guide=page.evaluate("i=>PRODUCTION_TASK_TUTORIALS[i]",index);page.evaluate("id=>showTaskGuide(id)",guide["id"])
        assert page.locator("#taskGuideModal").get_attribute("data-task-tutorial")==guide["id"]
        assert guide["text"] in page.locator("#taskGuideNarration").inner_text();assert guide["success"] in page.locator("#taskGuidePanel").inner_text()
        assert page.locator("#taskGuideSteps li").count()==len(guide["instructions"]);assert page.locator("#taskGuideImage").get_attribute("src").startswith("data:image/png;base64,")
        page.locator("#taskGuideClose").click()
    assert not errors,errors;browser.close()
print("PASS: 9 active production task guides render exact image/audio/text/instructions/status")
