---
name: machine-generator
description: Generate a new machine definition for REINDUSTRIALIZE — stats, economy balance, sprite spec, and quest hooks. Use when adding any machine, station, or piece of shop equipment to the game.
---

# Machine Generator

You are adding a machine to `data/machines.json`. Machines must feel authentic to real
manufacturing (Zach's audience will notice fake specs) while staying balanced.

## Procedure
1. Read `data/machines.json` and `docs/GAME_DESIGN.md` (tier table + economy sketch).
2. Choose class + tier. Every machine maps to a real-world archetype (e.g. "3-axis VMC,
   VF-2SS class"). Use *class* names in-game; real brand references only in `inspiration`.
3. Balance stats with the invariants below, then emit the JSON entry + a sprite spec block
   for the sprite-spec skill.
4. Add at least one quest hook: what does buying/mastering this machine unlock or teach?

## Schema (zod: game-core/src/machines/schema.ts)
```json
{
  "id": "vmc_t2_01", "name": "3-Axis VMC", "class": "vmc", "tier": 2,
  "inspiration": "Haas VF-2SS",
  "footprint": [3,3], "price": 12000, "powerDraw": 3,
  "cycleSpeed": 1.0, "quality": 0.92, "reliability": 0.95,
  "requiresOperatorSkill": {"cnc_programming": 2},
  "automation": {"cobotTendable": true, "mtconnect": true},
  "spriteSpec": {"sheet":"vmc_t2_01","states":["idle","running","alarm","setup"],"frames":{"running":4}},
  "questHooks": ["first_cnc_setup", "connect_machine_live"],
  "zachTip": "Warm the spindle up. Cold machine, scrapped part."
}
```

## Balance invariants (do not violate)
- `price(tier n) ~= 3x price(tier n-1)` for the same class.
- Payback: a machine pays for itself in 20-40 shipped jobs at its tier.
- `quality * reliability` never exceeds 0.97 below tier 5 (perfection is a lights-out reward).
- Higher tier must trade off *something* (footprint, power, operator skill gate) — no
  strict upgrades.
- Every tier-3+ machine sets `"mtconnect": true` (the connectivity story is the point).

## Output
Append the entry to `data/machines.json` (keep sorted by tier, then class) and print the
sprite spec block for handoff to `skills/sprite-spec`.
