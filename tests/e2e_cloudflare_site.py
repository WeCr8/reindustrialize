from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = os.environ.get("PLAYREIND_TEST_URL", "http://127.0.0.1:8790")
with sync_playwright() as p:
    browser = p.chromium.launch()
    desktop = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    desktop.on("pageerror", lambda error: errors.append(str(error)))
    desktop.goto(URL, wait_until="networkidle")
    assert "industrial powerhouse" in desktop.locator("h1").inner_text().lower()
    assert desktop.locator("video").is_visible()
    assert desktop.locator("a[href='/game/']").count() >= 3
    desktop.screenshot(path=ROOT / "tmp" / "playreind-landing-desktop.png", full_page=True)
    desktop.locator("a[href='/game/']").first.click()
    desktop.wait_for_url("**/game/")
    desktop.wait_for_function("loaded===total")
    assert desktop.locator("#preFounder").is_visible()
    assert desktop.locator("#preFounderArt").evaluate("el => el.naturalWidth > 0")
    assert not errors, errors

    mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    mobile.goto(URL, wait_until="networkidle")
    assert mobile.locator("h1").is_visible()
    assert mobile.locator("a[href='/game/']").first.is_visible()
    mobile.screenshot(path=ROOT / "tmp" / "playreind-landing-mobile.png", full_page=True)
    browser.close()
print("PASS: Cloudflare landing desktop/mobile -> /game/ -> opening art and runtime assets")
