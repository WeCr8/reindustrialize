"""Render every launch founder through every active player story scene."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
MANIFEST = json.loads((ROOT / "data/player-scene-manifest.json").read_text(encoding="utf-8"))

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded === total")
    for _ in range(4):
        page.locator("#preFounderNext").click()
    assert page.locator(".avatarChoice").count() == len(MANIFEST["founders"])
    for avatar, profile in MANIFEST["founders"].items():
        family = profile["family"]
        card = page.locator(f'.avatarChoice[data-avatar="{avatar}"]')
        card.click()
        assert page.evaluate("selectedAvatar") == avatar
        assert "selected" in (card.get_attribute("class") or "")
        assert page.locator("#titleScreen").get_attribute("data-variant") == f"title-{family}"
        assert page.locator("#sceneFounderBadge").get_attribute("data-founder-avatar") == avatar
        assert page.evaluate("id => IMG[id].complete && IMG[id].naturalWidth === ATLAS[id].w && IMG[id].naturalHeight === ATLAS[id].h", avatar)
        assert page.evaluate("id => { const c=document.querySelector(`[data-avatar='${id}'] canvas`),d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; return Array.from(d).some((v,i)=>i%4===3&&v>0); }", avatar)
        for scene in [x for x, value in MANIFEST["scenes"].items() if value["active"] and x != "title"]:
            page.evaluate("scene => setStoryArt(scene)", scene)
            assert page.locator("#introArt").get_attribute("data-variant") == f"{scene}-{family}"
            assert page.evaluate("document.querySelector('#introArt').complete && document.querySelector('#introArt').naturalWidth > 0")
            assert page.locator("#sceneFounderBadge").get_attribute("data-founder-avatar") == avatar
        page.evaluate("draw()")
        assert page.locator("#cv").get_attribute("data-player-avatar") == avatar
    assert not errors, errors
    browser.close()
print(f"PASS: {len(MANIFEST['founders'])} founders render across selection, floor, and all active story scenes")
