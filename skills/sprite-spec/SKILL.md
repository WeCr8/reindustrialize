---
name: sprite-spec
description: Convert an entity's sprite spec into a constrained pixel-art generation prompt (or artist brief) matching the REINDUSTRIALIZE concept art, then define ingest/validation steps. Use whenever new art is needed.
---

# Sprite Spec

Goal: every generated asset looks like it came from the same cartridge as the concept image.

## Hard constraints (embed in every prompt/brief)
- 3/4 top-down 16-bit SNES style, 1px black outlines, **no anti-aliasing, no gradients**.
- Exact canvas: tiles 32x32; characters 32x48; machines per `footprint` (n x 32).
- Palette: only hexes from `packages/assets/palette.json` (WeCr8 navy #1a2e44,
  orange #e8491d, sky #4a9fd4, HUD gold #e8b93b, terminal green #3fd08a + steel ramp).
- Transparent background. All states/frames on one sheet, left-to-right, consistent origin.

## Prompt template
"16-bit SNES pixel art spritesheet, {entity description}, 3/4 top-down factory view,
{W}x{H} px per frame, {N} frames: {state list}, strict palette {hexes}, 1px black
outline, no anti-aliasing, transparent background, industrial machine shop setting,
style-matched to a retro factory tycoon RPG."

## Machine visual language
- Tier 1: worn paint, wood benches. Tier 3+: enclosure windows w/ terminal-green screens.
- `running`: subtle 2-4 frame loop (spindle blur / chip spray / status LED).
- `alarm`: red beacon 2-frame flash. `LIVE` badge: gold 8x8 overlay, top-right.

## Ingest & validation (scripts/ingest.py)
1. Quantize to palette (error if >2% off-palette pixels — regenerate, don't fix silently).
2. Verify frame grid + transparent bg; build atlas JSON (Aseprite format).
3. Hash into `manifest.json`; drop into `packages/assets/sprites/`.
4. Add to the dev gallery for human review. Nothing ships unreviewed.
