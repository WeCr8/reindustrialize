# Robotics and Factory-Logistics Progression

Robots solve travel and handling problems after the factory is large enough to have those problems. They do not replace process knowledge, qualified people, safe routes, or maintenance.

## Facility growth

| Chapter | Facility shape | Material-flow lesson | Robotics allowance |
| --- | --- | --- | --- |
| 1 | Shared Garage work zones | The founder can safely move each labeled job by hand. | None |
| 2 | Compact Job Shop with marked zones | Repeated trips between receiving, preparation, machines, inspection, and shipping can become a small bottleneck. | One fixed-route tugger AGV; 300 sq ft total logistics allowance |
| 3 | Connected Plant with separate departments | WIP travels between receiving, material prep, machining, fabrication, inspection, assembly, and shipping. | Capped AMR fleets; 1,800 sq ft allowance |
| 4 | Smart Factory with automated departments | Heavy fixtures and WIP need validated digital handoffs and safe docking. | Capped heavy mobile platforms; 6,000 sq ft allowance |
| 5 | Multiple production halls | Night operation needs maintained routes, charging, recovery drills, and human exception ownership. | Broader AMR/cobot operation; 18,000 sq ft allowance |
| 6 | Multi-building campus | Assistance must remain supervised and task-specific across a large organization. | At most two humanoid pilots; 50,000 sq ft campus allowance |

## Catalog ladder

- **Starter Tugger AGV — Chapter 2, 22,000 coins, cap 1.** Carries one cart on a painted route. Requires five employees, a material handler, a maintenance technician, four open work zones, 140 sq ft for charging/cart parking, and a reviewed pedestrian crossing.
- **AMR WIP Fleet — Chapter 3, 78,000 coins per first fleet, cap 3.** Moves labeled WIP among seven separate departments. It requires logistics, manufacturing-engineering, and maintenance coverage, 420 sq ft per fleet, a traffic map, crossing review, and a manual recovery plan.
- **Heavy Mobile Robot Platform — Chapter 4, 165,000 coins, cap 4.** Moves fixtures and heavy WIP only between validated docks. It requires automation, engineering, and maintenance roles, 650 sq ft per platform, approved heavy-load routes, machine interlocks, and recovery planning.
- **Supervised Humanoid Assistant — Chapter 6, 285,000 coins, cap 2.** Performs approved non-hazardous kitting, paperwork, and maintenance-parts delivery beside trained people. It may not replace a qualified operator, make independent quality dispositions, or enter hazardous work alone.

Repeat purchases retain the store's escalating-price rule. Every purchase must recheck job progress, current facility, remaining logistics space, headcount, named roles, operational departments, safety approvals, maintenance coverage, cash, and the fleet cap.

## Young-player language

Each robotics card answers three questions in short sentences:

1. **What does it carry?** A labeled cart, WIP, a fixture, or approved supplies.
2. **Where does it go?** The named department route shown on the card.
3. **Who stays responsible?** A trained person always owns loading, priorities, exceptions, recovery, and maintenance.

AGV means a robot that follows a fixed marked route. AMR means a robot that can choose among approved aisles. The game should introduce those plain-language meanings before using the initials alone.

## Workforce fit

The existing roster already models assignment qualifications separately from general skill ratings. That is correct: a high automation score does not qualify a worker for every robot or station. The catalog therefore uses canonical roster role IDs for its named-role gates:

- Andre Wilson (`material_handler`) supports the starter tugger route.
- Marcus Reed (`maintenance_technician`) is required for every mobile-robot purchase.
- Owen Price (`shipping_receiving`) and Noah Kim (`manufacturing_engineer`) support the Connected Plant AMR fleet.
- Tessa Morgan (`automation_technician`) unlocks only at the Smart Factory and is therefore required for the heavy platform and later humanoid pilot, not the early tugger.

Future playable robotics assignments must be added to each candidate's `qualifications` list before the UI offers that assignment. Catalog role readiness must never silently grant a station qualification.
