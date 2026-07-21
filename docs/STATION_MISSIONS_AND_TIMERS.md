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

Timers use saved absolute start/end timestamps. They continue while the player explores, closes an overlay, reloads the browser, or resumes a local save. The factory floor, production HUD, station prompt, and station detail surface show remaining time or a clear completion flag.

The founder-run VMC uses a short RPG-first setup: secure the stock, confirm the tool, and start the timed simulation. True G/M code is available as optional Shop Class material and does not gate the base campaign.

## Worker production contract

- Only the mechanically playable bandsaw and VMC accept unattended production queues. Orientation-only stations never mint generic work or rewards.
- A queued batch must reference the active customer work order and ordered material, and its assigned employee must be qualified for that exact station.
- Each installed machine adds a parallel lane with a fixed standard cycle; it does not unrealistically accelerate one part. Each lane may hold three committed batches.
- Bandsaw collection creates prepared work-in-process blanks. A worker VMC batch consumes one collected blank and a verified tool kit, then creates finished output inventory.
- Busy workers remain reserved until their committed production has completed. Queue IDs, workers, stations, timestamps, slots, rewards, work order, and WIP are validated during local-save recovery.

The storybook contains a `Station Missions & Timers` section generated from the same contract, alongside its full graphics/audio catalog and missing-production queue. The full fourteen-stop Shop Tour is optional and replayable; the campaign teaches starter stations in context as the player reaches real work.
