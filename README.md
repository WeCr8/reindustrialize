# REINDUSTRIALIZE — 32-bit Manufacturing RPG by WeCr8 Solutions

> **Release identity:** Development targets `0.7.0-alpha`. After each deployment, compare the current checkout with [https://playreind.com/release.json](https://playreind.com/release.json) and read [the public release notes](https://playreind.com/release-notes/). The source release note is [docs/releases/0.7.0-alpha.md](docs/releases/0.7.0-alpha.md).

> **Amazon Luna preparation:** See [docs/AMAZON_LUNA_RELEASE_PREPARATION.md](docs/AMAZON_LUNA_RELEASE_PREPARATION.md). The bundle prepares listing, review, controller/TV, privacy, and artifact requirements but deliberately stops before identity authorization or submission.

> **Build and test status:** See [FINAL_E2E_STATUS.md](FINAL_E2E_STATUS.md) for the verified gameplay journey, controls, facility progression, and remaining release work.

> **Internal bug bounty:** Run `pnpm bug-bounty:baseline` for the safe automated guard. Detailed vulnerability reports remain outside the public repository and follow [docs/BUG_BOUNTY_PROGRAM.md](docs/BUG_BOUNTY_PROGRAM.md).

> **Current-to-final roadmap:** See [GROWTH_ROADMAP_AND_RELEASE_STATUS.md](GROWTH_ROADMAP_AND_RELEASE_STATUS.md) for the honest playable-alpha status, six-chapter growth plan, milestone exit criteria, and final 1.0 ship gate.

> **Game-development audit:** See [docs/GAME_DEVELOPMENT_REPO_AUDIT.md](docs/GAME_DEVELOPMENT_REPO_AUDIT.md) for the repository-wide production assessment, implemented recovery/settings/diagnostics foundation, remaining release blockers, and standard developer commands. Run `pnpm game:doctor` before starting work and `pnpm game:smoke` before handing off a gameplay change.

> **Developer workflow:** Follow [docs/DEVELOPER_WORKFLOW.md](docs/DEVELOPER_WORKFLOW.md). `pnpm game:verify` runs strict types, deterministic unit tests, content/release contracts, backend boundaries, bug-bounty checks, and the Git security guard. `pnpm game:verify:full` adds all browser E2E, the Cloudflare artifact, and the dependency audit.

> **Independent expert review:** See [docs/MULTI_DISCIPLINE_GAME_REVIEW.md](docs/MULTI_DISCIPLINE_GAME_REVIEW.md). The reusable senior game-developer, narrative-designer, and manufacturing-business reviewer contracts live in `data/review-agents.json` and are validated by `pnpm agents:review:check`.

> **Verified game bundle:** Run `pnpm bundle:game` to rebuild the standalone game, enforce release and E2E gates, exclude secrets, produce SHA-256 checksums, and create the versioned Windows/web ZIP under `dist/`.

> **Story production status:** See [STORY_AUDIO_VISUAL_CHECKLIST.md](STORY_AUDIO_VISUAL_CHECKLIST.md) for the ordered storyline, exact voice-caption pairs, required images, runtime triggers, and missing future scenes.

> **Required release gate:** `pnpm build` and `pnpm test:e2e` now block automatically unless implemented images, audio, story order, captions, tutorials, founder scenes, maps, progression, and game references pass. Run `pnpm release:gate` for the faster standalone checklist.

> **Audio production:** See [docs/ELEVENLABS_AUDIO_SETUP.md](docs/ELEVENLABS_AUDIO_SETUP.md) for the consent-gated, server-side ElevenLabs voice and music generation workflow. API credentials are never included in the browser build.

> **Station asset and audio plan:** See [docs/STATION_ASSET_AUDIO_MASTER_PLAN.md](docs/STATION_ASSET_AUDIO_MASTER_PLAN.md) for the complete station-by-station visual, animation, SFX, narration, interaction, failure-state, and E2E requirements from the Garage Bay through the American Titan Campus.

> **Accounts and cloud saves:** See [docs/BACKEND_OPTIONS_AND_RELEASE.md](docs/BACKEND_OPTIONS_AND_RELEASE.md) for disabled, local Supabase, direct Supabase, and Lovable-compatible deployment choices. Cloud features remain disabled by default.

> **Future free-form Zach Q&A:** See [docs/LLM_MENTOR_READINESS.md](docs/LLM_MENTOR_READINESS.md) for the disabled, provider-neutral OpenRouter/Groq/Hugging Face adapter. The reviewed scripted mentor remains the default.

> **Demo video:** The repeatable Playwright screenshot path and Remotion composition live under `scripts/capture-demo-screenshots.py` and `demo/remotion`. Run `pnpm demo:studio` to review or `pnpm demo:render` to produce the 60-second gameplay overview with generated game music.

> **Current promo slate:** V2 exports preserve V1 and add running/proximity gameplay across horizontal, vertical, square, long-form, Zach, founder, growth, and scripted-player cuts. See [videos/README.md](videos/README.md); rebuild all current exports with `pnpm media:render:v2` and verify them with `pnpm promo:check:v2-media`.

> **Current website film:** The V7 homepage campaign film uses real human-bot gameplay, expressive ElevenLabs narration, music ducking, burned-in captions, WebVTT captions, and a tested play-with-sound control. Render it with `pnpm hero:render:v7` and validate it with `pnpm hero:check:v7`. The broader V5 gameplay slate remains indexed in [DEMO_VIDEO_INDEX.md](DEMO_VIDEO_INDEX.md).

> **Visual storybook review:** Open [storybook/v1/index.html](storybook/v1/index.html) for numbered slide-by-slide review of the prologue, all ten founder options, every founder scene variant, the shop tour, production tutorials, and planned art gaps. Rebuild and export every slide with `pnpm storybook:release`.

> **Public hosting:** `PlayReInd.com` is configured for Cloudflare Workers Static Assets. Run `pnpm cloudflare:build` to create the limit-checked public build and `pnpm cloudflare:deploy` after Cloudflare login and zone activation. See [docs/CLOUDFLARE_HOSTING.md](docs/CLOUDFLARE_HOSTING.md).

## Local Test URLs

Start the game server from the repository root:

```powershell
pnpm --dir server start
```

- Computer browser: [http://localhost:8787/game](http://localhost:8787/game)
- TV or another device on the same network: [http://192.168.1.22:8787/game](http://192.168.1.22:8787/game)
- Phone controller pairing is available from **CONTROLS & PHONE** inside the game.
- Select **TALK WITH ZACH** in the shop HUD for contextual task help, machining lessons, quality guidance, people development, and business mentoring.

The LAN address can change after a router or computer restart. If the TV URL stops working, run `ipconfig`, find the active adapter's IPv4 address, and replace `192.168.1.22` while retaining port `8787` and `/game`. Allow Node.js through Windows Firewall on Private networks if another device cannot connect.

> **Campaign progression:** See [docs/PROGRESSION_SCALE.md](docs/PROGRESSION_SCALE.md) for the 30-level, six-chapter graduation model and facility gates.

> **Campaign length target:** 10–12 hours for the six-chapter main story and 16–20 hours for mastery, optional contracts, team stories, and 24 manufacturing-themed Easter eggs. The current Garage-to-Job-Shop playable slice is approximately 30–45 minutes for a new player.

> "We are here to help reindustrialize and help manufacturing dominate in America." — Zach, LVL 34 CNC Specialist

A retro factory-builder RPG that teaches real manufacturing. Players build a job shop from
an empty bay: buy machines, hire and level up operators, connect machines to data (MTConnect),
deploy robots/cobots, and complete quests that mirror real shop-floor workflows.

Runs in two modes on two properties:

| Property     | Mode        | Audience                | Data source        |
|--------------|-------------|-------------------------|--------------------|
| wecr8.info   | **Arcade**  | Public / STEM / leads   | Simulated economy  |
| jobline.ai   | **Shop Mode** | JobLine customers     | Live shop data via jobline-mcp — real machine uptime, jobs, and handoffs feed XP & quests |

The game is a Trojan horse for the funnel: Arcade players learn what JobLine does by
*playing* it; Shop Mode turns real operational hygiene (clean handoffs, connected machines,
preset tools) into XP, achievements, and leaderboards.

## Monorepo layout

```
reindustrialize/
├── docs/                  Design + architecture docs (start here)
│   ├── GAME_DESIGN.md     Core loop, progression, economy, Zach the Guide
│   ├── ARCHITECTURE.md    Packages, data flow, public vs private boundary
│   ├── AUTH.md            Shared identity across wecr8.info / jobline.ai
│   └── ASSET_PIPELINE.md  Sprite specs, generation loop, CDN layout
├── skills/                Code-gen loop skills for Claude / Carnegie agents
│   ├── machine-generator/     New machine defs (stats + sprite spec + quest hooks)
│   ├── character-generator/   NPCs, operators, robots
│   ├── quest-generator/       Quests mapped to real manufacturing workflows
│   ├── sprite-spec/           Pixel-art prompt + palette standards
│   └── level-designer/        Shop-floor tilemaps & progression gates
├── data/                  Canonical game content (single source of truth, JSON)
│   ├── machines.json      Machine registry (VF-2SS, lathes, ZOLLER, HERO-CART…)
│   ├── characters.json    Zach the Guide, operators, robots
│   ├── quests.json        Quest chains incl. real-data-linked Shop Mode quests
│   └── skills-tree.json   Player skill tree (mirrors the screenshot HUD)
├── packages/
│   ├── game-core/         Engine-agnostic sim: economy, quests, save system (TS)
│   ├── game-ui/           React components + hooks (HUD, dialog box, shop grid)
│   ├── assets/            Public game assets + manifest (CDN-served)
│   └── auth/              Shared auth client (JWT, SSO across both domains)
├── apps/
│   ├── wecr8-info/        Arcade embed for wecr8.info
│   └── jobline/           Shop Mode embed for jobline.ai (auth-gated)
└── server/                Private API: saves, leaderboard, telemetry, JobLine bridge
```

## Public vs non-public boundary

**Public (CDN / open):** `packages/assets`, `data/*.json` (game content is marketing),
Arcade build of the game.

**Private:** `server/` (saves, leaderboards, JobLine data bridge), `packages/auth` server
secrets, Shop Mode build, any endpoint touching customer shop data.

## Quick start (dev)

```bash
pnpm install
pnpm build                 # mandatory production gate, then workspace build
pnpm test:e2e              # same gate, then complete browser gameplay suite
pnpm --filter wecr8-info dev     # Arcade mode on :5173
pnpm --filter server dev         # API on :8787
```

## Brand

Palette anchors to WeCr8: navy `#1a2e44`, orange `#e8491d`, sky `#4a9fd4`, plus the
retro HUD golds/greens from the concept art. See `skills/sprite-spec/SKILL.md`.
