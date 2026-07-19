# Manufacturing and Human Realism Standard

The main campaign is a 25–35 hour game representing roughly 10–20 years of company growth; completionist contracts, mastery, team stories, and Easter eggs extend it to approximately 40–55 hours. Active player time is not wall-clock factory time. Setup, production, inspection, maintenance, hiring, training, supplier delivery, customer approval, payment, construction, and commissioning advance through explicit simulated calendar events. Chapters 1–2 teach through forgiving guided play; complex operating constraints phase in from Chapter 3 onward only after Zach demonstrates them.

The canonical numerical contract is [manufacturing-realism-contract.json](../data/manufacturing-realism-contract.json). It prevents the game from teaching that a person, machine, supplier, employee, or building responds instantly.

## Preserve the fun first

Chapter 1 remains a generous teaching chapter. It scores safe completion, quality, and process breadth. It does not gate the player on OEE, utilization, payroll, accounts receivable, management span, maintenance compliance, or commissioning. Zach demonstrates a concept before its first scored consequence, and every later recurring pressure receives a visible grace period.

Systems phase in one at a time:

| Chapter | Newly scored operating reality |
|---|---|
| 1 | Safe sequence, material identity, setup, first article, quality |
| 2 | Capacity calendar, due dates, supervised qualification, payroll, receivables |
| 3 | OEE context, downtime, preventive maintenance, multi-shift leadership |
| 4 | Automation commissioning, change control, capability, tool life |
| 5 | Unattended readiness, robot/AMR flow, escalation and recovery |
| 6 | Program finance, multi-building capacity, executive spans and talent pipeline |

## Time and people

- Standard shifts are eight hours; sustained work above 48 hours per person per week triggers a warning, and plans may not assume more than 60.
- New CNC jobs generally require hours of setup; repeats still require deliberate setup. First-article and lot inspection consume scheduled capacity.
- A hire is not instantly qualified. Orientation takes shifts, independent repeat work takes supervised repetitions, and setup/programming qualification may take 40–120 shifts.
- Frontline leaders normally span 5–10 people and managers 4–8 direct reports. After Chapter 3, the founder may not directly manage the whole organization.
- Key named roster gates are not total employment. The realism contract separately defines simulated per-shift site occupancy so a large facility is not represented as operating with a handful of people.

## Capacity, cash, and commissioning

- Healthy scheduled utilization is 65–85%, leaving capacity for variation, setup, inspection, maintenance, and recovery.
- OEE rises with process maturity but is never treated as a simple speed score or an automatic 100% target.
- Coins are not US dollars. The game teaches quote completeness, margin, payment timing, reserves, payroll cadence, supplier terms, and capital readiness using balanced ratios.
- Capital approval requires profitable demand, staffing, utilities, tooling, inspection, working capital, and a commissioning plan.
- Moves advance the calendar: a small move takes weeks, a plant expansion months, and a large campus program years. Installation, leveling, utilities, safety, calibration, training, first article, and ramp-up remain required even when compressed into playable decisions.

## Space planning

Every facility's interior square footage is fully allocated across:

- machines, guarding, operator zones and service clearance;
- pedestrian aisles, forklift travel and egress;
- raw material, WIP and finished inventory;
- receiving, shipping and docks;
- inspection and metrology;
- maintenance and toolroom;
- electrical, air, coolant, ventilation, network and plant support;
- offices, training and employee amenities;
- at least 10% expansion reserve.

Parking is recorded as exterior site capacity and is not counted inside building square footage. The validator requires aisle/flow space of at least 12%, at least 250 square feet of production zone per declared machine, enough shift occupancy to staff the machines, exterior parking for peak shift occupancy, and exact agreement with each facility's declared floor area.

## Recovery and ethics

Bad jobs, late payments, staffing gaps, and breakdowns create bounded consequences and mentored recovery choices. Players may renegotiate, schedule rework, stage investment, train, or accept lower-risk work. No single mistake silently compounds into an unrecoverable campaign. The game rewards safe, repeatable systems—not unpaid overtime, bypassed inspection, hidden defects, or 100% utilization.

Run the contract check with:

```powershell
node scripts/validate-manufacturing-realism.mjs
```
