/**
 * JobLine data bridge — Shop Mode only. READ-ONLY. Org-scoped by JWT org_id.
 * POST /bridge/link      — exchange JobLine session for game JWT with org_id
 * GET  /bridge/events    — poll real events mapped to game rewards:
 *    machine connected (MTConnect)  -> bridge.machine_connected
 *    clean shift handoff            -> bridge.handoff_completed
 *    weekly OEE improved            -> bridge.oee_improved
 * Implementation: consume jobline-mcp server tools; never write to customer systems.
 */
export {};
