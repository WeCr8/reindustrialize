from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = os.environ.get("PLAYREIND_GAME_URL", (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri())
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded===total")
    page.evaluate("startAmbience('shop_ambience_small')")
    assert page.evaluate("ambienceId") == "shop_ambience_small"
    assert page.evaluate("ambienceAudio.loop") is True
    assert abs(page.evaluate("ambienceAudio.volume") - 0.16) < 0.001
    page.click("#testVoice")
    page.wait_for_function("zachAudio && zachAudio.duration > 0 && zachAudio.currentTime > 0")
    assert page.evaluate("zachAudio.error === null")
    assert abs(page.evaluate("zachAudio.volume") - 1) < 0.001
    page.evaluate("setAmbienceLevel(true)")
    assert page.evaluate("ambienceAudio.volume") < 0.07
    page.evaluate("voiceEnabled=false;stopZach('VOICE: MUTED')")
    assert abs(page.evaluate("ambienceAudio.volume") - 0.16) < 0.001
    assert "MUTED" in page.locator("#audioState").inner_text()
    page.evaluate("voiceEnabled=true;setAmbienceLevel(true);stopZach('VOICE: NARRATION PAUSED')")
    assert abs(page.evaluate("ambienceAudio.volume") - 0.16) < 0.001
    assert "PAUSED" in page.locator("#audioState").inner_text()
    page.evaluate("setAmbienceLevel(false);setMap('bay_02')")
    assert page.evaluate("ambienceId") == "job_shop_ambience"
    assert abs(page.evaluate("ambienceAudio.volume") - 0.16) < 0.001
    page.evaluate("preFounder.classList.add('closed');titleScreen.classList.add('closed');intro.classList.add('closed')")
    page.click("#bambience")
    assert "AMBIENCE OFF" in page.locator("#bambience").inner_text()
    assert not errors, errors
    browser.close()
print("PASS: quiet ambience loops, facility switching, Zach ducking, mute/skip recovery, and independent opt-out")
