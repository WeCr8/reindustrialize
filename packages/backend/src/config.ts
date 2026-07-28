export type BackendMode = "disabled" | "local" | "supabase" | "lovable-supabase";

export interface BackendConfig {
  mode: BackendMode;
  enabled: boolean;
  supabaseUrl?: string;
  publishableKey?: string;
}

/** Browser-safe configuration only. A service-role key is never accepted here. */
export function readBackendConfig(env: Record<string, string | undefined>): BackendConfig {
  const forbidden = ["SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_SECRET_KEY", "SUPABASE_SECRET_KEYS", "SUPABASE_DB_URL"];
  const leaked = forbidden.find(key => env[key]);
  if (leaked) throw new Error(`${leaked} must never enter browser configuration.`);
  const mode = (env.PUBLIC_BACKEND_MODE || "disabled") as BackendMode;
  if (!["disabled", "local", "supabase", "lovable-supabase"].includes(mode)) throw new Error(`Unsupported backend mode: ${mode}`);
  const enabled = env.PUBLIC_CLOUD_FEATURES_ENABLED === "true";
  if (!enabled || mode === "disabled") return { mode: "disabled", enabled: false };
  const supabaseUrl = env.PUBLIC_SUPABASE_URL;
  const publishableKey = env.PUBLIC_SUPABASE_PUBLISHABLE_KEY;
  if (!supabaseUrl || !publishableKey) throw new Error("Enabled cloud features require a Supabase URL and publishable key.");
  let url: URL;
  try { url = new URL(supabaseUrl); } catch { throw new Error("Supabase URL is invalid."); }
  if (mode !== "local" && (url.protocol !== "https:" || url.username || url.password)) throw new Error("A production backend requires an HTTPS Supabase URL without credentials.");
  if (/^(sb_secret_|eyJ)/.test(publishableKey) || !publishableKey.startsWith("sb_publishable_")) throw new Error("Browser configuration requires an sb_publishable_ key, never a secret or legacy service-role key.");
  return { mode, enabled, supabaseUrl, publishableKey };
}
