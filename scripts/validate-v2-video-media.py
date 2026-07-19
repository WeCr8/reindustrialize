"""Decode V2 promo metadata in Chromium without requiring system ffprobe."""
import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "videos/promo-catalog.json").read_text(encoding="utf-8"))
videos = [item for item in catalog["videos"] if item["id"].endswith(("-v2", "-v3", "-v4"))]
assert len(videos) == 16, f"Expected 11 V2, one V3, and four V4 catalog entries, found {len(videos)}"

class QuietMediaHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass  # Chromium intentionally closes after reading MP4 metadata.

handler = partial(QuietMediaHandler, directory=str(ROOT))
server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for item in videos:
            url = f'http://127.0.0.1:{server.server_port}/videos/{quote(item["file"])}'
            page.set_content(f'<video id="media" preload="metadata" src="{url}"></video>')
            page.wait_for_function("media.readyState >= 1", timeout=30000)
            metadata = page.evaluate("({duration:media.duration,width:media.videoWidth,height:media.videoHeight,error:media.error?.message||null})")
            assert not metadata["error"], f'{item["id"]}: {metadata["error"]}'
            assert abs(metadata["duration"] - item["durationSeconds"]) < 0.2, f'{item["id"]}: duration {metadata["duration"]}'
            expected = item["aspect"]
            actual = metadata["width"] / metadata["height"]
            target = {"16:9": 16/9, "9:16": 9/16, "1:1": 1}[expected]
            assert abs(actual - target) < 0.01, f'{item["id"]}: dimensions {metadata["width"]}x{metadata["height"]}'
        browser.close()
finally:
    server.shutdown()

print("PASS: 16 versioned V2/V3/V4 MP4 files expose playable Chromium metadata with exact catalog durations and aspect ratios")
