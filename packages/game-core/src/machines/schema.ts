import { z } from "zod";

/** Validates data/machines.json at build time. Code-gen skills must satisfy this. */
export const MachineDef = z.object({
  id: z.string(), name: z.string(),
  class: z.enum(["bench","saw","mill","vmc","lathe","infra","toolroom","robot"]),
  tier: z.number().int().min(1).max(6),
  inspiration: z.string(),
  footprint: z.tuple([z.number().int().positive(), z.number().int().positive()]),
  price: z.number().positive(), powerDraw: z.number().min(0),
  cycleSpeed: z.number().positive(),
  quality: z.number().min(0).max(1), reliability: z.number().min(0).max(1),
  requiresOperatorSkill: z.record(z.number().int().min(0).max(5)),
  automation: z.object({ cobotTendable: z.boolean(), mtconnect: z.boolean() }),
  spriteSpec: z.object({ sheet: z.string(), states: z.array(z.string()), frames: z.record(z.number()).optional() }),
  questHooks: z.array(z.string()),
  zachTip: z.string(),
}).refine(m => m.tier < 3 || m.automation.mtconnect, { message: "Tier 3+ machines must support MTConnect" })
  .refine(m => m.tier >= 5 || !["saw","mill","vmc","lathe","bench"].includes(m.class) || m.quality * m.reliability <= 0.97,
    { message: "quality*reliability > 0.97 reserved for tier 5+ production machines" });

export type MachineDefT = z.infer<typeof MachineDef>;
