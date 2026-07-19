"""E2E: standard Xbox/Gamepad mapping controls title entry and shop movement."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.add_init_script("""
      window.__pad={id:'Xbox Wireless Controller (STANDARD GAMEPAD)',axes:[0,0,0,0],buttons:Array.from({length:17},()=>({pressed:false,value:0})),connected:true,mapping:'standard'};
      navigator.getGamepads=()=>[window.__pad];
      window.padButton=(i,on)=>{window.__pad.buttons[i]={pressed:on,value:on?1:0}};
      window.padAxis=(i,v)=>{window.__pad.axes[i]=v};
    """)
    page.goto(URL)
    page.wait_for_function("loaded === total")
    for _ in range(5):
        page.evaluate("padButton(0,true)"); page.wait_for_timeout(50); page.evaluate("padButton(0,false)"); page.wait_for_timeout(50)
    page.wait_for_function("document.querySelector('#titleScreen').classList.contains('closed')")
    for _ in range(5): page.locator("#introNext").click()
    page.locator("#tourSkip").wait_for(timeout=10000);page.locator("#tourSkip").click()
    page.evaluate("inputMode='gamepad';document.querySelector('#inputMode').value='gamepad'")
    x0 = page.evaluate("P.x")
    page.evaluate("padAxis(0,1)")
    page.wait_for_function(f"P.x === {x0 + 1}")
    page.evaluate("padAxis(0,0)")
    assert "Xbox" in page.locator("#gamepadState").inner_text()
    browser.close()
print("PASS: Xbox A starts game -> standard stick moves player -> status detected")
