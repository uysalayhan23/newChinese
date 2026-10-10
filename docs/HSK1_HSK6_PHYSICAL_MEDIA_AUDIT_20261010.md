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

## HSK6 face-right and preview production tooling (2026-10-10 continuation)

The physical WebP numbers above remain unchanged (**HSK6 126/250; HSK5 226/250; overall 1352/1500**). Additional fail-closed tools were committed to `main`:

- `tools/prepare_hsk6_face_right_candidates.py`: generates 20 **candidate**, not approved, HSK6 face-right character WebPs for scenes SC001/003/005/007/009 (Wang Ming), SC011/013/015/017/019 (Liu Mei), SC021/023/025/027/029 (Chen Yu) and SC031/033/035/037/039 (Wang Ming). Exact source blobs, identity, wardrobe and manifest path are checked in an all-scenes preflight. Mirroring a character is not proof of visual identity/continuity suitability.
- `tools/compose_hsk6_ready_previews.py`: can physically compose 16 existing 4-layer scene packages (SC002/006/008/012/018/022/024/028/030/041/043/044/046/047/049/050) into 720×1280 preview WebPs. Input files must match their exact hashes in `tools/hsk6_ready_preview_blobs.json`, which pins **64 physically staged canonical Git blobs**. No upscale of small BG or FG is permitted; transparent actor and overlap guards apply. `--publish` stages only preview files and their source-provenance manifests in a `[skip ci]` main-branch commit, without setting acceptance.
- Offline test suites `tools/tests/test_prepare_hsk6_face_right_candidates.py` and `tools/tests/test_compose_hsk6_ready_previews.py` were added. These test scripts have been committed but **were not run in the GitHub-connected execution environment**.

These are production mechanisms, **not claims that candidate assets or previews have already been rendered or uploaded**. Network-disabled local image processing remains a separate execution blocker; GitHub connector read/write permissions are functional. Independent visual QA of actual outputs is required before changing the `accepted` counters; all HSK6 visual batches remain 0/10 accepted. GitHub Actions have not been started.

## Live main staging addendum — HSK6_SC041/047

The historical 126/250 counts in the original table above describe the **pre-preview-candidate** snapshot, not the latest main HEAD. GitHub commit `cd791b42dd190fd6bd30d17e52d2c42a0eb7999c` placed two physically verifiable high-resolution canonical preview candidates into HSK6_SC041 and HSK6_SC047.

| Level | Current physical WebP | Missing | Scenes with five physical WebPs |
| --- | ---: | ---: | ---: |
| HSK1–HSK4 | 1000/1000 | 0 | 200 |
| HSK5 | 226/250 | 24 | 35 |
| HSK6 | 128/250 | 122 | 2 |
| **Total** | **1354/1500** | **146** | **237** |

Both newly staged previews are existing 941×1672 West Lake accepted-source images (four source layers match). They are **not** exact 720×1280 rendered outputs and do not constitute HSK6 scene acceptance. HSK6 accepted remains **0/50**, and physical HSK6 previews are missing in 48 scenes. The user-requested new 720×1280 previews and 20 right-facing character candidate binaries have not been rendered in the isolated Python runtime.

The 16-scene preview compositor now validates an independent character/outfit/facing/location manifest in `tools/hsk6_ready_preview_identity_pins.json`, with fail-closed unit tests committed. Connector-side static checks verified all 64 input Git SHA pins and all 20 face-right target manifests; these are **not** evidence that the offline Python test suites ran.
