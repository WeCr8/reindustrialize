"""E2E: host creates QR session, phone pairs, and movement reaches the game."""
import subprocess
import time
import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
env = dict(os.environ, PORT="8799")
server = subprocess.Popen(["node", "src/dev-server.js"], cwd=ROOT / "server", env=env)
try:
    time.sleep(0.8)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        host = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        host.on("pageerror", lambda error: errors.append(str(error)))
        host.goto("http://localhost:8799/game")
        host.wait_for_function("loaded === total")
        for _ in range(4): host.locator("#preFounderNext").click()
        host.locator("#newGame").click()
        for _ in range(3): host.locator("#introNext").click()
        host.locator("#tourNext").wait_for(timeout=10000);host.evaluate("tourMandatory=false;finishTour()")
        x0 = host.evaluate("P.x")
        host.locator("#bphone").click()
        host.locator("#pairStart").click()
        host.wait_for_function("document.querySelector('#pairUrl').textContent.includes('/controller?token=')")
        raw = urlsplit(host.locator("#pairUrl").inner_text())
        phone_url = urlunsplit((raw.scheme, f"localhost:{raw.port}", raw.path, raw.query, ""))
        phone = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        phone.goto(phone_url)
        phone.wait_for_function("document.querySelector('#status').textContent === 'CONNECTED'")
        host.wait_for_function("document.querySelector('#pairState').textContent === 'PHONE CONNECTED'")
        phone.locator('[data-key="right"]').dispatch_event("pointerdown")
        phone.locator('[data-key="right"]').dispatch_event("pointerup")
        host.wait_for_function(f"P.x === {x0 + 1}")
        assert not errors, errors
        browser.close()
finally:
    server.terminate()
    server.wait(timeout=5)

print("PASS: QR session -> phone pair -> WebSocket input -> player movement")
