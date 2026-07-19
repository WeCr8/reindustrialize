export type BackendMode = "disabled" | "local" | "supabase" | "lovable-supabase";

export interface BackendConfig {
  mode: BackendMode;
  enabled: boolean;
  supabaseUrl?: string;
  publishableKey?: string;
}

/** Browser-safe configuration only. A service-role key is never accepted here. */
export function readBackendConfig(env: Record<string, string | undefined>): BackendConfig {
  const mode = (env.PUBLIC_BACKEND_MODE || "disabled") as BackendMode;
  if (!["disabled", "local", "supabase", "lovable-supabase"].includes(mode)) throw new Error(`Unsupported backend mode: ${mode}`);
  const enabled = env.PUBLIC_CLOUD_FEATURES_ENABLED === "true";
  if (!enabled || mode === "disabled") return { mode: "disabled", enabled: false };
  const supabaseUrl = env.PUBLIC_SUPABASE_URL;
  const publishableKey = env.PUBLIC_SUPABASE_PUBLISHABLE_KEY;
  if (!supabaseUrl?.startsWith("https://") && mode !== "local") throw new Error("A production backend requires an HTTPS Supabase URL.");
  if (!supabaseUrl || !publishableKey) throw new Error("Enabled cloud features require a Supabase URL and publishable key.");
  if ("SUPABASE_SERVICE_ROLE_KEY" in env) throw new Error("A service-role key must never enter browser configuration.");
  return { mode, enabled, supabaseUrl, publishableKey };
}
