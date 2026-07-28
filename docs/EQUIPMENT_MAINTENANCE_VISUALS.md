# Equipment Maintenance Visual Contract

The maintenance floor-art contract lives in `data/equipment-maintenance-visuals.json`. It covers every machine in `data/machines.json` plus the employee restroom facility station.

## State order

Every atlas uses the same four columns:

1. `available` — normal guarded operating condition.
2. `locked_out` — safely stopped with a visible fault beacon and lockout/tagout marker.
3. `service_in_progress` — powered down, service panel open, work area controlled with a cart and cones.
4. `restored` — panels closed with a green test-pass indicator.

Rows are declared explicitly in the manifest, so runtime code never guesses a machine's cell. The three transparent atlases cover Garage Bay machines, toolroom/digital infrastructure, automation, mobile robotics, and facility service.

## Honest gameplay status

- The VMC has a playable wear, lockout, qualified-technician, paid repair, test, and release loop. Its locked-out and restored floor states are runtime wired.
- The restroom has a playable report, isolate, qualified repair, sanitize, inspect, and reopen sequence.
- Remaining equipment has complete four-state floor art and maintenance definitions but is marked `visual_ready` or `orientation_only` until its failure mechanics are implemented.

## Adding equipment

Add the machine to `data/machines.json`, create or extend a four-state atlas, register it in `packages/assets/sprites/atlas.json`, add a manifest record with a real fault, preventive task, return-to-service check, and qualified roles, then qualify at least one maintenance hire in `data/hiring-roster.json`.

Run:

```powershell
pnpm maintenance:visuals:check
pnpm release:gate
```

The release gate fails if a machine lacks art, an atlas is not RGBA, the 4x4 dimensions are invalid, a row is out of bounds, or a declared maintenance role has no qualified hire.
