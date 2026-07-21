"""E2E: every visible station opens and production timers persist/complete."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.add_init_script("localStorage.setItem('reindustrialize.learnerMode','off')")
    page.goto(URL)
    page.wait_for_function("loaded === total")
    page.evaluate("""
      gameStarted=true;
      document.querySelector('#titleScreen').classList.add('closed');
      document.querySelector('#preFounder').classList.add('closed');
      document.querySelector('#intro').classList.add('closed');
      setMap('bay_02');
    """)

    # Every formerly silent station now opens a real details/mission surface.
    for station in [
        "presetter_t4", "toolcrib_rfid_t4", "bench_deburr_t1", "network_node_t3",
        "handoff_terminal_t4", "nox_pallet", "chalkboard", "cobot_t5", "amr_t5",
    ]:
        page.evaluate("sprite => walkToStation(sprite, true)", station)
        page.wait_for_function(
            "sprite => document.querySelector('#task').classList.contains('open') && cv.dataset.interaction === sprite",
            arg=station,
            timeout=10000,
        )
        assert page.locator("#ttitle").inner_text().strip()
        assert page.locator("#tcontrols").inner_text().strip()
        if station != "presetter_t4":
            assert page.evaluate("cv.dataset.lastStationDetails") == station
            assert "STATION MISSION" in page.locator("#tcontrols").inner_text()
        page.evaluate("closeOverlay()")

    page.evaluate("setMap('bay_01')")
    page.evaluate("sprite => walkToStation(sprite, true)", "mill_manual_t1")
    page.wait_for_function("cv.dataset.lastStationDetails === 'mill_manual_t1'")
    page.locator("#stationDetailsClose").click()

    # A nearby employee no longer steals a machine interaction selected by click-to-walk.
    page.evaluate("""
      const candidate=HIRE_ROSTER.candidates[0];
      workers.push({id:candidate.id,candidate,x:P.x,y:P.y,assignment:null,status:'MEANDERING',nextMove:Date.now()+999999,workPulse:0});
      walkToStation('network_node_t3',true);
    """)
    page.wait_for_function("cv.dataset.lastStationDetails === 'network_node_t3'")
    assert page.locator("#ttitle").inner_text().startswith("MTCONNECT NODE")
    page.locator("#stationDetailsClose").click()

    # The bandsaw creates a real five-minute saved run and resumes after reload.
    page.evaluate("state.materialOrders=[{sku:'6061-T6-PLATE'}];state.job=JOBS[0];openSawTask()")
    cut_length = page.evaluate("state.job.stockLength")
    page.locator("#cutLength").evaluate(
        "(element,value)=>{element.value=String(value);element.dispatchEvent(new Event('input'))}", cut_length
    )
    page.locator("#cutStock").click()
    saw_duration = page.evaluate("stationRuns().saw_t1.durationMs")
    assert saw_duration == 5 * 60 * 1000
    assert page.locator("#sawFlag").is_visible()
    assert "REMAINING" in page.locator("#sawFlag").inner_text()
    page.reload()
    page.wait_for_function("loaded === total")
    page.locator("#continueGame").click()
    page.wait_for_function("stationRuns().saw_t1?.status === 'running'")
    page.locator("#sawFlag").wait_for()
    page.evaluate("stationRuns().saw_t1.endAt=Date.now()-1;renderProductionHud()")
    assert "COMPLETE" in page.locator("#sawFlag").inner_text()
    page.locator("#sawFlag").click()
    page.locator("#collectSawBlank").click()
    assert page.evaluate("state.rawStockReady && !stationRuns().saw_t1")

    # The initial VMC has a ten-minute persisted cycle, progress UI, and inspection-ready state.
    page.evaluate("state.toolReady=true;state.toolsSet=['PRIMARY','PROBE','CHAMFER'];startAutonomousRun(state.job)")
    assert page.evaluate("state.machineRun.durationMs") == 10 * 60 * 1000
    assert "REMAINING" in page.locator("#machineFlag").inner_text()
    page.locator("#machineFlag").click()
    page.locator("#activeStationTimer").wait_for()
    assert page.locator("#activeStationProgress").is_visible()
    page.locator("#leaveRunning").click()
    page.evaluate("state.machineRun.endAt=Date.now()-1;renderProductionHud()")
    assert page.evaluate("state.machineRun.status === 'inspection'")
    assert "COMPLETE" in page.locator("#machineFlag").inner_text()

    assert not errors, errors
    browser.close()

print("PASS: all map stations open details; saw/VMC timers persist, display, complete, and require collection")
