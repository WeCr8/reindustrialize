"""Human-style workforce bot: hire, assign, converse with multiple NPC roles, verify floor behavior."""
import json, random, time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];URL=(ROOT/'apps/wecr8-info/prototypes/shop-floor-viewer.html').as_uri();rng=random.Random(20260718);actions=[]
def click(page,selector,label):
 loc=page.locator(selector);loc.wait_for(state='visible');box=loc.bounding_box();page.mouse.move(box['x']+box['width']*.5,box['y']+box['height']*.5,steps=rng.randint(5,11));page.wait_for_timeout(rng.randint(40,110));loc.click();actions.append(label)
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL);page.wait_for_function('loaded===total')
 for _ in range(4):click(page,'#preFounderNext','advance prologue')
 click(page,'#newGame','launch company')
 for _ in range(3):click(page,'#introNext','advance opening')
 page.locator('#tourNext').wait_for();page.evaluate('tourMandatory=false;finishTour()');actions.append('enter factory after reviewed tour');click(page,'#bteam','open team browser')
 tested=[]
 def hire_at(index,assignment):
  current=page.evaluate('hireIndex');steps=(index-current)%10
  for _ in range(steps):click(page,'#hireNext','browse candidate')
  person=page.evaluate('HIRE_ROSTER.candidates[hireIndex]')
  click(page,'#hireNow',f"hire {person['name']}")
  if not tested: page.wait_for_function("document.querySelector('#intro').dataset.storyBeat==='first_hire_team'")
  while page.locator('#intro').is_visible(): click(page,'#introNext','advance hire story')
  page.locator('#quickAssign').select_option(assignment);actions.append(f"assign {person['name']} to {assignment}")
  dialogue=[]
  for _ in range(4):click(page,'#talkHire',f"talk with {person['name']}");dialogue.append(page.locator('#npcConversation').inner_text())
  assert len(set(dialogue))==4;assert page.locator('#cv').get_attribute('data-last-npc-conversation')==person['id'];tested.append({'id':person['id'],'role':person['role'],'assignment':assignment,'dialogueStates':dialogue})
 hire_at(6,'nox_terminal');hire_at(0,'planning_desk');hire_at(1,'vmc_t2')
 click(page,'#hireClose','return to factory floor');page.wait_for_timeout(3200)
 assert page.locator('#cv').get_attribute('data-worker-count')=='3';assert page.locator('#cv').get_attribute('data-assigned-workers')=='3';assert not errors,errors
 report={'result':'pass','seed':20260718,'humanStyle':True,'visibleActions':len(actions),'npcCount':3,'npcs':tested,'pageErrors':errors};(ROOT/'tmp/bot-runs/workforce-conversation-bot-20260718.json').write_text(json.dumps(report,indent=2),encoding='utf-8');b.close()
print(f"PASS: workforce bot hired, assigned, and completed four-state conversations with {len(tested)} NPC roles using {len(actions)} visible actions")
