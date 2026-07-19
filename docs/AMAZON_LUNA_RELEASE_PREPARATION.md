# Amazon Luna Release Preparation

Status: pre-authorization draft. No Amazon submission, approval, commercial agreement, or platform certification is claimed.

## What official documentation establishes

Amazon's public Luna developer page describes a cloud service reaching Windows, Mac, Fire TV, iOS, and other endpoints from a single source. Its public page does not publish a self-service game-binary submission specification. Amazon's official Luna announcement for GOG says developers with games available through GOG can use a GOG intake route for Luna onboarding. That is a possible future route, not evidence this game is eligible, onboarded, or accepted.

Amazon Appstore is a separate distribution route. Its current official submission workflow requires an authorized developer account, an eligible binary, targeting, listing details, review, and explicit submission. Officially documented binary families are APK/AAB for Fire OS and VPKG for Vega OS. The current browser artifact is none of those.

Official Appstore guidance also requires physical-device testing, accurate product behavior, listing assets and text, content-policy compliance, privacy disclosures, targeting, support details, export compliance, and reviewer instructions. The privacy questionnaire is required for new submissions and updates. The Console status—not repository metadata—determines whether an app is incomplete, ready, submitted, under review, approved, live, pending, rejected, or suppressed.

## Prepared without identity access

- Draft store copy and release notes
- Honest current playable-scope disclosure
- Reviewer route and input/television checks
- Platform certification backlog
- Version and artifact-identity plan
- Luna/Appstore route separation
- Official-source register
- Machine-readable authorization boundary
- Validator preventing false submission, approval, identity, or binary claims

The bundle is under `release/amazon-luna/`; its contract is `data/amazon-luna-release.json`.

## Version visibility plan

`data/release-manifest.json` is canonical. A candidate artifact must expose:

1. Exact semantic version, such as `0.7.0-alpha`.
2. Immutable source revision.
3. UTC build timestamp.
4. Artifact checksum manifest.

These must appear on the title screen, pause/settings or credits, support diagnostics, submission metadata, release notes, and checksums. The current title says `BUILD 0.7`; the contract records exact-version and source-revision injection as unfinished rather than hiding the gap.

## Authorized actions still required

Only the verified account owner or expressly authorized publisher may verify identity, accept agreements, enter tax/banking data, choose price and territories, make rating/privacy declarations, obtain Luna/GOG intake access, upload a build, or submit it. Credentials and personal compliance data must never be committed to this repository.

## Validation

```powershell
node scripts/validate-amazon-luna-release.mjs
```

The validator proves bundle consistency and truthful status. It cannot prove Amazon eligibility, certification, submission, approval, or publication.

## Official sources

- [Amazon Luna developer overview](https://developer.amazon.com/luna)
- [Official Amazon Luna announcement describing GOG developer intake](https://amazonluna.blog/coming-soon-games-from-gog-coming-to-amazon-luna-e5695978f617)
- [Get started with Appstore submission](https://developer.amazon.com/docs/app-submission/getting-started.html)
- [Submit an app](https://developer.amazon.com/docs/app-submission/submitting-apps-to-amazon-appstore.html)
- [Presubmission checklist](https://developer.amazon.com/docs/app-submission/presubmission-checklist.html)
- [Appstore details, images, descriptions, and feature bullets](https://developer.amazon.com/docs/app-submission/appstore-details.html)
- [Targeting and privacy](https://developer.amazon.com/docs/app-submission/target-app.html)
- [Privacy labels](https://developer.amazon.com/docs/app-submission/appstore-privacy-labels.html)
- [App test criteria](https://developer.amazon.com/docs/app-testing/test-criteria.html)
- [Review, submit, and status definitions](https://developer.amazon.com/docs/app-submission/review-submit.html)
- [Developer identity verification](https://developer.amazon.com/docs/app-submission/identity-verification.html)
