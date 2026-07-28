"""Validate the published responsive video library and player."""
from pathlib import Path
import subprocess
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
server = subprocess.Popen(["python", "-m", "http.server", "8792", "--bind", "127.0.0.1"], cwd=ROOT / "cloudflare-dist", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(0.6)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height in [(1440, 1000), (390, 844)]:
            page = browser.new_page(viewport={"width": width, "height": height})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto("http://127.0.0.1:8792/videos/", wait_until="domcontentloaded")
            assert page.locator(".card").count() == 11
            assert page.locator(".category h2").all_inner_texts() == ["CAMPAIGN AND FULL GAMEPLAY", "HORIZONTAL DEMOS", "VERTICAL SHORTS", "SQUARE SOCIAL"]
            for card in page.locator(".card").all():
                source = card.get_attribute("data-src")
                response = page.request.get("http://127.0.0.1:8792" + source)
                assert response.ok, source
            page.locator('[data-title="Campaign Film V8"]').click()
            assert page.locator("#player").is_visible()
            assert page.locator("#libraryVideo").evaluate("el => el.currentSrc.endsWith('/media/gameplay-hero-v8.mp4')")
            page.locator("#portrait").click()
            assert page.locator("#stage").evaluate("el => el.classList.contains('portrait')")
            assert page.locator("#libraryVideo").evaluate("el => !el.muted && el.volume === 1")
            page.locator("#landscape").click()
            assert not page.locator("#stage").evaluate("el => el.classList.contains('portrait')")
            assert page.locator("#libraryVideo").evaluate("el => !el.muted && el.volume === 1")
            assert page.locator("#fullscreen").is_visible()
            page.locator("#closePlayer").click()
            assert not page.locator("#player").is_visible()
            page.locator('[data-title="Founder Selection V2"]').click()
            assert page.locator("#stage").evaluate("el => el.classList.contains('portrait')")
            page.locator("#closePlayer").click()
            assert page.locator("body").evaluate("el => el.scrollWidth <= innerWidth")
            assert not errors, errors
            page.close()
        browser.close()
finally:
    server.terminate()
    server.wait(timeout=5)
print("PASS: 11 published videos, responsive library, portrait/landscape modal, and fullscreen control")
