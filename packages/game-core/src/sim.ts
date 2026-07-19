import type { GameState, GameEvent, Tick } from "./types";
import { QuestEngine } from "./quests/engine";

/** Mulberry32 — tiny deterministic PRNG so saves replay identically server-side. */
export function rng(seed: number) {
  return function () {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function createGame(seed: number, mode: "arcade" | "shop"): GameState {
  return {
    seed, tick: 0, mode,
    player: { name: "Player", level: 1, xp: 0, coins: 500, reputation: 50, tier: 1,
      skills: { cnc_programming: 0, automation: 0, software_dev: 0, problem_solving: 0, communication: 0 } },
    bay: { id: "bay_01", machines: [] },
    staff: [], jobs: [], activeQuests: ["tut_01_first_cut"], completedQuests: [], eventLog: [],
  };
}

/** Player intents enter here; everything is logged for replay. */
export function dispatch(s: GameState, quests: QuestEngine, type: string, data?: Record<string, unknown>): GameState {
  const ev: GameEvent = { t: s.tick, type, data };
  s.eventLog.push(ev);
  quests.onEvent(s, ev);
  return s;
}

/** Advance the sim one tick. Pure-ish: mutates s in place, deterministic given seed+log. */
export function step(s: GameState, quests: QuestEngine): GameState {
  s.tick++;
  const rand = rng(s.seed ^ s.tick);
  for (const m of s.bay.machines) {
    if (m.state !== "running") continue;
    m.wearTicks++;
    // Breakdown chance scales with wear; reliability comes from the machine def at load time.
    if (rand() < 0.00005 * Math.sqrt(m.wearTicks)) {
      m.state = "alarm";
      dispatch(s, quests, "machine.alarm", { defId: m.defId });
    }
  }
  // TODO(cycle system): job routing, operator pathing, cycle completion events.
  return s;
}
