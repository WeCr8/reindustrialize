from pathlib import Path

from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL)
    page.wait_for_function("loaded===total")
    for _ in range(4): page.locator("#preFounderNext").click()
    page.locator("#newGame").click()
    for _ in range(5):
        page.locator("#introNext").click()
    page.locator("#tourSkip").wait_for(timeout=10000);page.locator("#tourSkip").click()
    page.evaluate("openNoxOrder()")

    assert page.locator("#ttitle").inner_text() == "NOX METALS — MATERIAL ORDERING"
    assert page.locator("#tview").is_visible()
    assert page.locator(".noxOrder").count() == 3
    assert "6061-T6 ALUMINUM PLATE" in page.locator(".noxOrder").first.inner_text()

    coins_before = int(page.locator("#coins").inner_text())
    page.locator(".noxOrder").first.click()
    assert int(page.locator("#coins").inner_text()) == coins_before - 420
    assert "ORDER CONFIRMED" in page.locator("#noxStatus").inner_text()
    assert page.evaluate("state.materialOrders[0].sku") == "6061-T6-PLATE"
    assert page.evaluate("state.materialOrders[0].status") == "NEXT-DAY DELIVERY"
    browser.close()

print("PASS: NOX terminal -> material catalog -> order confirmed -> coins and delivery state updated")
