# Chapter 1 Story and Audio Contract

Chapter 1 tells the story of the player launching and owning a self-named manufacturing company. Zach is always the shop teacher and business mentor; he never owns the player's company or makes its decisions.

## Playable milestone order

1. Opening: the player chooses and names a founder and company.
2. First customer: accepting the first JobLine contract triggers `first_customer`.
3. NOX delivery: purchasing the first certified stock triggers `nox_delivery`.
4. First verified article: completing the first graded CNC part triggers `first_verified_article`.
5. First hire: hiring the first employee triggers `first_hire` and asks the founder to assign and lead them.
6. Garage graduation: five shipped jobs at a quality average of at least 3.0 trigger `garage_graduation`, followed by the Job Shop expansion sequence and Bay 02.

Each milestone is stored in `state.storySequences`, included in local saves, and shown only once per company. Every Zach voice line must exactly match its on-screen caption in `data/story-production.json` and `data/audio-generation.json`.

## Visual truth

All five milestones are functional with the active selected-founder identity overlay. They currently reuse the existing opening or expansion scene families. Dedicated NOX dock, inspection, and candidate-specific story illustrations remain visual upgrades and are documented as planned fallbacks rather than represented as finished.

## Validation

Run:

```powershell
node scripts/validate-story-production.mjs
python tests/e2e_chapter_one_story.py
```

The validator blocks missing captions, voice text mismatches, absent MP3s, absent player identity overlays, or deleted runtime milestone hooks. The E2E test verifies one-time playback and the final Bay 02 transition.
