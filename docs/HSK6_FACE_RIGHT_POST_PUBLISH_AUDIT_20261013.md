# HSK6 post-publication QA and next missing-layer audit — 2026-10-13

Repository: `uysalayhan23/newChinese`, `main`. GitHub Actions not used.

## Preserved verified deliverables

- `HSK6` 16/16 previously published 720x1280 preview assets remain at their canonical scene paths. All 16 checked against their live `visual_manifest.json.previewComposition.previewBlob` and previously recorded SHA; all 16 PASS. Camera, lighting, speaker and pending acceptance fields are present and unchanged.
- `HSK6` 20/20 right-facing first-character layers exist: Wang Ming 10/10 exact canonical Git SHA `067fcfe261c52adebc383f5551d7ed365abd747e`; Liu Mei 5/5 `1944d13b2565d618ad183da64fd33ef68a11191a`; Chen Yu 5/5 `55885be8637e7df4b7ff300a710ed9d1b6f78847`.
- The ten Liu Mei/Chen Yu per-scene SHA-256 approvals remain scoped to their `HSK6_SCxxx` identifiers. `identityRegeneration.status` remains `required`, and no complete scene has been accepted.

## New 20 odd-scene inventory

Scenes audited: 001,003,005,007,009,011,013,015,017,019,021,023,025,027,029,031,033,035,037,039.

- **7** have BG+FG present alongside both character WebPs: SC003, SC005, SC009, SC015, SC021, SC025, SC027. The preview is absent in all 20 odd scenes.
- **13** currently have only characterA and characterB WebPs, lacking both BG and FG: SC001, SC007, SC011, SC013, SC017, SC019, SC023, SC029, SC031, SC033, SC035, SC037, SC039.
- All **20 characterB** files presently use Zhang Wei blob `316717c873fade2a1e98564bdf6ac037e7cc354e`, **not** in the global approved canonical list. Their pictured face and outfit visibly differ from the approved Zhang Wei `44a7a521b7fa64466111c30f6830904081c3767d`. A target-specific orientation and composition review is required before replacing them. Do not whitelist unapproved bytes or mark these scenes accepted.

## Recurrence prevention

`tools/prepare_hsk6_face_right_candidates.py` previously mirrored all three source characters, including **Wang Ming whose pinned approved original already faces right**. This would recreate the rejected left-facing Wang Ming candidate during a future build. Fixed the generator to byte-copy the approved Wang Ming source, and mirror only Liu Mei and Chen Yu; added regression coverage asserting Wang Ming's exact source bytes and correct alpha-side orientation.

## Remaining sequence

1. Run full updated original offline Python test suite in an executable checkout before accepting this generator change as regression-PASS.
2. Independently determine an approved LEFT-facing Zhang Wei characterB source or scene-specific QA-approved derivation, without bypassing locked identity pins.
3. Produce previews for the seven four-layer odd scenes only after their characterB identity/orientation is resolved and all source SHA manifests are pinned.
4. Acquire missing BG/FG for remaining 13, then preview/continuity QA; leave all full-scene status pending until complete.

All code/documentation commits use `[skip ci]` and no Actions.
