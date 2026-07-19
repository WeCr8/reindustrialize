import type { GameState, GameEvent } from "../types";

interface QuestStep { event: string; filter?: Record<string, unknown>; count?: number }
interface QuestDef {
  id: string; type: string; tier: number; lesson: string;
  steps: QuestStep[];
  rewards: { coins?: number; xp?: number; unlock?: string; skillPoint?: string; badge?: string };
  zachIntro: string[]; zachOutro: string[];
}

/** Event-driven quest tracker. Data-only quests from data/quests.json. */
export class QuestEngine {
  private defs: Map<string, QuestDef>;
  private progress = new Map<string, number[]>(); // questId -> per-step counts

  constructor(defs: QuestDef[]) { this.defs = new Map(defs.map(d => [d.id, d])); }

  get(id: string) { return this.defs.get(id); }

  onEvent(s: GameState, ev: GameEvent) {
    for (const qid of [...s.activeQuests]) {
      const def = this.defs.get(qid); if (!def) continue;
      const prog = this.progress.get(qid) ?? def.steps.map(() => 0);
      const idx = prog.findIndex((c, i) => c < (def.steps[i]?.count ?? 1));
      if (idx === -1) continue;
      const stepDef = def.steps[idx];
      if (!stepDef) continue;
      if (stepDef.event !== ev.type) continue;
      if (stepDef.filter && !matches(stepDef.filter, ev.data ?? {})) continue;
      prog[idx] = (prog[idx] ?? 0) + 1;
      this.progress.set(qid, prog);
      if (prog.every((c, i) => c >= (def.steps[i]?.count ?? 1))) this.complete(s, def);
    }
  }

  private complete(s: GameState, def: QuestDef) {
    if (s.completedQuests.includes(def.id)) {
      s.activeQuests = s.activeQuests.filter(q => q !== def.id);
      return;
    }
    s.activeQuests = s.activeQuests.filter(q => q !== def.id);
    s.completedQuests.push(def.id);
    s.player.coins += def.rewards.coins ?? 0;
    s.player.xp += def.rewards.xp ?? 0;
    s.eventLog.push({ t: s.tick, type: "quest.completed", data: { id: def.id } });
  }
}

function matches(filter: Record<string, unknown>, data: Record<string, unknown>) {
  return Object.entries(filter).every(([k, v]) => data[k] === v);
}
