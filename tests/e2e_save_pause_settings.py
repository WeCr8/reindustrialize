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
        page.evaluate("""intro.classList.add('closed'); state.jobsShipped=2; coins=7123; P.x=7; P.y=8;
            tourActive=true; tourMandatory=true; tourIndex=3; tourPhase=2; tourPracticeStep=1;
            completedTourStops.clear(); SHOP_TOUR.stops.slice(0,3).forEach(stop=>completedTourStops.add(stop.id));""")

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
        page.wait_for_function("document.querySelector('#task').dataset.tourPhase === 'practice'")
        assert page.evaluate("[tourIndex,tourPracticeStep,tourMandatory]") == [3, 1, True]
        assert page.evaluate("completedTourStops.size") == 3
        assert page.locator("#qpct").inner_text() == "0%"
        assert page.evaluate("masterVolume") == 0.55
        assert page.locator("body").evaluate("el=>el.classList.contains('reducedMotion')")
        page.keyboard.press("F3")
        page.wait_for_timeout(1100)
        assert "REIND DEV HUD" in page.locator("#debugHud").inner_text()

        # A malformed newest save automatically falls back to the previous atomic checkpoint.
        page.reload()
        page.wait_for_function("loaded===total")
        page.evaluate("preFounder.classList.add('closed')")
        page.evaluate("localStorage.setItem('reindustrialize.save.v1', JSON.stringify({v:1,companyName:'BROKEN'}))")
        page.locator("#continueGame").click()
        assert page.evaluate("gameStarted") is True
        assert page.evaluate("state.jobsShipped") == 2
        assert page.locator("#continueGame").is_enabled()
        assert page.evaluate("JSON.parse(localStorage.getItem('reindustrialize.save.v1')).companyName") == "AMERICAN FORGE WORKS"
        browser.close()
finally:
    server.terminate()
    server.wait(timeout=5)

print("PASS: crash recovery, onboarding resume, atomic backup fallback, pause, settings persistence, and F3 diagnostics")
