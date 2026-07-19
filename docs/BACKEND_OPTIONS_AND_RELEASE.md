# Backend Options and Controlled Release

Status: **prepared, not enabled**. The game must continue to run without an account or network backend until the release gate is approved.

## Available paths

| Mode | Best use | Ownership and tradeoff |
|---|---|---|
| `disabled` | Current gameplay testing | No cloud dependency; safest while the save format and gameplay are changing. |
| `local` | Developer auth, RLS, migration, and save tests | Reproducible Supabase CLI stack. Development only; it has default credentials, no TLS, and no production hardening. |
| `supabase` | Direct production backend | Maximum infrastructure control and portability. The team owns Auth configuration, migrations, monitoring, backups, and incident response. |
| `lovable-supabase` | Lovable-assisted UI and account flows | Fast UI iteration while retaining the same Supabase tables and RLS. Review every generated migration and security change before applying it. |

Lovable and direct Supabase are not separate database designs here. Both consume the committed `supabase/migrations` contract, which prevents the game from becoming locked to a generated frontend.

## Data prepared

- `profiles`: display name, selected avatar, and locale.
- `game_saves`: five owner-scoped slots, versioning, revision, checksum, facility summary, and a size-limited JSON state.
- `player_settings`: keyboard/gamepad/phone preference, captions, accessibility, and audio levels.
- `support_requests`: owner-visible bug, account, save, accessibility, and feedback submissions.

All tables have Row Level Security. Authenticated players can access only rows whose `user_id` equals `auth.uid()`. Anonymous database access is revoked. Support staff do not automatically receive save access.

## Secure developer access

1. Use individual developer identities—never a shared developer login.
2. Require MFA on Supabase, Lovable, source control, hosting, and the production email provider.
3. Use separate local, staging, and production projects. Developers test migrations locally and against staging; production changes require reviewed CI or an explicitly approved maintainer.
4. Grant staff roles through server-controlled Auth `app_metadata`, never editable `user_metadata`. Do not add a staff bypass policy until a real support workflow requires it.
5. Keep database passwords, secret keys, service-role keys, SMTP credentials, and OAuth secrets in the hosting/CI secret manager. A service-role key must never enter a browser bundle, Lovable public variable, log, screenshot, or repository.
6. Use the public publishable/anon key only with RLS enabled. Treat RLS as the authorization boundary, not key secrecy.
7. Review audit logs regularly, rotate credentials, remove former developers promptly, and keep a break-glass account offline.

## Local preparation (optional)

Install the Supabase CLI and a Docker-compatible runtime, then run `supabase start` and `supabase db reset`. Keep it bound to localhost. The local stack must never be exposed to the internet.

Run the repository-only guard at any time:

```powershell
pnpm backend:check
```

No remote project is linked and no live migration is applied by these files.

## Release sequence

1. Freeze and version the game save schema; add upgrade tests for older saves.
2. Run local migrations from zero and add two-user RLS tests proving users cannot read or modify each other's records.
3. Create a separate staging project and configure email confirmation, approved redirect URLs, rate limits, bot protection, leaked-password detection, account recovery, and optional social providers.
4. Test signup, verification, login, logout, recovery, deletion, save conflict handling, offline failure, and restore on staging.
5. Validate backups and perform a real restore drill. Publish privacy, retention, deletion, and support policies.
6. Complete a security review and scan the final browser artifact for secrets.
7. Approve `data/backend-options.json` release gates, then set deployment configuration to `PUBLIC_BACKEND_MODE=supabase` or `lovable-supabase` and `PUBLIC_CLOUD_FEATURES_ENABLED=true` in staging first.
8. Promote to production only after acceptance. Keep a rollback deployment with cloud features disabled.

Never run a linked database reset against production. Never let Lovable or a dashboard make untracked production schema changes; capture and review migrations in this repository.
