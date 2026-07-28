from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = os.environ.get("PLAYREIND_GAME_URL", (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri())
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded===total")
    page.evaluate("preFounder.classList.add('closed');titleScreen.classList.add('closed');intro.classList.add('closed')")
    page.click("#bcustomerphone")
    assert page.locator("#customers").is_visible()
    assert "ACCEPT TO JOBLINE QUEUE" in page.locator("#customerIntakeGuide").inner_text()
    assert page.locator("[data-customer]").count() == 4
    assert page.locator(".customerPortrait").evaluate("e => getComputedStyle(e).backgroundImage !== 'none'")
    assert page.locator(".companyImage").evaluate("e => getComputedStyle(e).backgroundImage !== 'none'")
    page.click("#shopPhoneProp")
    page.click("#acceptContract")
    assert page.evaluate("state.pendingContract.id") == "rfq_northstar_1042"
    assert page.evaluate("state.contracts[0].status") == "accepted"
    assert page.locator('[data-mission-action="customers"]').evaluate("el => el.classList.contains('done')")
    assert page.evaluate("currentObjective().action !== 'customers'")
    page.wait_for_function("document.querySelector('#intro').dataset.storyBeat === 'first_customer_call'")
    page.click("#introNext")
    page.click("#introNext")
    page.evaluate("P.x=6;P.y=2;interact()")
    assert page.evaluate("state.job.id") == "drill"
    assert page.evaluate("state.job.contract.customer") == "Northstar Robotics"
    assert page.evaluate("state.contracts[0].status") == "released to production"
    assert not errors, errors
    browser.close()
print("PASS: phone call -> customer/company review -> RFQ accept -> JobLine work order -> planning traveler")
