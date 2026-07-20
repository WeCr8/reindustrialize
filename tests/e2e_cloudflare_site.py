from pathlib import Path
import os
import subprocess
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
external_url = os.environ.get("PLAYREIND_TEST_URL")
server = None
if external_url:
    URL = external_url
else:
    URL = "http://127.0.0.1:8790"
    server = subprocess.Popen(["python", "-m", "http.server", "8790", "--bind", "127.0.0.1"], cwd=ROOT / "cloudflare-dist", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.6)
try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        desktop = browser.new_page(viewport={"width": 1440, "height": 1000})
        errors = []
        desktop.on("pageerror", lambda error: errors.append(str(error)))
        desktop.goto(URL, wait_until="domcontentloaded", timeout=90000)
        assert desktop.locator('script[src="https://www.googletagmanager.com/gtag/js?id=G-KRCJP5MHXH"]').count() == 1
        desktop.wait_for_function("typeof gtag === 'function' && Array.isArray(dataLayer)", timeout=30000)
        assert desktop.evaluate("typeof gtag === 'function' && Array.isArray(dataLayer)")
        if desktop.locator("#privacyConsent").is_visible():
            desktop.locator("[data-consent='declined']").click()
        headline = desktop.locator("h1").inner_text().lower()
        assert "factory doesn't" in headline and "build itself" in headline
        assert desktop.locator("video, .videoFallback").first.is_visible()
        if desktop.locator("video").count():
            assert desktop.locator("video track[kind='captions'][default]").count() == 1
            assert "gameplay-hero-v8.mp4" in desktop.locator("video").evaluate("el => el.currentSrc")
            assert desktop.locator("#soundBeacon").is_visible()
            desktop.locator("#soundBeacon").click()
            desktop.wait_for_timeout(1200)
            assert desktop.locator("video").evaluate("el => !el.muted && !el.paused && el.readyState >= 3")
            assert desktop.locator("#hero").evaluate("el => el.classList.contains('filmMode')")
            assert desktop.locator(".heroContent").evaluate("el => getComputedStyle(el).visibility === 'hidden'")
            desktop.locator("#portraitMode").click()
            assert desktop.locator("#hero").evaluate("el => el.classList.contains('portrait')")
            desktop.locator("#landscapeMode").click()
            assert not desktop.locator("#hero").evaluate("el => el.classList.contains('portrait')")
            desktop.locator("#filmExit").click()
            assert not desktop.locator("#hero").evaluate("el => el.classList.contains('filmMode')")
        assert desktop.locator("a[href='/game/']").count() >= 3
        assert desktop.locator(".hero").bounding_box()["y"] < 80
        assert desktop.locator(".proof span").count() == 3
        assert "first playable alpha" in desktop.locator("body").inner_text().lower()
        assert desktop.locator(".step").count() == 4
        assert desktop.locator(".characterCard").count() == 6
        assert desktop.locator("[data-role-filter]").count() == 4
        assert desktop.locator(".gameShot img").count() == 4
        desktop.wait_for_function("[...document.querySelectorAll('.gameShot img')].every(image => image.complete && image.naturalWidth > 0)")
        desktop.locator('[data-role-filter="maintenance"]').click()
        assert desktop.locator('.characterCard:not([hidden])').count() == 2
        assert all(desktop.locator('.characterCard:not([hidden])').nth(index).get_attribute('data-role') == 'maintenance' for index in range(2))
        desktop.locator('[data-role-filter="all"]').click()
        desktop.locator(".gameProof").scroll_into_view_if_needed()
        desktop.locator(".gameShot").last.scroll_into_view_if_needed()
        desktop.wait_for_function("Promise.all([...document.querySelectorAll('.gameShot img')].map(image => image.decode()))")
        desktop.screenshot(path=ROOT / "tmp" / "playreind-landing-desktop.png", full_page=True)
        desktop.locator("a[href='/game/']").first.click()
        desktop.wait_for_url("**/game/")
        desktop.wait_for_function("loaded===total")
        assert desktop.locator("#preFounder").is_visible()
        assert desktop.locator("#preFounderArt").evaluate("el => el.naturalWidth > 0")
        assert not errors, errors

        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        mobile.goto(URL, wait_until="domcontentloaded", timeout=90000)
        if mobile.locator("#privacyConsent").is_visible():
            mobile.locator("[data-consent='declined']").click()
        assert mobile.locator("h1").is_visible()
        assert mobile.locator("a[href='/game/']").first.is_visible()
        assert mobile.locator(".hero").is_visible()
        assert mobile.locator("#soundBeacon").is_visible()
        assert mobile.locator("body").evaluate("el => el.scrollWidth <= innerWidth")
        mobile.locator("#people").scroll_into_view_if_needed()
        assert mobile.locator(".characterCard").first.is_visible()
        assert mobile.locator(".gameShot img").first.is_visible()
        mobile.locator(".gameShot").last.scroll_into_view_if_needed()
        mobile.wait_for_function("Promise.all([...document.querySelectorAll('.gameShot img')].map(image => image.decode()))")
        mobile.locator("#soundBeacon").click()
        mobile.locator("#portraitMode").click()
        assert mobile.locator("#hero").evaluate("el => el.classList.contains('filmMode') && el.classList.contains('portrait')")
        assert mobile.locator("#fullScreen").is_visible()
        mobile.locator("#filmExit").click()
        mobile.screenshot(path=ROOT / "tmp" / "playreind-landing-mobile.png", full_page=True)
        browser.close()
finally:
    if server:
        server.terminate()
        server.wait(timeout=5)
print("PASS: Cloudflare landing desktop/mobile -> /game/ -> opening art and runtime assets")
