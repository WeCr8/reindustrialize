"""Build a versioned, slide-by-slide visual storybook from canonical game manifests."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'storybook'/'v1'
OUT.mkdir(parents=True,exist_ok=True)
data=lambda name:json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))
story=data('story-production.json');avatars=data('avatars.json');scenes=data('player-scene-manifest.json');tour=data('shop-tour.json');tasks=data('production-task-tutorials.json');station_operations=data('station-operations.json');release=data('release-manifest.json');founder_profiles=data('founder-profiles.json');hiring=data('hiring-roster.json');conversations=data('workforce-conversations.json')
visual_coverage=data('visual-coverage-v1.json');audio_coverage=data('audio-coverage-matrix.json')

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
tour_by_sprite={stop['sprite']:stop for stop in tour['stops']}
equipment_views={'tool_cart':'tool-cart-open-v1','vmc_t2':'vmc-open-v1','lathe_cnc_t2':'lathe-open-v1'}
for sprite,operation in station_operations['stations'].items():
    stop=tour_by_sprite.get(sprite)
    if sprite=='nox_terminal': image=asset('materials/nox-metals-exterior-v1.png')
    elif sprite in equipment_views: image=asset('equipment/'+equipment_views[sprite]+'.png')
    else: image=station_image({'image':sprite})
    timing=f"Standard station time: {operation['cycleMinutes']} minutes." if operation['cycleMinutes'] else 'No active production countdown at this station.'
    mode='playable' if operation['mode'] in {'playable','management','facility'} else 'orientation'
    queue_note='Qualified workers may queue customer-linked batches here; each installed machine adds one fixed-time parallel lane.' if sprite in {'saw_t1','vmc_t2'} else 'No unattended production queue is exposed unless this workflow becomes mechanically playable.'
    add('Station Missions & Timers',operation['name'],operation['details'],image,status=mode,location=sprite,instructions=[operation['mission'],timing,'Selected missions route through safe prerequisites; active timers continue while the founder explores or closes the browser.',queue_note],voice=stop.get('voice') if stop else None,success='Station opens its task/detail surface and reports an honest active, ready, locked, or orientation state.',note='Runtime station-operation evidence; 5-minute saw and 10-minute VMC jobs persist and require collection or inspection. True G/M code is optional Shop Class material.')
for task in tasks['tasks']:
    add('Production Tutorials',task['id'].replace('_',' ').upper(),task['text'],station_image(task),status=task['status'],location=task['location'],instructions=task['instructions'],voice=task.get('voice'),success=task['success'])
for hire in hiring['candidates']:
    detail=f"{hire['strength']}. Growth: {hire['growthTo'].replace('_',' ')}. Watch: {hire['flaw']}"
    columns=hire.get('atlasColumns',5);rows=hire.get('atlasRows',2)
    profile_atlas=hire.get('profileAtlas',hiring['profileAtlas'])
    sprite_atlas=(hiring.get('maintenanceSpriteAtlas') if hire.get('maintenanceQualified') and hire.get('spriteAtlas') else None) or hire.get('spriteAtlas',hiring['spriteAtlas'])
    add('Factory Workforce',f"{hire['title']} · {hire['name']}",detail,asset('story-expansion-male-founder-v1.png'),status='playable',location='Assignable to: '+', '.join(hire['qualifications']),instructions=['Hire through Build Your Team','Assign only to a qualified station','Worker travels, works, and meanders while idle'],success='Visible worker entity is active on the factory floor',portraitAtlas=asset('sprites/'+profile_atlas+'.png'),portraitCell=hire['atlasCell'],portraitColumns=columns,portraitRows=rows,spriteAtlas=asset('sprites/'+sprite_atlas+'.png'),spriteCell=hire['atlasCell'],spriteColumns=columns,spriteRows=rows,employeeId=hire['id'],note='Dedicated employee profile portrait and exact in-shop floor sprite use the same roster identity and atlas cell.')
    dialogue=conversations['employees'][hire['id']]
    add('Workforce Conversations',f"TALK WITH {hire['name']}",dialogue['greeting'],asset('story-expansion-male-founder-v1.png'),status='playable',location=hire['title'],instructions=[dialogue['idle'],dialogue['assigned'],f"PLAYER: {dialogue['question']}",f"{hire['name'].upper()}: {dialogue['answer']}"],success='Conversation text advances through greeting, status, question, and role guidance',portraitAtlas=asset('sprites/'+profile_atlas+'.png'),portraitCell=hire['atlasCell'],portraitColumns=columns,portraitRows=rows,spriteAtlas=asset('sprites/'+sprite_atlas+'.png'),spriteCell=hire['atlasCell'],spriteColumns=columns,spriteRows=rows,employeeId=hire['id'],note='Conversation portrait and factory-floor sprite share the same employee identity and roster cell.')
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

for slide in slides:
    if slide.get('voice'):
        shipped=ROOT/'packages/assets/audio/zach'/f"{slide['voice']}.mp3"
        generated=ROOT/'packages/assets/audio/generated/voice'/f"{slide['voice']}.mp3"
        if shipped.exists(): slide['voiceSrc']=uri(shipped.relative_to(ROOT))
        elif generated.exists(): slide['voiceSrc']=uri(generated.relative_to(ROOT))

reference_files=[]
for folder in ['data','packages/assets','demo/remotion/src']:
    base=ROOT/folder
    if not base.exists(): continue
    reference_files.extend(p for p in base.rglob('*') if p.is_file() and p.suffix.lower() in {'.json','.js','.mjs','.ts','.tsx','.py','.html','.md'} and p.stat().st_size<5_000_000)
reference_files.extend([ROOT/'scripts/build_level_viewer_v4.py',ROOT/'scripts/build-cloudflare-site.mjs',ROOT/'apps/playreind-landing/index.html'])
reference_text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in reference_files if p.exists())

def dimensions(path):
    raw=path.read_bytes()[:24]
    if len(raw)>=24 and raw[:8]==b'\x89PNG\r\n\x1a\n': return [int.from_bytes(raw[16:20],'big'),int.from_bytes(raw[20:24],'big')]
    return None

catalog=[]
for media in sorted((ROOT/'packages/assets').rglob('*')):
    if not media.is_file() or media.suffix.lower() not in {'.png','.mp3'}: continue
    rel=media.relative_to(ROOT).as_posix();stem=media.stem;refs=reference_text.count(media.name)+reference_text.count(stem)
    parts=set(media.parts);lower=rel.lower()
    if 'generated' in parts: lifecycle='generated-candidate'
    elif 'legacy' in lower or '-source.' in lower: lifecycle='source-reference'
    elif refs: lifecycle='implemented-reference'
    else: lifecycle='storybook-review'
    kind='graphic' if media.suffix.lower()=='.png' else 'audio'
    if kind=='graphic':
        category='sprite' if '/sprites/' in rel else 'equipment' if '/equipment/' in rel else 'customer' if '/customers/' in rel else 'tool' if '/tools/' in rel else 'story'
    else:
        category='voice' if '/zach/' in rel or '/voice/' in rel else 'music' if '/music/' in rel else 'sfx'
    item={'id':stem,'kind':kind,'category':category,'path':rel,'src':uri(rel),'lifecycle':lifecycle,'referenceCount':refs,'bytes':media.stat().st_size}
    if kind=='graphic': item['dimensions']=dimensions(media)
    catalog.append(item)

missing=[]
for chapter in visual_coverage['chapters']:
    for need in chapter.get('missing',[]): missing.append({'kind':'graphic','chapter':chapter['chapter'],'status':'needed','need':need})
for chapter in audio_coverage['chapters']:
    for category,entry in chapter['coverage'].items():
        if entry['status']!='implemented': missing.append({'kind':'audio','chapter':chapter['chapter'],'status':entry['status'],'need':entry['need'],'category':category})
for planned in story['plannedSequences']:
    for need in planned['needs']: missing.append({'kind':'story','chapter':None,'status':'planned','need':need,'sequence':planned['id']})

manifest={'storybookVersion':1,'gameBuild':release['release'],'slideCount':len(slides),'founderCount':len(founders),'employeeCount':len(hiring['candidates']),'policy':{'oneSlidePerBeat':True,'allFoundersRequired':True,'allEmployeesRequireProfileAndSprite':True,'allPackagedGraphicsAndAudioCataloged':True,'plannedGapsVisible':True,'publishIntent':'review proof now; comic and short-book source later'},'assetSummary':{'total':len(catalog),'graphics':sum(x['kind']=='graphic' for x in catalog),'audio':sum(x['kind']=='audio' for x in catalog),'sprites':sum(x['category']=='sprite' for x in catalog),'missingNeeds':len(missing)},'assetCatalog':catalog,'missingNeeds':missing,'slides':slides}
(OUT/'storybook-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="index,follow,max-image-preview:large"><title>REINDUSTRIALIZE Visual Storybook V1</title><style>
:root{--ink:#07090c;--panel:#0c141b;--gold:#e8b93b;--green:#3fd08a;--red:#f06c5f;--line:#42515c}*{box-sizing:border-box}html,body{max-width:100%;overflow-x:hidden}body{margin:0;background:var(--ink);color:#fff;font-family:Inter,Arial,sans-serif}.book{width:100%;height:100dvh;display:grid;grid-template-rows:auto minmax(0,1fr) auto}.bar{display:flex;align-items:center;gap:12px;min-width:0;min-height:62px;padding:8px 18px;background:#0c1118;border-bottom:3px solid var(--gold)}.logo{font:20px "Arial Black";color:var(--gold);letter-spacing:2px}.viewTabs{display:flex;min-width:0;gap:7px;margin-left:auto}.viewTabs button,.nav button,.nav select,.catalogTools input,.catalogTools select{min-height:42px;min-width:0;background:#111923;color:#fff;border:2px solid var(--line);padding:8px 12px;font-weight:800}.viewTabs button.active{border-color:var(--green);color:var(--green)}.counter{min-width:138px;color:var(--green);font-weight:900;text-align:right}.stage{min-width:0;min-height:0;overflow:hidden}.slide{position:relative;width:100%;height:100%;overflow:hidden;background:#111}.art{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(3,5,8,.98) 0%,rgba(3,5,8,.82) 43%,rgba(3,5,8,.12) 77%)}.copy{position:absolute;z-index:2;left:4%;top:5%;bottom:5%;width:43%;display:flex;flex-direction:column;justify-content:center;overflow:auto;padding-right:8px}.section{color:var(--green);font:bold 16px "Arial Black";letter-spacing:3px}.copy h1{font:clamp(28px,3.4vw,52px)/1.02 "Arial Black";margin:12px 0;color:var(--gold);text-transform:uppercase}.copy p{font-size:clamp(15px,1.45vw,21px);line-height:1.35}.meta{font-size:13px;color:#cfd6de;margin-top:8px}.status{display:inline-block;width:max-content;padding:5px 8px;border:2px solid var(--green);color:var(--green);text-transform:uppercase;font-weight:bold}.status.planned{border-color:var(--red);color:var(--red)}.founder{position:absolute;right:3%;bottom:5%;width:135px;height:202px;object-fit:contain;image-rendering:pixelated;background:#05080ce8;border:3px solid var(--gold);padding:8px}.note{position:absolute;right:3%;top:4%;max-width:42%;background:#05080ced;border:2px solid var(--gold);padding:9px 12px}.missing{position:absolute;inset:10%;display:grid;place-items:center;border:6px dashed var(--red);background:#170b0b;color:var(--red);font:34px "Arial Black";text-align:center}.instructions{font-size:14px;line-height:1.3}.instructions li{margin:3px 0}.atlasPair{position:absolute;right:12%;top:13%;display:flex;align-items:end;gap:14px}.atlasCrop{background-repeat:no-repeat;background-color:#081018;border:4px solid var(--green);box-shadow:8px 8px 0 #000}.profileCrop{width:min(28vw,390px);height:min(67vh,570px)}.spriteCrop{width:140px;height:190px;image-rendering:pixelated;border-color:var(--gold)}.voice{width:min(100%,420px);height:38px;margin-top:10px}.nav{display:flex;align-items:center;min-width:0;gap:10px;padding:10px 18px;background:#0c1118;border-top:3px solid var(--gold)}.nav select{flex:1;width:0}.catalog{height:100%;overflow:auto;padding:22px}.catalogHead{display:flex;justify-content:space-between;gap:18px;align-items:end}.catalogHead h1{margin:0;color:var(--gold);font:36px "Arial Black";text-transform:uppercase}.summary{color:#b8c5cc}.catalogTools{position:sticky;z-index:4;top:-22px;display:grid;grid-template-columns:2fr 1fr 1fr;gap:8px;padding:12px 0;background:var(--ink)}.assetGrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.assetCard{min-width:0;padding:10px;background:var(--panel);border:1px solid var(--line)}.assetCard img{width:100%;height:170px;object-fit:contain;background:#05090c;image-rendering:pixelated}.assetCard audio{width:100%;max-width:100%;margin:53px 0}.assetCard h2{margin:8px 0 4px;font-size:15px;overflow-wrap:anywhere}.assetCard code{display:block;color:#aebcc4;font-size:10px;overflow-wrap:anywhere}.badge{display:inline-block;margin:4px 4px 0 0;padding:3px 5px;border:1px solid var(--green);color:var(--green);font:800 10px monospace;text-transform:uppercase}.badge.warn{border-color:var(--gold);color:var(--gold)}.needs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;margin-top:18px}.need{min-width:0;padding:12px;background:#160d0d;border:1px solid #7f3f39}.need b{color:var(--red)}.hidden{display:none!important}@media(max-width:1000px){.assetGrid{grid-template-columns:repeat(2,1fr)}.needs{grid-template-columns:1fr 1fr}.atlasPair{right:4%}.profileCrop{width:300px;height:450px}.slide.hasAtlas .founder,.slide.hasAtlas .note{display:none}}@media(max-width:680px){.book{grid-template-rows:auto minmax(0,1fr) auto}.bar{align-items:flex-start;flex-wrap:wrap;padding:7px 9px}.logo{max-width:220px;font-size:13px;letter-spacing:1px}.viewTabs{order:3;width:100%;margin:0}.viewTabs button{flex:1;padding:5px;font-size:11px}.counter{min-width:0;margin-left:auto;font-size:12px}.copy{left:4%;top:3%;bottom:3%;width:63%}.copy h1{font-size:25px}.copy p{font-size:14px}.instructions{font-size:12px}.atlasPair{right:2%;top:15%;display:block}.profileCrop{width:32vw;height:46vh}.spriteCrop{width:26vw;height:22vh;margin-top:8px}.note{display:none}.founder{width:28vw;height:32vh;right:2%}.nav{padding:7px}.nav button{padding:5px 8px;font-size:11px}.catalog{padding:12px}.catalogHead{display:block}.catalogHead h1{font-size:27px}.catalogTools{top:-12px;grid-template-columns:1fr}.assetGrid,.needs{grid-template-columns:minmax(0,1fr)}.assetCard img{height:210px}}
</style></head><body><main class="book"><header class="bar"><div class="logo">REINDUSTRIALIZE · STORYBOOK V1</div><div class="viewTabs" role="group" aria-label="Storybook views"><button data-view="slides">Story slides</button><button data-view="assets">Asset library</button><button data-view="needs">Missing needs</button></div><div class="counter" id="counter"></div></header><div class="stage" id="stage"></div><footer class="nav" id="nav"><button id="prev">◀ PREV</button><select id="picker" aria-label="Choose story slide"></select><button id="next">NEXT ▶</button></footer></main><script>
const BOOK=__BOOK__,el=id=>document.getElementById(id),esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));let params=new URLSearchParams(location.search),view=params.get('view')||'slides',i=Math.max(0,Math.min(BOOK.slides.length-1,Number(params.get('slide')||1)-1));
const atlas=(src,cell,columns=5,rows=2,className='profileCrop',label='Atlas crop')=>{const x=cell%columns,y=Math.floor(cell/columns),px=columns===1?0:x*100/(columns-1),py=rows===1?0:y*100/(rows-1);return `<div class="atlasCrop ${className}" role="img" aria-label="${esc(label)}" style="background-image:url('${src}');background-size:${columns*100}% ${rows*100}%;background-position:${px}% ${py}%"></div>`};
function setUrl(){history.replaceState(null,'',`?view=${view}${view==='slides'?'&slide='+(i+1):''}`)}function setTabs(){document.querySelectorAll('[data-view]').forEach(button=>button.classList.toggle('active',button.dataset.view===view));el('nav').classList.toggle('hidden',view!=='slides');setUrl()}
function renderSlide(){const s=BOOK.slides[i],instructions=s.instructions?.length?`<ul class="instructions">${s.instructions.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:'',profile=s.portraitAtlas?atlas(s.portraitAtlas,s.portraitCell,s.portraitColumns||5,s.portraitRows||2,'profileCrop',`${s.title} profile portrait`):'',floor=s.spriteAtlas?atlas(s.spriteAtlas,s.spriteCell,s.spriteColumns||5,s.spriteRows||2,'spriteCrop',`${s.title} floor sprite`):'';el('counter').textContent=`SLIDE ${i+1} / ${BOOK.slides.length}`;el('picker').value=String(i);el('stage').innerHTML=`<section class="slide ${(profile||floor)?'hasAtlas':''}">${s.image?`<img class="art" src="${s.image}" alt="${esc(s.title)} story scene">`:`<div class="missing">PLANNED ART GAP<br>${esc(s.title)}</div>`}<div class="shade"></div><div class="copy"><span class="status ${s.status==='planned'?'planned':''}">${esc(s.status)}</span><div class="section">${esc(s.section)}</div><h1>${esc(s.title)}</h1><p>${esc(s.text)}</p>${instructions}<div class="meta">${esc(s.location||'')}${s.voice?' · VOICE: '+esc(s.voice):''}${s.success?' · SUCCESS: '+esc(s.success):''}</div>${s.voiceSrc?`<audio class="voice" controls preload="none" src="${s.voiceSrc}">Voice playback unavailable.</audio>`:''}</div>${(profile||floor)?`<div class="atlasPair">${profile}${floor}</div>`:''}${s.sprite?`<img class="founder" src="${s.sprite}" alt="${esc(s.title)} floor sprite">`:''}${s.note?`<div class="note">${esc(s.note)}</div>`:''}</section>`;setTabs()}
function assetCard(item){const media=item.kind==='graphic'?`<img loading="lazy" src="${item.src}" alt="${esc(item.id)} ${esc(item.category)} asset">`:`<audio controls preload="none" src="${item.src}">Audio playback unavailable.</audio>`;return `<article class="assetCard" data-kind="${item.kind}" data-category="${item.category}" data-life="${item.lifecycle}" data-search="${esc((item.id+' '+item.path).toLowerCase())}">${media}<h2>${esc(item.id)}</h2><code>${esc(item.path)}</code><span class="badge">${esc(item.category)}</span><span class="badge ${item.lifecycle==='implemented-reference'?'':'warn'}">${esc(item.lifecycle)}</span><span class="badge">REFS ${item.referenceCount}</span>${item.dimensions?`<span class="badge">${item.dimensions[0]}×${item.dimensions[1]}</span>`:''}</article>`}
function filterAssets(){const query=el('assetSearch').value.trim().toLowerCase(),kind=el('assetKind').value,life=el('assetLife').value;document.querySelectorAll('.assetCard').forEach(card=>card.classList.toggle('hidden',!!((query&&!card.dataset.search.includes(query))||(kind!=='all'&&card.dataset.kind!==kind)||(life!=='all'&&card.dataset.life!==life))));el('visibleAssets').textContent=`${document.querySelectorAll('.assetCard:not(.hidden)').length} shown`}
function renderAssets(){el('counter').textContent=`${BOOK.assetSummary.total} ASSETS`;el('stage').innerHTML=`<section class="catalog"><div class="catalogHead"><div><h1>Complete asset library</h1><p class="summary">Every packaged graphic and audio file is visible here with lifecycle and canonical-reference status. Review-only, source, legacy, and generated candidates are never mislabeled as live gameplay.</p></div><b>${BOOK.assetSummary.graphics} graphics · ${BOOK.assetSummary.sprites} sprite assets · ${BOOK.assetSummary.audio} audio</b></div><div class="catalogTools"><input id="assetSearch" type="search" placeholder="Search asset name or path"><select id="assetKind"><option value="all">All media</option><option value="graphic">Graphics</option><option value="audio">Audio</option></select><select id="assetLife"><option value="all">All lifecycle states</option>${[...new Set(BOOK.assetCatalog.map(x=>x.lifecycle))].map(x=>`<option>${x}</option>`).join('')}</select></div><div id="visibleAssets" class="summary"></div><div class="assetGrid">${BOOK.assetCatalog.map(assetCard).join('')}</div></section>`;['assetSearch','assetKind','assetLife'].forEach(id=>el(id).addEventListener(id==='assetSearch'?'input':'change',filterAssets));filterAssets();setTabs()}
function renderNeeds(){el('counter').textContent=`${BOOK.missingNeeds.length} OPEN NEEDS`;el('stage').innerHTML=`<section class="catalog"><div class="catalogHead"><div><h1>Production needs queue</h1><p class="summary">This is the explicit backlog for missing graphics, narration, sound, music, mechanics, and later-chapter coverage. Adding a canonical need here prevents silent gaps.</p></div><b>${BOOK.assetSummary.missingNeeds} tracked needs</b></div><div class="needs">${BOOK.missingNeeds.map(item=>`<article class="need"><b>${esc(item.kind)} · ${item.chapter?'CHAPTER '+item.chapter:'GLOBAL'} · ${esc(item.status)}</b><p>${esc(item.need)}</p>${item.category?`<span class="badge warn">${esc(item.category)}</span>`:''}</article>`).join('')}</div></section>`;setTabs()}
function render(){if(view==='assets')renderAssets();else if(view==='needs')renderNeeds();else renderSlide()}el('picker').innerHTML=BOOK.slides.map((s,n)=>`<option value="${n}">${String(n+1).padStart(3,'0')} · ${esc(s.section)} · ${esc(s.title)}</option>`).join('');el('prev').onclick=()=>{i=(i-1+BOOK.slides.length)%BOOK.slides.length;render()};el('next').onclick=()=>{i=(i+1)%BOOK.slides.length;render()};el('picker').onchange=event=>{i=Number(event.target.value);render()};document.querySelectorAll('[data-view]').forEach(button=>button.onclick=()=>{view=button.dataset.view;render()});addEventListener('keydown',event=>{if(view!=='slides')return;if(event.key==='ArrowRight'){i=(i+1)%BOOK.slides.length;render()}if(event.key==='ArrowLeft'){i=(i-1+BOOK.slides.length)%BOOK.slides.length;render()}});render();
</script></body></html>'''.replace('__BOOK__',json.dumps(manifest))
(OUT/'index.html').write_text(html,encoding='utf-8')
print(f"PASS: visual storybook V1 built with {len(slides)} slides, {len(founders)} founders, {len(hiring['candidates'])} employees, {len(catalog)} cataloged assets, and {len(missing)} tracked needs at {OUT}")
