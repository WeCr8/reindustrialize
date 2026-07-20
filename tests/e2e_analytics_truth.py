from pathlib import Path
import subprocess
import time

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:8793"
CONSENT_KEY = "reindustrialize.analyticsConsent.v1"


def event_names(page):
    return page.evaluate(
        """() => window.dataLayer
        .map(entry => Array.from(entry))
        .filter(entry => entry[0] === 'event')
        .map(entry => entry[1])"""
    )


server = subprocess.Popen(
    ["python", "-m", "http.server", "8793", "--bind", "127.0.0.1"],
    cwd=ROOT / "cloudflare-dist",
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(0.6)
try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        context.route("https://www.googletagmanager.com/**", lambda route: route.abort())
        context.add_init_script(f"localStorage.setItem('{CONSENT_KEY}', 'accepted')")

        landing = context.new_page()
        landing.goto(URL, wait_until="domcontentloaded")
        landing.wait_for_timeout(500)
        names = event_names(landing)
        assert names.count("page_view") == 1, names
        assert "hero_video_play" not in names, "muted autoplay must not count as an engaged play"
        landing.locator("#soundBeacon").click()
        landing.locator("#soundBeacon").click()
        names = event_names(landing)
        assert names.count("hero_video_play") == 1, names
        assert landing.evaluate("reindAnalytics('landing_play') && !reindAnalytics('landing_play')")
        assert event_names(landing).count("landing_play") == 1

        game = context.new_page()
        game.goto(URL + "/game/", wait_until="domcontentloaded")
        game.wait_for_function("loaded === total")
        game.evaluate("document.getElementById('preFounder').classList.add('closed')")
        game.locator('.avatarChoice[data-avatar="av_m_01"]').click()
        assert not any(
            event["event"] == "founder_select"
            for event in game.evaluate("window.__reindAnalyticsDebug || []")
        )
        game.locator('.avatarChoice[data-avatar="av_m_founder_02_hd"]').click()
        game.locator('.avatarChoice[data-avatar="av_m_founder_02_hd"]').click()
        founder_events = game.evaluate("(window.__reindAnalyticsDebug || []).filter(e => e.event === 'founder_select')")
        assert len(founder_events) == 1, founder_events
        game.locator('.controlChoice[data-control="auto"]').click()
        game.locator('.controlChoice[data-control="keyboard"]').click()
        game.locator('.controlChoice[data-control="keyboard"]').click()
        control_events = game.evaluate("(window.__reindAnalyticsDebug || []).filter(e => e.event === 'control_mode')")
        assert len(control_events) == 1, control_events
        game.locator("#newGame").click()
        game.evaluate("document.getElementById('b1').click()")
        debug = game.evaluate("window.__reindAnalyticsDebug || []")
        assert sum(event["event"] == "game_start" for event in debug) == 1, debug
        assert not any(event["event"] == "facility_milestone" for event in debug), debug
        game.evaluate("""() => {
          openNoxOrder();
          placeNoxOrder(NOX_CATALOG.find(item => item.sku === '7075-T651-PLATE'));
        }""")
        assert not any(
            event["event"] == "task_complete"
            for event in game.evaluate("window.__reindAnalyticsDebug || []")
        ), "rejected material choices must not count as completed tasks"
        game.evaluate("placeNoxOrder(NOX_CATALOG.find(item => item.sku === '6061-T6-PLATE'))")
        task_events = game.evaluate("(window.__reindAnalyticsDebug || []).filter(e => e.event === 'task_complete')")
        assert len(task_events) == 1 and task_events[0]["params"]["task_id"] == "material_order", task_events

        declined_context = browser.new_context()
        declined_context.route("https://www.googletagmanager.com/**", lambda route: route.abort())
        declined_context.add_init_script(f"localStorage.setItem('{CONSENT_KEY}', 'declined')")
        declined = declined_context.new_page()
        declined.goto(URL, wait_until="domcontentloaded")
        declined.wait_for_timeout(100)
        assert "page_view" not in event_names(declined)
        assert declined.evaluate("reindAnalytics('landing_play')") is False
        declined_context.close()
        context.close()
        browser.close()
finally:
    server.terminate()
    server.wait(timeout=5)

print("PASS: consent-only page views, human video engagement, dedupe, and success-only gameplay analytics")
