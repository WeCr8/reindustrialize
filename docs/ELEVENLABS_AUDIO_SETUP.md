# ElevenLabs Audio Production Setup

This integration is an offline production pipeline. The shipped browser game never receives the ElevenLabs API key or Zach's hosted voice ID.

## Security and consent gate

1. Zach reviews and signs `docs/ZACH_VOICE_CONSENT.md` before any recording upload.
2. Create or verify Zach's voice inside the approved ElevenLabs workspace. Do not automate sample upload from this repository.
3. Create a restricted ElevenLabs API key for production audio generation and rotate it if exposed.
4. Inject secrets into the process environment from your operating-system or CI secret manager; never add them to source, HTML, screenshots, receipts, or chat.
5. Set `ZACH_VOICE_CONSENT_CONFIRMED=yes` only after the signed record exists.
6. Review every generated line for meaning, tone, pronunciation, and misuse before moving it into a release asset directory.

PowerShell example for the current terminal:

```powershell
$env:ELEVENLABS_API_KEY = "..."
$env:ELEVENLABS_ZACH_VOICE_ID = "..."
$env:ZACH_VOICE_CONSENT_CONFIRMED = "yes"
pnpm audio:plan
pnpm audio:generate -- --voice-only
pnpm audio:generate -- --music-only
pnpm audio:generate -- --sfx-only
```

`audio:plan` makes no network request. Generated files and receipts are written under `packages/assets/audio/generated/`, which is gitignored until a maintainer reviews and deliberately promotes them.

## Production policy

- Zach's clone is mentor dialogue only. The player remains the founder.
- Dialogue text comes from the reviewed manifest in `data/audio-generation.json`; do not accept arbitrary browser text.
- TTS requests ask for `enable_logging=false`. This only provides Zero Retention Mode for eligible Enterprise workspaces; verify account history and plan eligibility.
- ElevenLabs Music and voice-cloning uploads are not eligible for Zero Retention Mode at this time. Submit no confidential information in music prompts and upload no voice recording before consent.
- Music prompts must not name artists, songs, or copyrighted melodies. The manifest forces instrumental output, disables inpainting storage, and requests C2PA signing.
- Confirm that the project distribution and platform are covered by the applicable ElevenLabs paid-plan or Enterprise game license before release.
- Generated audio must be cached and shipped as local assets. Never synthesize Zach dynamically from player-supplied text.

## Adding audio to gameplay

After human approval, copy selected files from the ignored generation folder into a versioned release-audio directory, normalize loudness, establish loop points for music, and add captions for every spoken line. Wire playback only after those review steps so the current silent build remains deterministic and E2E-friendly.
