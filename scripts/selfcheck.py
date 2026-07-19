#!/usr/bin/env python3
"""
REINDUSTRIALIZE selfcheck — find bugs, self-repair what's safe, report the rest.
Run: python3 scripts/selfcheck.py [--fix]   (--fix enables auto-repairs; default report-only? No:
safe fixes are applied by default and reported as AUTO-FIXED; use --dry to disable.)
Exit code 0 = clean/warns only, 1 = errors remain.
"""
import json, os, sys, itertools

ROOT = os.path.join(os.path.dirname(__file__), "..")
DRY = "--dry" in sys.argv
issues = {"ERROR": [], "WARN": [], "AUTO-FIXED": []}
def err(m): issues["ERROR"].append(m)
def warn(m): issues["WARN"].append(m)
def fixed(m): issues["AUTO-FIXED"].append(m)

def load(p):
    try:
        return json.load(open(os.path.join(ROOT, p)))
    except Exception as e:
        err(f"{p}: unparseable JSON ({e})"); return None

def save(p, data):
    if not DRY:
        json.dump(data, open(os.path.join(ROOT, p), "w"), indent=1)

machines = load("data/machines.json")
quests   = load("data/quests.json")
chars    = load("data/characters.json")
vendors  = load("data/vendors.json")
gcode    = load("data/gcode-challenges.json")
shopcls  = load("data/shopclass.json")
prog     = load("data/progression.json")
facilities = load("data/facilities.json")
career = load("data/career-progression.json")
equipment_views = load("data/equipment-views.json")
hires = load("data/hiring-roster.json")
zach_identity = load("data/zach-visual-identity.json")
atlas    = load("packages/assets/sprites/atlas.json")
maps     = {m: load(f"data/maps/{m}.json") for m in ("bay_01", "bay_02")}

# ---------- 1. Machine balance invariants ----------
if machines:
    seen_ids = set()
    for m in machines["machines"]:
        mid = m["id"]
        if mid in seen_ids: err(f"machines: duplicate id {mid}")
        seen_ids.add(mid)
        if m["tier"] >= 3 and not m["automation"]["mtconnect"]:
            m["automation"]["mtconnect"] = True
            fixed(f"machines/{mid}: tier {m['tier']} must be mtconnect - set true")
        PROD = {"saw","mill","vmc","lathe","bench"}
        if m["class"] in PROD and m["tier"] < 5 and m["quality"] * m["reliability"] > 0.97:
            err(f"machines/{mid}: quality*reliability={m['quality']*m['reliability']:.3f} > 0.97 below tier 5")
        if m["price"] <= 0: err(f"machines/{mid}: nonpositive price")
    # tier pricing sanity per class
    byclass = {}
    for m in machines["machines"]:
        byclass.setdefault(m["class"], []).append(m)
    for cls, ms in byclass.items():
        ms.sort(key=lambda x: x["tier"])
        for a, b in zip(ms, ms[1:]):
            if b["tier"] > a["tier"] and b["price"] < a["price"]:
                warn(f"machines: {b['id']} (t{b['tier']}) cheaper than {a['id']} (t{a['tier']}) in class {cls}")
    save("data/machines.json", machines)

# ---------- 2. Quest cross-references ----------
KNOWN_EVENTS = {
    "job.accepted","job.shipped","machine.purchased","machine.cycle_complete","machine.connected",
    "machine.alarm","setup.completed","network.node_installed","dashboard.viewed","tool.preset",
    "handoff.completed","robot.purchased","robot.install_started","robot.programmed",
    "material.ordered","material.received","gcode.challenge_passed","avatar.created",
    "shopclass.entered","shopclass.lesson_passed","quest.completed",
    "bridge.machine_connected","bridge.handoff_completed","bridge.oee_improved",
}
if quests:
    qids = set()
    for q in quests["quests"]:
        if q["id"] in qids: err(f"quests: duplicate id {q['id']}")
        qids.add(q["id"])
        for s in q["steps"]:
            if s["event"] not in KNOWN_EVENTS:
                err(f"quests/{q['id']}: unknown event '{s['event']}' (add to sim or fix typo)")
        for key in ("zachIntro", "zachOutro"):
            if not q.get(key): warn(f"quests/{q['id']}: missing {key}")
    # machine questHooks must exist
    if machines:
        for m in machines["machines"]:
            for h in m.get("questHooks", []):
                if h not in qids and h not in ("first_finish","first_cut","first_part","first_turned_part",
                                               "no_more_missing_tools","lights_out_night","material_flow_master"):
                    warn(f"machines/{m['id']}: questHook '{h}' has no quest yet (backlog ok)")

# ---------- 3. G-code challenge sanity ----------
if gcode:
    for c in gcode["challenges"]:
        toks = set()
        for lineno, ln in enumerate(c["program"]):
            i = 0
            while "{{" in ln[i:]:
                s = ln.index("{{", i); e = ln.index("}}", s)
                toks.add(ln[s+2:e]); i = e
        declared = set(c["blanks"].keys())
        for t in toks - declared: err(f"gcode/{c['id']}: blank '{{{{{t}}}}}' in program but not declared")
        for t in declared - toks: err(f"gcode/{c['id']}: declared blank '{t}' never used in program")
        if len(declared) > 3: warn(f"gcode/{c['id']}: {len(declared)} blanks (>3, one concept per challenge)")
        # unlock refs
        for b in c["blanks"].values():
            if b.get("validate") == "range" and "compute" not in b and "min" not in b:
                err(f"gcode/{c['id']}: range blank without compute or min/max")

# ---------- 4. Shop Class links ----------
if shopcls and quests and gcode:
    qids = {q["id"] for q in quests["quests"]}
    gids = {c["id"] for c in gcode["challenges"]}
    unlockables = qids | gids | {"nox_catalog_full"}
    for l in shopcls["lessons"]:
        if l.get("unlocks") and l["unlocks"] not in unlockables:
            warn(f"shopclass/{l['id']}: unlocks '{l['unlocks']}' not found in quests/challenges")

# ---------- 5. Maps: bounds, overlaps, atlas refs, footprint match ----------
if atlas:
    for mid, mp in maps.items():
        if not mp: continue
        w, h = mp["size"]
        rects = []
        for p in mp["placements"]:
            x, y = p["tile"]; fw, fh = p["footprint"]
            if x < 1 or y < 1 or x + fw > w - 1 or y + fh > h - 1:
                err(f"{mid}: {p['sprite']} at {p['tile']} exceeds playable bounds")
            for (ox, oy, ow, oh, os_) in rects:
                if x < ox + ow and ox < x + fw and y < oy + oh and oy < y + fh:
                    err(f"{mid}: {p['sprite']} overlaps {os_}")
            rects.append((x, y, fw, fh, p["sprite"]))
            a = atlas.get(p["sprite"])
            if not a:
                err(f"{mid}: sprite '{p['sprite']}' not in atlas")
            else:
                render_tile = 64  # HD gameplay renderer: two source pixels per logical map pixel
                if a["fw"] > fw * render_tile or a["fh"] > fh * render_tile + 32:  # tall-sprite allowance
                    warn(f"{mid}: {p['sprite']} art {a['fw']}x{a['fh']} larger than footprint {fw*render_tile}x{fh*render_tile}")
        sx, sy = mp["spawn"]
        for (ox, oy, ow, oh, os_) in rects:
            if ox <= sx < ox + ow and oy <= sy < oy + oh:
                err(f"{mid}: spawn {mp['spawn']} inside {os_}")

# ---------- 6. Character/atlas refs ----------
if chars and atlas:
    for ch in chars["characters"]:
        sheet = ch.get("spriteSpec", {}).get("sheet")
        if sheet and sheet not in atlas:
            warn(f"characters/{ch['id']}: sheet '{sheet}' not generated yet")

# ---------- 7. Vendor SFM coverage for gcode compute ----------
if vendors and gcode:
    has_sfm = all("sfm" in i for v in vendors["vendors"] for i in v.get("catalog", []))
    if not has_sfm: err("vendors: catalog item missing sfm (gcode compute depends on it)")

# ---------- 8. Progression gate refs ----------
if prog and shopcls and gcode:
    lids = {l["id"] for l in shopcls["lessons"]}
    gids = {c["id"] for c in gcode["challenges"]}
    for t in prog["tiers"]:
        g = t.get("masteryGate", {})
        for l in g.get("lessons", []):
            if l not in lids: err(f"progression tier {t['tier']}: unknown lesson '{l}'")
        for c in g.get("gcodePassed", []):
            if c not in gids: err(f"progression tier {t['tier']}: unknown challenge '{c}'")

# ---------- Report ----------
# ---------- 9. Facility growth arc ----------
if facilities:
    fs = facilities.get("facilities", [])
    ids = {f["id"] for f in fs}
    if len(ids) != len(fs): err("facilities: duplicate id")
    for a, b in zip(fs, fs[1:]):
        if b["floorAreaSqFt"] <= a["floorAreaSqFt"]:
            err(f"facilities: {b['id']} must be larger than {a['id']}")
        if a.get("next") != b["id"]:
            err(f"facilities: {a['id']} next must point to {b['id']}")
    for f in fs:
        if f.get("next") and f["next"] not in ids: err(f"facilities/{f['id']}: unknown next '{f['next']}'")

# ---------- 10. Career progression references ----------
if career and facilities and machines:
    fids = {f["id"] for f in facilities["facilities"]}
    mids = {m["id"] for m in machines["machines"]}
    sids = {s["id"] for s in (load("data/skills-tree.json") or {}).get("playerSkills", [])}
    mins = [b["min"] for b in career["reputation"]["bands"]]
    if mins != sorted(mins) or len(mins) != len(set(mins)): err("career: reputation bands must be unique and ascending")
    for d in career["departments"]:
        if d["unlocksAtFacility"] not in fids: err(f"career/departments/{d['id']}: unknown facility")
    for c in career["chapterUnlocks"]:
        if c["facility"] not in fids: err(f"career/chapter {c['chapter']}: unknown facility")
        for mid in c["machines"]:
            if mid not in mids: err(f"career/chapter {c['chapter']}: unknown machine '{mid}'")
        for sid in c["skills"]:
            if sid not in sids: err(f"career/chapter {c['chapter']}: unknown skill '{sid}'")

# ---------- 11. Opened equipment views ----------
if equipment_views and machines:
    mids = {m["id"] for m in machines["machines"]} | {"tool_cart"}
    for vid, view in equipment_views["views"].items():
        if vid not in mids: err(f"equipment-views: unknown equipment '{vid}'")
        if not os.path.exists(os.path.join(ROOT, "packages", "assets", view["asset"])): err(f"equipment-views/{vid}: missing asset '{view['asset']}'")

# ---------- 12. Hiring roster ----------
if hires and facilities and machines:
    fids = {f["id"] for f in facilities["facilities"]}; mids = {m["id"] for m in machines["machines"]}
    for map_data in maps.values(): mids.update(p["sprite"] for p in map_data.get("placements", []))
    atlas_path = os.path.join(ROOT, "packages", "assets", "sprites", hires.get("spriteAtlas", "") + ".png")
    if not os.path.exists(atlas_path): err("hires: missing workforce sprite atlas")
    for h in hires["candidates"]:
        if h["unlocksAtFacility"] not in fids: err(f"hires/{h['id']}: unknown facility")
        if not isinstance(h.get("atlasCell"), int): err(f"hires/{h['id']}: missing atlas cell")
        for mid in h["qualifications"]:
            if mid not in mids: err(f"hires/{h['id']}: unknown qualification '{mid}'")

# ---------- 13. Zach visual identity ----------
if zach_identity:
    for role, asset in zach_identity["activeAssets"].items():
        variants = asset.values() if isinstance(asset, dict) else [asset]
        for variant in variants:
            if not os.path.exists(os.path.join(ROOT, "packages", "assets", variant)):
                err(f"zach-identity/{role}: missing active asset '{variant}'")
    if zach_identity.get("role") != "mentor_only": err("zach-identity: Zach must remain mentor_only")

# ---------- Report ----------
print("=" * 56)
print("REINDUSTRIALIZE SELFCHECK" + (" (dry run)" if DRY else ""))
print("=" * 56)
for level in ("AUTO-FIXED", "ERROR", "WARN"):
    for m in issues[level]:
        print(f"[{level}] {m}")
print("-" * 56)
print(f"auto-fixed: {len(issues['AUTO-FIXED'])}  errors: {len(issues['ERROR'])}  warns: {len(issues['WARN'])}")
sys.exit(1 if issues["ERROR"] else 0)
