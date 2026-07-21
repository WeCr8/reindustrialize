"""E2E: qualified workers run persistent multi-batch equipment queues while away."""
from pathlib import Path

from playwright.sync_api import sync_playwright


URL = (Path(__file__).resolve().parents[1] / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded === total")
    page.evaluate("""
      gameStarted=true;preFounder.classList.add('closed');titleScreen.classList.add('closed');intro.classList.add('closed');setMap('bay_01');
      const candidate=HIRE_ROSTER.candidates.find(entry=>entry.id==='luis_ortega');
      hired.add(candidate.id);workers.push({id:candidate.id,candidate,x:P.x,y:P.y,assignment:'saw_t1',status:'WORKING',nextMove:Date.now()+999999,workPulse:0});
      state.equipment.saw=2;
      state.job={...JOBS[0],contract:{quantity:3}};
      state.materialOrders=[{sku:'6061-T6-PLATE'}];
    """)

    assert page.evaluate("queueWorkerTask('saw_t1')")
    assert page.evaluate("queueWorkerTask('saw_t1')")
    assert page.evaluate("queueWorkerTask('saw_t1')")
    assert page.evaluate("stationWorkerQueue('saw_t1').length") == 3
    assert page.evaluate("stationWorkerQueue('saw_t1').filter(item=>item.status==='running').length") == 2
    assert page.evaluate("stationWorkerQueue('saw_t1').filter(item=>item.status==='queued').length") == 1
    assert page.evaluate("stationWorkerQueue('saw_t1').every(item=>item.durationMs===5*60*1000)")
    page.locator("#workerFlag-saw_t1").wait_for()

    # Saved absolute times and queued work survive a browser restart.
    page.reload()
    page.wait_for_function("loaded === total")
    page.locator("#continueGame").click()
    page.wait_for_function("stationWorkerQueue('saw_t1').length === 3")
    assert page.evaluate("stationWorkerQueue('saw_t1')[2].status") == "queued"

    # Simulate returning after the entire queue has elapsed, then collect output.
    page.evaluate("""
      stationWorkerQueue('saw_t1').forEach((item,index)=>{item.startedAt=Date.now()-400000-index*1000;item.endAt=Date.now()-1000;});
      processWorkerQueues();renderProductionHud();openWorkerQueue('saw_t1');
    """)
    assert "COLLECT 3 COMPLETE BATCHES" in page.locator("#collectWorkerBatches").inner_text()
    coins_before = page.evaluate("coins")
    page.locator("#collectWorkerBatches").click()
    assert page.evaluate("stationWorkerQueue('saw_t1').length") == 0
    assert page.evaluate("coins") == coins_before
    assert page.evaluate("state.workerWip.sawBlanks") == 3

    # Collected saw WIP can be routed into a qualified VMC queue and reserves the worker.
    page.evaluate("assignWorker(HIRE_ROSTER.candidates.find(entry=>entry.id==='luis_ortega'),'vmc_t2');state.toolReady=true;state.toolsSet=['PRIMARY','PROBE','CHAMFER']")
    assert page.evaluate("queueWorkerTask('vmc_t2')")
    assert page.evaluate("state.workerWip.sawBlanks") == 2
    page.evaluate("assignWorker(HIRE_ROSTER.candidates.find(entry=>entry.id==='luis_ortega'),'saw_t1')")
    assert page.evaluate("workers[0].assignment") == "vmc_t2"
    page.evaluate("stationWorkerQueue('vmc_t2')[0].endAt=Date.now()-1;processWorkerQueues();collectWorkerTasks('vmc_t2')")
    assert page.evaluate("state.workerWip.finishedParts") == 1
    assert page.evaluate("coins") > coins_before

    # Orientation/management surfaces never pretend to be unattended production equipment.
    assert not page.evaluate("queueableStation('planning_desk')")
    assert not page.evaluate("queueableStation('lathe_cnc_t2')")

    # Runtime qualification is enforced even if stale state assigns the wrong worker.
    page.evaluate("workers[0].candidate={...workers[0].candidate,qualifications:['vmc_t2']};workers[0].assignment='saw_t1'")
    assert not page.evaluate("queueWorkerTask('saw_t1')")
    assert page.evaluate("""(()=>{const snapshot=saveSnapshot();snapshot.state.workerQueues.lathe_cnc_t2=[{station:'lathe_cnc_t2'}];try{validateSaveSnapshot(snapshot);return false}catch{return true}})()""")
    assert not errors, errors
    browser.close()

print("PASS: qualified workers run parallel/queued saved equipment batches, finish while away, and require collection")
