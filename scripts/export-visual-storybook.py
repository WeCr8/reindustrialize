"""Export every storybook slide as a numbered 1920x1080 PNG proof."""
import json, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];book=ROOT/'storybook/v1';manifest=json.loads((book/'storybook-manifest.json').read_text(encoding='utf-8'));out=book/'slides';out.mkdir(exist_ok=True)
for old in out.glob('*.png'): old.unlink()
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
    for slide in manifest['slides']:
        page.goto((book/'index.html').as_uri()+f"?view=slides&slide={slide['number']}");page.wait_for_load_state('load');page.wait_for_function("document.querySelector('.slide')");page.wait_for_function("[...document.images].every(image => image.complete && image.naturalWidth > 0)");page.wait_for_timeout(80)
        slug=''.join(c.lower() if c.isalnum() else '-' for c in slide['title']).strip('-')[:54]
        page.screenshot(path=str(out/f"{slide['number']:03d}-{slug}.png"),full_page=False)
    browser.close()
print(f"PASS: exported {manifest['slideCount']} numbered storybook slide PNGs to {out}")
