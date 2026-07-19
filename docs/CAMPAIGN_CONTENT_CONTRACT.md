# Full Campaign Content Contract

Every chapter must ship as a complete, testable bundle rather than a map with disconnected placeholders.

## Required chapter package

A chapter may move from **locked** to **playable** only when all of these exist:

- facility map, collision, spawn, equipment placement and visual-debug route
- entry, midpoint, graduation and facility-move story sequences
- selected-founder scene treatment wherever the player appears
- approved Zach narration, exact captions, music and task/location SFX
- orientation tutorial for every visible station
- playable guide for every active task with prerequisites, instructions, success and validation state
- complete production, people, quality, cash and facility graduation loop
- four original Easter eggs: three environmental and one multi-step discovery
- save/restore boundaries at entry, task completion, failure recovery and graduation
- keyboard, controller, touch and phone completion paths
- automated chapter E2E from prior-facility move through next-facility arrival
- human review of story, identity, art, audio, difficulty and manufacturing correctness

Visible equipment without mechanics must say **orientation only**. Planned scenes and chapters remain locked. Neither may be counted as playable by the bundle manifest or release roadmap.

## Bundle states

- `playable`: required chapter loop completes normally and passes E2E.
- `in_development`: some real content exists, but graduation is not complete.
- `locked`: roadmap/data may exist, but the player cannot enter it as released gameplay.

## Final campaign definition

Version 1.0 requires six playable chapter packages, 30 levels, six facility graduations, the ending and credits, 10–12 hours of mainline play, 24 discoverable Easter eggs, and every final ship gate in `GROWTH_ROADMAP_AND_RELEASE_STATUS.md`.
