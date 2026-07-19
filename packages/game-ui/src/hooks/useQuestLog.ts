import { useMemo } from "react";
import type { GameState, QuestEngine } from "@wecr8/game-core";

/** Feeds the TODAY'S MISSIONS panel and Zach's dialog box. */
export function useQuestLog(state: GameState, quests: QuestEngine) {
  return useMemo(() => {
    const active = state.activeQuests.map(id => quests.get(id)).filter(Boolean);
    const justCompleted = [...state.eventLog].reverse()
      .find(e => e.type === "quest.completed");
    return {
      missions: active.map(q => ({ id: q!.id, lesson: q!.lesson, type: q!.type })),
      zachSays: justCompleted
        ? quests.get(String(justCompleted.data?.id))?.zachOutro
        : active[0]?.zachIntro,
    };
  }, [state.activeQuests.length, state.eventLog.length]);
}
