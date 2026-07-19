---
name: level-designer
description: Design shop-floor tilemaps, expansion layouts, and progression gates for REINDUSTRIALIZE. Use for new bays, tier expansions, and routing/flow puzzles.
---

# Level Designer

The shop floor is the board. Layout *is* gameplay: material flow, walking distance,
and future robot paths are the puzzle.

## Procedure
1. Read `data/machines.json` footprints + tier table.
2. Design bays as tile grids (JSON tilemap, layer order: floor > walls > stations >
   overlays). Start bay: 20x14 tiles; each expansion +8 columns.
3. Reserve infrastructure lanes: power drops (yellow floor tape tiles), network runs
   (tier 3 visual), AMR lanes (tier 5) — players who ignored lanes early feel the
   retrofit pain (mild, teachable, never punitive).
4. Validate: every station reachable; flow can run left-to-right (receiving to shipping);
   at least two viable layouts per bay (no single solution).

## Tilemap schema
```json
{"id":"bay_01","size":[20,14],
 "layers":{"floor":[],"walls":[],"zones":{"receiving":[[0,0],[2,13]],"shipping":[[18,0],[19,13]]}},
 "powerDrops":[[4,2],[4,8],[10,2]],
 "unlocks":{"tier":1}}
```

## Teaching intent per tier
- T1-2: distance matters (walk time visible as operator pathing).
- T3: network topology mini-layer (switch placement, cable runs — mirrors the real
  Haas MTConnect checklist).
- T4: tool crib placement (presetter near machines cuts setup ticks).
- T5: robot reach + AMR lane conflicts (the routing puzzle).
