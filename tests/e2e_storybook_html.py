from pathlib import Path
import os
import subprocess
import time

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
external = os.environ.get("PLAYREIND_TEST_URL")
URL = (external.rstrip("/") + "/storybook/") if external else "http://127.0.0.1:8794/storybook/v1/"
server = None
if not external:
    server = subprocess.Popen(
        ["python", "-m", "http.server", "8794", "--bind", "127.0.0.1"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.6)

try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_function("BOOK.slides.length === 238")
        assert page.locator('[data-view="slides"]').evaluate("el => el.classList.contains('active')")
        assert page.evaluate("BOOK.slides.filter(s => s.section === 'Station Missions & Timers').length") == 18
        assert "5 minutes" in page.evaluate("BOOK.slides.find(s => s.location === 'saw_t1').instructions.join(' ')")
        assert "10 minutes" in page.evaluate("BOOK.slides.find(s => s.location === 'vmc_t2').instructions.join(' ')")
        employee_slide = page.evaluate("BOOK.slides.find(s => s.section === 'Factory Workforce').number")
        page.goto(URL + f"?view=slides&slide={employee_slide}", wait_until="domcontentloaded")
        assert page.locator(".profileCrop").count() == 1
        assert page.locator(".spriteCrop").count() == 1
        profile_image = page.locator(".profileCrop").evaluate("el => getComputedStyle(el).backgroundImage")
        sprite_image = page.locator(".spriteCrop").evaluate("el => getComputedStyle(el).backgroundImage")
        assert profile_image != "none" and sprite_image != "none" and profile_image != sprite_image
        page.screenshot(path=ROOT / "tmp" / "storybook-employee-desktop.png")
        voiced_slide = page.evaluate("BOOK.slides.find(s => s.voiceSrc).number")
        page.goto(URL + f"?view=slides&slide={voiced_slide}", wait_until="domcontentloaded")
        page.locator("audio.voice").evaluate("audio => audio.load()")
        page.wait_for_function("document.querySelector('audio.voice').readyState >= 1")
        page.screenshot(path=ROOT / "tmp" / "storybook-slide-desktop.png")

        page.locator('[data-view="assets"]').click()
        assert page.locator(".assetCard").count() == 357
        assert page.locator(".assetCard img").count() == 106
        assert page.locator(".assetCard audio").count() == 251
        page.locator("#assetKind").select_option("graphic")
        assert page.locator(".assetCard:not(.hidden)").count() == 106
        page.locator("#assetSearch").fill("maintenance-team")
        assert 1 <= page.locator(".assetCard:not(.hidden)").count() <= 10
        page.wait_for_function("[...document.querySelectorAll('.assetCard:not(.hidden) img')].every(image => image.complete && image.naturalWidth > 0)")
        page.screenshot(path=ROOT / "tmp" / "storybook-assets-desktop.png")
        page.locator('[data-view="needs"]').click()
        assert page.locator(".need").count() == 123
        assert not errors, errors

        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(URL + f"?view=slides&slide={employee_slide}", wait_until="domcontentloaded")
        assert mobile.locator(".profileCrop").is_visible()
        assert mobile.locator(".spriteCrop").is_visible()
        assert mobile.locator("body").evaluate("el => el.scrollWidth <= innerWidth")
        mobile.locator('[data-view="assets"]').click()
        assert mobile.locator(".assetCard").first.is_visible()
        assert mobile.locator("body").evaluate("el => el.scrollWidth <= innerWidth")
        mobile.screenshot(path=ROOT / "tmp" / "storybook-mobile.png")
        browser.close()
finally:
    if server:
        server.terminate()
        server.wait(timeout=5)

print("PASS: storybook slides, employee profile/sprite identity, audio, complete asset library, needs queue, and mobile layout")
