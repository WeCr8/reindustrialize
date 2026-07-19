# Internal Bug Bounty Program

## Purpose

Find reproducible security, gameplay, content-integrity, accessibility, and deployment defects before a public release. This is an internal, authorized review of this repository and the project's own test deployments only.

## Authorized targets

- Source and generated files in this repository
- Local development servers started from this repository
- `https://playreind-game.zach-30b.workers.dev`
- `PlayReInd.com` only after it serves this project and the owner confirms the DNS cutover

## Never authorized

- Squarespace, Cloudflare, ElevenLabs, Supabase, registrars, or any other provider infrastructure
- Denial of service, load testing, credential guessing, social engineering, persistence, destructive writes, or data exfiltration
- Testing another user, account, tenant, domain, device, or network
- Displaying, copying, committing, or transmitting secrets or personal data

Stop immediately if a test could affect a real user or third party. Record the minimum evidence needed and redact secrets.

## Review agents

### Security and trust-boundary agent

Inspect secrets, browser/server boundaries, injection, unsafe HTML, auth and save readiness, dependency risks, headers, third-party calls, and accidental publication. Never print secret values.

### Gameplay and economy agent

Inspect progression gates, state transitions, material/economy exploits, station interaction, hiring and assignments, saves, controls, story/audio ordering, task completion, and test blind spots.

### Deployment and web agent

Inspect landing and game routes, static export integrity, caching, file limits, production/local feature parity, DNS configuration, accessibility, performance, and public information leakage.

## Severity

- **Critical:** credential exposure, remote code execution, cross-user account/save compromise, or destructive production impact.
- **High:** practical authorization bypass, persistent script injection, major progression/save corruption, or a public release blocker.
- **Medium:** meaningful exploit or broken core workflow requiring plausible conditions.
- **Low:** limited-impact defect, hardening gap, accessibility defect, or misleading presentation.
- **Informational:** useful observation without a demonstrated security or gameplay impact.

## Required report fields

1. ID and concise title
2. Severity and confidence
3. Affected build, route, file, and line
4. Preconditions
5. Minimal reproducible steps
6. Expected and actual behavior
7. Impact
8. Redacted evidence
9. Recommended remediation
10. Regression-test recommendation

Duplicate reports are merged by root cause. A finding is not closed until its regression test passes and the relevant release gate succeeds.
