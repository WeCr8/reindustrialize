#!/usr/bin/env python3
"""
REINDUSTRIALIZE pixel art generator v0.1 ("programmer art, on-brand").
Generates palette-locked 16-bit style sprites: tileset, machines, characters.
Output: packages/assets/sprites/*.png + atlas.json. These are playable placeholders
that establish footprints/states; final art gets regenerated via skills/sprite-spec.
"""
from PIL import Image, ImageDraw
import json, os, hashlib

OUT = os.path.join(os.path.dirname(__file__), "..", "packages", "assets", "sprites")
os.makedirs(OUT, exist_ok=True)

# ---- Palette (packages/assets/palette.json) ----
P = {
    "K": (10, 11, 14),        # near-black outline
    "navy": (26, 46, 68), "navy2": (14, 24, 38),
    "orange": (232, 73, 29), "gold": (232, 185, 59),
    "sky": (74, 159, 212), "green": (63, 208, 138), "greendim": (29, 122, 79),
    "alert": (208, 67, 63), "purple": (155, 89, 208),
    "s1": (43, 47, 54), "s2": (74, 79, 88), "s3": (110, 116, 127),
    "s4": (154, 161, 171), "s5": (196, 201, 208),
    "w1": (90, 70, 50), "w2": (138, 106, 72), "w3": (201, 160, 94),
    "skin": (201, 160, 94), "denim": (44, 74, 110), "white": (230, 235, 238),
    "T": (0, 0, 0, 0),        # transparent
}

def canvas(w, h): return Image.new("RGBA", (w, h), P["T"])
def d(img): return ImageDraw.Draw(img)

def R(dr, x, y, w, h, c, outline=True):
    dr.rectangle([x, y, x + w - 1, y + h - 1], fill=P[c])
    if outline: dr.rectangle([x, y, x + w - 1, y + h - 1], outline=P["K"])

def px(dr, x, y, c): dr.point((x, y), fill=P[c])

ATLAS = {}
def save(img, name, frames=1, fw=None, fh=None):
    img.save(os.path.join(OUT, f"{name}.png"))
    ATLAS[name] = {"file": f"{name}.png", "w": img.width, "h": img.height,
                   "frames": frames, "fw": fw or img.width // frames, "fh": fh or img.height}

# ================= TILESET (32x32 each, one strip) =================
def tile_floor(seed=0):
    t = canvas(32, 32); dr = d(t)
    dr.rectangle([0, 0, 31, 31], fill=P["s2"])
    dr.rectangle([0, 0, 31, 31], outline=P["s1"])
    for i in range(6):  # speckle
        x = (seed * 7 + i * 11) % 30 + 1; y = (seed * 13 + i * 5) % 30 + 1
        px(dr, x, y, "s3")
    return t

def tile_tape():
    t = tile_floor(2); dr = d(t)
    dr.rectangle([0, 13, 31, 18], fill=P["gold"])
    for x in range(0, 32, 8): dr.rectangle([x, 13, x + 3, 18], fill=P["K"])
    return t

def tile_wall():
    t = canvas(32, 32); dr = d(t)
    dr.rectangle([0, 0, 31, 31], fill=P["navy"])
    dr.rectangle([0, 0, 31, 31], outline=P["K"])
    for yy in (8, 16, 24): dr.line([(0, yy), (31, yy)], fill=P["navy2"])
    for i, xx in enumerate((10, 22, 4, 16, 28, 10)):
        dr.line([(xx if i % 2 == 0 else xx - 6, i * 5 + 3)] * 2, fill=P["navy2"])
    return t

def tile_dock():
    t = canvas(32, 32); dr = d(t)
    dr.rectangle([0, 0, 31, 31], fill=P["s3"]); dr.rectangle([0, 0, 31, 31], outline=P["K"])
    for yy in range(2, 30, 5): dr.line([(2, yy), (29, yy)], fill=P["s2"])  # roll-up slats
    dr.rectangle([12, 26, 19, 31], fill=P["gold"])  # handle
    return t

def tile_zone(color):
    t = tile_floor(4); dr = d(t)
    dr.rectangle([1, 1, 30, 30], outline=P[color])
    dr.rectangle([2, 2, 29, 29], outline=P[color])
    return t

strip = canvas(32 * 7, 32)
for i, tl in enumerate([tile_floor(0), tile_floor(1), tile_tape(), tile_wall(),
                        tile_dock(), tile_zone("sky"), tile_zone("orange")]):
    strip.paste(tl, (i * 32, 0))
save(strip, "tileset", frames=7, fw=32, fh=32)
# tile ids: 0 floor,1 floor2,2 tape,3 wall,4 dock,5 zone_recv(sky),6 zone_ship(orange)

# ================= MACHINES =================
def machine_vmc(running=False):
    """3x3 tiles (96x96). Haas-style VMC: sheet-metal enclosure, window, control pendant."""
    m = canvas(96, 96); dr = d(m)
    R(dr, 4, 10, 88, 82, "s4")                       # enclosure
    R(dr, 8, 14, 80, 10, "s5")                       # top band
    dr.text((14, 14), "VMC-2S", fill=P["K"])
    R(dr, 12, 28, 44, 40, "navy2")                   # window
    if running:
        R(dr, 28, 40, 12, 16, "s3")                  # spindle head
        dr.rectangle([30, 56, 37, 60], fill=P["sky"])# coolant spray
        dr.rectangle([14, 62, 52, 66], fill=P["w2"]) # chips
    else:
        R(dr, 28, 34, 12, 16, "s3")
    dr.rectangle([12, 28, 55, 67], outline=P["K"])
    R(dr, 62, 26, 26, 34, "s2")                      # control pendant
    R(dr, 65, 29, 20, 14, "greendim" if not running else "green", outline=False)
    dr.rectangle([65, 29, 84, 42], outline=P["K"])
    for i in range(6):                                # keypad
        px(dr, 66 + (i % 3) * 7, 47 + (i // 3) * 5, "s5")
    R(dr, 40, 2, 14, 10, "alert" if running else "s3")   # beacon
    R(dr, 4, 84, 88, 8, "s1")                        # base
    return m

def machine_lathe(running=False):
    """3x2 tiles (96x64)."""
    m = canvas(96, 64); dr = d(m)
    R(dr, 2, 12, 92, 46, "s4")
    R(dr, 6, 16, 40, 26, "navy2")                    # door window
    R(dr, 10, 24, 10, 10, "s3")                      # chuck
    if running:
        dr.arc([8, 22, 22, 36], 0, 360, fill=P["s5"])
        dr.rectangle([22, 27, 40, 31], fill=P["w3"]) # bar
    dr.rectangle([6, 16, 45, 41], outline=P["K"])
    R(dr, 54, 16, 22, 18, "s2")                      # control
    R(dr, 57, 19, 16, 8, "green" if running else "greendim", outline=False)
    dr.rectangle([57, 19, 72, 26], outline=P["K"])
    dr.text((56, 44), "CNC LATHE", fill=P["K"])
    R(dr, 2, 52, 92, 8, "s1")
    R(dr, 80, 4, 10, 10, "alert" if running else "s3")
    return m

def machine_saw(running=False):
    m = canvas(64, 64); dr = d(m)
    R(dr, 2, 30, 60, 26, "s3")                       # base/table
    R(dr, 6, 14, 34, 18, "orange")                   # saw head
    dr.rectangle([10, 30, 34, 33], fill=P["s5"])     # blade slot
    if running:
        for i in range(4): px(dr, 14 + i * 5, 34, "gold")  # sparks
    R(dr, 44, 34, 16, 8, "w3")                       # stock bar
    R(dr, 2, 56, 60, 6, "s1")
    dr.text((8, 16), "SAW", fill=P["K"])
    return m

def machine_mill_manual():
    m = canvas(64, 64); dr = d(m)
    R(dr, 24, 4, 16, 22, "s4")                       # head
    R(dr, 28, 26, 8, 10, "s3")                       # quill
    R(dr, 8, 36, 48, 8, "s4")                        # table
    R(dr, 4, 38, 6, 4, "s5"); R(dr, 54, 38, 6, 4, "s5")  # handles
    R(dr, 22, 44, 20, 16, "s2")                      # knee/base
    dr.text((14, 8), "KNEE", fill=P["s1"])
    return m

def machine_bench():
    m = canvas(64, 32); dr = d(m)
    R(dr, 2, 8, 60, 16, "w2")                        # wood top
    R(dr, 4, 24, 6, 8, "s2"); R(dr, 54, 24, 6, 8, "s2")  # legs
    R(dr, 10, 4, 10, 6, "s3"); R(dr, 26, 4, 8, 6, "gold")  # tools on top
    return m

def machine_presetter():
    m = canvas(64, 64); dr = d(m)
    R(dr, 8, 40, 48, 18, "s5")                       # base (ZOLLER-white-ish)
    R(dr, 14, 8, 8, 34, "s4")                        # column
    R(dr, 22, 16, 16, 10, "s3")                      # optics head
    R(dr, 30, 30, 6, 12, "gold")                     # toolholder
    R(dr, 42, 14, 16, 14, "navy2")                   # screen
    R(dr, 44, 16, 12, 6, "green", outline=False); dr.rectangle([44, 16, 55, 21], outline=P["K"])
    R(dr, 8, 58, 48, 4, "s1")
    return m

def machine_crib():
    m = canvas(64, 64); dr = d(m)
    R(dr, 4, 8, 56, 50, "navy")
    for r in range(3):
        for c in range(4): R(dr, 9 + c * 13, 13 + r * 13, 10, 10, "s2")
    R(dr, 22, 2, 20, 8, "sky")                       # RFID antenna bar
    px(d(m), 30, 5, "white"); px(d(m), 34, 5, "white")
    R(dr, 4, 58, 56, 4, "s1")
    return m

def machine_terminal(kind="handoff"):
    m = canvas(32, 32); dr = d(m)
    R(dr, 6, 4, 20, 16, "s2")                        # CRT
    col = "green" if kind == "handoff" else "sky"
    R(dr, 9, 7, 14, 10, col, outline=False); dr.rectangle([9, 7, 22, 16], outline=P["K"])
    R(dr, 12, 20, 8, 4, "s3")                        # neck
    R(dr, 6, 24, 20, 6, "s1")                        # desk stand
    return m

def machine_netnode():
    m = canvas(32, 32); dr = d(m)
    R(dr, 4, 10, 24, 14, "s1")                       # switch box
    for i in range(4): R(dr, 7 + i * 6, 13, 4, 4, "green" if i % 2 else "greendim")
    dr.line([(28, 14), (31, 8)], fill=P["sky"]); dr.line([(28, 18), (31, 24)], fill=P["sky"])
    R(dr, 10, 24, 12, 4, "s2")
    return m

def machine_cobot(state="idle"):
    m = canvas(32, 32); dr = d(m)
    R(dr, 10, 24, 12, 6, "s2")                       # base
    a2 = {"idle": (16, 12), "pick": (24, 16), "fault": (16, 12)}[state]
    dr.line([(16, 24), (12, 16)], fill=P["s5"], width=3)   # lower arm
    dr.line([(12, 16), a2], fill=P["s5"], width=3)          # upper arm
    R(dr, a2[0] - 2, a2[1] - 2, 5, 5, "sky" if state != "fault" else "alert")  # wrist
    R(dr, 4, 2, 8, 6, "alert" if state == "fault" else "greendim")             # status
    return m

def machine_amr():
    m = canvas(32, 32); dr = d(m)
    R(dr, 4, 12, 24, 12, "s4")
    R(dr, 6, 8, 20, 6, "w2")                         # pallet on top
    px(d(m), 8, 22, "K"); px(d(m), 23, 22, "K")
    R(dr, 13, 14, 6, 4, "sky")                       # lidar window
    return m

def machine_desk():
    m = canvas(64, 32); dr = d(m)
    R(dr, 2, 10, 60, 16, "w1")                       # desk
    R(dr, 8, 2, 16, 12, "s2")                        # PC
    R(dr, 10, 4, 12, 7, "green", outline=False); dr.rectangle([10, 4, 21, 10], outline=P["K"])
    R(dr, 34, 4, 18, 8, "white")                     # papers
    dr.text((35, 3), "RFQ", fill=P["K"])
    R(dr, 6, 26, 6, 6, "s2"); R(dr, 52, 26, 6, 6, "s2")
    return m

def machine_chalkboard():
    m = canvas(64, 48); dr = d(m)
    R(dr, 4, 4, 56, 32, "navy2")                     # board
    dr.rectangle([4, 4, 59, 35], outline=P["w2"])
    dr.text((8, 8), "SHOP", fill=P["white"]); dr.text((8, 20), "CLASS", fill=P["gold"])
    dr.line([(38, 12), (54, 12)], fill=P["white"]); dr.line([(38, 18), (50, 18)], fill=P["white"])
    dr.line([(38, 24), (52, 24)], fill=P["white"])
    R(dr, 4, 36, 56, 4, "w2")                        # chalk tray
    R(dr, 8, 40, 4, 8, "s2"); R(dr, 52, 40, 4, 8, "s2")  # wheels legs
    return m

# two-frame sheets for animated machines
for name, fn, fw, fh in [
    ("vmc_t2", machine_vmc, 96, 96), ("lathe_cnc_t2", machine_lathe, 96, 64),
    ("saw_t1", machine_saw, 64, 64),
]:
    sheet = canvas(fw * 2, fh)
    sheet.paste(fn(False), (0, 0)); sheet.paste(fn(True), (fw, 0))
    save(sheet, name, frames=2, fw=fw, fh=fh)

for name, img in [
    ("mill_manual_t1", machine_mill_manual()), ("bench_deburr_t1", machine_bench()),
    ("presetter_t4", machine_presetter()), ("toolcrib_rfid_t4", machine_crib()),
    ("handoff_terminal_t4", machine_terminal("handoff")), ("network_node_t3", machine_netnode()),
    ("amr_t5", machine_amr()), ("planning_desk", machine_desk()),
    ("chalkboard", machine_chalkboard()), ("nox_terminal", machine_terminal("nox")),
]:
    save(img, name)

cobot = canvas(32 * 3, 32)
for i, st in enumerate(["idle", "pick", "fault"]): cobot.paste(machine_cobot(st), (i * 32, 0))
save(cobot, "cobot_t5", frames=3, fw=32, fh=32)

# ================= CHARACTERS (32x48) =================
def character(cap_c, shirt_c, hair_c, beard=False, pony=False, apron=False, frame=0):
    m = canvas(32, 48); dr = d(m)
    bob = 1 if frame == 1 else 0
    # legs
    R(dr, 10, 38 + bob, 5, 9 - bob, "denim"); R(dr, 17, 38 + bob, 5, 9 - bob, "denim")
    R(dr, 9, 45, 7, 3, "w1"); R(dr, 16, 45, 7, 3, "w1")     # boots
    # torso
    R(dr, 8, 24 + bob, 16, 15, shirt_c)
    if apron: R(dr, 11, 26 + bob, 10, 12, "w1")
    # arms
    R(dr, 5, 25 + bob, 4, 11, shirt_c); R(dr, 23, 25 + bob, 4, 11, shirt_c)
    px(dr, 6, 36 + bob, "skin"); px(dr, 25, 36 + bob, "skin")
    # head
    R(dr, 10, 10 + bob, 12, 12, "skin")
    px(dr, 13, 15 + bob, "K"); px(dr, 18, 15 + bob, "K")     # eyes
    if beard: R(dr, 11, 18 + bob, 10, 4, hair_c, outline=False)
    if pony:
        R(dr, 9, 8 + bob, 14, 5, hair_c, outline=False)
        R(dr, 22, 12 + bob, 4, 10, hair_c)                   # ponytail
    if cap_c:
        R(dr, 9, 7 + bob, 14, 5, cap_c)
        dr.rectangle([9, 11 + bob, 26, 12 + bob], fill=P[cap_c])  # brim
    elif not pony:
        R(dr, 9, 7 + bob, 14, 4, hair_c, outline=False)
    return m

def char_sheet(name, **kw):
    sheet = canvas(64, 48)
    sheet.paste(character(frame=0, **kw), (0, 0))
    sheet.paste(character(frame=1, **kw), (32, 0))
    save(sheet, name, frames=2, fw=32, fh=48)

char_sheet("guide_zach", cap_c="navy2", shirt_c="s1", hair_c="w1", beard=True)
char_sheet("av_m_01", cap_c="orange", shirt_c="navy", hair_c="w1", beard=True)
char_sheet("av_m_02", cap_c=None, shirt_c="greendim", hair_c="s1")
char_sheet("av_f_01", cap_c=None, shirt_c="denim", hair_c="w1", pony=True)
char_sheet("av_f_02", cap_c="sky", shirt_c="s1", hair_c="s1", apron=True)
char_sheet("nox_rep_dana", cap_c=None, shirt_c="gold", hair_c="s1", pony=True)

# NOX pallet
pal = canvas(32, 32); dr = d(pal)
R(dr, 4, 22, 24, 6, "w2")
for xx in (6, 14, 22): R(dr, xx, 26, 4, 4, "w1")
R(dr, 6, 10, 20, 12, "s5")                            # plate stack
dr.line([(8, 14), (24, 14)], fill=P["s3"]); dr.line([(8, 18), (24, 18)], fill=P["s3"])
R(dr, 22, 6, 8, 6, "green")                           # cert tag
save(pal, "nox_pallet")

# ================= ATLAS =================
for k, v in ATLAS.items():
    with open(os.path.join(OUT, v["file"]), "rb") as f:
        v["sha256"] = hashlib.sha256(f.read()).hexdigest()[:12]
with open(os.path.join(OUT, "atlas.json"), "w") as f:
    json.dump(ATLAS, f, indent=1)
print(f"generated {len(ATLAS)} sheets -> {OUT}")
