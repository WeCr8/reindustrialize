# Story, Audio, and Visual Production Checklist

Last verified: **2026-07-18**

This document is the human-readable companion to `data/story-production.json`. A scene is complete only when its trigger, ordered story beat, image, exact caption, voice clip, runtime wiring, and E2E assertion agree.

## Pre-founder sequence

| # | Beat | Visual | Zach audio | Exact caption | Runtime |
|---|---|---|---|---|---|
| 1 | Welcome to REINDUSTRIALIZE | `story-pre-founder-welcome-v1.png` | `zach_pre_founder_welcome.mp3` | Verified | Implemented before selection |
| 2 | Garage-to-powerhouse path | `story-pre-founder-path-v1.png` | `zach_pre_founder_path.mp3` | Verified | Implemented before selection |
| 3 | Choose founder and company | `story-pre-founder-choice-v1.png` | `zach_pre_founder_choice.mp3` | Verified | Hands off to Founder A–J selection |

Identity reference: the approved close-up controls Zach's facial cues; the approved black-cap full-body photo controls his tall lean build, charcoal-gray shacket, jeans, and brown shoes.

## Founding-day opening sequence

| # | Beat | Visual family | Zach audio | Exact caption | Runtime |
|---|---|---|---|---|---|
| 1 | Founder signs the lease | selected-founder opening scene | none | On-screen narration | Implemented |
| 2 | Welcome to the shop | selected-founder opening scene | `zach_shop_welcome.mp3` | Verified | Implemented |
| 3 | Zach's mentor role | selected-founder opening scene | `zach_welcome.mp3` | Verified | Implemented |
| 4 | First customer at planning | selected-founder opening scene | `zach_first_job.mp3` | Verified | Implemented |
| 5 | Long-term powerhouse goal | selected-founder opening scene | none | On-screen narration | Implemented |

## Job Shop expansion sequence

| # | Beat | Visual family | Zach audio | Exact caption | Runtime |
|---|---|---|---|---|---|
| 1 | Move after five completed jobs | selected-founder expansion scene | none | On-screen narration | Implemented |
| 2 | Standardize the system | selected-founder expansion scene | `zach_job_shop.mp3` | Verified | Implemented |
| 3 | You outgrew the garage | selected-founder expansion scene | `zach_expansion.mp3` | Verified | Implemented |

## Garage Bay shop tour and equipment tutorials

- [x] Starts after the founding-day sequence and before the first production objective
- [x] Replayable from **SHOP TOUR** in the shop toolbar
- [x] Fourteen ordered stops cover all thirteen unique Garage Bay equipment types
- [x] Every station has two narrated panels: **What & Why** and **How to Operate**
- [x] Twenty-eight tutorial panels each retain the correlated station image, exact caption, Zach MP3, location, prerequisites, operating sequence, and success condition
- [x] Planning, NOX ordering, bandsaw, tool setup, VMC, mission routing, and overview are marked playable
- [x] CNC lathe is marked inspection-only
- [x] Shop Class, manual mill, deburr, MTConnect, JobLine handoff, and receiving are marked orientation-only where mechanics remain incomplete
- [x] **SHOW ON FLOOR** closes the tutorial and routes the founder to that station for visual debugging
- [x] Automated checks ensure every map equipment type has a tutorial and every narration matches its caption exactly

Canonical registry: `data/shop-tour.json`. Run `pnpm tour:check`.

## Active production task tutorials

- [x] Material ordering
- [x] Customer-job acceptance
- [x] Raw-stock bandsaw cut
- [x] Primary cutter selection
- [x] Tool stickout setting
- [x] Complete three-tool CNC kit
- [x] G-code proofing
- [x] CNC cycle execution and safe-stop guidance
- [x] Quality result and first-article review

Each active task has its own location, correlated image, exact Zach narration, prerequisites, ordered operating instructions, success condition, and **playable** validation status. Access the contextual guide from **TASK GUIDE** in the toolbar or inside a station overlay.

Canonical registry: `data/production-task-tutorials.json`. Run `pnpm tasks:check`.

## Required future sequences

- [ ] NOX supplier introduction: five shots, supplier SFX, Zach/player dock variants, first-catalog trigger
- [ ] NOX delivery: truck/pallet animation, delivery SFX, material-received trigger
- [ ] Shop Class opening: chalkboard artwork, chalk/tool-tap SFX, first-entry trigger
- [ ] First-article inspection: measurement artwork/SFX and pass/fail branches
- [ ] First hire: team-introduction scene and selected-candidate portrait
- [ ] Chapters 3–6: entry, mid-chapter, graduation, facility, and business milestone scenes
- [ ] Dedicated artwork for each opening beat instead of shared selected-founder opening composition
- [ ] Human visual approval of Zach identity on every existing title, opening, expansion, equipment, and marketing scene

## Release gate

- [x] Story order is data-driven
- [x] Every implemented voiced beat has exact matching caption text
- [x] Every implemented voice ID has an MP3 file
- [x] Every implemented story beat names a visual
- [x] Player-containing scenes require selected-founder identity overlay
- [x] Pre-founder scenes contain no selected player
- [ ] All planned sequences produced and activated
- [ ] Human review signs off Zach identity consistency across every scene

Run `pnpm story:check` and `pnpm test:e2e` before publishing a new playable build.

## Mandatory automated release gate

- [x] `pnpm build` runs `pnpm release:gate` before any workspace build can succeed
- [x] `pnpm test:e2e` runs the same release gate before browser gameplay tests begin
- [x] Required runtime PNG and MP3 files are checked for existence, minimum size, and valid file signatures
- [x] Implemented story order, visuals, player overlays, exact narration captions, shop tutorials, playable task guides, progression data, maps, and cross-references are checked
- [x] Any failed item prints an unchecked box and exits nonzero, blocking the build or E2E run
- [x] Planned future content stays visible above but does not masquerade as implemented or block the current playable build

Run `pnpm release:gate` directly for a fast production-readiness check.
