"""Capture a visual review set and verify the timed-RPG production loop."""
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
OUT = ROOT / "tmp" / "game-review"
OUT.mkdir(parents=True, exist_ok=True)


def shot(page, order, name):
    page.screenshot(path=OUT / f"{order:02d}-{name}.png", full_page=False)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    page.wait_for_function("loaded === total")

    for _ in range(4):
        page.locator("#preFounderNext").click()
    assert page.locator("#preFounder.selecting #titleUi").is_visible()
    assert page.locator("#preFounder .avatarChoice").count() == 10
    shot(page, 1, "zach-unified-founder-selection")

    page.locator('[data-avatar="av_f_middle_eastern_hd"]').click()
    shot(page, 2, "founder-profile-and-play-style")

    page.evaluate(
        """
        gameStarted=true;
        preFounder.classList.add('closed');
        titleScreen.classList.add('closed');
        intro.classList.add('closed');
        state.job=JOBS[0];
        state.rawStockReady=true;
        state.toolReady=true;
        state.toolsSet=['end','twist','chamfer'];
        startStationRun('saw_t1',18000,{jobId:state.job.id,cutLength:state.job.stockLength});
        startAutonomousRun(state.job);
        P.x=4;P.y=10;P.rx=P.x;P.ry=P.y;draw();
        """
    )
    first_timer = page.locator("#machineFlag").inner_text()
    assert "REMAINING" in first_timer
    shot(page, 3, "parallel-equipment-timers-on-floor")

    page.evaluate("P.x=15;P.y=7;P.rx=P.x;P.ry=P.y;draw();saveGame('TIMER REVIEW')")
    page.wait_for_timeout(1200)
    page.evaluate("renderProductionHud()")
    second_timer = page.locator("#machineFlag").inner_text()
    assert first_timer != second_timer
    assert page.locator("#sawFlag").is_visible()
    shot(page, 4, "timers-continue-during-other-work")

    end_at = page.evaluate("state.machineRun.endAt")
    page.reload()
    page.wait_for_function("loaded === total")
    page.evaluate("preFounder.classList.add('closed');restoreGame()")
    assert page.evaluate("state.machineRun.endAt") == end_at
    page.evaluate("renderProductionHud()")
    page.wait_for_function("document.querySelector('#machineFlag')")
    assert page.locator("#machineFlag").is_visible()

    page.evaluate(
        """
        state.machineRun.endAt=Date.now()-1;
        state.stationRuns.saw_t1.endAt=Date.now()-1;
        renderProductionHud();
        """
    )
    assert "COMPLETE" in page.locator("#machineFlag").inner_text()
    assert "COMPLETE" in page.locator("#sawFlag").inner_text()
    shot(page, 5, "completed-work-waits-for-collection")

    page.evaluate("openEquipmentMarket()")
    shot(page, 6, "equipment-store-and-expansion-costs")
    page.locator("#equipmentMarketClose").click()
    page.locator("#bteam").click()
    shot(page, 7, "hire-and-assign-team")
    page.evaluate("document.getElementById('hireClose').click();showExpansion()")
    shot(page, 8, "shop-expansion-progression")

    assert not errors, errors
    browser.close()

print(f"PASS: 8 review screenshots captured; timers count down off-station, survive reload, and wait for collection in {OUT}")
