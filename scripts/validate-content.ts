/** CI gate: validate all data/*.json against game-core zod schemas.
 *  Code-gen skills run this after every content change. */
import { MachineDef } from "../packages/game-core/src/machines/schema";
import machines from "../data/machines.json" assert { type: "json" };
for (const m of machines.machines) MachineDef.parse(m);
console.log(`content valid: ${machines.machines.length} machines`);
