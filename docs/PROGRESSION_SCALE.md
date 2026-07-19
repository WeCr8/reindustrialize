# Player Progression and Chapter Graduation Scale

This is the progression source of truth for the campaign. Machine and quest definitions may add detail, but they must not allow a player to skip these competency gates. The machine-readable companion is [`data/chapter-progression.json`](../data/chapter-progression.json).

## Progression philosophy

The player is building a manufacturing company, not clearing a sequence of disconnected minigames. Advancement must prove four things:

1. **Breadth:** the player completed different kinds of manufacturing work.
2. **Quality:** the work met a rising grade standard.
3. **Process:** the shop can repeat the result through planning, tooling, inspection, maintenance, and delivery.
4. **Organization:** the company has the people, systems, and financial strength required by the next facility.

XP alone never unlocks a chapter. Production volume alone never unlocks a facility.

## Thirty-level campaign

The campaign has 30 levels, five per chapter. Each chapter repeats a readable learning rhythm:

| Phase | Level within chapter | Player experience |
|---|---:|---|
| Orient | 1 | Enter the new facility, understand its pressure, and meet the new system. |
| Learn | 2 | Complete guided tasks with Zach explaining why. |
| Prove | 3 | Perform the skill with fewer prompts and pass a graded challenge. |
| Operate | 4 | Combine the skill with production, people, quality, and cash pressure. |
| Graduate | 5 | Complete a multi-system capstone and satisfy the facility move gate. |

Recommended XP curve: `round(750 × level^1.35)` for the next level. Filling the XP bar makes the player eligible; completing the phase competency grants the level.

## Campaign scale

| Chapter | Levels | Target time | Facility | Required production | Core graduation standard |
|---|---:|---:|---|---:|---|
| 1. Founder and Apprentice | 1–5 | 0.5–0.75 h | Garage Bay | 5 jobs | C average, three job families, certified material, one lesson |
| 2. From Craftsperson to Team | 6–10 | 1.5–2 h | Job Shop | 8 chapter jobs | B average, 85% on time, three staff, concurrency and inspection |
| 3. Manage What You Cannot See | 11–15 | 1.5–2 h | Connected Plant | 10 chapter jobs | B average, 88% on time, connected machines, OEE and recovery |
| 4. Standardize and Automate | 16–20 | 2–2.25 h | Smart Factory | 12 chapter jobs | B+ average, 90% on time, controlled tools, handoffs and cells |
| 5. Reliability at Industrial Scale | 21–25 | 2–2.5 h | Lights-Out Complex | 14 chapter jobs | B+ average, 92% on time, under 3% scrap and reliable nights |
| 6. Build the Institution | 26–30 | 2.5–3 h | Titan Campus | 16 chapter jobs | A- average, 95% on time, strategic programs and developed leaders |

The intended main campaign is a focused console-adventure length of approximately **10–12 hours**. Optional contracts, mastery grades, hidden interactions, team stories, and Easter eggs extend a thorough playthrough to approximately **16–20 hours** without making repetition a graduation requirement.

## Easter egg scale

Target **24 discoverable Easter eggs** across the six chapters: three visible environmental secrets and one deeper multi-step secret per facility. Rewards should be original and manufacturing-themed—hidden Zach shop sayings, unusual machine animations, prototype parts, founder cosmetics, historic manufacturing references, secret NOX shipments, and a final mentor-room reveal. Discovery may grant cosmetics, lore, music, or modest coins, but never competency-gate progress or paid power.

Each chapter should also contain one optional secret route or interaction chain that takes roughly 10–20 minutes to solve. The chapter menu records silhouettes rather than solutions so completion-minded players know secrets exist without spoiling them.

## Chapter 1 playable sequence

Chapter 1 now requires more than the tutorial part:

1. Name and launch the company.
2. Order certified 6061-T6 stock through NOX Metals.
3. Accept five customer jobs and cut each raw blank to its traveler length at the bandsaw.
4. Prepare a three-tool CNC kit for every job: primary cutter, touch probe, and chamfer tool.
5. Prove the G/M-code, run, grade, and ship each part.
6. Complete all three introductory job families: drilling, pocketing, and 3D finishing.
7. Maintain at least a C quality average.
8. Complete the alloy-identification Shop Class lesson when that lesson UI is enabled.
9. Review the Garage graduation summary and move into the Job Shop.

The current playable build enforces the material order, five shipments, and quality average. Distinct-family and Shop Class enforcement remain documented implementation requirements until those systems are connected to the viewer.

## Difficulty ramp

- Chapters 1–2 teach controls and direct production decisions.
- Chapter 3 reduces handholding and shifts attention from individual machines to plant signals.
- Chapter 4 asks the player to design repeatable systems before automating them.
- Chapter 5 tests reliability through unattended operation and recovery.
- Chapter 6 tests leadership, customer trust, capital allocation, and knowledge transfer.

Zach’s assistance should taper across the phases: full explanation during Orient/Learn, optional hints during Prove, exception-only coaching during Operate, and a graduation review during the capstone.

## Anti-grind and recovery

- After three jobs from the same family in one chapter, additional copies provide money but reduced mastery credit.
- A D or F routes the player to a relevant lesson and a recovery job.
- Failure never deletes the company or permanently blocks the story.
- Facility gates display every unmet requirement and the closest actionable way to improve it.
- Optional stretch contracts provide money, reputation, cosmetics, and leaderboards without becoming mandatory campaign padding.
