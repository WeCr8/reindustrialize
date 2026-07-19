# Art Direction — Closing the Gap to Concept Quality

## Where quality comes from (three layers)
1. **HUD chrome (DONE, matches concept now):** chunky gold double-border panels on near-black,
   drop shadows, VT323 type, segmented skill bars in green/blue/gold/purple, portrait dialog
   box. This is CSS/canvas and already at concept fidelity in the viewer.
2. **Procedural sprites v2 (DONE, playable):** shading ramps, top-light + shadow edges,
   dithered large surfaces, grimy mottled concrete with grout, VF-2SS-style detailing
   (red logo block, dark windows with reflection streaks, tan retro control pendant with
   colored buttons), teal tool cart, shaded characters, 64x64 Zach dialog portrait.
   This is strong placeholder art — it will not fully match the concept's illustration density.
3. **Final art (NEXT):** the concept image is AI-generated illustration-grade pixel art.
   Matching it means generating final sheets with an image model against the atlas contract,
   then quantizing/ingesting. The contract (names, frame sizes, states) is already locked,
   so final art is a pure asset swap — zero code changes.

## Master style prompt (derived from the concept image)
"detailed 16-bit SNES pixel art, industrial machine shop, 3/4 top-down view,
muted steel grays and warm concrete, strong 1px black outlines, top-left key light,
subtle dithered shading on large surfaces, grimy realistic floor with stains and grout,
occupational-realist detail (control pendants, beacon lights, tool holders),
color accents: safety orange #e8491d, HUD gold #e8b93b, terminal teal-green #3fd08a,
navy #1a2e44 — no anti-aliasing, no gradients, transparent background"

## Per-asset prompt seeds (append to master)
- vmc_t2 (96x96, 2 frames): "white vertical machining center, VF-2SS style, red logo plate,
  dark enclosure windows with diagonal glass reflections, tan retro CNC control pendant with
  green CRT and orange/green/red buttons; frame 2: spindle down, blue coolant spray, bronze chips, red beacon lit"
- lathe_cnc_t2 (96x64, 2 frames): "CNC turning center, chuck visible through door window, tailstock,
  tan control panel; frame 2: bar stock turning, chip curl sparks"
- tool_cart (64x64): "dark teal rolling tool cabinet, three drawers with steel handles,
  butcher-block top holding CAT40 toolholders, black casters" (matches concept cart)
- guide_zach sheet (32x48 x states) + zach_portrait (64x64): "bearded machinist, black ball cap,
  charcoal work jacket over black tee, jeans, tan work boots" (concept character, no logo)
- tileset floor: "large concrete slabs, dark grout lines, oil stains, hairline cracks, subtle mottle"
- full list + states: packages/assets/nox-asset-specs.json and data/*.json spriteSpec blocks

## Pipeline (per skills/sprite-spec)
model output -> scripts/ingest.py (quantize to palette.json, verify frame grid + transparency,
rebuild atlas.json + manifest hashes) -> dev gallery review -> asset swap. Regenerate the
viewer with scripts/build_level_viewer_v2.py to see it in-world instantly.

## Review gates
No sheet ships unless: on-palette (>98%), correct frame grid, reads at 1x zoom,
silhouette identifiable at 50% size, consistent key light (top-left).
