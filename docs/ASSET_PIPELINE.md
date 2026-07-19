# Asset Pipeline

## Standards (locked to the concept art)
- Base resolution: 32×32 tile grid; characters 32×48; large machines up to 96×96 (3×3 tiles).
- Render at 1× and integer-scale in engine (`image-rendering: pixelated`). Never resample.
- Palette: 32-color master ramp derived from the concept image — WeCr8 navy `#1a2e44`,
  orange `#e8491d`, sky `#4a9fd4`, HUD gold `#e8b93b`, terminal green `#3fd08a`,
  steel grays, warm wood. Full ramp lives in `packages/assets/palette.json`.
- File layout: spritesheets per entity, JSON atlas (Aseprite export format).

## Generation loop (with skills/)
1. `machine-generator` or `character-generator` skill produces the **entity JSON** +
   a **sprite spec** (states, frames, footprint, palette slots).
2. `sprite-spec` skill turns that into a repeatable pixel-art prompt for the image model
   (or a brief for a human pixel artist) with hard constraints: grid size, palette hexes,
   ¾ top-down view matching the concept art, black 1px outlines, no anti-aliasing.
3. Generated art → `scripts/ingest.py` (quantize to palette, verify grid, build atlas,
   update `manifest.json` with sha256).
4. Visual review in the asset gallery page (`apps/wecr8-info /dev/gallery`).

## Required animation states
- Machines: `idle`, `running` (2–4 frame loop), `alarm` (red beacon), `setup`, `LIVE-badge`
- Characters: `idle`, `walk×4dir`, `work`, `talk` (portrait mouth flap), `celebrate`
- Robots: `idle`, `move`, `pick`, `place`, `fault`

## Audio
Chiptune SFX (jsfxr-generated ok for v0.1): machine hum loops per tier, coin, quest-complete
jingle, alarm. Music: 2 loops (day shift / lights-out) — license or commission, do not ship
copyrighted tracker files.

## CDN layout (public)
`assets.wecr8.info/game/{version}/…` — immutable, hashed. `manifest.json` is the only
mutable pointer.
