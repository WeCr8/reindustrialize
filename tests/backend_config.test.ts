import assert from "node:assert/strict";
import test from "node:test";
import { readBackendConfig } from "../packages/backend/src/config";

test("cloud backend remains safely disabled by default", () => {
  assert.deepEqual(readBackendConfig({}), {mode:"disabled",enabled:false});
  assert.deepEqual(readBackendConfig({PUBLIC_BACKEND_MODE:"supabase",PUBLIC_CLOUD_FEATURES_ENABLED:"false"}), {mode:"disabled",enabled:false});
});

test("browser backend accepts only HTTPS and modern publishable keys", () => {
  const config=readBackendConfig({PUBLIC_BACKEND_MODE:"supabase",PUBLIC_CLOUD_FEATURES_ENABLED:"true",PUBLIC_SUPABASE_URL:"https://example.supabase.co",PUBLIC_SUPABASE_PUBLISHABLE_KEY:"sb_publishable_example_for_test_only"});
  assert.equal(config.enabled,true);
  assert.throws(()=>readBackendConfig({PUBLIC_BACKEND_MODE:"supabase",PUBLIC_CLOUD_FEATURES_ENABLED:"true",PUBLIC_SUPABASE_URL:"http://example.supabase.co",PUBLIC_SUPABASE_PUBLISHABLE_KEY:"sb_publishable_example_for_test_only"}),/HTTPS/);
  assert.throws(()=>readBackendConfig({PUBLIC_BACKEND_MODE:"supabase",PUBLIC_CLOUD_FEATURES_ENABLED:"true",PUBLIC_SUPABASE_URL:"https://example.supabase.co",PUBLIC_SUPABASE_PUBLISHABLE_KEY:"sb_secret_never"}),/publishable/);
});

test("privileged Supabase values are rejected even while cloud features are disabled", () => {
  for(const key of ["SUPABASE_SERVICE_ROLE_KEY","SUPABASE_SECRET_KEY","SUPABASE_SECRET_KEYS","SUPABASE_DB_URL"]){
    assert.throws(()=>readBackendConfig({[key]:"test-secret"}),/must never enter browser/);
  }
});
