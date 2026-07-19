# Auth & Identity

## Goals
- One WeCr8 identity across wecr8.info and jobline.ai (game progress follows the player).
- Arcade playable **anonymously** — never gate the funnel entrance.
- Shop Mode requires a JobLine org session and maps player → org for the data bridge.

## Model
1. **Anonymous-first.** Arcade issues a device ID (localStorage-free? No — artifact-style
   embeds may restrict storage; use a signed anonymous JWT held in memory + cookie on
   our domain). Progress saves against the anon ID.
2. **Claim flow.** "Save your shop" prompt at Tier 2 → email or OAuth (Google/Microsoft)
   → anon progress merges into the account. This is the lead-capture moment.
3. **SSO across domains.** Central identity at `auth.wecr8.info` issuing short-lived JWTs
   (RS256). Both sites verify with the public JWKS. Silent SSO via top-level redirect
   (no third-party-cookie dependence).
4. **Shop Mode linkage.** JobLine session token exchanged at `/bridge/link` for a game JWT
   carrying `org_id` + `role`. Bridge endpoints authorize on `org_id`.

## Token claims
```json
{ "sub": "usr_…", "anon": false, "org_id": "org_…|null",
  "roles": ["player","org_member"], "iat": 0, "exp": 900 }
```

## Rules
- Refresh tokens httpOnly + SameSite=Lax, 30d, rotated on use.
- Bridge scope is read-only and org-scoped; leaderboard exposure is opt-in per org admin.
- COPPA posture: Arcade collects nothing without the claim flow; claim flow is 13+.
- Secrets never ship in `packages/*` or `apps/*`; server-only env.
