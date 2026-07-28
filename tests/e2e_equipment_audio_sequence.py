from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL)
    page.wait_for_function("loaded===total")

    missing = page.evaluate("""() => {
      const mapped = new Set([...MAPS.bay_01.placements, ...MAPS.bay_02.placements].map(x => x.sprite));
      return [...mapped].filter(sprite => !STATION_SFX[sprite]);
    }""")
    assert not missing, f"Stations without interaction sound: {missing}"
    assert page.evaluate("Object.values(STATION_SFX).every(id => Boolean(SFX_AUDIO[id]))")

    page.evaluate("""() => {
      window.sfxLog=[];
      playSfx=(id,opt={})=>{window.sfxLog.push(id);return null};
      stopSfxLoop=()=>{};
      state.job=JOBS[0];state.tool='twist';runAnim(state.job);
    }""")
    page.wait_for_function("state.machineRun?.status === 'running'", timeout=35_000)
    page.evaluate("state.machineRun.endAt=Date.now()-1;renderProductionHud()")
    page.wait_for_timeout(800)
    log = page.evaluate("window.sfxLog")
    expected = ["cnc_door_close", "cnc_tool_change", "spindle_start", "coolant_on", "cnc_rapid_traverse", "drill_cut_aluminum", "coolant_off", "spindle_stop"]
    positions = [log.index(item) for item in expected]
    assert positions == sorted(positions), (expected, log)
    assert page.locator("#tscene").get_attribute("data-motion-code") == "M30"

    program = "\n".join(page.evaluate("JOBS[0].prog"))
    for code in ["M06", "G90", "G00", "G43", "H01", "G81", "G80", "M09", "M05", "G28", "G91", "M30"]:
        assert code in program, (code, program)
    blanks = page.evaluate("JOBS[0].blanks")
    assert "54" in blanks["o"]["ans"] and "03" in blanks["s"]["ans"] and "08" in blanks["c"]["ans"]
    browser.close()

print("PASS: every mapped station has SFX; true G/M code drives ordered CNC rapid, cut, and stop audio")
