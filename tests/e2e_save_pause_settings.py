"""E2E: local recovery, pause semantics, settings persistence, and diagnostics."""
import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
env = dict(os.environ, PORT="8803")
server = subprocess.Popen(["node", "src/dev-server.js"], cwd=ROOT / "server", env=env)
try:
    time.sleep(0.8)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.goto("http://127.0.0.1:8803/game")
        page.wait_for_function("loaded===total")
        page.evaluate("preFounder.classList.add('closed')")
        page.locator("#newGame").click()
        page.evaluate("intro.classList.add('closed'); state.jobsShipped=2; coins=7123; P.x=7; P.y=8")

        page.locator("#bpause").click()
        assert page.locator("#pauseMenu").get_attribute("class") == "open"
        assert page.evaluate("paused") is True
        page.locator("#masterVolume").fill("0.55")
        page.locator("#reducedMotion").check()
        page.locator("#uiScale").select_option("1.15")
        page.locator("#saveNow").click()
        assert "MANUAL SAVE" in page.locator("#saveStatus").inner_text()
        page.locator("#resumeGame").click()
        assert page.evaluate("paused") is False

        page.reload()
        page.wait_for_function("loaded===total")
        page.evaluate("preFounder.classList.add('closed')")
        assert page.locator("#continueGame").is_enabled()
        page.locator("#continueGame").click()
        assert page.evaluate("state.jobsShipped") == 2
        assert page.evaluate("coins") == 7123
        assert page.evaluate("[P.x,P.y]") == [7, 8]
        assert page.locator("#qpct").inner_text() == "0%"
        assert page.evaluate("masterVolume") == 0.55
        assert page.locator("body").evaluate("el=>el.classList.contains('reducedMotion')")
        page.keyboard.press("F3")
        page.wait_for_timeout(1100)
        assert "REIND DEV HUD" in page.locator("#debugHud").inner_text()

        # A malformed local save must never partially start the game or trap Continue.
        page.reload()
        page.wait_for_function("loaded===total")
        page.evaluate("preFounder.classList.add('closed')")
        page.evaluate("localStorage.setItem('reindustrialize.save.v1', JSON.stringify({v:1,companyName:'BROKEN'}))")
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator("#continueGame").click()
        assert page.evaluate("gameStarted") is False
        assert page.locator("#continueGame").is_disabled()
        assert page.evaluate("localStorage.getItem('reindustrialize.save.v1')") is None
        assert page.evaluate("localStorage.getItem('reindustrialize.save.recovery')") is not None
        browser.close()
finally:
    server.terminate()
    server.wait(timeout=5)

print("PASS: save/continue, corrupt-save quarantine, autosave foundation, pause, settings persistence, and F3 diagnostics")
