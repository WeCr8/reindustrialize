# Facility Amenities and Maintenance Events

Facility care begins in Chapter 2, after the forgiving Garage chapter. The Job Shop introduces an employee restroom as an orientation-only amenity station. Later facilities inherit this system as their teams and buildings grow.

The first planned incident is a rare restroom service interruption. It is workplace-management teaching, not gross-out humor: no graphic imagery, embarrassing dialogue, or surprise during onboarding or machine-safety sequences. Zach explains that maintaining the workplace is part of protecting the team.

The correct response is always ordered and visible:

1. Isolate the affected restroom.
2. Post an out-of-service sign and direct employees to another available restroom.
3. Assign a maintenance or facilities worker qualified for the restroom station to clear the blockage safely.
4. Clean and sanitize the area.
5. Inspect, document, and reopen only after normal operation is verified.

The event temporarily makes the station unavailable and reduces morale by 2. Correct resolution costs 450 coins and restores availability with 1 morale recovered. Ignoring it for a simulated shift increases the cost to 900 coins, reduces morale by 6, and leaves the station unavailable. An unqualified worker cannot perform the corrective step.

The canonical event definition is [facility-amenity-events.json](../data/facility-amenity-events.json). The Job Shop location is declared in [bay_02.json](../data/maps/bay_02.json). Runtime mechanics, art, audio, and narration remain explicitly orientation-only until implemented and validated; the data must not imply that the event is already playable.
