from pathlib import Path
from playwright.sync_api import sync_playwright
URL=(Path(__file__).resolve().parents[1]/"apps/wecr8-info/prototypes/shop-floor-viewer.html").as_uri()
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={"width":1440,"height":1000});errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
 page.goto(URL);page.wait_for_function("loaded===total");[page.locator("#preFounderNext").click() for _ in range(4)];page.locator("#newGame").click();[page.locator("#introNext").click() for _ in range(3)];page.locator("#tourNext").wait_for(timeout=10000);page.evaluate("tourMandatory=false;finishTour()");page.locator("#bteam").click()
 assert page.evaluate("HIRE_ROSTER.profileAtlas")=="workforce-profile-atlas-v1"
 assert page.evaluate("getComputedStyle(document.querySelector('#hireCard .atlasPortrait')).backgroundImage.includes(IMG[HIRE_ROSTER.profileAtlas].src)")
 assert page.locator("#hireCount").inner_text().startswith("1 / 10")
 assert "CNC Programmer" in page.locator("#hireCard").inner_text()
 page.locator("#hireNext").click();assert "Luis Ortega" in page.locator("#hireCard").inner_text();assert "CNC Operator" in page.locator("#hireCard").inner_text()
 page.locator("#viewProfile").click();assert page.locator("#profile").is_visible();assert "QUALIFIED" in page.locator("#profile").inner_text();assert page.evaluate("getComputedStyle(document.querySelector('#profile .atlasPortrait')).backgroundImage.includes(IMG[HIRE_ROSTER.profileAtlas].src)")
 before=int(page.locator("#coins").inner_text());page.locator("#profileHire").click();assert int(page.locator("#coins").inner_text())==before-1800;assert page.locator("#profileHire").inner_text()=="HIRED"
 page.wait_for_function("document.querySelector('#intro').dataset.storyBeat === 'first_hire_team'");page.locator("#introNext").click();page.locator("#introNext").click();page.locator("#profileAssign").wait_for()
 page.locator("#profileAssign").select_option("vmc_t2");assert page.evaluate("workers[0].assignment")=="vmc_t2"
 page.locator("#profileBack").click();page.locator("#hireClose").click();page.wait_for_timeout(2500)
 assert page.locator("#cv").get_attribute("data-worker-count")=="1";assert page.locator("#cv").get_attribute("data-assigned-workers")=="1";assert "VMC" in page.evaluate("workers[0].status")
 assert not errors,errors;b.close()
print("PASS: 10-role roster -> hire -> qualified station assignment -> visible autonomous worker")
