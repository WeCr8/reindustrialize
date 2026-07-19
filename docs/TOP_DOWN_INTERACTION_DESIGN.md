# Top-Down Interaction Design

The shop-floor loop should have the immediate readability associated with popular proximity-task games while remaining an original manufacturing RPG. Do not reproduce another game's characters, map layouts, terminology, interface art, sounds, story, or visual identity.

## Player loop

1. Read one achievable manufacturing objective.
2. Move around a readable top-down shop with keyboard, controller, touch, click-to-walk, or QR phone controls.
3. Approach the highlighted station; solid equipment and walls block movement.
4. Enter one-tile proximity and receive a pulsing **USE** highlight and control prompt.
5. Use the station with E, Space, Enter, Xbox A, touchscreen, or phone action.
6. Complete a focused production task, receive immediate validation, and return to the floor with the next route visible.

## Interaction rules

- Stations cannot be operated remotely.
- The nearest usable station is highlighted in green; the active objective remains highlighted in gold.
- A failed remote interaction teaches the player to move beside a station.
- Task overlays pause floor input so actions do not leak into movement.
- Every playable station provides clear success/failure feedback and advances or preserves the objective correctly.
- Movement and interaction behavior remains equivalent across supported control methods.
- Holding Shift or Xbox RT/left-stick-click runs; touchscreen and phone controls expose a run toggle. Click-to-walk uses the faster route pace.
- Running uses a faster two-frame cadence, stronger body bob, a slight directional lean, compressed shadow, motion streaks, and shop-floor dust accents so it reads differently from walking even with compact founder sprites.

## Automated acceptance

`tests/e2e_topdown_task_loop.py` proves collision, remote-use rejection, approach routing, proximity highlighting, Space-key interaction, and station opening. It runs automatically inside `pnpm test:e2e`.
