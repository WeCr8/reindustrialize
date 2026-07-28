"""E2E: alpha entry exposes input choices and phone selection creates a QR session."""
import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
external_url = os.environ.get("PLAYREIND_GAME_URL")
server = None
if external_url:
    URL = external_url
else:
    env = dict(os.environ, PORT="8801")
    server = subprocess.Popen(["node", "src/dev-server.js"], cwd=ROOT / "server", env=env)
    URL = "http://127.0.0.1:8801/game"
    time.sleep(0.8)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.goto(URL)
        page.wait_for_function("typeof loaded !== 'undefined' && loaded === total")
        page.evaluate("preFounder.classList.add('closed')")
        choices = page.locator(".controlChoice")
        assert choices.count() == 4
        launch_box = page.locator("#newGame").bounding_box()
        assert launch_box and launch_box["y"] >= 0 and launch_box["y"] + launch_box["height"] <= 1000
        assert "AUTO" in choices.nth(0).inner_text()
        assert "KEYBOARD" in choices.nth(1).inner_text()
        assert "XBOX" in choices.nth(2).inner_text()
        assert "PHONE QR" in choices.nth(3).inner_text()
        choices.nth(2).click()
        assert page.locator("#inputMode").input_value() == "gamepad"
        assert "GAMEPAD SELECTED" in page.locator("#selectedControlStatus").inner_text()
        choices.nth(3).click()
        assert page.locator("#connect").get_attribute("class") == "open"
        page.wait_for_function("document.querySelector('#pairQr').getAttribute('src')?.startsWith('data:image')")
        assert page.locator("#inputMode").input_value() == "phone"
        assert page.locator("#pairUrl").inner_text().strip()
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(URL)
        mobile.wait_for_function("typeof loaded !== 'undefined' && loaded === total")
        mobile.evaluate("preFounder.classList.add('closed')")
        mobile_box = mobile.locator("#newGame").bounding_box()
        assert mobile_box and mobile_box["y"] >= 0 and mobile_box["y"] + mobile_box["height"] <= 844
        assert mobile.locator("body").evaluate("el => el.scrollWidth <= innerWidth")
        mobile.close()
        browser.close()
finally:
    if server:
        server.terminate()
        server.wait(timeout=5)

print("PASS: alpha entry exposes keyboard, Xbox, and phone controls; phone selection creates QR")
