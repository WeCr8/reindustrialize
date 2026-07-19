import { useCallback, useEffect } from "react";
import { serialize, deserialize, type GameState } from "@wecr8/game-core";
import { useAuth } from "./useAuth";

const AUTOSAVE_MS = 30_000;

/**
 * Cloud-first saves via server API (see server/src/routes/saves.ts).
 * NOTE: no localStorage — embeds may run in storage-restricted contexts; anonymous
 * players save against their anon JWT and merge on account claim.
 */
export function useSave(getState: () => GameState, apiBase: string) {
  const { token } = useAuth();

  const save = useCallback(async () => {
    if (!token) return; // anon token is still a token; null means auth not ready
    await fetch(`${apiBase}/saves`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: serialize(getState()),
    });
  }, [token, apiBase, getState]);

  const load = useCallback(async (): Promise<GameState | null> => {
    if (!token) return null;
    const res = await fetch(`${apiBase}/saves/latest`, { headers: { Authorization: `Bearer ${token}` } });
    if (!res.ok) return null;
    return deserialize(await res.text());
  }, [token, apiBase]);

  useEffect(() => {
    const id = setInterval(save, AUTOSAVE_MS);
    return () => clearInterval(id);
  }, [save]);

  return { save, load };
}
