# Architecture

## Principles
1. **One sim, two skins.** `game-core` is pure TypeScript with zero DOM/React deps.
   Both apps import the same engine; only data adapters and chrome differ.
2. **Content is data.** All machines/characters/quests live in `data/*.json`, validated
   by zod schemas in `game-core`. Code-gen skills write JSON, not code.
3. **Public by default, private by exception.** Assets and content JSON are CDN-public
   (they double as marketing). Anything touching identity or customer shop data lives
   behind `server/`.

## Data flow

```
                         ┌──────────────────────┐
  data/*.json ──build──▶ │  packages/game-core   │ ◀── deterministic sim, seeded RNG
                         │  (economy/quests/save)│
                         └──────┬───────────────┘
                                │
                  ┌─────────────┴─────────────┐
        packages/game-ui (React hooks + HUD components)
                  │                           │
        apps/wecr8-info (Arcade)     apps/jobline (Shop Mode)
                  │                           │
                  └───────── server/ ─────────┘
                    /saves /leaderboard /auth
                    /bridge/jobline  ← jobline-mcp (live shop data)
```

## Packages
- **game-core** — tick-based sim (1 tick = 1s game time). Deterministic given seed +
  input log → replayable saves, cheap server-side validation of leaderboard claims.
- **game-ui** — React components styled to the concept art (HUD panels, dialog box,
  quest tracker) + hooks (`useGameState`, `useSave`, `useQuestLog`, `useAuth`).
  Canvas layer for the shop floor (pixel-perfect, integer scaling, `image-rendering: pixelated`).
- **assets** — sprites/tilesets/audio + `manifest.json` with content hashes for cache-busting.
- **auth** — browser client for the shared identity service (see AUTH.md).

## Server (private)
- `POST /saves` — save blob + input log; server replays sim to validate (anti-cheat).
- `GET/POST /leaderboard` — Arcade global; Shop Mode per-org, opt-in.
- `POST /telemetry` — funnel events (tier reached, quest completed, CTA clicked).
- `GET /bridge/jobline/*` — Shop Mode only. Reads via jobline-mcp; **read-only**, org-scoped,
  never writes to customer systems. Maps real events → game rewards (see GAME_DESIGN.md).

## Embedding
Each app builds to a self-contained web component `<reindustrialize-game mode="arcade|shop">`
so either site drops it into any page. Arcade requires no auth; Shop Mode requires a
JobLine session (silent SSO, see AUTH.md).

## Suggested stack
- pnpm workspaces, TypeScript strict, Vite builds
- Rendering: plain Canvas 2D (16-bit doesn't need WebGL); consider Pixi.js only if
  particle/lighting wants grow
- zod for content schemas; vitest for sim determinism tests

## Mobile rendering (v0.6.1)
Phones don't shrink the map; they get a **camera**. The canvas renders a viewport of
~9-12x11 tiles that follows and clamps to the player, so sprites stay full-size and
readable on a 390px screen. Fit logic picks viewport tile counts from available width and
applies a fit-to-screen CSS scale (integer-preferring). Mobile HUD collapses to a mini
strip (name / coins / quest %) + compact dialog; side panels are desktop-only. Inputs are
additive: keyboard, mouse click-to-step, touch D-pad with hold-repeat, and tap-to-walk
(camera-offset corrected). One build serves both form factors; the old full-map behavior
is simply the camera at max viewport. Generator: scripts/build_level_viewer_v3.py
(v1/v2 removed - prototypes always regenerate from the single current script).
