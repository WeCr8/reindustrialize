# Privacy-conscious analytics

PlayReInd uses Google Analytics tag `G-KRCJP5MHXH` only under a shared consent controller on the landing page, video library, and game.

## Consent behavior

- Analytics and all advertising-related storage are denied before the Google script loads.
- Accept and decline are equally available and persist in local storage under `reindustrialize.analyticsConsent.v1`.
- Declining keeps analytics events disabled. Advertising storage remains denied even after analytics is accepted.
- The interface states that founder/factory names, saves, free text, and raw controls are never sent.

## Data contract

Code may emit telemetry only through `window.reindAnalytics(eventName, params)`. The controller rejects unknown event names, unknown parameters, unsafe values, and sensitive-looking keys. Do not call `gtag('event', ...)` directly.

Allowed gameplay data is limited to anonymous progression identifiers: start/resume, founder archetype, control mode, task/station progress, hire role, qualified station assignment, equipment ID/tier, maintenance repair, chapter, and facility milestones. IDs must be short slugs; never provide player-entered strings.

## Verification

After building the Cloudflare bundle, run:

```powershell
node scripts/validate-privacy-analytics.mjs
```

This fails when any generated page does not deny consent before loading Google Analytics or when the gameplay event contract is incomplete.
