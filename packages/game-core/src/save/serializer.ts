import type { GameState } from "../types";

const SAVE_VERSION = 1;

/** Versioned save blob. Server replays eventLog against seed to validate leaderboards. */
export function serialize(s: GameState): string {
  return JSON.stringify({ v: SAVE_VERSION, state: s });
}

export function deserialize(blob: string): GameState {
  const parsed = JSON.parse(blob);
  if (parsed.v !== SAVE_VERSION) throw new Error(`Save version ${parsed.v} needs migration`);
  return parsed.state as GameState;
}
