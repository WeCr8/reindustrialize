"""E2E: timed drilling, pocketing, and ball-milling retain recognizable parts."""
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded === total")
    page.evaluate("""
      gameStarted=true;
      preFounder.classList.add('closed');
      titleScreen.classList.add('closed');
      intro.classList.add('closed');
    """)

    for job_id in ["drill", "pocket", "dome"]:
        page.evaluate("""jobId => {
          state.job=JOBS.find(job => job.id === jobId);
          state.machineRun={station:'vmc_t2',jobId,status:'running',startedAt:Date.now()-300000,endAt:Date.now()+300000,durationMs:600000,capacity:1};
          openVmcTask();
        }""", job_id)
        page.wait_for_function("tscene.dataset.liveProduction === 'true' && tscene.dataset.productionProgress")
        assert page.locator("#tscene").is_visible()
        assert page.locator("#tscene").get_attribute("data-part-shape") == job_id
        progress = int(page.locator("#tscene").get_attribute("data-production-progress"))
        assert 49 <= progress <= 51
        page.screenshot(path=ROOT / "tmp" / f"live-machining-{job_id}.png")
        page.evaluate("closeOverlay();state.machineRun=null")

    # Added equipment represents parallel lot capacity and keeps the cell occupied.
    page.evaluate("""
      state.job=JOBS[0];state.equipment.vmc=2;
      startAutonomousRun(state.job);
    """)
    assert page.evaluate("state.machineRun.capacity") == 2
    assert page.evaluate("state.machineRun.durationMs") == 5 * 60 * 1000
    page.evaluate("startAutonomousRun(state.job)")
    assert page.evaluate("state.machineRun.capacity") == 2

    assert not errors, errors
    browser.close()

print("PASS: live timed drilling, bounded pocket milling, and retained dome geometry render; purchased VMCs add lot capacity")
