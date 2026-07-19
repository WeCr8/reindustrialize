# Full Campaign Completion Matrix

This is the release-truth checklist for Chapters 1–6. A working opening chapter, a successful Garage-to-Job-Shop bot run, or a rendered marketing video is not proof of a complete game.

The machine-readable source is `data/full-campaign-completion.json`. Each chapter must provide passing evidence in all seven categories:

| Chapter | Current status | Gameplay | Bot/E2E | Story | Audio | Visuals | Facility | Difficulty |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 — First Promise | Playable alpha | Complete | Complete | Partial | Partial | Partial | Complete | Partial |
| 2 — The Team Is the Machine | Arrival only | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| 3 — Signals and Blind Spots | Planned | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| 4 — Automate the Standard | Planned | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| 5 — Trust the Night | Planned | Missing | Missing | Missing | Missing | Missing | Missing | Missing |
| 6 — Build Beyond Yourself | Planned | Missing | Missing | Missing | Missing | Missing | Missing | Missing |

Detailed chapter requirements live in the JSON so automation and documentation share one source of truth.

## Gates

Validate that the matrix remains complete and honest during alpha development:

```powershell
node scripts/validate-full-campaign.mjs
```

The command passes when the checklist is structurally valid, even while work is unfinished. Before any `1.0`, “full campaign,” or “complete game” claim, run:

```powershell
node scripts/validate-full-campaign.mjs --assert-1.0
```

That command intentionally fails today. It succeeds only when all 42 chapter/category proof records are `complete`, their evidence is present, the product version is `1.0`, and `fullCampaignClaimAllowed` is true.

## Evidence standard

- Gameplay proof must exercise mechanics, failure, recovery, save/reload, and graduation—not only open a screen.
- Automation proof must use visible player inputs and must not teleport or mutate progress directly.
- Story proof includes beginning, escalation, consequence, callbacks, graduation, and transition.
- Audio proof includes dialogue, captions/text agreement, equipment sequencing, ambience, mixing, opt-out, and audible browser E2E.
- Visual proof covers every selectable founder, recurring character, station state, facility, and story variant.
- Facility proof requires a meaningfully new playable production system, not a background swap.
- Difficulty proof documents the mastery curve and verifies that progression is neither grind-only nor blocked by hidden rules.

Production deployment is a separate final gate. A full-campaign claim also requires the exact deployed version to pass the clean-install bot, landing-to-ending E2E, asset checks, and live URL verification.
