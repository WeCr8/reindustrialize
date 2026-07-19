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
        desktop.goto(URL, wait_until="networkidle")
        assert desktop.locator('script[src="https://www.googletagmanager.com/gtag/js?id=G-KRCJP5MHXH"]').count() == 1
        assert desktop.evaluate("typeof gtag === 'function' && Array.isArray(dataLayer)")
        assert "outgrow it" in desktop.locator("h1").inner_text().lower()
        assert desktop.locator("video, .videoFallback").first.is_visible()
        if desktop.locator("video").count():
            assert desktop.locator("video track[kind='captions'][default]").count() == 1
            assert "gameplay-demo-v6.mp4" in desktop.locator("video").evaluate("el => el.currentSrc")
        assert desktop.locator("a[href='/game/']").count() >= 3
        assert desktop.locator(".heroMedia").bounding_box()["y"] < 800
        assert desktop.locator(".proof span").count() == 4
        assert "first playable alpha" in desktop.locator("body").inner_text().lower()
        assert "planned" in desktop.locator(".route").inner_text().lower()
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
        assert mobile.locator(".heroMedia").is_visible()
        assert mobile.locator("body").evaluate("el => el.scrollWidth <= innerWidth")
        mobile.screenshot(path=ROOT / "tmp" / "playreind-landing-mobile.png", full_page=True)
        browser.close()
finally:
    if server:
        server.terminate()
        server.wait(timeout=5)
print("PASS: Cloudflare landing desktop/mobile -> /game/ -> opening art and runtime assets")
