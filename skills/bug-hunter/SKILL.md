---
name: bug-hunter
description: Find bugs and self-repair the REINDUSTRIALIZE project. Run after ANY content or code change, when something looks wrong in a prototype, or on a schedule. Also the home of the project's must-have coding principles.
---

# Bug Hunter & Self-Repair

## Procedure (the loop)
1. **Detect** — run `python3 scripts/selfcheck.py`. It validates every data file against
   schemas + cross-references (quest events vs sim events, sprite sheets vs atlas, map
   overlaps/collisions, balance invariants, dangling ids).
2. **Triage** — selfcheck reports `AUTO-FIXED` (safe repairs it already made), `ERROR`
   (breaks the game - fix now), `WARN` (drift - fix or consciously accept).
3. **Reproduce** — for behavior bugs, write the smallest failing case as a vitest in
   game-core (deterministic sim = every bug is replayable from seed + event log).
4. **Repair** — fix root cause, not symptom. If a schema allowed the bad data, tighten
   the schema in the same commit.
5. **Regress-proof** — the reproduction test stays forever. Re-run selfcheck; must be clean.

## Must-have coding principles (enforced, not aspirational)
- **Determinism is sacred.** Sim output = f(seed, eventLog). No Date.now/Math.random in
  game-core; only the seeded rng. Anti-cheat, replays, and bug repro all depend on it.
- **Content is data, validated at the door.** Every data/*.json passes zod + selfcheck in CI.
  Code-gen skills run selfcheck after every write - generated content gets zero trust.
- **Single source of truth.** Balance numbers live in data/, never duplicated in code.
  Atlas contract (names/frames/sizes) is law; art and code both conform to it.
- **Versioned saves, forward-only migrations.** Bump SAVE_VERSION on any GameState change
  and add a migration. Never strand a player's shop.
- **No browser storage in embeds.** Saves go through the server (anon JWT); embeds may run
  storage-restricted. useState/refs for session state.
- **Fail toward teaching.** Runtime errors in minigames degrade to Zach dialog + retry,
  never a crash screen. Mirrors the game's own philosophy.
- **Boundaries stay clean.** game-core: zero DOM/React. Secrets: server-only. Bridge: read-only.
- **Every prototype regenerates from scripts.** If you hand-edit a built HTML file, you've
  created a bug - change the generator instead.

## When invoked with a symptom (e.g. "avatar walks through the lathe")
Check in order: data (map footprint?) -> contract (atlas fw/fh?) -> code (collision math?).
Most bugs here are data bugs; selfcheck should have caught it - if it didn't, add the check.
