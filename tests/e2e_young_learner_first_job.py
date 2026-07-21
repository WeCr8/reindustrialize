"""Young learner follows only the on-screen route through one shipped part."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

URL=os.environ.get("REINDUSTRIALIZE_TEST_URL") or (Path(__file__).resolve().parents[1]/"apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={"width":1024,"height":768});errors=[]
    page.on("pageerror",lambda error:errors.append(str(error)))
    page.add_init_script("localStorage.setItem('reindustrialize.learnerMode','on')")
    page.goto(URL);page.wait_for_function("loaded===total")
    for _ in range(4): page.locator("#preFounderNext").click()
    page.locator("#newGame").click()
    for _ in range(3): page.locator("#introNext").click()
    assert not page.locator("#task").is_visible()
    assert page.locator("#btour").is_visible()
    # Every station is reached through the single visible objective button.
    page.locator("#objectiveAction").click();page.locator("#customers").wait_for(state="visible")
    page.locator("#acceptContract").click();page.wait_for_function("document.querySelector('#intro').dataset.storyBeat==='first_customer_call'")
    page.locator("#introNext").click();page.locator("#introNext").click()
    page.wait_for_function("currentObjective().sprite==='nox_terminal'")
    page.locator("#objectiveAction").click();page.locator(".noxOrder").first.wait_for(timeout=10000)
    page.locator(".noxOrder").nth(2).click();assert page.evaluate("state.materialOrders.length===0")
    page.locator(".noxOrder").first.click();page.locator("#tclose").click()
    page.locator("#introNext").wait_for(timeout=10000);page.locator("#introNext").click()
    page.wait_for_function("document.querySelector('#intro').classList.contains('closed')")
    page.locator("#objectiveAction").click();page.wait_for_function("state.job!==null",timeout=10000)
    page.locator("#objectiveAction").click();page.locator("#cutStock").wait_for(timeout=10000)
    page.locator("#kidSetCut").click();page.locator("#cutStock").click()
    page.evaluate("stationRuns().saw_t1.endAt=Date.now()-1;renderProductionHud()")
    page.locator("#sawFlag").click();page.locator("#collectSawBlank").click();page.wait_for_function("state.rawStockReady")
    page.locator("#objectiveAction").click();page.locator(".toolbtn").first.wait_for(timeout=10000)
    tool=page.evaluate("state.job.tool");index={"twist":0,"end":1,"ball":2}[tool]
    page.locator(".toolbtn").nth((index+1)%3).click();page.locator(".toolbtn").nth(index).click()
    page.locator("#kidSetStick").click();page.locator("#lockin").click();page.locator("#kidLoadKit").wait_for()
    page.locator("#kidLoadKit").click();page.locator("#installKit").click()
    page.wait_for_function("state.toolReady")
    page.locator("#objectiveAction").click();page.locator('[data-setup-check]').first.wait_for(state="attached",timeout=10000)
    assert page.locator("#startProduction").is_disabled()
    page.locator('[data-setup-check]').nth(0).click();page.locator('[data-setup-check]').nth(1).click()
    page.locator("#startProduction").click();page.locator("#machineFlag").wait_for()
    assert "REMAINING" in page.locator("#machineFlag").inner_text()
    page.evaluate("state.machineRun.endAt=Date.now()-1;renderProductionHud()")
    page.wait_for_function("state.machineRun?.status==='inspection'",timeout=30000)
    page.locator("#machineFlag").click();page.locator("#inspectPart").click();assert page.evaluate("state.jobsShipped===0")
    page.locator("#inspectPart").click();page.locator("#tdone").wait_for(timeout=10000);page.locator("#tdone").click()
    assert page.evaluate("state.jobsShipped===1")
    assert not errors,errors
    browser.close()
print("PASS: young learner navigates visible objectives, recovers, runs VMC autonomously, and ships first job")
