# Audio, Storyline, and Timeline Audit

Last verified: **2026-07-18**

## Result

**PASS for the currently implemented game.** The implemented story beats appear in the intended order, every required image and MP3 is present, voiced captions match their registered narration exactly, and all embedded Zach clips decode in Chromium.

This is not a claim that the entire planned story is produced. The unbuilt sequences are listed under **Remaining production**, below, and remain unchecked in `STORY_AUDIO_VISUAL_CHECKLIST.md`.

## Verified player timeline

1. **Pre-founder introduction** — 3 player-advanced, narrated beats
2. **Founder and company selection** — 10 selectable founders, custom player name, and custom company name
3. **Founding-day opening** — 5 ordered beats; 3 voiced and 2 intentionally silent on-screen narration cards
4. **Garage Bay shop tour** — 14 ordered stops, each with a What & Why panel followed by a How to Operate panel (28 narrated panels total)
5. **Garage production loop** — 9 contextual task tutorials with ordered operating instructions and validation states
6. **Garage graduation** — five completed customer jobs required before expansion
7. **Job Shop expansion** — 3 ordered beats; 2 voiced and 1 intentionally silent on-screen narration card

Story cards are advanced by the player; they are not forced onto a fixed wall-clock schedule. Advancing a card starts its registered clip from the beginning. Entering an intentionally silent card now stops the preceding Zach clip.

## Audio verification

- **61 / 61** embedded Zach clips decoded successfully in Chromium
- **0** decode failures and **0** page errors
- Total decoded narration: **405.23 seconds**
- Clip duration range: **2.69–10.54 seconds**
- 11 implemented cinematic story beats validated
- 8 voiced cinematic beats match their captions exactly
- 28 shop-tour panels match their registered narration exactly
- 9 active production task guides have correlated narration, image, location, instructions, success condition, and validation status

## Correction made during this audit

The runtime previously left the current Zach clip playing when the next story card intentionally had no voice assignment. `renderIntro()` now pauses narration at silent-card boundaries and displays **VOICE: NARRATION PAUSED**. A browser timeline pass verified both silent opening boundaries and the complete ordered tour after the correction.

## Automated regression status

`pnpm test:e2e`, `pnpm story:check`, `pnpm tour:check`, `pnpm tasks:check`, and `python scripts/selfcheck.py` all pass. Coverage includes:

- all 10 founder variants in selection, gameplay, and active story scenes
- contextual Zach mentoring and coaching
- the full opening and five-job Garage-to-Job-Shop progression
- all 14 shop-tour stops and 28 correlated panels
- all 9 active production task guides
- hiring, NOX material ordering, movement and equipment approach
- Xbox controls and QR-paired phone controls

## Remaining production

These sequences are planned but are **not yet release-complete**:

- NOX supplier introduction and delivery cinematics
- Shop Class opening cinematic
- first-article pass/fail cinematic branches
- first-hire team introduction
- Chapters 3–6 entry, milestone, facility, and graduation scenes
- dedicated art for each opening beat instead of the shared founder composition
- human visual sign-off that Zach's identity is consistent in every scene

Canonical records: `data/story-production.json`, `data/shop-tour.json`, and `data/production-task-tutorials.json`.
