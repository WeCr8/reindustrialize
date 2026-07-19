# Chapters 2–6 Story and Difficulty Blueprint

This document is a production blueprint, not a claim of playable content. The canonical structured source is `data/story-production.json` under `campaignPlan`; progression gates remain canonical in `data/chapter-progression.json` and facility scale remains canonical in `data/facilities.json`.

Every later chapter must ship six narrative phases: entry, learn, prove, operate, recover, and graduate. Zach teaches principles, asks the founder to verify results, and helps interpret failure. The player remains the owner and makes every customer, hiring, capital, production, and leadership decision.

## Difficulty progression

| Chapter | Facility | Difficulty | Core escalation | Current truth |
|---|---|---|---|---|
| 2 | The Job Shop | Intermediate | Concurrent work, first team, inspection, payroll, cash | Entry is implemented; remaining arc is planned |
| 3 | Connected Plant | Advanced | Telemetry, OEE, bottlenecks, maintenance, multi-shift leadership | Planned |
| 4 | Smart Factory | Expert | Tool control, standards, fixtures, cobots, capability | Planned |
| 5 | Lights-Out Complex | Master | Unattended readiness, robot/AMR flow, reliability, recovery | Planned |
| 6 | American Titan Campus | Titan | Strategic programs, certified traceability, leaders, apprentices, legacy | Planned |

Difficulty rises through new decision domains, not inflated repetition. Each graduation combines volume, quality, delivery, process breadth, and organizational capability. Recovery beats teach the player to diagnose and correct a system instead of grinding duplicate jobs.

## Story production rules

- A planned storybook slide is visibly labeled `planned` and must not contain a finished-art path or voice ID.
- `audioNeeds` describes future approved writing and recording work; it is not an audio manifest entry.
- Chapter entry and graduation art must match the relevant facility scale and selected founder before activation.
- A planned beat becomes implemented only after its mechanic trigger, save persistence, selected-founder visual, exact caption/audio pair, and E2E path all pass.
- The storybook must contain entry, learn, prove, operate, recover, and graduate coverage for every chapter.

## Release validation

```powershell
node scripts/validate-story-production.mjs
python scripts/build-visual-storybook.py
python scripts/export-visual-storybook.py
node scripts/validate-visual-storybook.mjs
node scripts/validate-storybook-versioning.mjs
```

The detailed milestones, mechanic dependencies, future Zach guidance, graduation gates, and expansion needs are maintained in the structured campaign plan so future developers cannot mistake the roadmap for shipped gameplay.
