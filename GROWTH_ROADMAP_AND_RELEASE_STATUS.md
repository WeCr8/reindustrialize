# Growth Roadmap and Release Status

Last verified: **2026-07-18**  
Canonical machine-readable status: `data/release-roadmap.json`

## Executive status

**Current decision: playable alpha / demonstration-ready / not production-ready.**

The game has a coherent, completable opening slice: a player launches a named manufacturing company, learns from Zach, tours the Garage Bay, orders material, completes five production jobs, graduates the facility, and arrives at the Job Shop. That front-to-back path passes the mandatory production gate and browser E2E suite.

The final six-chapter game is **not yet complete**. Job Shop management is partial, Chapters 3–6 are progression designs rather than playable campaigns, saves and Continue are not connected, and several platform, accessibility, security, story, audio, and facility requirements remain open.

| Release question | Status |
|---|---|
| Can a new player start and finish the current slice? | **Yes** |
| Does the Garage-to-Job-Shop path pass E2E? | **Yes** |
| Is every currently declared playable task validated? | **Yes** |
| Is Chapter 1 fully content-complete? | **No**—inspection, shipping, Shop Class and family gates remain |
| Are all six chapters playable? | **No** |
| Is this ready for unrestricted public production release? | **No** |

## Player growth vision for 1.0

The final game is a 30-level, six-chapter factory-growth adventure targeted at **10–12 hours for the main story** and **16–20 hours for a thorough playthrough**. Twenty-four optional manufacturing-themed Easter eggs add exploration without controlling graduation.

| Chapter | Facility | Player growth | Mainline target | Release state |
|---|---|---|---:|---|
| 1. Founder and Apprentice | Garage Bay, 2,400 sq ft | Safely plan, prepare, machine and ship repeatable work | 0.5–0.75 h | Playable loop; content-polish gaps |
| 2. Craftsperson to Team | Job Shop, 12,000 sq ft | Hire, qualify and schedule people across concurrent work | 1.5–2 h | Map and entry scene only; mechanics partial |
| 3. Manage What You Cannot See | Connected Plant, 45,000 sq ft | Connect machines, understand OEE and recover bottlenecks | 1.5–2 h | Data/design only |
| 4. Standardize and Automate | Smart Factory, 120,000 sq ft | Control tools, handoffs, cells and safe automation | 2–2.25 h | Data/design only |
| 5. Reliability at Scale | Lights-Out Complex, 350,000 sq ft | Build unattended reliability and planned recovery | 2–2.5 h | Data/design only |
| 6. Build the Institution | American Titan Campus, 1,000,000 sq ft | Lead programs, departments, apprentices and the mentor legacy | 2.5–3 h | Data/design only |

## Development roadmap

### M0 — First Playable Alpha: complete

- [x] Entry, prologue, founder/company creation and opening story
- [x] Ten selectable founders with floor and active-scene identity
- [x] Zach narration, captions, reusable mentoring and shop tour
- [x] Keyboard, mouse, touch, Xbox and QR phone input
- [x] Walking, running, collision, proximity USE and click-to-route
- [x] NOX ordering, five jobs, saw, tooling, G-code, CNC and grading
- [x] Hiring preview and Job Shop expansion
- [x] Release gate, complete-slice E2E and V3 gameplay video

Exit evidence: `pnpm release:gate`, `pnpm test:e2e`, and the V3 full-gameplay recording pass.

### M1 — Chapter 1 Release Complete: in progress

- [ ] Make inspection and shipping real playable stations
- [ ] Enforce distinct job families and Shop Class graduation requirements
- [ ] Add NOX delivery, first-article branches and first-hire cinematics
- [ ] Add save slots, autosave, Continue and versioned restore tests
- [ ] Complete pause, audio mixer, captions, reduced motion and UI scaling
- [ ] Complete gamepad-only menus, remapping and reconnect UX
- [ ] Human sign-off for Zach and founder identity consistency

Exit: every Chapter 1 gate is mechanically enforced and a saved campaign restores at each critical boundary.

### M2 — Chapter 2 Management Loop: planned

- [ ] Concurrent job routing across production VMC and lathe workflows
- [ ] Operators/programmers assigned by qualification and shift
- [ ] Recurring wages, utilization, morale, training and retention
- [ ] Inspection, shipping, cash-flow and capacity decisions
- [ ] Equipment purchase, placement and facility-move confirmation
- [ ] Complete Job Shop story, tutorials, art, audio and Easter eggs

Exit: the player can graduate the Job Shop and move into the Connected Plant through E2E without debug state changes.

### M3 — Chapters 3–4 Alpha: planned

- [ ] Connected Plant map, MTConnect signals, OEE, downtime and maintenance
- [ ] Multi-shift scheduling, toolroom ownership and bottleneck recovery
- [ ] Smart Factory map, preset tooling, digital handoffs and fixtures
- [ ] Safe cobot/cell deployment and automation validation
- [ ] Complete story/audio/art/tutorial packages and eight Easter eggs

Exit: Chapters 1–4 are continuously playable with upgrades from older saves.

### M4 — Content-Complete Six-Chapter Alpha: planned

- [ ] Lights-Out reliability, AMRs, robots, material flow and recovery drills
- [ ] Titan Campus multi-building strategy, programs and department leadership
- [ ] Apprentice academy, mentor legacy, final capstone, ending and credits
- [ ] All facility maps, equipment states, hires, story scenes and narration
- [ ] All 24 Easter eggs discoverable and recorded without blocking progression

Exit: the complete 10–12 hour campaign reaches a durable completion state.

### M5 — Full-Campaign Beta: planned

- [ ] Content lock, economy balance, anti-grind and failure-recovery tuning
- [ ] Save migration, corruption recovery, offline behavior and cloud conflict tests
- [ ] Accessibility review with keyboard, controller, touch and phone alternatives
- [ ] Chrome, Edge, Firefox, Safari, Android and iOS compatibility matrix
- [ ] Performance budgets, asset streaming, memory testing and long-session soak
- [ ] Auth/RLS staging tests, backups, restore drill and secret scan

Exit: no open content gaps; all supported platforms complete the campaign with telemetry and recoverable errors.

### M6 — Release Candidate: planned

- [ ] Blocker and critical defects at zero
- [ ] Final human review of story, Zach identity, captions, audio and visual consistency
- [ ] Privacy, retention, deletion, support and accessibility statements published
- [ ] Production deployment, rollback and incident procedures rehearsed
- [ ] Release build signed off by gameplay, art/audio, platform and security owners

Exit: one immutable candidate passes every automated and human release gate.

### M7 — Version 1.0: planned

- [ ] Deploy the complete six-chapter campaign
- [ ] Enable cloud accounts/saves only after explicit security approval
- [ ] Monitor crashes, save failures, completion funnels and accessibility issues
- [ ] Preserve a cloud-disabled rollback build

## Final 1.0 ship gate

Version 1.0 may be called **fully playable and released** only when all conditions below are checked:

- [ ] Six chapters, 30 levels and six facility graduations complete through normal gameplay
- [ ] Main campaign completion state, ending, credits and post-game Continue work
- [ ] Every active scene has approved art, exact caption, audio and runtime trigger
- [ ] Every playable task has location, instructions, feedback and E2E validation
- [ ] Saves survive upgrades, interruption, offline use and cloud conflicts
- [ ] Keyboard, controller, touch and phone controls can complete the campaign
- [ ] Accessibility, browser/device, performance and long-session gates pass
- [ ] Auth, database, QR transport, privacy, backup and rollback security gates pass
- [ ] No blocker/critical defects and human asset review approved
- [ ] Full-campaign E2E video and automated completion run reflect the release candidate

## Current commands and evidence

```powershell
pnpm release:gate
pnpm test:e2e
pnpm promo:check:current-media
pnpm gameplay:record:full:v3
pnpm gameplay:render:full:v3
```

Related evidence: `FINAL_E2E_STATUS.md`, `STORY_AUDIO_VISUAL_CHECKLIST.md`, `AUDIO_STORY_TIMELINE_AUDIT.md`, `docs/PROGRESSION_SCALE.md`, and `docs/BACKEND_OPTIONS_AND_RELEASE.md`.
