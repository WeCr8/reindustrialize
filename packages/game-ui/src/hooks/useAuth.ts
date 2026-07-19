import { createContext, useContext } from "react";

export interface AuthCtx {
  token: string | null;      // short-lived JWT (anon or claimed) — held in memory only
  user: { sub: string; anon: boolean; orgId: string | null } | null;
  claim: () => Promise<void>;   // opens the account-claim flow (lead capture moment)
  linkShop: () => Promise<void>; // Shop Mode: exchange JobLine session for org-scoped JWT
}

export const AuthContext = createContext<AuthCtx | null>(null);

export function useAuth(): AuthCtx {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider> from @wecr8/auth");
  return ctx;
}
