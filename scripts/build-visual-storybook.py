"""Build a versioned, slide-by-slide visual storybook from canonical game manifests."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'storybook'/'v1'
OUT.mkdir(parents=True,exist_ok=True)
data=lambda name:json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))
story=data('story-production.json');avatars=data('avatars.json');scenes=data('player-scene-manifest.json');tour=data('shop-tour.json');tasks=data('production-task-tutorials.json');release=data('release-manifest.json');founder_profiles=data('founder-profiles.json');hiring=data('hiring-roster.json');conversations=data('workforce-conversations.json')

def uri(path): return '../../'+Path(path).as_posix()
def asset(name): return uri(Path('packages/assets')/name)
def station_image(item):
    name=item['image']
    if item.get('imageType')=='equipment': return asset(f'equipment/{name}.png')
    if item.get('imageType')=='nox': return asset(f'materials/{name}.png')
    hd=ROOT/'packages/assets/sprites'/f'{name}_hd.png'
    return '../../packages/assets/sprites/'+hd.name if hd.exists() else asset(f'sprites/{name}.png')

slides=[]
def add(section,title,text,image,status='implemented',**extra):
    slides.append({'number':len(slides)+1,'section':section,'title':title,'text':text,'image':image,'status':status,**extra})

pre_art={'pre_founder_welcome':'story-pre-founder-welcome-v1.png','pre_founder_path':'story-pre-founder-path-v1.png','pre_founder_choice':'story-pre-founder-choice-v1.png'}
for beat in story['sequences']['pre_founder']:
    add('Prologue',beat['kicker'],beat['text'],asset(pre_art[beat['id']]),voice=beat.get('voice'))

founders=[a for a in avatars['avatars'] if a.get('selectableAtLaunch')]
for founder in founders:
    family=scenes['founders'][founder['id']]['family']
    profile=next(p for p in founder_profiles['profiles'] if p['avatar']==founder['id'])
    detail=f"{profile['specialty']} — {profile['ability']['name']}: {profile['ability']['effect']} Stats: "+', '.join(f"{k} {v}/5" for k,v in profile['stats'].items())+f". Upgrade path: {' to '.join(profile['upgradePath'])}."
    add('Founder Selection',founder['name'],detail,asset('story-title-'+family+'-founder-v1.png'),founder=founder['id'],sprite=asset('sprites/'+founder['spriteSpec']['sheet']+'.png'),portraitAtlas=asset('sprites/'+founder_profiles['portraitAtlas']+'.png'),portraitCell=profile['atlasCell'],note='Large selection portrait plus exact floor sprite, balanced starting stats, signature ability, and upgrade path.')

scene_sequences=[('title','Founder Title','opening'),('opening','Chapter 1 · Garage Bay','opening'),('expansion','Chapter 2 · Job Shop','job_shop_expansion')]
for scene_id,scene_label,sequence_id in scene_sequences:
    beats=story['sequences'].get(sequence_id,story['sequences']['opening'])
    summary=' '.join(b['text'] for b in beats)
    for founder in founders:
        family=scenes['founders'][founder['id']]['family'];image=scenes['scenes'][scene_id]['assets'][family]
        add('Founder Scene Variants',f"{scene_label} · {founder['name']}",summary,asset(image),founder=founder['id'],sprite=asset('sprites/'+founder['spriteSpec']['sheet']+'.png'),note=f'Exact {founder["name"]} identity overlay; shared {family} cinematic background.')

# Every playable milestone gets an exact slide for every selectable founder. This
# is intentionally more explicit than the scene summaries above: the storybook is
# the versioned proof that runtime beat order, caption, voice, and player identity
# have not drifted apart.
milestone_sequences=['first_customer','nox_delivery','first_verified_article','first_hire','garage_graduation']
for sequence_id in milestone_sequences:
    for beat in story['sequences'][sequence_id]:
        for founder in founders:
            family=scenes['founders'][founder['id']]['family'];image=scenes['scenes'][beat['visual']]['assets'][family]
            add('Chapter 1 Milestones',f"{beat['kicker']} · {founder['name']}",beat['text'],asset(image),founder=founder['id'],sprite=asset('sprites/'+founder['spriteSpec']['sheet']+'.png'),voice=beat.get('voice'),storySequence=sequence_id,storyBeat=beat['id'],note=f'Exact runtime caption and {founder["name"]} identity proof; Zach is mentor and the founder owns the company decision.')

for stop in tour['stops']:
    add('Shop Tour',f"{stop['order']:02d} · {stop['title']}",stop['text'],station_image(stop),status=stop.get('status','playable'),location=stop['location'],instructions=[stop['operation']],voice=stop.get('voice'))
for task in tasks['tasks']:
    add('Production Tutorials',task['id'].replace('_',' ').upper(),task['text'],station_image(task),status=task['status'],location=task['location'],instructions=task['instructions'],voice=task.get('voice'),success=task['success'])
for hire in hiring['candidates']:
    detail=f"{hire['strength']}. Growth: {hire['growthTo'].replace('_',' ')}. Watch: {hire['flaw']}"
    add('Factory Workforce',f"{hire['title']} · {hire['name']}",detail,asset('story-expansion-male-founder-v1.png'),status='playable',location='Assignable to: '+', '.join(hire['qualifications']),instructions=['Hire through Build Your Team','Assign only to a qualified station','Worker travels, works, and meanders while idle'],success='Visible worker entity is active on the factory floor',portraitAtlas=asset('sprites/'+hiring['profileAtlas']+'.png'),portraitCell=hire['atlasCell'],note='Dedicated employee profile portrait matching the same identity used by the in-shop floor sprite.')
    dialogue=conversations['employees'][hire['id']]
    add('Workforce Conversations',f"TALK WITH {hire['name']}",dialogue['greeting'],asset('story-expansion-male-founder-v1.png'),status='playable',location=hire['title'],instructions=[dialogue['idle'],dialogue['assigned'],f"PLAYER: {dialogue['question']}",f"{hire['name'].upper()}: {dialogue['answer']}"],success='Conversation text advances through greeting, status, question, and role guidance',portraitAtlas=asset('sprites/'+hiring['profileAtlas']+'.png'),portraitCell=hire['atlasCell'],note='Conversation portrait and factory-floor sprite share the same employee identity and roster cell.')
for chapter in story['campaignPlan']['chapters']:
    for beat in chapter['beats']:
        implemented=beat['status']=='implemented';image=asset('story-expansion-male-founder-v1.png') if implemented else None
        needs=[]
        if beat.get('mechanicNeeds'): needs.append('MECHANICS: '+', '.join(beat['mechanicNeeds']))
        if beat.get('visualNeeds'): needs.append('VISUAL: '+beat['visualNeeds'])
        if beat.get('audioNeeds'): needs.append('AUDIO: '+beat['audioNeeds'])
        add(f"Campaign Chapter {chapter['chapter']}",f"{beat['phase'].upper()} · {beat['title']}",beat['text'],image,status=beat['status'],location=f"{chapter['title']} · {chapter['facility'].replace('_',' ').title()}",instructions=needs,success=f"DIFFICULTY: {chapter['difficulty']} · TARGET: {chapter['targetHours'][0]}–{chapter['targetHours'][1]} HOURS",chapter=chapter['chapter'],chapterStatus=chapter['status'],campaignPhase=beat['phase'],note='Production blueprint only; planned beats are not playable and have no generated voice or finished art.' if not implemented else 'Existing Chapter 2 entry is playable; later beats remain explicitly planned.')
for planned in story['plannedSequences']:
    add('Planned Story Gaps',planned['id'].replace('_',' ').upper(),'Not yet implemented. Required before this story beat may be presented as complete.',None,status='planned',instructions=planned['needs'])

manifest={'storybookVersion':1,'gameBuild':release['release'],'slideCount':len(slides),'founderCount':len(founders),'policy':{'oneSlidePerBeat':True,'allFoundersRequired':True,'plannedGapsVisible':True,'publishIntent':'review proof now; comic and short-book source later'},'slides':slides}
(OUT/'storybook-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

html='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>REINDUSTRIALIZE Visual Storybook V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07090c;color:#fff;font-family:Arial,sans-serif}.book{height:100vh;display:grid;grid-template-rows:58px 1fr 76px}.bar{display:flex;align-items:center;gap:18px;padding:8px 22px;background:#0c1118;border-bottom:3px solid #e8b93b}.logo{font:22px "Arial Black";color:#e8b93b;letter-spacing:2px}.counter{margin-left:auto;color:#3fd08a;font-weight:bold}.slide{position:relative;overflow:hidden;background:#111}.art{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(3,5,8,.97) 0%,rgba(3,5,8,.78) 39%,rgba(3,5,8,.08) 72%)}.copy{position:absolute;left:4%;top:8%;bottom:7%;width:40%;display:flex;flex-direction:column;justify-content:center}.section{color:#3fd08a;font:bold 18px "Arial Black";letter-spacing:3px}.copy h1{font:42px/1.04 "Arial Black";margin:14px 0;color:#e8b93b;text-transform:uppercase}.copy p{font-size:20px;line-height:1.35}.meta{font-size:15px;color:#cfd6de;margin-top:10px}.status{display:inline-block;width:max-content;padding:6px 10px;border:2px solid #3fd08a;color:#3fd08a;text-transform:uppercase;font-weight:bold}.status.planned{border-color:#f06c5f;color:#f06c5f}.founder{position:absolute;right:5%;bottom:7%;width:170px;height:255px;object-fit:contain;image-rendering:pixelated;background:rgba(5,8,12,.88);border:4px solid #e8b93b;padding:12px}.note{position:absolute;right:4%;top:5%;max-width:38%;background:rgba(5,8,12,.9);border:2px solid #e8b93b;padding:10px 14px}.missing{position:absolute;inset:12%;display:grid;place-items:center;border:6px dashed #f06c5f;background:#170b0b;color:#f06c5f;font:38px "Arial Black";text-align:center}.nav{display:flex;align-items:center;gap:12px;padding:12px 22px;background:#0c1118;border-top:3px solid #e8b93b}.nav button,.nav select{background:#111923;color:#fff;border:2px solid #e8b93b;padding:10px 15px;font-weight:bold}.nav select{flex:1}.instructions{font-size:15px;line-height:1.35}.instructions li{margin:4px 0}@media(max-width:900px){.copy{width:55%}.copy h1{font-size:30px}.copy p{font-size:16px}.founder{width:110px;height:165px}}
.founderPortrait{position:absolute;right:14%;top:16%;width:430px;height:620px;background-repeat:no-repeat;background-color:rgba(5,8,12,.9);border:5px solid #3fd08a;box-shadow:10px 10px 0 #000;image-rendering:pixelated}.slide.hasPortrait .founder{right:4%;width:125px;height:188px}.slide.hasPortrait .note{top:auto;bottom:4%;right:13%;max-width:430px}@media(max-width:1100px){.founderPortrait{right:5%;width:330px;height:500px}.slide.hasPortrait .founder{display:none}}
</style></head><body><main class="book"><header class="bar"><div class="logo">REINDUSTRIALIZE · VISUAL STORYBOOK V1</div><div id="status"></div><div class="counter" id="counter"></div></header><section class="slide" id="slide"></section><footer class="nav"><button id="prev">◀ PREV</button><select id="picker"></select><button id="next">NEXT ▶</button></footer></main><script>
const BOOK=__BOOK__;let i=Number(new URLSearchParams(location.search).get('slide')||1)-1;i=Math.max(0,Math.min(BOOK.slides.length-1,i));const el=id=>document.getElementById(id);const esc=s=>(s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function render(){const s=BOOK.slides[i];history.replaceState(null,'','?slide='+(i+1));el('counter').textContent=`SLIDE ${i+1} / ${BOOK.slides.length}`;el('status').innerHTML=`<span class="status ${s.status==='planned'?'planned':''}">${esc(s.status)}</span>`;el('picker').value=String(i);el('slide').className='slide'+(s.portraitAtlas?' hasPortrait':'');let instructions=s.instructions?.length?`<ul class="instructions">${s.instructions.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:'',portrait=s.portraitAtlas?`<div class="founderPortrait" style="background-image:url('${s.portraitAtlas}');background-size:500% 200%;background-position:${(s.portraitCell%5)*25}% ${Math.floor(s.portraitCell/5)*100}%"></div>`:'';el('slide').innerHTML=`${s.image?`<img class="art" src="${s.image}">`:`<div class="missing">PLANNED ART GAP<br>${esc(s.title)}</div>`}<div class="shade"></div><div class="copy"><div class="section">${esc(s.section)}</div><h1>${esc(s.title)}</h1><p>${esc(s.text)}</p>${instructions}<div class="meta">${esc(s.location||'')} ${s.voice?' · VOICE: '+esc(s.voice):''} ${s.success?' · SUCCESS: '+esc(s.success):''}</div></div>${portrait}${s.sprite?`<img class="founder" src="${s.sprite}">`:''}${s.note?`<div class="note">${esc(s.note)}</div>`:''}`}
el('picker').innerHTML=BOOK.slides.map((s,n)=>`<option value="${n}">${String(n+1).padStart(2,'0')} · ${esc(s.section)} · ${esc(s.title)}</option>`).join('');el('prev').onclick=()=>{i=(i-1+BOOK.slides.length)%BOOK.slides.length;render()};el('next').onclick=()=>{i=(i+1)%BOOK.slides.length;render()};el('picker').onchange=e=>{i=Number(e.target.value);render()};addEventListener('keydown',e=>{if(e.key==='ArrowRight'){i=(i+1)%BOOK.slides.length;render()}if(e.key==='ArrowLeft'){i=(i-1+BOOK.slides.length)%BOOK.slides.length;render()}});render();
</script></body></html>'''.replace('__BOOK__',json.dumps(manifest))
(OUT/'index.html').write_text(html,encoding='utf-8')
print(f'PASS: visual storybook V1 built with {len(slides)} slides and {len(founders)} founder variants at {OUT}')
