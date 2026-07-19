"""Zach mentor panel: contextual coaching, shop teaching, business guidance, imagery and voice."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/"apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={"width":1440,"height":1000})
    errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto(URL);page.wait_for_function("loaded === total")
    for _ in range(4): page.locator("#preFounderNext").click()
    page.locator("#newGame").click()
    for _ in range(5): page.locator("#introNext").click()
    page.locator("#tourSkip").wait_for(timeout=10000);page.locator("#tourSkip").click()
    page.locator("#askMentor").click()
    assert page.locator("#mentor").is_visible()
    assert page.locator(".mentorTab").count()==5
    assert page.locator("#mentorPortrait").get_attribute("src").startswith("data:image/png;base64,")
    assert "Order certified stock" in page.locator("#mentorAnswer").inner_text()
    page.locator('[data-c="machining"]').click()
    assert page.locator(".mentorQuestion").count()==3
    page.get_by_role("button",name="What should I check before cycle start?").click()
    assert "work offset" in page.locator("#mentorAnswer").inner_text()
    assert page.evaluate("zachAudio !== null")
    page.locator('[data-c="business"]').click()
    page.get_by_role("button",name="How should I price a job?").click()
    assert "overhead" in page.locator("#mentorAnswer").inner_text()
    page.locator("#mentorClose").click();assert not page.locator("#mentor").is_visible()
    assert not errors,errors;browser.close()
print("PASS: contextual Zach mentor -> machining questions -> business coaching -> image and voice")
