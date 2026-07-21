"""Later machine wear requires a hired maintenance technician and paid repair."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded===total")
    page.evaluate("document.querySelector('#preFounder').classList.add('closed');document.querySelector('#titleScreen').classList.add('closed');gameStarted=true;state.job=JOBS[0];state.maintenance={vmc:{condition:15,status:'DOWN FOR MAINTENANCE'}};coins=5000")

    page.evaluate("openVmcTask()")
    assert "DOWN FOR MAINTENANCE" in page.locator("#ttitle").inner_text()
    assert "HIRE A MAINTENANCE TECHNICIAN" in page.locator("#tztext").inner_text().upper()
    page.evaluate("draw()")
    page.wait_for_function("IMG['garage-machine-maintenance-sprite-atlas-v1']?.complete")
    page.evaluate("draw()")
    assert page.locator("#cv").get_attribute("data-maintenance-visual") == "locked_out"
    page.locator("#hireMaintenance").click()
    assert page.locator("#hire").is_visible()
    assert "Maintenance Technician" in page.locator("#hireCard").inner_text()
    page.locator("#hireNow").click()
    page.wait_for_function("document.querySelector('#intro').dataset.storyBeat==='first_hire_team'")
    while page.locator("#intro").is_visible():
        page.locator("#introNext").click()
    page.locator("#hireClose").click()

    assert page.evaluate("maintenanceWorker().candidate.role") == "maintenance_technician"
    page.evaluate("openVmcTask()")
    assert page.locator("#repairVmc").is_visible()
    coins_before = page.evaluate("coins")
    page.locator("#repairVmc").click()
    assert page.evaluate("maintenanceState().condition") == 100
    assert page.evaluate("maintenanceState().status") == "READY"
    assert page.evaluate("maintenanceState().visualState") == "restored"
    page.evaluate("document.getElementById('task').classList.remove('open');draw()")
    assert page.locator("#cv").get_attribute("data-maintenance-visual") == "restored"
    assert page.evaluate("coins") == coins_before - 350
    assert page.evaluate("JSON.parse(localStorage.getItem('reindustrialize.save.v1')).state.maintenance.vmc.condition") == 100
    page.evaluate("state.jobsShipped=5;state.maintenance.vmc.condition=100;applyVmcWear()")
    assert page.evaluate("maintenanceState().condition") < 100
    assert not errors, errors
    browser.close()

print("PASS: later VMC wear -> lockout -> maintenance hire -> paid repair -> saved release")
