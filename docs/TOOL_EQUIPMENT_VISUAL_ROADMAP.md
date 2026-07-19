# Tool and Equipment Visual Roadmap

Status date: 2026-07-19

## Implemented now

- Twist drill: large selection view and matching atlas sprite.
- Flat end mill: large selection view and matching atlas sprite.
- Ball nose end mill: large selection view and matching atlas sprite.
- Touch probe: tool-kit inspection image and matching compact sprite.
- Chamfer mill: tool-kit inspection image and matching compact sprite.
- Stickout task: displays the selected cutter beside the length control and explains the holder-face-to-tip measurement.

The same transparent HD-2D source atlases serve both inspection and compact UI views so silhouettes cannot drift between screens.

## Next playable-task assets

1. Toolholder family: ER collet chuck, hydraulic holder, shell-mill arbor, drill chuck.
2. Length-setting equipment: height presetter, gauge line, spindle taper, retention knob, and offset readout states.
3. Cutting-tool wear states: new, usable, chipped, built-up edge, and broken.
4. Drilling family: spot drill, jobber drill, carbide drill, center drill, reamer, and tap.
5. Milling family: roughing end mill, finishing end mill, face mill, corner-radius mill, thread mill, and engraving tool.
6. Turning family: OD holder, boring bar, grooving tool, cutoff blade, threading tool, and live-tool holder.

## Equipment views required by progression

- Garage Bay: bandsaw clamp and stop close-up; VMC spindle/toolchanger; vise and work-offset probing; deburr tools; caliper and micrometer inspection.
- Job Shop: lathe chuck/turret setup; tool presetter; modular fixturing; CMM probe and datum setup; wash and shipping stations.
- Connected Plant: RFID tool crib; worn-tool replacement; maintenance inspection points; connected-machine status hardware.
- Smart Factory and later: pallet pool, robot grippers, cobot end effectors, AMR load interfaces, automated inspection, and lights-out recovery hardware.

## Production rules

- Large view: technically readable at 700-pixel panel width.
- UI sprite: readable at approximately 48×80 CSS pixels.
- Style: crisp 32-bit HD-2D pixel art, cool steel, industrial teal reflection, restrained gold highlights.
- Every tool must have a distinct working-end silhouette.
- No tool is marked playable until its image, compact sprite, instructions, narration, validation state, and E2E interaction are present.
