# Storybook, Comic, and Book Publishing Readiness

The game storybook is the canonical visual narrative record. Store packages are derivatives, never the source of truth.

## Release rule

Every game release must declare `storybookEdition` in `data/release-manifest.json`. The matching immutable edition must be registered in `storybook/releases.json` and contain its viewer, manifest, and exact numbered PNG set. The normal release gate fails when these do not agree.

When story, gameplay, art, characters, tutorials, or progression changes:

1. Create a new storybook edition rather than overwriting an edition already attached to a shipped game release.
2. Rebuild the full slide sequence from canonical data.
3. Review founder identity, Zach continuity, captions, voice IDs, task order, and planned gaps slide by slide.
4. Export and validate all numbered PNGs.
5. Register the game release and storybook edition together.
6. Only then derive comic, short-book, print, or digital packages.

## Publication derivatives

- Digital storybook: responsive HTML plus editorially selected EPUB layout.
- Comic eBook: fixed-layout EPUB or KPF with optional Guided View/virtual panels.
- Short print book: single-page print PDF plus separate cover PDF.
- Comic print book: portrait single-page print PDF plus separate cover PDF.

`data/publishing-profiles.json` records working output targets. These profiles must be rechecked against the distributor before upload.

## Amazon KDP preparation notes

As checked July 18, 2026, Amazon KDP accepts EPUB or KPF for fixed-layout books and no longer accepts MOBI for fixed-layout uploads. Print interiors with full-bleed artwork should use a print-ready PDF, single pages rather than spreads, 0.125-inch bleed, and images of at least 300 DPI. Trim, margins, gutter, page-count, ink/color, cover dimensions, and spine calculations must be finalized only after the edited book and final page count exist.

The current 1920×1080 review PNGs are proof images, not print-ready pages. Publication requires portrait page composition, editorial pacing, safe text areas, front/back matter, rights review, metadata, cover design, and final distributor previewer approval.
