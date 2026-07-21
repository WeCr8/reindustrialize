# Station missions and production timers

The canonical station contract is `data/station-operations.json`. Every placement in both Garage Bay maps must have a name, honest implementation mode, mission, details, and standard cycle time. `scripts/validate-station-operations.mjs` blocks a release if coverage or the timer model drifts.

## Player interaction contract

- Clicking a station walks to and opens that exact station; an adjacent employee or machine may not steal the interaction.
- Playable stations open their task. Management and facility stations open their active controls. Unfinished workflows say `orientation only` and show their intended mission.
- Mission buttons are selectable. When a required prior step is missing, Zach explains it and the game routes to the next achievable station.
- Founder and factory text fields always keep keyboard input; gameplay shortcuts are inactive while typing.

## Timer contract

| Station | Standard cycle | Completion gate |
| --- | ---: | --- |
| Bandsaw | 5 minutes | Collect, identify, and route the blank |
| VMC | 10 minutes | Inspect and approve the finished part |

Timers use saved absolute start/end timestamps. They continue while the player explores, closes an overlay, reloads the browser, or resumes a local save. The factory floor, production HUD, station prompt, and station detail surface show remaining time or a clear completion flag. Additional equipment and qualified employees may reduce later cycle time only within declared limits.

The storybook contains a `Station Missions & Timers` section generated from the same contract, alongside its full graphics/audio catalog and missing-production queue.
