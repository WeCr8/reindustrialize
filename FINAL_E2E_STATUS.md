# Final Gameplay and E2E Status

Last verified: **2026-07-19**

> The first playable milestone passes end to end. The complete six-chapter game is **not yet complete**; unfinished systems are listed below.

## Automated verification

- [x] Generated the current level viewer/game build
- [x] Neutral Founder A–J selection labels with no race, ethnicity, hair-color, or gender naming
- [x] Anywhere-to-objective routing opens the required station instead of leaving the action disabled
- [x] NOX material purchase reached from spawn, order confirmed, coins deducted, and delivery state recorded
- [x] Continuous 60 FPS presentation loop, eased tile movement, walk animation, foot shadow, machine-state animation, and objective pulse
- [x] Full click-to-walk pathfinding, direct equipment click-to-open, destination marker, left/right character facing, and manual-input cancellation of queued movement
- [x] Opening, story, first job, quest completion, Chapter 2 scene, and Job Shop expansion
- [x] Hiring carousel, expanded profiles, qualified operator hire, cost deduction, and team state
- [x] Xbox controller start and analog-stick player movement
- [x] QR session, phone pairing, WebSocket input, and player movement
- [x] Project self-check: **0 errors, 0 warnings**

```powershell
python scripts/build_level_viewer_v4.py
pnpm test:e2e
python scripts/selfcheck.py
```

Launch with `pnpm --filter @wecr8/game-server start`, then open `http://localhost:8787/game`.

## Front-to-back player journey

- [x] Full title/entry scene with New Game, controls, and credits
- [x] Three-beat narrated pre-founder prologue introduces REINDUSTRIALIZE, the garage-to-powerhouse path, and founder/company ownership before selection
- [x] Five-beat founding-day sequence includes “Welcome to the shop,” Zach's mentor role, first customer, and long-term powerhouse goal
- [x] Data-driven story/audio/visual manifest validates exact captions, voice files, scene art, order, and selected-founder overlays
- [x] Mandatory and replayable 14-station/28-panel Garage Bay tour pairs every equipment type with its location, image, exact Zach overview narration, operating walkthrough, and implementation status
- [x] Nine contextual active-production task guides independently cover ordering through quality review with location, imagery, narration, prerequisites, instructions, success criteria, and playable status
- [x] Ten visually varied, neutrally labeled Founder A–J choices, plus personal name and company name
- [x] Founder-specific male/female variants for Zach opening and expansion story scenes
- [x] Ten visual founder choices with distinct 32-bit sprites, exact scene identity overlays, scene-family persistence, and documented player-scene audit; selection labels do not identify demographic traits
- [x] Data-driven player-scene manifest and release validator cover 10 founders across title, opening, expansion, and playable floor rendering; future active scenes fail validation when art or mappings are missing
- [x] Zach Goodbody's 17 approved ElevenLabs voice clips generated and embedded for story, material, saw, tool, CNC, first-job, and expansion mentorship; captions remain visible
- [x] Interactive Zach mentor panel provides live next-step coaching plus 12 machining, quality, people, and business questions with portrait guidance, progressive station hints, captions, and matching approved voice clips
- [x] Twelve reusable Zach response clips cover print reading, safety stops, retry coaching, verification, root-cause correction, handoffs, cash discipline, questions, success, and next-step guidance with tagged usage metadata
- [x] Prologue story scene with Zach as mentor and apprentice introduction
- [x] Job 1042 first-production task
- [x] Tool cart, tool selection, and stickout lesson
- [x] VMC interaction and opened machine view
- [x] G-code loading, cycle start, part grading, and quest completion
- [x] Chapter 2 story transition and move from Garage Bay to Job Shop/Bay 2
- [x] Persisted Continue flow with validated current, temporary, and backup local recovery checkpoints

## Chapters and progression

| Chapter | Current status | Needed for chapter-complete gameplay |
|---|---|---|
| 1 — Garage Bay | **Playable five-job graduation loop** | Distinct-family gate, Shop Class enforcement, inspection, and shipping stations |
| 2 — Job Shop | **Playable map; chapter partial** | Concurrent jobs, staff assignments, quality department, production lathe, wages, and move gate |
| 3 — Connected Plant | **Progression data only** | Playable map, production chain, machine connectivity, and chapter quests |
| 4 — Smart Factory | **Progression data only** | Playable map, automation/cobot loop, staffing, and chapter quests |
| 5 — Lights-Out Complex | **Progression data only** | Playable map, autonomous production loop, and chapter quests |
| 6 — American Titan Campus | **Progression data only** | Playable campus, endgame production, final story, and completion state |

## Facility expansion

- [x] Six facility tiers grow from **2,400 sq ft** to **1,000,000 sq ft**
- [x] Mastery-based move requirements are represented in progression data
- [x] Bay 2 begins locked and the chapter transition moves the player into it
- [ ] Purchase/move confirmation with explicit costs and requirements
- [ ] Machine placement/layout editor
- [ ] Facility summary and walkthrough before accepting a move
- [ ] Playable moves from Chapters 2 through 6

1. Garage Bay — 2,400 sq ft
2. Job Shop — 12,000 sq ft
3. Connected Plant — 45,000 sq ft
4. Smart Factory — 120,000 sq ft
5. Lights-Out Complex — 350,000 sq ft
6. American Titan Campus — 1,000,000 sq ft

## Tasks and equipment

- [x] Staged 17-item factory market covers machining, welding, grinding, additive, inspection, and a capped robotics ladder from one Job Shop tugger through AMRs, heavy mobile platforms, and a supervised late-campus humanoid pilot
- [x] Robotics catalog data gates purchases by genuine facility growth, WIP department route, dedicated logistics space, named roster roles, safety approvals, maintenance coverage, cash, and fleet caps
- [x] Store cards show detailed 32-bit equipment imagery plus chapter, facility, utility/space, price, unlock, ownership, and honest playable/orientation status
- [x] All 17 store assets expose five comparable stats, capacity, real setup/cycle estimates, compressed game completion time, dependencies, utilities, space, and maintenance information
- [x] AGV, AMR, and supervised humanoid store previews animate from transparent 8 FPS sprite sheets; the humanoid has dedicated profile art
- [x] Zach's store walkthrough and live growth check teach when to buy, what full installation needs to include, and when to review the next facility
- [x] Store spending revalidates job, headcount, maintenance, and cash gates at purchase time; ownership and exact escalating prices persist in local saves
- [x] Later VMC wear produces service warnings and a production lockout that only a hired maintenance technician can repair through a paid, saved maintenance action
- [x] Founder selection uses large profile portraits at a portrait-safe aspect ratio and keeps movement sprites off the profile cards

- [x] Job planning and guided task sequence
- [x] Layered/opened equipment views
- [x] Tool choice, G-code, cycle, and grading interactions
- [x] NOX Metals ordering location, stock catalog, coin deduction, and next-day delivery state
- [x] Guided “Go to & Open” mechanics route the founder to NOX, planning, bandsaw, tool cart, and VMC objectives
- [x] Five-job Garage chapter with rotating drill, pocket, and 3D work plus a C-average graduation gate
- [x] Per-job raw-stock bandsaw operation and three-tool CNC setup before G/M-code proofing
- [ ] Bandsaw, manual mill, deburr, inspection, and shipping interactions
- [ ] Lathe production workflow
- [ ] Equipment purchasing and placement
- [x] VMC breakdown, lockout, qualified repair, test, and release
- [ ] Breakdown and repair mechanics for the remaining visual-ready machines
- [ ] MTConnect, tool presetter, and digital-handoff gameplay
- [ ] Robot/cobot and lights-out equipment loops

## Hiring and teams

- [x] Hiring entry point and candidate-card carousel
- [x] Expanded profiles with skills, qualifications, wage, and hiring cost
- [x] Hiring cost deduction and current-session team state
- [x] Programmer and operator candidate assets
- [ ] Persistent team save/load and recurring payroll
- [ ] Worker assignment to jobs and machines
- [ ] Qualification gates, skill progression, morale, retention, and training
- [ ] Hired-team representation on the shop floor

## Controls

- [x] Automatic input detection
- [x] Keyboard movement and actions
- [x] Mouse/touch UI and on-screen mobile directions
- [x] Phone/tablet thumb controls, held movement, sprint toggle, haptics, compact guidance trays, and portrait/landscape no-text-takeover checks
- [x] Xbox/gamepad movement and start action
- [x] Visible active-control status and explicit Keyboard, Xbox, and Phone choices
- [x] QR session generation, phone pairing, haptics, held-button repeat, and remote input
- [x] Phone-controller WebSocket E2E coverage
- [ ] Complete gamepad-only menu navigation
- [ ] Player-defined button remapping
- [ ] Reconnect/resume UX after phone or network loss
- [ ] Production HTTPS/WSS validation on a public host

## Visual and asset integration

- [x] Detailed title artwork and story scenes
- [x] Garage Bay map matching the established industrial imagery
- [x] Layered facility equipment and opened equipment views
- [x] Hire-card portraits
- [x] Zach mentor scenes use the selected **hat** version
- [ ] Final high-detail Job Shop/Bay 2 environment
- [ ] High-detail maps for Chapters 3–6
- [x] Repairable damage-state art mapped for every current equipment-store type
- [x] Four-state transparent maintenance floor sprites mapped for every placed machine
- [ ] Final Zach floor sprite matching the selected portrait
- [x] Hired-worker floor sprites, including the expanded maintenance team
- [ ] Apprentice floor sprites for the later academy chapter

## Platform and release needs

- [ ] Save slots, autosave, Continue, and reliable state restoration
- [ ] Audio, music, volume controls, and mute
- [ ] Pause/settings flow during gameplay
- [ ] Accessibility pass: scaling, contrast, captions, reduced motion, and control alternatives
- [ ] Performance/streaming pass for the approximately 28 MB standalone build
- [ ] Chrome, Edge, Firefox, Safari, Android, and iOS browser matrix
- [ ] Error telemetry and recoverable error screens
- [ ] QR session expiration, rate limiting, and production security review

## Release decision

- [x] Maintenance roster provides five stat-bearing, qualified repair/facilities hires with matching profile and floor art.
- [x] All 17 store equipment types have validated repairable damage-state mappings; VMC damage renders during lockout.
- [x] Job Shop restroom incident enforces qualified five-step repair, exact spending, morale, and saved reopening.
- [x] Analytics consent defaults to denied, persists accept/decline, and filters sensitive gameplay/profile values.

- [x] Suitable for demonstrating and testing the **first playable milestone**
- [x] Suitable for continued Chapter 2 gameplay development
- [ ] Complete six-chapter game
- [ ] Production-ready public gaming platform

## Critical next playable slice

Complete Chapter 2 as a true management loop: hire and assign staff, operate VMC and lathe jobs concurrently, inspect and ship parts, pay wages, satisfy a mastery gate, and purchase the move into the Connected Plant. This closes the largest gap between the current guided prototype and the intended factory-growth game.
