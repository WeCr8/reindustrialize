"""E2E performance budget: startup must not eagerly fetch the full runtime library."""
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(["node", "scripts/build-cloudflare-site.mjs"], cwd=ROOT, check=True)
server = subprocess.Popen(
    ["python", "-m", "http.server", "8802", "--bind", "127.0.0.1"],
    cwd=ROOT / "cloudflare-dist",
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
try:
    time.sleep(0.6)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        runtime_requests = []
        audio_requests = []
        page.on("request", lambda request: (
            runtime_requests.append(request.url) if "/assets/runtime/" in request.url else None,
            audio_requests.append(request.url) if request.resource_type == "media" else None,
        ))
        page.goto("http://127.0.0.1:8802/game/", wait_until="domcontentloaded")
        page.wait_for_function("typeof loaded !== 'undefined' && loaded === total")
        page.wait_for_timeout(500)
        assert len(set(runtime_requests)) <= 35, f"startup requested {len(set(runtime_requests))} runtime assets"
        assert not audio_requests, f"audio loaded before player interaction: {audio_requests}"
        assert page.evaluate("Object.keys(IMG).length < Object.keys(SPRITES).length")
        browser.close()
finally:
    server.terminate()
    server.wait(timeout=5)

print(f"PASS: lazy startup stayed within 35 runtime assets and loaded no audio before interaction")
