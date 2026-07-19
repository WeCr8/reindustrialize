#!/usr/bin/env python3
"""
REINDUSTRIALIZE pixel art generator v2 — shading ramps, dithering, texture.
Targets the concept-art look: top-lit surfaces, 1px black outlines, dithered
large surfaces, grimy concrete floor, VF-2SS-style machine detailing.
Same atlas contract as v1 (names, frame sizes) so the viewer drops in unchanged.
"""
from PIL import Image, ImageDraw
import json, os, hashlib

OUT = os.path.join(os.path.dirname(__file__), "..", "packages", "assets", "sprites")
os.makedirs(OUT, exist_ok=True)

P = {
    "K": (8, 9, 12),
    # steel ramp (machine sheet metal)
    "m0": (32, 35, 41), "m1": (74, 79, 88), "m2": (122, 128, 138), "m3": (168, 174, 182), "m4": (208, 213, 219), "m5": (236, 239, 242),
    # concrete ramp (floor)
    "c0": (58, 57, 54), "c1": (86, 84, 79), "c2": (108, 106, 100), "c3": (126, 124, 117), "c4": (142, 140, 132),
    # brand + hud
    "navy": (26, 46, 68), "navy2": (14, 24, 38), "navy3": (36, 62, 92),
    "orange": (232, 73, 29), "orange2": (170, 50, 20),
    "gold": (232, 185, 59), "gold2": (176, 136, 38),
    "sky": (74, 159, 212), "sky2": (46, 108, 150),
    "green": (63, 208, 138), "green2": (35, 130, 84), "greendark": (18, 70, 46),
    "alert": (208, 67, 63), "alert2": (140, 40, 38), "purple": (155, 89, 208),
    # wood / tan (control panels, bench, boots)
    "w0": (62, 47, 33), "w1": (96, 73, 50), "w2": (140, 108, 73), "w3": (186, 148, 100), "w4": (214, 180, 132),
    "tan": (196, 172, 132), "tan2": (156, 134, 98),
    # teal (tool cart)
    "t0": (16, 42, 50), "t1": (28, 66, 78), "t2": (44, 94, 108),
    # skin / hair / denim
    "skin": (206, 164, 122), "skin2": (170, 128, 92), "hair": (74, 55, 38), "hair2": (52, 38, 26),
    "denim": (52, 82, 120), "denim2": (36, 58, 88),
    "white": (236, 240, 243),
    "T": (0, 0, 0, 0),
}

def canvas(w, h): return Image.new("RGBA", (w, h), P["T"])
def d(img): return ImageDraw.Draw(img)
def rect(dr, x, y, w, h, c): dr.rectangle([x, y, x + w - 1, y + h - 1], fill=P[c])
def line(dr, x0, y0, x1, y1, c): dr.line([(x0, y0), (x1, y1)], fill=P[c])
def px(dr, x, y, c): dr.point((x, y), fill=P[c])
def outline(dr, x, y, w, h): dr.rectangle([x, y, x + w - 1, y + h - 1], outline=P["K"])

def shade_box(dr, x, y, w, h, mid, hi, lo, ol=True):
    """Filled box, top+left highlight, bottom+right shadow, optional outline."""
    rect(dr, x, y, w, h, mid)
    line(dr, x + 1, y + 1, x + w - 2, y + 1, hi)
    line(dr, x + 1, y + 1, x + 1, y + h - 2, hi)
    line(dr, x + 1, y + h - 2, x + w - 2, y + h - 2, lo)
    line(dr, x + w - 2, y + 2, x + w - 2, y + h - 2, lo)
    if ol: outline(dr, x, y, w, h)

def dither(dr, x, y, w, h, a, b, phase=0):
    """Checkerboard dither between two palette colors."""
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            dr.point((xx, yy), fill=P[a if (xx + yy + phase) % 2 == 0 else b])

def rnd(seed):
    s = [seed]
    def f(n):
        s[0] = (s[0] * 1103515245 + 12345) & 0x7fffffff
        return s[0] % n
    return f

ATLAS = {}
def save(img, name, frames=1, fw=None, fh=None):
    img.save(os.path.join(OUT, f"{name}.png"))
    ATLAS[name] = {"file": f"{name}.png", "w": img.width, "h": img.height,
                   "frames": frames, "fw": fw or img.width // frames, "fh": fh or img.height}

# ================= TILESET =================
def tile_floor(seed=0):
    """Concept-style concrete: mottled slab, dark grout right+bottom, stains."""
    t = canvas(32, 32); dr = d(t)
    rect(dr, 0, 0, 32, 32, "c2")
    r = rnd(seed * 977 + 3)
    for _ in range(46):  # mottle
        px(dr, r(30), r(30), "c3" if r(3) else "c1")
    for _ in range(5):   # bright flecks
        px(dr, r(30), r(30), "c4")
    if seed % 3 == 0:    # stain blotch
        sx, sy = 4 + r(16), 4 + r(16)
        for dy in range(4):
            line(dr, sx + dy, sy + dy, sx + 8 - dy, sy + dy, "c1")
    if seed % 4 == 1:    # crack
        cx0 = r(20) + 4
        for i in range(8): px(dr, cx0 + (i // 2) + r(2) - 1, 6 + i * 3, "c0")
    # grout
    line(dr, 0, 31, 31, 31, "c0"); line(dr, 31, 0, 31, 31, "c0")
    line(dr, 0, 30, 31, 30, "c1"); line(dr, 30, 0, 30, 31, "c1")
    return t

def tile_tape():
    t = tile_floor(7); dr = d(t)
    rect(dr, 0, 12, 32, 7, "gold")
    line(dr, 0, 12, 31, 12, "gold2"); line(dr, 0, 18, 31, 18, "gold2")
    for x in range(0, 32, 10): rect(dr, x, 13, 5, 5, "K")
    for x in range(2, 32, 9): px(dr, x, 15, "c1")  # wear
    return t

def tile_wall():
    """Painted block wall, top-lit, panel seams like the concept background."""
    t = canvas(32, 32); dr = d(t)
    dither(dr, 0, 0, 32, 32, "m1", "m0")
    for yy in (0, 11, 22):
        line(dr, 0, yy, 31, yy, "m2")
        line(dr, 0, yy + 10, 31, yy + 10, "K")
    for i, xx in enumerate((16, 6, 24)):
        line(dr, xx, i * 11 + 1, xx, i * 11 + 9, "m0")
    return t

def tile_dock():
    t = canvas(32, 32); dr = d(t)
    shade_box(dr, 0, 0, 32, 32, "m2", "m3", "m1")
    for yy in range(4, 29, 5):
        line(dr, 2, yy, 29, yy, "m1"); line(dr, 2, yy + 1, 29, yy + 1, "m3")
    rect(dr, 12, 25, 8, 4, "gold"); outline(dr, 12, 25, 8, 4)
    return t

def tile_zone(color, c2):
    t = tile_floor(11); dr = d(t)
    for xx in range(0, 32, 4):
        px(dr, xx, 1, color); px(dr, xx + 1, 1, color)
        px(dr, xx, 30, color); px(dr, xx + 1, 30, color)
    return t

strip = canvas(32 * 7, 32)
for i, tl in enumerate([tile_floor(0), tile_floor(4), tile_tape(), tile_wall(),
                        tile_dock(), tile_zone("sky", "sky2"), tile_zone("orange", "orange2")]):
    strip.paste(tl, (i * 32, 0))
save(strip, "tileset", frames=7, fw=32, fh=32)

# ================= MACHINES =================
def machine_vmc(running=False):
    """96x96 VF-2SS style: white sheet metal, dark window w/ reflection, red logo, tan retro control."""
    m = canvas(96, 96); dr = d(m)
    # base plinth
    shade_box(dr, 4, 84, 88, 10, "m0", "m1", "K")
    # main enclosure
    shade_box(dr, 4, 12, 88, 74, "m4", "m5", "m2")
    dither(dr, 6, 60, 84, 24, "m4", "m3")            # lower grime dither
    # crown
    shade_box(dr, 10, 4, 76, 10, "m1", "m2", "m0")
    # red logo block
    shade_box(dr, 8, 16, 22, 12, "orange", "orange", "orange2")
    dr.text((11, 17), "VF", fill=P["white"])
    dr.text((32, 18), "2SS", fill=P["m0"])
    # window (double door w/ chrome handles + diagonal reflection)
    shade_box(dr, 10, 30, 46, 38, "navy2", "navy", "K")
    for i in range(10):                               # reflection streaks
        px(dr, 16 + i, 34 + i, "navy3"); px(dr, 17 + i, 34 + i, "navy3")
        px(dr, 34 + i, 34 + i, "navy3")
    line(dr, 33, 31, 33, 66, "K")                     # door split
    rect(dr, 30, 44, 2, 8, "m4"); rect(dr, 35, 44, 2, 8, "m4")  # handles
    if running:
        rect(dr, 20, 38, 10, 14, "m2"); outline(dr, 20, 38, 10, 14)   # spindle head down
        rect(dr, 24, 52, 2, 6, "m4")
        for i in range(5): px(dr, 15 + i * 5, 60, "sky")               # coolant
        dither(dr, 12, 62, 42, 4, "w2", "w1")                          # chips
    else:
        rect(dr, 20, 33, 10, 12, "m2"); outline(dr, 20, 33, 10, 12)
    # control pendant (tan retro like concept)
    shade_box(dr, 62, 22, 28, 46, "tan", "w4", "tan2")
    shade_box(dr, 65, 25, 22, 14, "greendark", "green2", "K")          # CRT
    if running:
        for yy in (27, 30, 33): line(dr, 67, yy, 67 + (yy % 3) * 4 + 6, yy, "green")
    else:
        line(dr, 67, 30, 78, 30, "green2")
    # button rows (orange/green/red like the concept panel)
    for i, c in enumerate(["orange", "green", "alert", "sky", "gold", "m1"]):
        bx, by = 66 + (i % 3) * 8, 43 + (i // 3) * 8
        rect(dr, bx, by, 5, 5, c); outline(dr, bx, by, 5, 5)
    rect(dr, 66, 59, 20, 4, "m1"); outline(dr, 66, 59, 20, 4)          # handwheel slot
    # beacon
    shade_box(dr, 42, 0, 12, 6, "alert" if running else "m2", "alert" if running else "m3", "alert2" if running else "m1")
    return m

def machine_lathe(running=False):
    m = canvas(96, 64); dr = d(m)
    shade_box(dr, 2, 54, 92, 8, "m0", "m1", "K")
    shade_box(dr, 2, 10, 92, 46, "m4", "m5", "m2")
    dither(dr, 4, 42, 88, 12, "m4", "m3")
    # window
    shade_box(dr, 8, 16, 40, 30, "navy2", "navy", "K")
    for i in range(8): px(dr, 12 + i, 19 + i, "navy3")
    # chuck + part
    rect(dr, 12, 24, 10, 12, "m2"); outline(dr, 12, 24, 10, 12)
    px(dr, 15, 27, "m4"); px(dr, 19, 27, "m4"); px(dr, 15, 33, "m4"); px(dr, 19, 33, "m4")
    if running:
        rect(dr, 22, 28, 20, 5, "w3"); outline(dr, 22, 28, 20, 5)
        for i in range(4): px(dr, 24 + i * 5, 35, "gold")   # curl sparkle
    # tailstock hint
    rect(dr, 42, 27, 4, 8, "m3"); outline(dr, 42, 27, 4, 8)
    # control
    shade_box(dr, 56, 15, 26, 22, "tan", "w4", "tan2")
    shade_box(dr, 59, 18, 20, 9, "greendark", "green2", "K")
    if running: line(dr, 61, 22, 74, 22, "green")
    for i, c in enumerate(["orange", "green", "alert"]):
        rect(dr, 59 + i * 7, 30, 5, 4, c); outline(dr, 59 + i * 7, 30, 5, 4)
    dr.text((56, 42), "ST-10", fill=P["m1"])
    shade_box(dr, 80, 2, 10, 7, "alert" if running else "m2", "alert" if running else "m3", "m1")
    return m

def machine_saw(running=False):
    m = canvas(64, 64); dr = d(m)
    shade_box(dr, 2, 54, 60, 8, "m0", "m1", "K")
    shade_box(dr, 2, 32, 60, 24, "m2", "m3", "m1")
    dither(dr, 4, 44, 56, 10, "m2", "m1")
    # head
    shade_box(dr, 6, 12, 36, 22, "orange", "orange", "orange2")
    dr.text((10, 15), "SAW", fill=P["white"])
    rect(dr, 8, 28, 30, 3, "m5")                       # blade guard slit
    if running:
        for i in range(5): px(dr, 12 + i * 5, 33, "gold")
        for i in range(3): px(dr, 14 + i * 7, 35, "orange")
    # stock + roller
    shade_box(dr, 44, 36, 16, 7, "w3", "w4", "w1")
    rect(dr, 46, 45, 12, 2, "m3")
    return m

def machine_mill_manual():
    m = canvas(64, 64); dr = d(m)
    shade_box(dr, 22, 44, 22, 16, "m1", "m2", "m0")    # base
    shade_box(dr, 8, 34, 48, 9, "m3", "m4", "m1")      # table
    shade_box(dr, 2, 36, 7, 5, "m4", "m5", "m2"); shade_box(dr, 55, 36, 7, 5, "m4", "m5", "m2")  # handles
    shade_box(dr, 24, 4, 18, 24, "m3", "m4", "m1")     # head
    dither(dr, 26, 6, 14, 8, "m3", "m2")
    shade_box(dr, 29, 27, 8, 8, "m2", "m3", "m0")      # quill
    rect(dr, 32, 35, 2, 3, "m5")                       # tool
    px(dr, 12, 30, "gold"); px(dr, 13, 30, "gold")     # DRO dot
    return m

def machine_bench():
    m = canvas(64, 32); dr = d(m)
    shade_box(dr, 2, 8, 60, 15, "w2", "w3", "w0")
    for xx in range(6, 58, 8): line(dr, xx, 9, xx, 21, "w1")   # planks
    shade_box(dr, 4, 23, 6, 9, "m1", "m2", "m0"); shade_box(dr, 54, 23, 6, 9, "m1", "m2", "m0")
    # tools on top
    rect(dr, 10, 4, 12, 5, "m3"); outline(dr, 10, 4, 12, 5)
    rect(dr, 28, 4, 6, 6, "gold"); outline(dr, 28, 4, 6, 6)
    rect(dr, 40, 5, 10, 3, "m4"); outline(dr, 40, 5, 10, 3)
    return m

def machine_tool_cart():
    """2x2 teal rolling toolbox from the concept art, tool-studded wood top."""
    m = canvas(64, 64); dr = d(m)
    # wood top with toolholders
    shade_box(dr, 2, 10, 60, 10, "w3", "w4", "w1")
    for i in range(5):                                  # retention knobs / tools
        tx = 8 + i * 11
        rect(dr, tx, 2, 4, 9, "m3"); outline(dr, tx, 2, 4, 9)
        px(dr, tx + 1, 3, "m5")
    # cabinet
    shade_box(dr, 4, 20, 56, 36, "t1", "t2", "t0")
    dither(dr, 6, 46, 52, 8, "t1", "t0")
    for r_ in range(3):                                 # drawers
        dy = 23 + r_ * 11
        shade_box(dr, 8, dy, 48, 9, "t1", "t2", "t0")
        rect(dr, 24, dy + 3, 16, 3, "m3"); outline(dr, 24, dy + 3, 16, 3)
    # casters
    for cxx in (10, 48):
        rect(dr, cxx, 56, 8, 7, "m0"); outline(dr, cxx, 56, 8, 7); px(dr, cxx + 3, 59, "m3")
    return m

def machine_presetter():
    m = canvas(64, 64); dr = d(m)
    shade_box(dr, 6, 40, 52, 18, "m5", "m5", "m3")
    dither(dr, 8, 52, 48, 5, "m4", "m3")
    shade_box(dr, 12, 6, 9, 36, "m4", "m5", "m2")       # column
    shade_box(dr, 21, 14, 18, 11, "m3", "m4", "m1")     # optics head
    rect(dr, 37, 18, 3, 3, "sky")                       # lens
    shade_box(dr, 28, 30, 7, 12, "gold", "gold", "gold2")  # toolholder
    rect(dr, 30, 26, 3, 4, "m3")                        # tool tip
    shade_box(dr, 42, 12, 18, 14, "navy2", "navy", "K") # screen
    line(dr, 45, 16, 56, 16, "green"); line(dr, 45, 19, 52, 19, "green2")
    dr.text((42, 30), "PRESET", fill=P["m2"])
    return m

def machine_crib():
    m = canvas(64, 64); dr = d(m)
    shade_box(dr, 4, 8, 56, 50, "navy", "navy3", "navy2")
    for r_ in range(3):
        for c_ in range(4):
            bx, by = 9 + c_ * 13, 13 + r_ * 13
            shade_box(dr, bx, by, 10, 10, "m1", "m2", "m0")
            px(dr, bx + 4, by + 4, "m3")
    shade_box(dr, 20, 1, 24, 8, "sky", "sky", "sky2")    # RFID bar
    px(dr, 28, 4, "white"); px(dr, 32, 4, "white"); px(dr, 36, 4, "white")
    rect(dr, 4, 58, 56, 4, "m0"); outline(dr, 4, 58, 56, 4)
    return m

def machine_terminal(kind="handoff"):
    m = canvas(32, 32); dr = d(m)
    shade_box(dr, 5, 3, 22, 17, "m1", "m2", "m0")
    scr = "green" if kind == "handoff" else "sky"
    shade_box(dr, 8, 6, 16, 11, "greendark" if kind == "handoff" else "navy2", "green2" if kind == "handoff" else "navy3", "K")
    line(dr, 10, 9, 20, 9, scr); line(dr, 10, 12, 17, 12, scr)
    rect(dr, 13, 20, 6, 3, "m1"); outline(dr, 13, 20, 6, 3)
    shade_box(dr, 6, 23, 20, 6, "m0", "m1", "K")
    for i in range(5): px(dr, 9 + i * 3, 25, "m2")       # keys
    return m

def machine_netnode():
    m = canvas(32, 32); dr = d(m)
    shade_box(dr, 3, 10, 26, 13, "m0", "m1", "K")
    for i in range(4):
        rect(dr, 6 + i * 6, 13, 4, 3, "green" if i % 2 else "green2")
        rect(dr, 6 + i * 6, 18, 4, 2, "gold" if i == 1 else "m1")
    line(dr, 29, 13, 31, 7, "sky"); line(dr, 29, 19, 31, 25, "sky")
    px(dr, 31, 6, "sky"); px(dr, 31, 26, "sky")
    rect(dr, 11, 23, 10, 4, "m1"); outline(dr, 11, 23, 10, 4)
    return m

def machine_cobot(state="idle"):
    m = canvas(32, 32); dr = d(m)
    shade_box(dr, 9, 24, 14, 6, "m1", "m2", "m0")
    a2 = {"idle": (17, 11), "pick": (25, 17), "fault": (17, 11)}[state]
    dr.line([(16, 24), (11, 16)], fill=P["m4"], width=3)
    dr.line([(16, 24), (11, 16)], fill=P["m2"], width=1)
    dr.line([(11, 16), a2], fill=P["m4"], width=3)
    px(dr, 11, 16, "sky")                                # joint
    rect(dr, a2[0] - 2, a2[1] - 3, 5, 6, "sky" if state != "fault" else "alert")
    outline(dr, a2[0] - 2, a2[1] - 3, 5, 6)
    shade_box(dr, 3, 1, 9, 6, "alert" if state == "fault" else "green2", "alert" if state == "fault" else "green", "K")
    return m

def machine_amr():
    m = canvas(32, 32); dr = d(m)
    shade_box(dr, 3, 12, 26, 13, "m3", "m4", "m1")
    shade_box(dr, 5, 6, 22, 7, "w2", "w3", "w0")         # pallet load
    rect(dr, 12, 15, 8, 4, "sky"); outline(dr, 12, 15, 8, 4)  # lidar
    px(dr, 7, 22, "K"); px(dr, 24, 22, "K")
    px(dr, 4, 14, "gold"); px(dr, 27, 14, "gold")        # blinkers
    return m

def machine_desk():
    m = canvas(64, 32); dr = d(m)
    shade_box(dr, 2, 12, 60, 14, "w2", "w3", "w0")
    for xx in range(8, 58, 10): line(dr, xx, 13, xx, 24, "w1")
    shade_box(dr, 6, 26, 5, 6, "m1", "m2", "m0"); shade_box(dr, 53, 26, 5, 6, "m1", "m2", "m0")
    # monitor (JobLine teal like concept workstation)
    shade_box(dr, 8, 1, 18, 13, "m0", "m1", "K")
    shade_box(dr, 10, 3, 14, 9, "navy2", "navy3", "K")
    line(dr, 12, 5, 21, 5, "sky"); line(dr, 12, 8, 18, 8, "green2")
    # papers + keyboard
    rect(dr, 32, 4, 16, 8, "white"); outline(dr, 32, 4, 16, 8)
    line(dr, 34, 6, 45, 6, "m2"); line(dr, 34, 9, 42, 9, "m2")
    rect(dr, 30, 14, 20, 4, "m1"); outline(dr, 30, 14, 20, 4)
    return m

def machine_whiteboard():
    """TODAY'S MISSIONS board from the concept."""
    m = canvas(64, 48); dr = d(m)
    shade_box(dr, 4, 2, 56, 34, "white", "white", "m3")
    dr.text((8, 4), "MISSIONS", fill=P["sky2"])
    for i, c in enumerate(["green2", "green2", "green2"]):
        rect(dr, 8, 14 + i * 6, 4, 4, "white"); outline(dr, 8, 14 + i * 6, 4, 4)
        px(dr, 9, 15 + i * 6, c); px(dr, 10, 16 + i * 6, c)
        line(dr, 15, 16 + i * 6, 40 + i * 4, 16 + i * 6, c)
    line(dr, 15, 34, 44, 34, "alert")
    # tripod
    line(dr, 14, 36, 8, 47, "m2"); line(dr, 50, 36, 56, 47, "m2"); line(dr, 32, 36, 32, 47, "m2")
    return m

def machine_chalkboard():
    m = canvas(64, 48); dr = d(m)
    shade_box(dr, 2, 2, 60, 36, "w1", "w2", "w0")        # frame
    shade_box(dr, 5, 5, 54, 30, "greendark", "green2", "K")
    dr.text((9, 7), "SHOP", fill=P["white"]); dr.text((9, 18), "CLASS", fill=P["gold"])
    line(dr, 40, 12, 55, 12, "white"); line(dr, 40, 17, 51, 17, "white")
    line(dr, 40, 22, 53, 22, "white"); line(dr, 40, 27, 48, 27, "gold")
    dither(dr, 6, 30, 20, 4, "greendark", "green2")       # chalk dust smear
    rect(dr, 2, 38, 60, 4, "w2"); outline(dr, 2, 38, 60, 4)
    rect(dr, 6, 39, 5, 2, "white")                        # chalk stick
    shade_box(dr, 8, 42, 5, 6, "m1", "m2", "m0"); shade_box(dr, 51, 42, 5, 6, "m1", "m2", "m0")
    return m

# animated sheets
for name, fn, fw, fh in [("vmc_t2", machine_vmc, 96, 96), ("lathe_cnc_t2", machine_lathe, 96, 64), ("saw_t1", machine_saw, 64, 64)]:
    sheet = canvas(fw * 2, fh)
    sheet.paste(fn(False), (0, 0)); sheet.paste(fn(True), (fw, 0))
    save(sheet, name, frames=2, fw=fw, fh=fh)

for name, img in [
    ("mill_manual_t1", machine_mill_manual()), ("bench_deburr_t1", machine_bench()),
    ("tool_cart", machine_tool_cart()), ("presetter_t4", machine_presetter()),
    ("toolcrib_rfid_t4", machine_crib()), ("handoff_terminal_t4", machine_terminal("handoff")),
    ("nox_terminal", machine_terminal("nox")), ("network_node_t3", machine_netnode()),
    ("amr_t5", machine_amr()), ("planning_desk", machine_desk()),
    ("whiteboard", machine_whiteboard()), ("chalkboard", machine_chalkboard()),
]:
    save(img, name)

cob = canvas(96, 32)
for i, st in enumerate(["idle", "pick", "fault"]): cob.paste(machine_cobot(st), (i * 32, 0))
save(cob, "cobot_t5", frames=3, fw=32, fh=32)

# ================= CHARACTERS 32x48, shaded =================
def character(cap=None, jacket="m0", shirt="K", hair="hair", beard=False, pony=False,
              apron=False, vest=False, frame=0):
    m = canvas(32, 48); dr = d(m)
    bob = 1 if frame == 1 else 0
    # boots (tan, dark sole)
    rect(dr, 8, 44, 7, 4, "w3"); rect(dr, 17, 44, 7, 4, "w3")
    rect(dr, 8, 47, 7, 1, "w0"); rect(dr, 17, 47, 7, 1, "w0")
    outline(dr, 8, 44, 7, 4); outline(dr, 17, 44, 7, 4)
    # jeans with inseam shading + cuff
    rect(dr, 9, 33 + bob, 6, 11 - bob, "denim"); rect(dr, 17, 33 + bob, 6, 11 - bob, "denim")
    line(dr, 14, 34 + bob, 14, 43, "denim2"); line(dr, 17, 34 + bob, 17, 43, "denim2")
    rect(dr, 9, 41, 6, 2, "denim2"); rect(dr, 17, 41, 6, 2, "denim2")
    outline(dr, 9, 33 + bob, 6, 11 - bob); outline(dr, 17, 33 + bob, 6, 11 - bob)
    # torso: jacket open over shirt
    rect(dr, 8, 21 + bob, 16, 13, jacket)
    rect(dr, 13, 22 + bob, 6, 12, shirt)                       # shirt strip
    line(dr, 9, 22 + bob, 9, 32 + bob, "m2")                   # jacket highlight
    line(dr, 22, 23 + bob, 22, 33 + bob, "K")
    if vest: rect(dr, 9, 22 + bob, 3, 11, "gold"); rect(dr, 20, 22 + bob, 3, 11, "gold")
    if apron:
        rect(dr, 12, 23 + bob, 8, 11, "w1"); line(dr, 12, 23 + bob, 19, 23 + bob, "w0")
    outline(dr, 8, 21 + bob, 16, 13)
    # collar
    px(dr, 11, 21 + bob, "m2"); px(dr, 20, 21 + bob, "m2")
    # arms + cuffs + hands
    rect(dr, 4, 22 + bob, 4, 11, jacket); rect(dr, 24, 22 + bob, 4, 11, jacket)
    outline(dr, 4, 22 + bob, 4, 11); outline(dr, 24, 22 + bob, 4, 11)
    rect(dr, 5, 32 + bob, 2, 2, "skin"); rect(dr, 25, 32 + bob, 2, 2, "skin")
    # head with jaw shading
    rect(dr, 10, 8 + bob, 12, 12, "skin")
    line(dr, 10, 18 + bob, 21, 18 + bob, "skin2")
    line(dr, 21, 10 + bob, 21, 18 + bob, "skin2")
    # eyes + brow
    px(dr, 13, 13 + bob, "K"); px(dr, 18, 13 + bob, "K")
    line(dr, 12, 12 + bob, 14, 12 + bob, "hair2"); line(dr, 17, 12 + bob, 19, 12 + bob, "hair2")
    if beard:
        rect(dr, 11, 16 + bob, 10, 5, hair)
        dither(dr, 11, 16 + bob, 10, 2, hair, "hair2")
        px(dr, 14, 18 + bob, "skin2"); px(dr, 17, 18 + bob, "skin2")   # mouth gap
    outline(dr, 10, 8 + bob, 12, 12)
    # hair / cap / ponytail
    if pony:
        rect(dr, 9, 6 + bob, 14, 5, hair); dither(dr, 9, 6 + bob, 14, 2, hair, "hair2")
        rect(dr, 22, 10 + bob, 4, 11, hair); line(dr, 23, 11 + bob, 23, 19 + bob, "hair2")
        outline(dr, 22, 10 + bob, 4, 11)
    if cap:
        rect(dr, 9, 5 + bob, 14, 5, cap)
        line(dr, 10, 6 + bob, 20, 6 + bob, "m2" if cap in ("m0", "navy2") else "white")
        rect(dr, 9, 10 + bob, 17, 2, cap)                       # brim
        line(dr, 9, 11 + bob, 25, 11 + bob, "K")
        outline(dr, 9, 5 + bob, 14, 5)
    elif not pony:
        rect(dr, 9, 6 + bob, 14, 4, hair); dither(dr, 9, 6 + bob, 14, 2, hair, "hair2")
    return m

def char_sheet(name, **kw):
    sheet = canvas(64, 48)
    sheet.paste(character(frame=0, **kw), (0, 0))
    sheet.paste(character(frame=1, **kw), (32, 0))
    save(sheet, name, frames=2, fw=32, fh=48)

char_sheet("guide_zach", cap="navy2", jacket="m0", shirt="K", beard=True)
char_sheet("av_m_01", cap="orange", jacket="navy", shirt="K", beard=True)
char_sheet("av_m_02", cap=None, jacket="green2", shirt="m0")
char_sheet("av_f_01", cap=None, jacket="denim", shirt="m0", pony=True)
char_sheet("av_f_02", cap="sky", jacket="m0", shirt="K", apron=True)

char_sheet("op_rosie", cap="gold", jacket="denim", shirt="m0", pony=True)
char_sheet("op_earl", cap="m0", jacket="w1", shirt="m0", beard=True)
char_sheet("cust_aero", cap=None, jacket="navy2", shirt="white")
char_sheet("nox_rep_dana", cap=None, jacket="m0", shirt="K", pony=True, vest=True)

# ================= ZACH PORTRAIT 64x64 (dialog box, concept-style) =================
def zach_portrait():
    m = canvas(64, 64); dr = d(m)
    rect(dr, 0, 0, 64, 64, "navy2")
    dither(dr, 0, 0, 64, 20, "navy2", "navy")
    # shoulders / jacket
    rect(dr, 6, 46, 52, 18, "m0")
    line(dr, 8, 47, 55, 47, "m1")
    rect(dr, 26, 48, 12, 16, "K")                       # tee
    px(dr, 10, 50, "m2"); px(dr, 53, 50, "m2")          # collar points
    # neck
    rect(dr, 27, 42, 10, 6, "skin2")
    # head
    rect(dr, 18, 14, 28, 30, "skin")
    line(dr, 18, 42, 45, 42, "skin2")
    line(dr, 44, 18, 44, 42, "skin2")                    # side shade
    line(dr, 19, 15, 43, 15, "skin")
    # ears
    rect(dr, 16, 26, 3, 6, "skin"); rect(dr, 45, 26, 3, 6, "skin2")
    # eyes: white + pupil + brow
    for ex in (24, 35):
        rect(dr, ex, 26, 5, 3, "white")
        rect(dr, ex + 2, 26, 2, 3, "hair2")
        line(dr, ex - 1, 24, ex + 5, 24, "hair2")
    # nose
    line(dr, 31, 28, 31, 33, "skin2"); px(dr, 32, 33, "skin2")
    # beard (dithered)
    rect(dr, 20, 34, 24, 10, "hair")
    dither(dr, 20, 34, 24, 4, "hair", "hair2")
    rect(dr, 27, 37, 10, 2, "skin2")                     # mouth
    line(dr, 20, 33, 20, 43, "hair2"); line(dr, 43, 33, 43, 43, "hair2")
    # cap: crown + panel seams + brim + W-ish button
    rect(dr, 16, 6, 32, 12, "m0")
    line(dr, 18, 8, 45, 8, "m1")
    line(dr, 32, 6, 32, 16, "K")                         # front seam
    rect(dr, 14, 18, 38, 4, "m0")                        # brim
    line(dr, 14, 21, 51, 21, "K")
    rect(dr, 29, 10, 6, 5, "m1"); outline(dr, 29, 10, 6, 5)  # logo patch (blank)
    outline(dr, 16, 6, 32, 12)
    outline(dr, 18, 14, 28, 30)
    return m

save(zach_portrait(), "zach_portrait")

# NOX pallet (shaded)
pal = canvas(32, 32); dr = d(pal)
shade_box(dr, 4, 22, 24, 6, "w2", "w3", "w0")
for xx in (6, 14, 22): rect(dr, xx, 27, 4, 4, "w1")
shade_box(dr, 6, 9, 20, 13, "m4", "m5", "m2")
line(dr, 8, 13, 24, 13, "m3"); line(dr, 8, 17, 24, 17, "m3")
shade_box(dr, 21, 4, 9, 7, "green2", "green", "greendark")
px(dr, 24, 6, "white")
save(pal, "nox_pallet")

# ================= ATLAS =================
for k, v in ATLAS.items():
    with open(os.path.join(OUT, v["file"]), "rb") as f:
        v["sha256"] = hashlib.sha256(f.read()).hexdigest()[:12]
with open(os.path.join(OUT, "atlas.json"), "w") as f:
    json.dump(ATLAS, f, indent=1)
print(f"v2: generated {len(ATLAS)} sheets")
