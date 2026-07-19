"""Verify one-time Chapter 1 milestone stories are playable and retain exact captions."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded === total")
    page.evaluate("""() => {
      gameStarted=true;
      voiceEnabled=false;
      document.querySelector('#preFounder').classList.add('closed');
      document.querySelector('#titleScreen').classList.add('closed');
      document.querySelector('#intro').classList.add('closed');
    }""")

    def verify(sequence: str):
        assert page.evaluate("id => showStorySequence(id)", sequence)
        expected = page.evaluate("id => STORY_PRODUCTION.sequences[id].map(x => x.text)", sequence)
        for index, caption in enumerate(expected):
            assert page.locator("#introText").inner_text() == caption
            assert page.locator("#intro").get_attribute("data-story-beat")
            page.locator("#introNext").click()
            if index < len(expected) - 1:
                page.wait_for_function("i => introStep === i", arg=index + 1)
        assert "closed" in (page.locator("#intro").get_attribute("class") or "")
        assert not page.evaluate("id => showStorySequence(id)", sequence)

    for milestone in ["first_customer", "nox_delivery", "first_verified_article", "first_hire"]:
        verify(milestone)

    page.evaluate("showExpansion()")
    graduation_pages = page.evaluate("introPages.length")
    assert graduation_pages == 5
    assert page.locator("#intro").get_attribute("data-story-beat") == "garage_graduation_proof"
    for _ in range(graduation_pages):
        page.locator("#introNext").click()
    page.wait_for_function("map && map.id === 'bay_02'")
    seen = page.evaluate("state.storySequences")
    assert "garage_graduation" in seen and "job_shop_expansion" in seen
    assert not errors, errors
    browser.close()

print("PASS: five Chapter 1 milestone stories play once, captions match, and graduation enters Bay 02")
