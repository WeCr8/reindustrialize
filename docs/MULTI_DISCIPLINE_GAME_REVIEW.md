# Multi-Discipline Game Review

Review date: 2026-07-19  
Reviewers: senior video game developer, senior narrative designer/game writer, manufacturing business owner/economy designer. Each reviewer inspected the repository independently before findings were consolidated.

## Shared conclusion

REINDUSTRIALIZE is accurately described as a strong first-playable alpha or coherent vertical slice. The Garage campaign has meaningful gameplay and unusually good asset/story/audio validation. It is not yet a complete six-chapter campaign, a full manufacturing-business simulation, or a production-ready online platform.

## What is working

- Garage-to-Job-Shop route, visible objectives, station interactions, material order, cutting, tool setup, true G/M-code exercises, CNC cycle, grading, customers, hiring, controls, audio, saves, pause, settings, and developer diagnostics.
- Strong Playwright coverage, startup budget, strict TypeScript, deterministic core tests, clean-checkout storybook generation, security guards, Git hooks, and passing hosted CI.
- Zach is consistently positioned as the player's mentor rather than owner of the player's company.
- The planned manufacturing-growth arc—from craftsmanship to people, systems, connectivity, automation, and institutional leadership—is strategically sound.

## P0 shared blockers

1. **One authoritative runtime:** The shipped game remains a large generated HTML runtime separate from typed `game-core`. Migrate toward typed modules and one save/economy/progression contract.
2. **Finish the promised slice:** Complete Chapter 1 inspection, disposition, shipping, Shop Class gate, first-customer follow-through, first hire, and facility-purchase decision through natural-play E2E.
3. **Author the campaign:** Chapter 2 needs a full conflict/recovery/graduation arc. Chapters 3–6 need entry, midpoint, crisis, recovery, graduation, move, and ending sequences tied to real mechanics.
4. **Build a real job economy:** Add quoting, cost estimates, material reservation/consumption, labor and machine cost, due dates, finite capacity, quality disposition, payroll, overhead, cash flow, and funded expansion.
5. **Harden saves:** Add schema validation, corruption recovery, migrations, backup snapshot, slots/export, and natural-progression restoration tests.
6. **Keep online claims honest:** Auth, cloud saves, replay validation, leaderboards, and production QR relay are currently prepared or local-only, not implemented production services.

## Game-developer findings

- Later campaign labels and data are not playable campaign completion.
- Several E2E tests verify labels or directly inject state; natural-play recovery, soak, malformed saves, and cross-browser/device coverage remain necessary.
- Accessibility still needs rebinding, remapping, dead zones, caption presentation, color-blind support, focus management, and a non-canvas information alternative.
- Production needs strict CSP-compatible architecture, telemetry consent, crash recovery, loading/error UX, offline/update behavior, backup restore, and rollback drills.
- Canonical status documents currently drift and must be generated from one machine-readable release manifest.

## Narrative findings

- Current runtime story contains three pre-founder, five founding-day, and three Job Shop transition beats; later arcs do not exist yet.
- Opening exposition repeats the company-growth promise and delays play. Reach a concrete inciting job within roughly three to five minutes.
- Split the 28-panel shop tour into just-in-time teaching clusters.
- Founder profiles need background, motivation, reactions, meaningful ability effects, and consequential decisions.
- Customers and workers need memory, relationships, conflict, aspirations, complaints, praise, and callbacks.
- Zach needs a campaign arc: teach, allow struggle, challenge assumptions, delegate mentorship, and complete a legacy handoff.
- Lock a narrative bible and Zach model/expression sheet before producing large batches of voice and scene variants.

Recommended pressure spine:

1. First Promise — cash runway and first verified shipment.
2. The Team Is the Machine — capacity, delegation, payroll, and handoffs.
3. Signals and Blind Spots — data, downtime, and root cause.
4. Automate the Standard — unstable process, trust, and safe validation.
5. Trust the Night — unattended reliability and disciplined recovery.
6. Build Beyond Yourself — strategic programs, leadership, apprentices, and legacy.

## Business findings

- Existing RFQs offer fixed prices; players cannot quote, counter, or reject based on estimated cost and capacity.
- Contract payout is effectively gross revenue treated as profit. Material, labor, overhead, rework, freight, and payroll are absent.
- F-grade work currently receives partial payment and ships automatically; failed work needs disposition, rework/scrap/customer approval, and corrective action.
- `dueShifts` has no active clock or late consequence.
- Hiring has an upfront fee but wages are not paid, qualifications do not materially affect production, and capacity does not constrain contract acceptance.
- Material delivery is nearly immediate and stock is not reserved or consumed by work order.
- Facility expansion ignores declared capital, relocation downtime, installation, working capital, and commissioning.
- Starting cash and chapter shipment gates conflict across runtime/core/progression files and require one authoritative economy model.

## Implementation sequence

1. Consolidate runtime, save, progression, and economy authority.
2. Complete Chapter 1 mechanics and narrative with natural E2E.
3. Add guided quoting and estimated-versus-actual job costing.
4. Add inventory reservation/consumption, shop clock, due dates, and finite capacity.
5. Add inspection disposition, payroll, overhead, P&L, and cash runway.
6. Complete Chapter 2 around concurrent profitable flow and team leadership.
7. Add save migrations/recovery and accessibility/input certification.
8. Add production QR/backend only through staging security tests.
9. Build Chapters 3–6 one complete mechanic-and-story arc at a time.
10. Finish browser/device certification, telemetry/privacy/support, backup restore, rollback, balance, and release sign-off.

The durable reviewer definitions and blocking criteria are in `data/review-agents.json`. Run `pnpm agents:review:check` to validate that the three independent review roles remain present.
