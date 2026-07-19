import { useEffect, useRef, useState, useCallback } from "react";
import { createGame, step, dispatch, QuestEngine, type GameState } from "@wecr8/game-core";

const TICK_MS = 1000;

/** Owns the sim loop. One instance per mounted game. */
export function useGameState(mode: "arcade" | "shop", questDefs: any[], seed = Date.now() & 0xffff) {
  const questsRef = useRef(new QuestEngine(questDefs));
  const stateRef = useRef<GameState>(createGame(seed, mode));
  const [, force] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      step(stateRef.current, questsRef.current);
      force(n => n + 1);
    }, TICK_MS);
    return () => clearInterval(id);
  }, []);

  const act = useCallback((type: string, data?: Record<string, unknown>) => {
    dispatch(stateRef.current, questsRef.current, type, data);
    force(n => n + 1);
  }, []);

  return { state: stateRef.current, act, quests: questsRef.current };
}
