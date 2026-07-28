# Industry Specialization Roadmap

REINDUSTRIALIZE should let the player decide what kind of manufacturer their company becomes, but that decision must be earned through play. This roadmap is planned content for Chapters 3–6; it is not selectable in the current alpha. The machine-readable source is [`data/industry-specializations.json`](../data/industry-specializations.json).

## The decision arrives at the right time

Chapters 1 and 2 remain a shared, family-friendly manufacturing education. Every founder quotes work, orders material, cuts stock, sets tools, learns real G/M code, inspects parts, maintains equipment, hires people, and keeps promises to customers. A child should not need to understand the difference between an aircraft OEM and an automotive supplier on the title screen.

In Chapter 3, JobLine offers pilot contracts from at least three sectors. Zach helps the founder compare enjoyment, margin, equipment fit, quality risk, workforce, facility space, and customer expectations. Chapter 4 asks the player to select a primary division and approve a visible capital plan. Chapter 5 builds the specialist departments and supply chain. Chapter 6 delivers the chosen sector's major program and ending.

The player may still accept compatible work outside the primary division. One pivot is allowed before the Chapter 5 scale investment, with clear retraining, requalification, relationship, and capital consequences. This prevents an early choice from permanently ruining a long save.

## Eight primary paths

| Path | Early credible work | Late-game aspiration | Signature factory change |
|---|---|---|---|
| Aircraft & Aerospace Systems | brackets, housings, tooling | aircraft shipsets and a prototype integration program | aerospace quality, NDT, large assembly |
| Spacecraft & Launch Systems | satellite and test hardware | launch-stage or orbital-platform shipsets | clean assembly, pressure test, cylindrical fabrication |
| Automotive & Mobility | prototype chassis and EV fixtures | specialty/commercial vehicle production | body shop, battery-safe assembly, end-of-line testing |
| Robotics & Factory Automation | bases, mounts, end effectors | turnkey robotic factories | controls lab, integration floor, acceptance hall |
| Energy & Power Systems | pumps, valves, turbine tooling | modular generation and grid systems | heavy machining, pressure test, skid assembly |
| Medical & Precision Devices | instruments and diagnostic housings | validated device families | clean cells, precision metrology, validation suite |
| Heavy Equipment & Agriculture | hydraulics, pins, weld fixtures | complete specialty machines | heavy weld/machining halls and durability course |
| Tools, Appliances & Durable Hardware | tool and appliance components | a national durable-goods product family | product lab, mixed-model assembly, reliability testing |

## One game, meaningfully different companies

The target content mix is 70% shared factory systems, 20% sector tailoring, and 10% signature content. All paths use JobLine, NOX, staffing, maintenance, quality, scheduling, facilities, cash, and the same readable controls. Tailoring changes contracts, customers, materials, processes, department modules, qualifications, failure stories, equipment recommendations, visuals, and Zach's business questions. Signature content supplies the capstone program and ending.

Complete jets, vehicles, launch stages, medical platforms, or heavy machines never appear as instant Garage projects. The company advances through components, subassemblies, shipsets, integration, validation, and finally complete products when its people, space, systems, suppliers, and capital make that scale believable.

## Required implementation bundle per path

Before any path can be called playable, it needs:

- Chapter 3 pilot contracts and market-fit scorecards
- Chapter 4 selection scene, Zach narration, capital plan, customer arc, and facility module
- Chapter 5 scale contracts, supplier and qualification pressures, major subassembly, recovery event, and department art
- Chapter 6 strategic program, capstone product, ending variant, postgame contracts, and storybook coverage
- sector customers, profiles, sprites, companies, equipment views, finished-product visuals, ambience, SFX, music accents, and exact narration captions
- bot E2E for choosing, pivoting, saving/re-entering, completing the capstone, and rejecting unavailable work honestly

No path may grant paid power, bypass common competency gates, or imply professional certification from a game lesson. Qualification content teaches purpose and workflow while remaining honest about real training and approvals.
