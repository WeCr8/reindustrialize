# Player Scene Variant Audit

Last verified: **2026-07-18**

Every active raster scene containing the player must support all ten launch founders. Runtime selection follows `selectedAvatar`; Zach, equipment, camera, and lighting remain invariant. Cinematic backgrounds share male/female back-facing navy/tan workwear compositions, while every story card adds the exact selected founder sprite as an identity portrait layer. Selection portraits and playable floor sprites remain distinct.

## Launch selection

| Option | Sprite | Scene family | E2E selection |
|---|---|---|---|
| Male 01 | `av_m_01.png` | Male | Verified |
| Male 02 | `av_m_founder_02_hd.png` | Male | Verified |
| Female 01 | `av_f_founder_hd.png` | Female | Verified |
| Female 02 | `av_f_founder_02_hd.png` | Female | Verified |
| Blonde male | `av_m_blonde_hd.png` | Male + exact identity overlay | Verified |
| Blonde female | `av_f_blonde_hd.png` | Female + exact identity overlay | Verified |
| Middle Eastern male | `av_m_middle_eastern_hd.png` | Male + exact identity overlay | Verified |
| Middle Eastern female | `av_f_middle_eastern_hd.png` | Female + exact identity overlay | Verified |
| Indian male | `av_m_indian_hd.png` | Male + exact identity overlay | Verified |
| Indian female | `av_f_indian_hd.png` | Female + exact identity overlay | Verified |

## Active runtime scenes

| Scene | Contains player | Male asset | Female asset | Runtime switch | E2E status |
|---|---|---|---|---|---|
| Title / company creation | Yes | `story-title-male-founder-v1.png` | `story-title-female-founder-v1.png` | `setTitleArt()` | Verified |
| Founding Day / Zach introduction | Yes | `story-opening-male-founder-v1.png` | `story-opening-female-founder-v1.png` | `setStoryArt("opening")` | Verified |
| Garage graduation / Job Shop expansion | Yes | `story-expansion-male-founder-v1.png` | `story-expansion-female-founder-v1.png` | `setStoryArt("expansion")` | Verified |
| NOX material-ordering facility | No | Shared | Shared | Not required | Verified |
| VMC, lathe, and tool-cart equipment views | No | Shared | Shared | Not required | Verified |
| Hiring cards and profiles | No player | Shared | Shared | Not required | Verified |

## Identity invariants checked

- [x] Two visually distinct male founders are selectable, including dark wavy hair and short textured-curl options.
- [x] Two visually distinct female founders are selectable, including dark-brown and auburn braided low-ponytail options.
- [x] All four founders retain navy workwear, tan work pants, and safety boots for scene-family continuity.
- [x] Zach keeps the selected black cap, short beard, and charcoal-gray shacket.
- [x] Founder variants occupy the same composition and narrative role.
- [x] Each of ten visual cards changes the selected floor sprite and exact scene portrait immediately and maps correctly into title, opening, and expansion scenes.
- [x] Founder and company names remain independent from image selection.

## Specified but not yet active cutscenes

`data/cutscenes.json` describes a future NOX cinematic whose final dock shot includes Zach and the avatar. That cinematic has no runtime renderer or production shot assets yet. Before enabling it, generate both `nox-dock-male-founder` and `nox-dock-female-founder` and add an E2E variant assertion. The Shop Class specification contains Zach only, so it does not require player variants unless its composition changes.

## Release rule

A new scene may not be marked complete when it contains the player and does not support every launch founder. Add required scene-family files to `data/cutscenes.json`, wire every avatar ID through `selectedAvatar`, and assert each selection plus the scene's `data-variant` in E2E.

## Expansion workflow

Active runtime coverage is governed by `data/player-scene-manifest.json`. Add a new scene there with `active`, `chapter`, `containsPlayer`, `identityOverlay`, and male/female asset filenames. The build embeds assets from that manifest automatically. Run `pnpm validate:scenes`; it fails for missing founders, atlas sprites, identity overlays, family mappings, or scene files. `tests/e2e_character_story_variants.py` then renders every founder through every active scene and the playable floor canvas.
