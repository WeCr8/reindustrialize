import { z } from "zod";
import type { GameState } from "../types";

export const SAVE_VERSION = 1;

const nonNegativeInt = z.number().int().nonnegative().finite();
const skillSchema = z.object({
  cnc_programming: nonNegativeInt,
  automation: nonNegativeInt,
  software_dev: nonNegativeInt,
  problem_solving: nonNegativeInt,
  communication: nonNegativeInt,
}).passthrough();

const playerSchema = z.object({
  name: z.string().trim().min(1).max(80),
  avatarId: z.string().trim().min(1).max(120),
  accentColor: z.string().regex(/^#[0-9a-f]{6}$/i).optional(),
  level: z.number().int().min(1),
  xp: nonNegativeInt,
  coins: nonNegativeInt,
  skills: skillSchema,
  reputation: z.number().min(0).max(100).finite(),
  tier: z.union([z.literal(1), z.literal(2), z.literal(3), z.literal(4), z.literal(5), z.literal(6)]),
}).passthrough();

const machineSchema = z.object({
  defId: z.string().min(1),
  pos: z.tuple([z.number().finite(), z.number().finite()]),
  state: z.enum(["idle", "running", "alarm", "setup", "off"]),
  connected: z.boolean(),
  live: z.boolean().optional(),
  tendedBy: z.string().min(1).optional(),
  gcodeCleared: z.boolean(),
  wearTicks: nonNegativeInt,
}).passthrough();

const jobSchema = z.object({
  id: z.string().min(1),
  part: z.string().min(1),
  qty: z.number().int().positive(),
  done: nonNegativeInt,
  scrapped: nonNegativeInt,
  route: z.array(z.string().min(1)),
  payout: nonNegativeInt,
  dueTick: nonNegativeInt,
  status: z.enum(["open", "wip", "shipped", "late", "rejected"]),
}).passthrough().refine(job => job.done + job.scrapped <= job.qty, {
  message: "completed and scrapped quantities cannot exceed job quantity",
});

const eventSchema = z.object({
  t: nonNegativeInt,
  type: z.string().min(1),
  data: z.record(z.unknown()).optional(),
}).passthrough();

export const gameStateSchema = z.object({
  seed: z.number().int().finite(),
  tick: nonNegativeInt,
  mode: z.enum(["arcade", "shop"]),
  player: playerSchema,
  bay: z.object({ id: z.string().min(1), machines: z.array(machineSchema) }).passthrough(),
  staff: z.array(z.string().min(1)),
  jobs: z.array(jobSchema),
  activeQuests: z.array(z.string().min(1)),
  completedQuests: z.array(z.string().min(1)),
  eventLog: z.array(eventSchema),
}).passthrough().superRefine((state, context) => {
  for (const field of ["staff", "activeQuests", "completedQuests"] as const) {
    if (new Set(state[field]).size !== state[field].length) {
      context.addIssue({ code: z.ZodIssueCode.custom, path: [field], message: "entries must be unique" });
    }
  }
  const completed = new Set(state.completedQuests);
  if (state.activeQuests.some(id => completed.has(id))) {
    context.addIssue({ code: z.ZodIssueCode.custom, path: ["activeQuests"], message: "completed quests cannot remain active" });
  }
  if (state.eventLog.some(event => event.t > state.tick)) {
    context.addIssue({ code: z.ZodIssueCode.custom, path: ["eventLog"], message: "events cannot occur after the current tick" });
  }
});

type SaveEnvelope = { v: number; state: unknown };
type Migration = (envelope: SaveEnvelope) => SaveEnvelope;

// Add one deterministic vN -> vN+1 function whenever SAVE_VERSION advances.
const migrations: Readonly<Record<number, Migration>> = {
  0: envelope => ({ v: 1, state: envelope.state }),
};

/** Upgrade a parsed legacy envelope without weakening validation of its state. */
export function migrateSave(envelope: SaveEnvelope): SaveEnvelope {
  if (!Number.isInteger(envelope.v) || envelope.v < 0) throw new Error("Save version is invalid");
  if (envelope.v > SAVE_VERSION) throw new Error(`Save version ${envelope.v} needs migration`);
  let current = envelope;
  while (current.v < SAVE_VERSION) {
    const migrate = migrations[current.v];
    if (!migrate) throw new Error(`Save version ${current.v} needs migration`);
    current = migrate(current);
  }
  return current;
}

/** Versioned save blob. Server replays eventLog against seed to validate leaderboards. */
export function serialize(state: GameState): string {
  const validated = gameStateSchema.parse(state);
  return JSON.stringify({ v: SAVE_VERSION, state: validated });
}

export function deserialize(blob: string): GameState {
  let raw: unknown;
  try { raw = JSON.parse(blob); }
  catch { throw new Error("Save data is not valid JSON"); }

  if (typeof raw !== "object" || raw === null || !("v" in raw) || !("state" in raw)) {
    throw new Error("Save data is missing its version or state");
  }
  const envelope = z.object({ v: z.number(), state: z.unknown() }).passthrough().safeParse(raw);
  if (!envelope.success) throw new Error("Save data is missing its version or state");
  const migrated = migrateSave(envelope.data as SaveEnvelope);
  const state = gameStateSchema.safeParse(migrated.state);
  if (!state.success) {
    const issue = state.error.issues[0];
    const location = issue?.path.length ? issue.path.join(".") : "state";
    throw new Error(`Save data is corrupt at ${location}: ${issue?.message ?? "invalid value"}`);
  }
  return state.data as GameState;
}
