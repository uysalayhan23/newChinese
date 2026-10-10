# NewChinese HSK1–HSK6 physical WebP audit — 2026-10-10

Repository: `uysalayhan23/newChinese`, branch `main`.

This is an audit of physical `content/hskN/scNNN/assets/*.webp` paths in the GitHub tree, **not** a claim that image quality, preview composition, or continuity QA passed.

## Physical asset count (post HSK6 canonical SHA reuse)

| Level | Required | Present | Physically missing | Scenes with 5 physical WebPs |
| --- | ---: | ---: | ---: | ---: |
| HSK1 | 250 | 250 | 0 | 50 |
| HSK2 | 250 | 250 | 0 | 50 |
| HSK3 | 250 | 250 | 0 | 50 |
| HSK4 | 250 | 250 | 0 | 50 |
| HSK5 | 250 | 226 | 24 | 35 |
| HSK6 | 250 | 126 | 124 | 0 |
| **Total** | **1500** | **1352** | **148** | **235** |

The HSK5 SC031 low-resolution physical preview is counted as *present*, not as QA passed. HSK5 also contains low-resolution BGs requiring separate genuine HD regeneration.

## What was actually uploaded to GitHub

126 previously physically missing WebP files were added to HSK6 using **exact Git blob SHA references** to previously accepted canonical layers, after matching scene location and character IDs, outfits, and face orientation. No new face or extra character was invented; no image upscaling. Only approved source blobs and HD backgrounds/foregrounds (minimum 720×1280) were reused.

| HSK6 scenes | Physical WebPs added | Remaining physical missing |
| --- | ---: | ---: |
| SC001–SC010 | 27 | 23 |
| SC011–SC020 | 21 | 29 |
| SC021–SC030 | 29 | 21 |
| SC031–SC040 | 15 | 35 |
| SC041–SC050 | 34 | 16 |
| **Total** | **126** | **124** |

HSK6 missing **by role**: 27 BG + 27 FG + 20 character cutouts + 50 previews = **124**. Refusals were intentional when the only known source was a too-small 360×640, 540×960, or 576×1024 environment, or when an approved facing/identity-matched character did not physically exist.

## Acceptance and continuity gates

- HSK6 batch audio is 50/50 complete, but every visual batch stays 0/10 visual and 0/10 accepted, because all 50 physical preview composites still need production and independent QA.
- The 50 `content/hsk6/scNNN/media_status.json` files now distinguish staged physical presence from truly missing file paths. Their visual status is **pending**; no automatic completion/validation is inferred from a copied canonical blob.
- `content/visual_regeneration_queue.json` records HSK6 physical counts and remaining gates.
- HSK5 remains 226/250 physical, with 24 absent WebPs and at least one physically present low-resolution SC031 preview. `tools/compose_hsk5_sc031_sc040.py` and canonical-facing candidate tools remain available, but actual HSK5 four-layer binary preview rendering is blocked while images cannot be transferred into the local image-processing runtime.
- Existing `LOCKS.md`, locked dialogue and scene content, and golden character/identity declarations were **not altered**. GitHub Actions were not called; Git commits used `[skip ci]`.

## Next physical production order

1. Produce and inspect missing HSK5 SC031–SC050 previews and missing face-right character cutouts; create real HD Neighborhood assets for SC032/035/038.
2. Regenerate HSK6 BG/FG for 27 scene locations with only low-resolution sources (or find a genuinely HD matching approved source), and create/approve 20 correctly oriented character cutouts.
3. Compose 50 HSK6 scene-specific 9:16 previews from its existing newly staged layers and future repairs; require exact Git blob provenance and independent visual/continuity approval before incrementing acceptance counters.
