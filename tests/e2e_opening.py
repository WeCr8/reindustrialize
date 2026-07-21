"""Full opening-shift E2E test. Run with: python tests/e2e_opening.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
EXPECTED_ZACH_VOICES = len(list((ROOT / "packages/assets/audio/zach").glob("*.mp3")))


def stand_by(page, sprite):
    page.evaluate("""sprite => {
      const p = map.placements.find(x => x.sprite === sprite);
      P.x = p.tile[0]; P.y = p.tile[1] + p.footprint[1]; clampCam(); updateGuide(); draw();
    }""", sprite)


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.add_init_script("localStorage.setItem('reindustrialize.learnerMode','off')")
    page.goto(URL)
    page.wait_for_function("loaded === total")

    assert page.locator("#preFounder").is_visible()
    expected_pre = ["WELCOME TO REINDUSTRIALIZE", "FROM GARAGE TO POWERHOUSE", "BUILD YOUR FOUNDER"]
    assert expected_pre[0] in page.locator("#preFounderKicker").inner_text()
    page.locator("#preFounderNext").click()
    assert page.evaluate("zachAudio && !zachAudio.paused")
    for kicker in expected_pre[1:]:
        page.locator("#preFounderNext").click()
        assert kicker in page.locator("#preFounderKicker").inner_text()
    page.locator("#preFounderNext").click()
    assert not page.locator("#preFounder").is_visible()

    assert page.locator("#titleScreen").is_visible()
    assert page.locator(".avatarChoice").count() == 10
    assert page.locator(".avatarChoice span").all_inner_texts() == [f"Founder {letter}" for letter in "ABCDEFGHIJ"]
    assert page.locator(".founderCardPortrait").count() == 10
    assert page.locator("#founderProfile").is_visible()
    assert "FIRST PART FOCUS" in page.locator("#founderProfile").inner_text().upper()
    for avatar in ["av_m_01", "av_m_founder_02_hd", "av_f_founder_hd", "av_f_founder_02_hd", "av_m_blonde_hd", "av_f_blonde_hd", "av_m_middle_eastern_hd", "av_f_middle_eastern_hd", "av_m_indian_hd", "av_f_indian_hd"]:
        page.locator(f'[data-avatar="{avatar}"]').click()
        assert page.evaluate("selectedAvatar") == avatar
        assert page.locator("#founderProfile .atlasPortrait").is_visible()
        assert page.locator(f'[data-avatar="{avatar}"] .founderCardPortrait').is_visible()
        assert "SIGNATURE SKILL" in page.locator("#founderProfile").inner_text()
        assert "PLAY STYLE:" in page.locator("#founderProfile").inner_text()
        assert "GROWTH AREA:" in page.locator("#founderProfile").inner_text()
        assert page.locator("#founderProfile .founderStat").count() == 5
        assert "UPGRADES:" in page.locator("#founderProfile").inner_text()
        assert page.locator(f'[data-avatar="{avatar}"]').get_attribute("class").endswith("selected")
        assert page.locator("#sceneFounderBadge").get_attribute("data-founder-avatar") == avatar
    page.locator("#founderName").fill("Jordan Rivera")
    page.locator('[data-avatar="av_f_indian_hd"]').click()
    assert page.locator("#titleScreen").get_attribute("data-variant") == "title-female"
    page.locator("#companyName").fill("Zach Precision Works")
    page.locator("#newGame").click()
    assert page.locator("#intro").is_visible()
    assert page.evaluate("Object.keys(ZACH_VOICE).length") == EXPECTED_ZACH_VOICES
    assert page.evaluate("REUSABLE_ZACH.clips.length") == 12
    assert page.evaluate("companyName") == "ZACH PRECISION WORKS"
    assert page.evaluate("playerName") == "JORDAN RIVERA"
    assert page.evaluate("selectedAvatar") == "av_f_indian_hd"
    assert page.locator("#sceneFounderBadge").get_attribute("data-founder-avatar") == "av_f_indian_hd"
    assert page.locator("#playerName").inner_text() == "JORDAN RIVERA"
    assert page.locator("#introArt").get_attribute("data-variant") == "opening-female"
    assert "your manufacturing company" in page.locator("#introText").inner_text()
    page.locator("#introNext").click()
    assert "Welcome to the shop" in page.locator("#introText").inner_text()
    assert page.evaluate("zachAudio !== null && zachAudio.src.startsWith('data:audio/mpeg;base64,')")
    page.locator("#introNext").click()
    assert "I'm Zach" in page.locator("#introText").inner_text()
    page.locator("#introNext").click()
    assert "first customer job" in page.locator("#introText").inner_text()
    page.locator("#introNext").click()
    assert "manufacturing powerhouse" in page.locator("#introText").inner_text()
    assert page.locator("#pp .nm").inner_text() == "JORDAN RIVERA"
    page.locator("#introNext").click()
    assert not page.locator("#intro").is_visible()
    assert not page.locator("#task").is_visible()
    assert page.locator("#btour").is_visible()
    assert "done" in page.locator('[data-m="meet_zach"]').get_attribute("class")
    assert page.evaluate("currentObjective().action") == "customers"
    page.locator("#objectiveAction").click()
    page.locator("#customers").wait_for(state="visible")
    page.locator("#acceptContract").click()
    page.wait_for_function("document.querySelector('#intro').dataset.storyBeat === 'first_customer_call'")
    page.locator("#introNext").click()
    page.locator("#introNext").click()
    page.wait_for_function("currentObjective().sprite === 'nox_terminal'")
    # The objective CTA routes to the required material station and opens it.
    page.locator("#objectiveAction").click()
    page.locator(".noxOrder").first.wait_for(timeout=10000)
    assert page.locator("#ttitle").inner_text() == "NOX METALS — MATERIAL ORDERING"
    page.locator(".noxOrder").first.click()
    page.locator("#tclose").click()
    assert page.evaluate("state.materialOrders.length") == 1
    page.wait_for_function("document.querySelector('#intro').dataset.storyBeat === 'nox_delivery_arrives'")
    page.locator("#introNext").click()
    page.wait_for_function("document.querySelector('#intro').classList.contains('closed')")

    tool_index = {"twist": 0, "end": 1, "ball": 2}
    for job_number in range(1, 6):
        assert f"JOB {job_number} OF 5" in page.locator("#objectiveStep").inner_text()
        stand_by(page, "planning_desk")
        assert page.locator("#stationPrompt").is_visible()
        page.locator("#objectiveAction").click()

        cut_length = page.evaluate("state.job.stockLength")
        stand_by(page, "saw_t1")
        assert "Cut raw stock" in page.locator("#objectiveStep").inner_text()
        page.locator("#objectiveAction").click()
        page.locator("#cutLength").evaluate(
            "(e, value) => { e.value=String(value); e.dispatchEvent(new Event('input')); }", cut_length
        )
        page.locator("#cutStock").click()
        page.evaluate("stationRuns().saw_t1.endAt=Date.now()-1;renderProductionHud()")
        page.locator("#sawFlag").click()
        page.locator("#collectSawBlank").click()
        page.wait_for_function("state.rawStockReady && !document.querySelector('#task').classList.contains('open')")

        tool = page.evaluate("state.job.tool")
        target = page.evaluate("state.job.stickTarget")
        stand_by(page, "tool_cart")
        page.locator("#stationOpen").click()
        page.locator(".toolbtn").nth(tool_index[tool]).click()
        page.locator("#stick").evaluate(
            "(e, value) => { e.value=String(value); e.dispatchEvent(new Event('input')); }", target
        )
        page.locator("#lockin").click()
        page.locator(".kitTool").first.wait_for()
        page.locator(".kitTool").first.click()
        page.locator(".kitTool").nth(1).click()
        assert page.evaluate("state.toolsSet.length") == 3
        page.locator("#installKit").click()
        page.wait_for_function("!document.querySelector('#task').classList.contains('open')")

        stand_by(page, "vmc_t2")
        page.evaluate("state.equipmentCooldownUntil=0")
        page.locator("#objectiveAction").click()
        page.locator('[data-setup-check]').nth(0).click()
        page.locator('[data-setup-check]').nth(1).click()
        page.locator("#startProduction").click()
        page.evaluate("state.machineRun.endAt=Date.now()-1;renderProductionHud()")
        page.locator("#machineFlag").click()
        page.locator("#inspectPart").click()
        page.locator("#inspectPart").click()
        page.locator("#tdone").wait_for(timeout=20000)
        page.locator("#tdone").click()
        assert page.evaluate("state.jobsShipped") == job_number
        if job_number == 1:
            assert page.locator("#intro").is_visible()
            assert page.locator("#intro").get_attribute("data-story-beat") == "first_article_evidence"
            page.locator("#introNext").click()
            page.locator("#introNext").click()
        if job_number < 5:
            assert not page.locator("#intro").is_visible()

    assert "done" in page.locator('[data-m="task_vmc"]').get_attribute("class")
    assert page.locator("#qpct").inner_text() == "100%"
    assert page.locator("#shipProgress").inner_text() == "JOBS SHIPPED 5 / 5"
    assert page.evaluate("gradeAverage()") >= 3
    assert page.locator("#intro").is_visible()
    assert "CHAPTER 1 COMPLETE" in page.locator("#introKicker").inner_text()
    assert page.locator("#introArt").get_attribute("data-variant") == "expansion-female"
    assert not page.locator("#b2").is_disabled()
    for _ in range(5):
        page.locator("#introNext").click()
    assert page.evaluate("map.id") == "bay_02"
    assert not errors, errors
    browser.close()

print("PASS: founding -> material order -> five graded jobs -> Garage graduation -> Job Shop expansion")
