# Developer Workflow

## First setup

1. Install Node 22, pnpm 10.24, Python 3.12, and Git.
2. Run `pnpm install --frozen-lockfile`.
3. Install Chromium for E2E: `python -m playwright install chromium`.
4. Run `pnpm game:hooks:install` once per clone.
5. Run `pnpm game:doctor` and resolve every failure.

Provider credentials belong only in ignored `.env` or the hosting secret manager. Never put them in browser variables, commits, screenshots, recordings, fixtures, or issue text.

## Daily loop

1. `pnpm game:generate` after changing the Python game generator or content data.
2. `pnpm game:verify` before handing work to another developer.
3. `pnpm game:smoke` after input, save, settings, loading, or runtime changes.
4. `pnpm test:e2e` after gameplay, story, equipment, customer, progression, or audio changes.
5. Use F3 in the game for FPS, memory, map, player position, loaded assets, input, pause, save, team, and runtime-error diagnostics.

## Gates

- Pre-commit: secret/output scan and environment doctor.
- Pre-push: strict types, unit tests, content/release contracts, backend boundary, bug-bounty baseline, and Git security scan.
- Pull request: regenerate versioned storybook proofs from a clean checkout, then run strict TypeScript, deterministic unit tests, production build, performance budget, save recovery, Xbox, and phone control tests.
- Main release: full E2E, dependency audit, backend boundary, Cloudflare artifact, deployment verification, and rollback readiness.

## Generated source rule

`scripts/build_level_viewer_v4.py` is authoritative for the current playable HTML. Do not hand-edit `apps/wecr8-info/prototypes/shop-floor-viewer.html`; regenerate it. Long-term, migrate the runtime into typed modules so browser gameplay and `game-core` share one state contract.

## Debugging

- Reproduce with a fresh browser context before changing state manually.
- Preserve the seed, save blob version, facility, objective, input mode, and last runtime error.
- Add a regression test before or with the fix.
- Never weaken a release validator to make a broken build pass.
- Keep future content marked `planned` or `orientation only` until its mechanic completes E2E.
