# REINDUSTRIALIZE Visual Storybooks

Each meaningful game/media version must ship with a matching, immutable storybook folder (`v1`, `v2`, and so on). The storybook is both a visual QA artifact and source material for potential comics or short books.

Every version must include:

- an interactive `index.html` with keyboard and slide-picker navigation;
- a canonical `storybook-manifest.json`;
- a numbered `slides/` PNG export for every manifest entry;
- every selectable founder and every active scene containing the founder;
- story text, image, narration ID, tutorial instructions, and completion status;
- a complete searchable asset library covering every packaged graphic, sprite, Zach voice clip, SFX, ambience loop, music candidate, legacy/source asset, and its lifecycle/reference status;
- profile portrait and exact matching floor-sprite proof for every employee, including the maintenance team;
- a visible production-needs queue for every missing visual, audio, story, tutorial, and later-chapter requirement;
- visible planned-gap cards for content that is not implemented yet.

V1 intentionally labels the current cinematic art model: ten exact founder sprite overlays share male/female body-family backgrounds. This makes character coverage verifiable without claiming ten unique cinematic paintings already exist.

Run `pnpm storybook:release` from the game root whenever story, founder, tutorial, or scene data changes.

The current deployed HTML reviewer is available at `https://playreind.com/storybook/`.
