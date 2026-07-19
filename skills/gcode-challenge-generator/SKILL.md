---
name: gcode-challenge-generator
description: Generate G-code fill-in-the-blank challenges for REINDUSTRIALIZE. Use when adding CNC learning content — new operations, dialects, or machine classes.
---

# G-code Challenge Generator

Challenges must be REAL G-code that would run on a real control. Zach's audience includes
working machinists; a wrong modal code is a credibility hit.

## Procedure
1. Read `data/gcode-challenges.json` (avoid duplicate lessons) and the schema in
   `game-core/src/gcode/challenge.ts`.
2. Pick one operation and one lesson sentence. One concept per challenge.
3. Write the full correct program first. Verify modality (G90/G91 state, cycle cancel,
   coolant off before home). Then choose 2-3 blanks max.
4. Blank types:
   - **exact** — vocabulary (M03, G54, G43, G81, G80, G96, G28, M08/09, M30). Accept
     leading-zero variants ("03","3").
   - **range + compute** — physics. Use `rpmFromMaterial` / `feedFromRpm` /
     `sfmFromMaterial` so answers derive from the job's NOX material. Tolerance 0.2-0.3
     (0.5 for plunge). Never hardcode an RPM the material should decide.
5. Write zachFail (teach the formula/why, his voice) and zachPass (short, earned).

## Rules
- Dialect: Haas/Fanuc for launch. Tag future Siemens/Mazak/Okuma variants with
  `"dialect"` — mirror jobline-gcode extension dialects.
- Never blank safety-critical values in ways where a "pass" would crash a real machine
  if copied verbatim (e.g., don't accept negative R planes).
- Tier 2 = basics (spindle, feed, offsets, ends). Tier 3 = cycles, CSS. Tier 4+ =
  cutter comp (G41/42), rigid tapping, macros.
- 3 fails -> teach and retry. The console is a classroom, not a gate to grind on.

## Output
Append to `data/gcode-challenges.json`, run `pnpm validate:content`, and list which
quests should reference the new challenge id.
