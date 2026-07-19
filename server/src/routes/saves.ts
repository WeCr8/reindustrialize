/**
 * POST /saves        — store save blob; enqueue replay validation (anti-cheat)
 * GET  /saves/latest — latest save for the authed subject (anon or claimed)
 * Replay validation: re-run game-core sim with seed + eventLog; reject if final
 * coins/xp diverge from the submitted state. Deterministic sim makes this cheap.
 */
export {};
