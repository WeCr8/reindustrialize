# REINDUSTRIALIZE Demo Video Index

Open this file from the repository root whenever you need to find the current videos.

## Recommended V5 human-bot gameplay videos

- [3:10 uninterrupted bot campaign](videos/gameplay-longform/reindustrialize-human-bot-full-gameplay-v5.mp4) — complete founder-to-Job-Shop run
- [60-second horizontal bot demo](videos/horizontal-demos/reindustrialize-human-bot-demo-60s-v5.mp4) — TV, browser, pitch deck and YouTube
- [45-second bot gameplay feature](videos/gameplay-longform/reindustrialize-human-bot-feature-45s-v5.mp4) — saw, tooling, CNC, inspection and growth
- [30-second vertical bot short](videos/vertical-shorts/reindustrialize-human-bot-short-30s-v5.mp4) — Shorts, Reels and TikTok
- [30-second square bot cut](videos/square-social/reindustrialize-human-bot-square-30s-v5.mp4) — social feeds and marketplace previews

V5 is generated from one seeded, uninterrupted Playwright run. The bot uses visible player controls, natural cursor motion and reading pauses, makes two intentional beginner errors, recovers through the UI, ships five jobs, and expands to the Job Shop. Its machine-readable evidence is in `tmp/bot-runs/human-bot-run-20260718.json`.

## Earlier real-gameplay demos

- [60-second horizontal real-gameplay demo](videos/horizontal-demos/reindustrialize-real-gameplay-demo-60s-v4.mp4) — TV, browser, pitch deck and YouTube
- [45-second real-gameplay feature reel](videos/gameplay-longform/reindustrialize-real-gameplay-features-45s-v4.mp4) — production tasks and machines
- [30-second vertical real-gameplay short](videos/vertical-shorts/reindustrialize-real-gameplay-short-30s-v4.mp4) — Shorts, Reels and TikTok
- [30-second square real-gameplay social cut](videos/square-social/reindustrialize-real-gameplay-square-30s-v4.mp4) — social feeds and marketplace previews
- [2:09 complete current-campaign gameplay](videos/gameplay-longform/reindustrialize-full-gameplay-garage-to-job-shop-v3.mp4) — founder creation through Job Shop expansion

V4 remains as the previous manual/accelerated slate. V1 and V2 remain in their category folders as version history; V2 primarily uses gameplay screenshots with Remotion motion treatment.

## Source and editing files

- Real gameplay source capture: `demo/remotion/public/captures/reindustrialize-full-gameplay-garage-to-job-shop-v3.webm`
- Real-footage Remotion editor: `demo/remotion/src/real-gameplay-promo.tsx`
- Full-gameplay Remotion editor: `demo/remotion/src/full-gameplay.tsx`
- Composition registry: `demo/remotion/src/root.tsx`
- Repeatable capture driver: `scripts/record-full-gameplay.py`
- Human-style completion bot: `scripts/human-gameplay-bot.py`
- V5 bot source capture: `demo/remotion/public/captures/reindustrialize-human-bot-full-gameplay-v5.webm`
- V5 bot Remotion editor: `demo/remotion/src/human-bot-gameplay.tsx`
- Video catalog: `videos/promo-catalog.json`

Run `OPEN_DEMO_VIDEOS.ps1` to open the video library in Windows Explorer.
