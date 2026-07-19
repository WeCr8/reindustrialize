---
name: character-generator
description: Generate NPCs, hireable operators, and robots for REINDUSTRIALIZE — personality, stats, dialog voice, sprite spec. Use for any new character, hire, robot, or dialog-bearing entity.
---

# Character Generator

Characters carry the teaching. Every character exists to make a real manufacturing
lesson memorable.

## Procedure
1. Read `data/characters.json` for existing cast + voice ranges (avoid overlap).
2. Pick role: `guide` (Zach only), `operator` (hireable), `vendor`, `customer`, `robot`.
3. Write the entry: stats, growth, 3 sample dialog lines *in their voice*, sprite spec.
4. Operators need a flaw + a growth arc (they level up; perfect hires are boring and
   teach nothing about developing people).

## Schema
```json
{
  "id": "op_rosie", "role": "operator", "name": "Rosie",
  "archetype": "young-gun apprentice",
  "hireCost": 800, "wagePerShift": 60,
  "skills": {"cnc_programming":1,"automation":0,"problem_solving":2,"communication":1},
  "growth": {"fast":["automation"],"slow":["communication"]},
  "flaw": "skips the handoff notes when rushed",
  "arcQuest": "rosie_learns_handoffs",
  "voice": ["Cycle's done — want me to break edges too?",
            "I can program the cobot. Probably. Mostly.",
            "Wrote it all in the handoff. Every word. You're welcome, night shift."],
  "spriteSpec": {"sheet":"op_rosie","base":"32x48","states":["idle","walk","work","talk","celebrate"]}
}
```

## Voice rules
- Zach's voice is defined in GAME_DESIGN.md and is the only voice allowed to address
  the player as teacher. Never generate a second guide.
- Shop-floor plainspoken. No corporate speak, no memes that will age.
- Robots don't talk; they beep and display status glyphs (see sprite-spec).

## Robots
Robots are `role: "robot"` with `skills` replaced by `{"throughput", "faultRate",
"programmingGate"}` and no wages — their cost is install downtime + maintenance.

## Player avatars
Avatars live in `data/avatars.json`, not characters.json. Rules: selectable male/female
bodies with 2+ presets each, cosmetic only (zero stat differences), silent protagonist
(no voice lines ever — Zach teaches). Required states: idle, walk4dir, work, carry, plan,
celebrate. Every preset gets 2 accent slots mapped to brand palette colors.
