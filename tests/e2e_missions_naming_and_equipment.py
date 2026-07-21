"""E2E: title text input, selectable missions, and active station routing."""
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

    # Gameplay keys must remain ordinary text while a naming field has focus.
    page.evaluate("document.querySelector('#preFounder').classList.add('closed')")
    page.locator("#founderName").fill("")
    page.locator("#founderName").press_sequentially("Wade Anderson")
    page.locator("#companyName").fill("")
    page.locator("#companyName").press_sequentially("Apex Works")
    assert page.locator("#founderName").input_value() == "Wade Anderson"
    assert page.locator("#companyName").input_value() == "Apex Works"

    page.evaluate("""
      gameStarted=true;
      companyName=document.querySelector('#companyName').value;
      playerName=document.querySelector('#founderName').value;
      document.querySelector('#titleScreen').classList.add('closed');
      document.querySelector('#intro').classList.add('closed');
      setMap('bay_01');
    """)

    # A mission is actionable. Customer acceptance is required before material and planning.
    page.locator('[data-m="planning_desk"]').click()
    page.locator("#customers").wait_for(state="visible")
    assert "INCOMING SHOP CALL" in page.locator("#customerHeader").inner_text()
    page.evaluate("""
      document.querySelector('#customers').classList.remove('open');
      const offer=CUSTOMER_CONTRACTS.customers[0].offer;
      state.pendingContract={...offer,customerId:CUSTOMER_CONTRACTS.customers[0].id,customer:CUSTOMER_CONTRACTS.customers[0].company};
      state.contracts=[{offerId:offer.id,customerId:CUSTOMER_CONTRACTS.customers[0].id,status:'accepted'}];
      updateGuide();
    """)
    page.locator('[data-m="planning_desk"]').click()
    page.wait_for_function("cv.dataset.interaction === 'nox_terminal'")
    assert page.locator("#task").get_attribute("data-station") == "nox_terminal"
    assert "ORDER" in page.locator("#ttitle").inner_text()
    page.evaluate("closeOverlay();state.materialOrders=[{sku:'6061-T6-PLATE'}]")

    page.locator('[data-m="planning_desk"]').click()
    page.wait_for_function("state.job !== null")
    assert page.locator('[data-m="planning_desk"]').get_attribute("class") is not None

    page.locator('[data-m="task_tool"]').click()
    page.wait_for_function("cv.dataset.interaction === 'saw_t1'")
    assert page.locator("#task").get_attribute("data-station") == "saw_t1"
    page.evaluate("closeOverlay();state.rawStockReady=true")

    page.locator('[data-m="task_tool"]').click()
    page.wait_for_function("cv.dataset.interaction === 'tool_cart'")
    assert page.locator("#tcontrols .toolbtn").count() == 3
    page.evaluate("closeOverlay();state.toolReady=true;state.toolsSet=['PRIMARY','PROBE','CHAMFER']")

    page.locator('[data-m="task_vmc"]').click()
    page.wait_for_function("cv.dataset.interaction === 'vmc_t2'")
    assert page.locator("#cycst").count() == 1
    assert page.locator(".partPreview[data-part-shape='drill']").count() == 1
    assert page.locator(".codeTab").count() == 12
    assert page.locator("#guidedCodeFill").count() == 1
    page.locator("#guidedCodeFill").click()
    assert page.evaluate("task.dataset.programReady") == "true"
    assert page.locator(".codeTab.selected").count() == 3
    assert page.locator('[data-m="task_vmc"]').get_attribute("class") is not None

    assert not errors, errors
    browser.close()

print("PASS: founder/factory typing works; mission buttons route through prerequisites and activate production equipment")
