# REINDUSTRIALIZE — Game Design Document v0.1

## Fantasy
You inherit an empty industrial bay in America. Build it into a world-class job shop:
machines, people, data, robots. Zach the Guide teaches you real manufacturing along the way.

## Long-term player goal: outgrow the building
The player is expected to outgrow each facility. Mastery makes the current floor visibly
crowded and operationally constrained; quality, delivery, process maturity, and capital earn
the move into a substantially larger building. The arc is Garage Bay -> Job Shop -> Connected
Plant -> Smart Factory -> Lights-Out Complex -> multi-building American Titan Campus.
Facility definitions and move gates live in `data/facilities.json`.

## Core loop (Arcade)
1. **Take a job** (RFQ board) — part, qty, tolerance, due date, payout.
2. **Plan** — route the job across stations (saw → mill → deburr → inspect → ship).
3. **Run** — machines cycle in real time; operators affect speed/quality; breakdowns happen.
4. **Ship & get paid** — coins + XP. Quality escapes cost reputation.
5. **Reinvest** — buy machines, hire/train operators, unlock automation & robots.

Session target: 3–5 minutes to ship a first job. Idle-friendly: shop keeps running
(slower) while away, capped so it never becomes a pure idle clicker.

## Progression tiers ("Eras of Reindustrialization")
| Tier | Name              | Unlocks                                              |
|------|-------------------|------------------------------------------------------|
| 1    | Garage Shop       | Manual mill, bandsaw, deburr bench                   |
| 2    | Job Shop          | CNC VMC (VF-2SS class), CNC lathe, first hire        |
| 3    | Connected Shop    | **MTConnect network** — live machine dashboards, OEE |
| 4    | Smart Shop        | Tool presetter (ZOLLER class), RFID tool crib (HERO-CART class), shift handoff terminal (JobLine class) |
| 5    | Lights-Out        | Cobots, pallet robots, AMRs; night shift runs itself |
| 6    | American Titan    | Second building, aerospace contracts, export jobs    |

Tier 3–4 is the funnel core: the *game mechanic* that makes your shop dramatically better
is literally connecting machines to data and running clean handoffs — i.e., JobLine's pitch.

## Player skill tree (mirrors the HUD in the concept art)
- **CNC Programming** (green) — cycle time reduction, fewer scrapped setups
- **Automation** (green) — robot efficiency, lights-out duration
- **Software Dev** (blue) — build in-game "apps" that buff the shop (dashboards, alerts)
- **Problem Solving** (gold) — faster breakdown recovery, root-cause minigame bonuses
- **Communication** (purple) — handoff quality, operator morale, fewer "mystery scrap" events

## Zach the Guide
- Appears in the dialog box (bottom bar, portrait left) exactly as in the concept art.
- Voice: shop-floor plainspoken, encouraging, zero corporate fluff. Teaches the *why*
  ("A bad handoff costs you a whole shift. Write it down or lose it.").
- Tutorial = Quest Chain 0. Later he shows up at tier gates and after failures.
- In Shop Mode he references the player's *real* shop data ("Your Haas #2 sat idle
  4 hours yesterday — let's fix that").

## Robots & automation gameplay
- **Cobot arm**: tends one machine; needs a trained operator to program it first
  (Automation skill gate). Misprogrammed = crash animation + repair cost.
- **Pallet bot / AMR**: moves WIP between stations; routing puzzle mechanic.
- **Robot implementation quests**: risk/reward — install downtime now for throughput later.
  Teaches real automation ROI thinking.

## Shop Mode (jobline.ai) — real-data hooks
Auth-gated. The player's game state is enriched by live JobLine data via the server bridge:
- **Connect a real machine** (MTConnect) → in-game machine gets a gold "LIVE" badge + XP.
- **7 clean shift handoffs in a row** (real) → in-game Communication skill point.
- **Real OEE this week > last week** → coin bonus.
- Shop-vs-shop leaderboards (opt-in, anonymized by default).

## Economy sketch
- Coins (soft currency, earned by shipping). No paid currency at launch.
- Machine prices scale ~3x per tier. First VMC ≈ 12,000 coins ≈ 25–35 shipped jobs.
- Scrap/rework is the main coin sink; reputation gates better-paying contracts.

## Failure states & teaching moments
No game-overs. Failures (crash, scrap, missed due date) trigger a short Zach root-cause
dialog + a recovery quest. The game's stance: shops don't die, they learn.

## Out of scope v0.1
Multiplayer co-op shops, mobile native, PvP, cosmetics store.

## v0.2 additions

### Playable machinist (avatar)
Game opens with character creation: choose **male or female** body, pick one of 2+ presets
per body, accent color from the brand palette, and a name. Avatars are cosmetic-only
(never stat-different) and silent — Zach stays the sole teaching voice. The avatar is the
player's presence on the floor: walks the tile grid, carries stock, runs equipment from
each machine's operator tile, and plans jobs at the planning desk (RFQ board, routing,
NOX ordering). Walking distance costs real ticks, which makes layout a live decision.
Content lives in `data/avatars.json`; new presets come from the character-generator skill.

### NOX Metals (material supply chain)
NOX Metals is the in-game distributor, fronted by Dana (vendor NPC). From the planning
desk the player orders from a real-feeling catalog (6061, 7075, 1018, 4140 PH, DOM 1020
tube, 304, Ti-6-4) with lead times, rush pricing (1.5x), weekly seeded price drift (+-8%),
and optional **material certs** (+10%) — required for tier-6 aerospace jobs, which are
rejected at inspection without them. Wrong alloy on a job = guaranteed scrap + root-cause
dialog. Lessons: procurement planning, cash flow vs lead time, traceability.
Data: `data/vendors.json`; sim: `game-core/src/materials/inventory.ts`.

### G-code Console (fill-in-the-blank)
CNC machines won't run until the player completes that machine's G-code challenge on a
CRT-styled console (green on black, matching the concept art's control screens). Programs
render with blanks: `S{{rpm}} M{{spindleOn}}`, `G01 F{{cutFeed}}`, `G{{workOffset}}`…
Exact blanks (M03, G54, G43, G81, G80, G96, M30) teach vocabulary; numeric blanks are
**computed from the actual material the player ordered from NOX** (RPM = SFM x 3.82 / dia,
F = RPM x flutes x chip load) — swap 6061 for 4140 and the right answers change. Three
misses triggers Zach teaching the formula, then retry; never a hard fail. Passing sets
`machine.gcodeCleared` and awards CNC Programming XP. Haas/Fanuc dialect at launch,
matching the jobline-gcode extension's dialect list for future cross-promotion.
Data: `data/gcode-challenges.json`; engine: `game-core/src/gcode/challenge.ts`.

### NOX cutscenes & ordering terminal (v0.3)
NOX gets full cinematic treatment: `data/cutscenes.json` specs the intro (Detroit skyline
-> automated saw line -> instant-quote POV -> next-day truck at the dock) and a 2.5s
non-blocking delivery vignette on every material.received. Ordering happens on **NOX-NET**,
a retro terminal at the planning desk (also playable on the in-game phone) styled like a
BBS-era ordering system: browse catalog -> cut-to-size dimensions -> "NESTING..."
optimization animation -> instant stamped quote (certs included, zero markups line-itemed
as ⛁0) -> confirm -> truck delivery. The Legacy vendor's phone-tag flow is the deliberate
foil. Playable prototype: `apps/wecr8-info/prototypes/nox-net-terminal.html`.
Real-company note: NOX Metals (noxmetals.co, Detroit) is real and mission-aligned
("reindustrialize America" is literally their line) — partnership sign-off required
before shipping their name/brand; placeholder styling until then.

### Shop Class (v0.3)
Zach's second job: teacher. A chalkboard corner in the bay (`data/shopclass.json`) with six
lessons — SFM->RPM, chip load, offsets, alloy ID, mill certs, handoffs — each a short
chalkboard scene + one interactive check (quick calc, tap-the-code, or match). Lessons
unlock the matching game systems (G-code challenges, full NOX catalog, cert jobs, handoff
streaks) and are always replayable. Zach gains teach_point / teach_write / teach_nod sprite
states and a chalk-dust portrait variant. Graduating all six earns the Shop Class Graduate
badge.

### Level maps + first playable art (v0.4)
`data/maps/` now holds real tilemaps: **bay_01 Garage** (20x14, T1: saw->mill->bench flow,
VMC/lathe island, Shop Class corner, planning desk + NOX-NET, receiving/shipping docks,
power drops, network lane, AMR lane) and **bay_02 Job Shop** (28x14, T3-4: twin VMCs,
cobot tending, toolroom cluster with presetter beside RFID crib). `scripts/gen_pixel_art.py`
procedurally generates 22 palette-locked spritesheets (tileset, 14 machines/props with
idle/running frames, Zach, 4 avatars, Dana, NOX pallet) into packages/assets/sprites with
atlas.json + hashed manifest — playable placeholders that lock footprints, states, and
palette; final art regenerates through skills/sprite-spec on the same atlas contract.
`scripts/build_level_viewer.py` bundles everything into a standalone walkable prototype
(apps/wecr8-info/prototypes/shop-floor-viewer.html): WASD/arrow movement with collision,
machine run animations, lane/power/zone overlay toggle, and Zach station dialog.

### Graphics quality pass (v0.5)
Art generator v2 (`scripts/gen_pixel_art_v2.py`): shading ramps + dithering + texture across
all 25 sheets — mottled concrete with grout/stains/cracks, VF-2SS-style VMC (red logo, glass
reflections, tan retro pendant with button clusters), teal 3-drawer tool cart, missions
whiteboard, shaded characters, and a 64x64 Zach dialog portrait. Viewer v2 wraps the floor in
the concept HUD: gold double-border panels, HP/XP bars, segmented skill bars, live quest
tracker (visit stations -> missions check off -> coins + progress bar), and the portrait
dialog box. Path to full concept fidelity documented in docs/ART_DIRECTION.md — final art is
an asset swap against the locked atlas contract.

### Progression & grading — the whole game in one rule (v0.6)
The arc is fixed: **new job shop -> large-scale American manufacturer** (Garage -> Job Shop ->
Connected -> Smart -> Lights-Out -> American Titan, `data/progression.json`). Advancement is
mastery-gated, not volume-gated: every task is graded A-F (setups, cycles, G-code, handoffs,
material calls, deliveries). B+ streaks build a Craftsmanship coin multiplier; any F resets it.
Reputation = rolling average of your last 20 grades and hard-gates which customers offer work,
so grinding low-quality volume stalls you. Every D/F routes into the matching Shop Class
micro-lesson before retry — failure always lands on teaching, never a dead end. Tier 6's end
state: multi-building campus, aerospace LTAs, apprentice program.

### Mobile + desktop (v0.6)
Desktop: keyboard (WASD/arrows) + mouse. Mobile: on-screen D-pad with hold-to-repeat (shows
only on coarse-pointer devices), tap-to-walk on the canvas, responsive single-column HUD.
Same build serves both; input is additive, never exclusive.

### Engineering: bug-hunting & self-repair (v0.6)
`skills/bug-hunter` + `scripts/selfcheck.py`: schema validation, cross-reference checks
(quest events vs sim events, sprites vs atlas, map bounds/overlaps/spawn, Shop Class ->
challenge links, progression gate refs), balance invariants, safe auto-fixes. First run
caught 4 schema bugs + 3 missing sheets; root-caused (invariant scoped to production
machine classes in zod + selfcheck together) and now green. Principles enforced:
determinism (sim = f(seed, eventLog)), content validated at the door, single source of
truth, versioned saves, no browser storage in embeds, fail-toward-teaching.
