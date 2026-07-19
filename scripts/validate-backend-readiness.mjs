import { readFile } from "node:fs/promises";

const required = [
  ["data/backend-options.json", ["\"defaultMode\": \"disabled\"", "\"cloudFeaturesEnabled\": false"]],
  ["supabase/migrations/20260718000100_accounts_and_saves.sql", ["enable row level security", "auth.uid()", "revoke all", "pg_column_size(state)"]],
  ["packages/backend/src/config.ts", ["PUBLIC_CLOUD_FEATURES_ENABLED", "SUPABASE_SERVICE_ROLE_KEY"]],
];
for (const [file, markers] of required) {
  const text = await readFile(file, "utf8");
  for (const marker of markers) if (!text.includes(marker)) throw new Error(`${file} is missing security marker: ${marker}`);
}
const example = await readFile(".env.example", "utf8");
if (/SUPABASE_(SERVICE_ROLE|SECRET)_KEY\s*=/.test(example)) throw new Error("Do not place privileged Supabase key fields in the browser-facing environment template.");
if (!example.includes("PUBLIC_BACKEND_MODE=disabled") || !example.includes("PUBLIC_CLOUD_FEATURES_ENABLED=false")) throw new Error("Cloud backend must remain disabled by default.");
console.log("PASS: backend disabled; portable schema, RLS, and secret boundaries present");
