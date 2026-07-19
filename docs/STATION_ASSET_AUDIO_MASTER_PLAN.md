# Station Asset and Audio Master Plan

Status date: 2026-07-19  
Scope: six-chapter campaign, Garage Bay through American Titan Campus

## Production principle

A station is not complete because it has a map sprite. A playable station requires one coherent state model shared by visuals, animation, audio, controls, instruction, validation, NPC behavior, and save data.

Every station moves through only the states that make sense for it:

`locked → orientation → available → approach → open → setup → ready → active → pause/stop → inspect → pass/rework/fault → complete`

The UI must never show an active machine while playing an idle sound, show a stopped spindle while cutting audio continues, or call an orientation-only station playable.

## Required asset bundle for every playable station

### Visuals

- Map sprite: idle, active, attention/fault, and maintenance frames where applicable.
- Large establishing view: the entire station in its facility context.
- Open-station view: operator perspective with usable components visible.
- Component close-ups: one for every control or part the player manipulates.
- Process animation: material/tool motion, safe zones, chips, coolant, gauges, or data flow.
- Output states: untouched input, in-process work, accepted output, rework, scrap, and empty state.
- Tutorial overlays: labels, motion arrows, datum/measurement lines, hazard boundaries, and success highlight.
- NPC poses: approach, operate, inspect, material-handle, idle, discuss, and abnormal-stop response.
- Storybook frames: first introduction, first successful use, failure lesson, and facility-growth comparison.

### Audio

- Local ambience or powered-idle loop.
- Start and stop transitions; never fake these by abruptly cutting a loop.
- Interaction foley for doors, clamps, buttons, drawers, material, tools, and measurement.
- Active-process loop with variants based on material, tool, load, or operation.
- Safe completion cue.
- Rework/fault cue that informs without sounding like a catastrophic alarm unless a real crash occurred.
- Spatial falloff and occlusion so the shop sounds alive without becoming an undifferentiated wall of noise.
- Zach orientation, operating instructions, safe-stop guidance, failure diagnosis, and mastery response.

### Gameplay and validation

- Clear prerequisites, objective, controllable action, immediate feedback, pass tolerance, recoverable failure, and saved result.
- Keyboard, Xbox, touch, and QR-phone equivalents for every action.
- Captions or named sound indicators for consequential audio: `[SPINDLE ACCELERATING]`, `[UNSTABLE CHATTER]`, `[PROBE CONTACT]`.
- Mixer buses: voice, music, machine/process, interface, and ambience.
- A build gate proving required assets exist and E2E proving each event calls the correct state and sound.

## Chapter 1 — Garage Bay

### Mission board / shop overview — playable

- Visuals: readable board, chapter gate, pinned traveler, completion stamps, pulsing next-step route, before/after bay growth.
- Audio: marker squeak, paper pin, objective update, quest complete, facility unlock, quiet room tone.
- Zach: how to read the gate, why the next achievable step matters, graduation review.
- Interaction: focus objective, route to station, replay tour, inspect chapter requirements.

### Planning desk — playable

- Visuals: desk sprite states, job-card close-up, print, traveler, quote sheet, capacity calendar, accepted/rejected stamp.
- Audio: folder open, paper shuffle, keyboard/mouse, approval stamp, new-order notification.
- Zach: print reading, material/feature/tolerance/finish, route planning, quote risk.
- Later variants: scheduling board, concurrent jobs, customer priority conflicts.

### NOX material terminal — playable

- Visuals: terminal idle/active, supplier exterior, searchable catalog, alloy/size/condition cards, certification, cart, delivery confirmation.
- Audio: terminal wake, UI navigation, order confirm, payment, delivery truck/forklift, pallet set-down.
- Zach: alloy, dimensions, certification, cost, lead time, traceability.
- Failure/recovery: wrong alloy, insufficient dimensions, missing cert, unaffordable order, late delivery.

### Receiving and material rack — next playable priority

- Visuals: empty/arriving/verified/quarantined pallet; heat-lot tag; damage; rack locations; forklift and pallet-jack motion.
- Audio: dock door, truck idle, forklift approach, hydraulic lowering, banding cut, metal stock handling, barcode scan.
- Zach: purchase-order match, alloy/size/quantity/certification, quarantine discipline.
- Interaction: compare documents, scan heat lot, inspect damage, accept or quarantine, assign rack location.

### Horizontal bandsaw — playable, needs expanded views

- Current audio: power on, aluminum cut, power off.
- Add visuals: full open-station view; blade, vise, stock stop, coolant, guarding, length scale; blade-up/down and cut-progress frames.
- Add audio: vise clamp/release, stock loading, blade idle loop, coolant trickle, cut-complete drop, unsafe loose-stock rattle.
- Zach: finish allowance, clamping, blade clearance, hand safety, correct stop setting.
- Variants: aluminum bar, plate, steel; dull blade, crooked cut, insufficient allowance.

### Tool cart and offline setup — playable, needs holders and wear

- Current visuals: drill, flat end mill, ball nose, probe, chamfer tool; shared large/sprite atlases.
- Add visuals: ER collet, hydraulic holder, drill chuck, retention knob, taper, gauge line, presetter readout, tool-wear states.
- Audio: drawer open/close, tool placed in foam, collet torque click, retention-knob wrench, presetter contact, probe contact, RFID/tool-ID scan.
- Zach: geometry selection, holder compatibility, runout, gauge length, minimum safe stickout, wear recognition.
- Failure/recovery: wrong cutter, wrong holder, excessive stickout, dirty taper, missing offset, chipped edge.

### VMC — playable, highest production priority

- Current audio: power, door, spindle, coolant, drill/end-mill/ball-mill cutting, controlled stop.
- Add visuals: off/boot/idle/ready/running/hold/fault map frames; control close-up; vise and fixture; spindle taper; toolchanger; probe; chips/coolant; finished part.
- Add audio: servo home, door open, vise clamp, tool load, tool change, rapid traverse, feed motion, spindle-only air cut, feed hold, cycle stop, air blowoff, chip conveyor, healthy/overloaded/chatter variants.
- Zach: startup checklist, workholding, offsets, dry run, single block, load/sound/chip observation, safe stop, first article.
- Failure/recovery: open door, missing tool, incorrect offset, wrong spindle/coolant code, collision risk, chatter, tool wear, dimension drift.

### Manual mill — orientation; future playable

- Visuals: large operator view; vise, table, handwheels, DRO, spindle controls, quill, edge finder, workpiece and parallels.
- Audio: power and spindle ramp/stop, handwheel detents, table feed, edge-finder kick, vise clamp, light/heavy cuts, quill feed.
- Gameplay: tram/orientation lesson, clamp stock, edge-find, choose RPM, touch off, hand-feed path, measure result.
- Zach: hands-on control, climb/conventional context, backlash, depth discipline, never leave a wrench in the spindle.

### Deburr bench — orientation; future playable

- Visuals: raw burr close-ups, safe edge, overbroken edge, protected critical feature, hand scraper/file/stone/chamfer tool.
- Audio: scraper, fine file, abrasive pad, part set-down, air blowoff, glove/hand handling.
- Gameplay: identify required edges, choose tool, trace only allowed edges, control edge-break amount, inspect by touch/visual.
- Zach: safe handling, print-controlled edges, protecting sealing/locating surfaces.

### Inspection bench — missing as a dedicated station

- Visuals: granite plate, caliper, micrometer, height gauge, indicators, pins, surface-finish comparator, marked inspection report.
- Audio: caliper slide, micrometer ratchet, indicator contact, gauge pin placement, part on granite, result stamp.
- Gameplay: choose instrument, clean surfaces, zero gauge, measure correct feature, record value, accept/rework/scrap.
- Zach: resolution versus tolerance, measurement force, temperature, first-article evidence.

### CNC lathe — inspection; Chapter 2 playable target

- Current visuals: large inspection view. Current catalog includes generic lathe cycle.
- Add visuals: power states, chuck open/closed, stock extension, jaws, turret positions, inserts, tailstock, part catcher, finished turned features.
- Add audio: chuck clamp/unclamp, spindle ramp/run/stop, turret index, OD cut, facing, drilling, boring, grooving, cutoff, bar pull/feed, coolant.
- Gameplay: choose jaws, set stock stickout and chuck pressure, assign turret tools, set work/tool offsets, prove path, inspect diameter/length.
- Failure/recovery: excess stickout, jaw collision, wrong insert, poor chip control, taper, oversize/undersize diameter.

### Shop Class — orientation shell; lesson system target

- Visuals: chalkboard diagrams, animated formula examples, cutaway tools, chips, failures, quizzes, earned lesson badges.
- Audio: chalk/marker, page turn, subtle success/fail UI, optional reduced shop ambience.
- Zach: full narrated lesson and contextual remediation selected from the player’s actual mistake.

### MTConnect node — orientation; Chapter 3 playable

- Visuals: node offline/connecting/healthy/stale/fault; signal-path overlay; machine state timeline; OEE/downtime dashboard.
- Audio: cable click, network confirmation, restrained notification, data-loss warning; no fantasy modem noises.
- Gameplay: map machine signals, classify states, diagnose missing/stale data, compare plan versus actual.

### JobLine handoff terminal — orientation; Chapter 2 playable

- Visuals: operator login, job status, counts, offsets, tool life, inspection status, abnormal note, next action, signed handoff.
- Audio: badge scan, keyboard, note save, handoff sent/received, escalation notification.
- Gameplay: assemble a complete shift handoff from observed production facts; incomplete context creates downstream risk.

## Chapter 2 — Job Shop

Add duplicate VMC/lathe cells with machine-specific identities and spatial audio, not cloned anonymous loops.

- Scheduling/dispatch: board animations, radio/notification cues, late-job and capacity-conflict feedback.
- Toolroom/presetter: tool crib drawers, RFID scan, presetter contact, assembly torque, tool-life states.
- CMM/quality lab: bridge motion, probe touches, program selection, datum setup, report generation.
- Wash/finish: parts washer cycle, drying air, basket loading; cleanliness states.
- Shipping: pack materials, label printer, tape, crate/pallet, dock departure.
- Maintenance cart: lubrication, filter, belt, way-cover, spindle-health inspection; wrench/grease/diagnostic audio.
- Employee stations: job-specific operating poses, footsteps, short contextual dialogue, handoff and help-request signals.

## Chapter 3 — Connected Plant

- Central production dashboard, machine connectors, downtime board, maintenance planning, quality lab, toolroom, material supermarket, shipping dock.
- Visual focus: state visibility over microscopic manual control—green/run, yellow/starved, red/fault, blue/setup must be readable without relying only on color.
- Audio focus: layered zones and notification priority. Distant machines form ambience; only selected cells expose detailed process sound.
- Gameplay focus: bottleneck discovery, downtime classification, dispatching people, restoring data, root-cause verification.

## Chapter 4 — Smart Factory

- Robotic machine-tending cell, cobot assembly/inspection, fixture-design station, digital work-instruction station, controlled toolroom, pallet pool.
- Visuals: guarding, interlocks, grippers, safe zones, part-present sensors, fixture locators, robot path previews.
- Audio: servo motion, pneumatic gripper, vacuum, interlock, pallet clamp, scanner, safe start/stop, abnormal contact.
- Gameplay: choose end effector, set safe approach, validate interlocks, prove reduced-speed path, check capability, standardize handoff.

## Chapter 5 — Lights-Out Complex

- AMR dispatch, automated storage/retrieval, palletized machining lines, robot recovery, centralized maintenance, energy and condition monitoring.
- Visuals: day/night variants, battery/charge, blocked aisle, queue buffers, unattended-ready checklist, fault camera and recovery views.
- Audio: AMR motor and courteous proximity cue, lift/conveyor/pallet transfers, distant cell layers, bearing/air-leak anomaly cues, night-shift ambience.
- Gameplay: plan unattended window, verify tools/material/inspection capacity, respond to faults, choose safe recovery, measure successful nights.

## Chapter 6 — American Titan Campus

- Campus operations center, aerospace traceability, training academy, engineering/programming, maintenance command, quality/metrology, multiple production buildings, customer/program office.
- Visuals: campus map and building interiors, department dashboards, program milestones, apprentice demonstrations, leadership handoffs.
- Audio: distinct building ambiences, campus logistics, large-cell process beds, restrained executive/strategy UI, graduation and mentor-legacy cues.
- Gameplay: delegate through leaders, protect certified-program traceability, balance capacity across buildings, develop apprentices, preserve knowledge.

## Audio mixing and behavior rules

- Never run every machine loop at full volume. Use a maximum detailed-source budget and collapse distant activity into facility ambience.
- Machine loop follows distance and room occlusion; UI, Zach, and critical safety cues remain intelligible.
- Duck machine/process audio under Zach narration by approximately 6–10 dB; do not mute it completely unless in a formal lesson.
- Start, run, engagement, disengagement, and stop are separate clips joined by state transitions.
- Healthy cutting, chatter, overload, air cutting, and collision-risk sounds must be meaningfully different and paired with visual/caption feedback.
- Loops must be seamless, normalized consistently, and free of voices, music, brand tones, and unintended alarms.
- Mobile/TV mode needs a reduced-dynamic-range mix and mono-compatibility check.

## Recommended production order

1. Finish Garage Bay sound state machine: idle, tool change, rapid/feed, clamps, failure variants, spatial ambience.
2. Make receiving, inspection, manual mill, and deburr fully playable with complete asset bundles.
3. Complete CNC lathe workflow and Chapter 2 scheduling/toolroom/quality/shipping.
4. Add reusable component libraries: controls, clamps, holders, gauges, material states, warnings, and NPC work poses.
5. Build Connected Plant visibility and downtime gameplay before adding large numbers of decorative machines.
6. Add automation, lights-out, and campus assets only alongside their playable management systems.

## Definition of done

A station graduates from orientation to playable only when all are true:

- Map presence and interaction radius work.
- Large view and all manipulated component views exist.
- Idle/active/fault/completion visuals exist.
- Required voice, SFX, captions, and mixer routing exist.
- Tutorial states exact prerequisites, operation, validation, and recovery.
- NPC can be assigned and visibly perform its role.
- Keyboard, Xbox, touch, and QR-phone controls pass.
- Save/load preserves station and job state.
- E2E completes success and at least one recoverable failure path.
- Storybook includes introduction, operation, outcome, and facility-growth context.
- Release gate rejects missing or mismatched assets.
