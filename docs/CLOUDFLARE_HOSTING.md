# PlayReInd.com Cloudflare hosting

The public Arcade build is prepared as a Cloudflare Worker with Static Assets. It serves the marketing landing page at `/` and the game at `/game/`, with a compatibility redirect from `/play`.

## One-time domain setup

1. Add `PlayReInd.com` as a website/zone in the same Cloudflare account used for deployment.
2. If the domain was purchased from another registrar, replace its nameservers with the two nameservers Cloudflare assigns to the zone and wait until Cloudflare reports the zone as **Active**.
3. Authenticate Wrangler locally with `pnpm exec wrangler login`. Do not place a Cloudflare API token in browser code or commit it to `.env`.

## Verify and deploy

```powershell
pnpm cloudflare:build
pnpm cloudflare:dev
pnpm cloudflare:deploy
```

The build command regenerates the game, runs the release gate, extracts embedded images/audio into immutable hashed files, and rejects any file over Cloudflare's 25 MiB static-asset limit. The deploy command publishes `cloudflare-dist/` and attaches both `playreind.com` and `www.playreind.com` as custom domains.

After deployment, test:

- `https://playreind.com/`
- `https://www.playreind.com/`
- `https://playreind.com/game` (redirect compatibility)
- New game, Zach voice, music/SFX, founder selection, material purchase, equipment interaction, hiring/profile images, save/reload, keyboard, gamepad, and phone-controller pairing.

## Current DNS cutover status

As of July 19, 2026, `PlayReInd.com` still resolves to Squarespace IP addresses. The game is deployed at `https://playreind-game.zach-30b.workers.dev`, but Cloudflare cannot attach the apex or `www` custom domains until the domain is added to this Cloudflare account and its registrar nameservers are changed to the Cloudflare-assigned pair. Do not delete the Squarespace DNS records before reviewing whether the domain currently receives email.

Cloud saves, authentication, ElevenLabs generation, and future LLM calls remain server-side or disabled. Never add those provider keys to `cloudflare-dist` or frontend JavaScript.
