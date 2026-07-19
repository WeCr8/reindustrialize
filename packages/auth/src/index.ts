/**
 * Browser auth client for auth.wecr8.info (see docs/AUTH.md).
 * - boot(): fetch anon JWT if no session (silent SSO check first)
 * - claim(): redirect flow -> email/OAuth -> merges anon progress
 * - linkShop(): jobline.ai only -> POST /bridge/link with JobLine session
 * Tokens are RS256, verified server-side via JWKS. Never persisted to storage;
 * refresh handled via httpOnly cookie on our domains.
 */
export async function boot(authBase: string): Promise<string> {
  const res = await fetch(`${authBase}/session`, { credentials: "include" });
  if (res.ok) return (await res.json()).token;
  const anon = await fetch(`${authBase}/anon`, { method: "POST", credentials: "include" });
  return (await anon.json()).token;
}
