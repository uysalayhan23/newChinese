# HSK6 SC032 / SC038 — existing high-resolution electronics-store sources and camera evidence (2026-10-17)

Repo `uysalayhan23/newChinese`, `main`; verified input HEAD `a3e0dcd1aa1677c7055623f1b837cbb6183d7413`. **Read-only binary/source research; this commit contains only new QA text.** No production media or new graphics were produced.

## Fresh current-turn physical/source checks

The authenticated untruncated GitHub tree (19,202 entries) was checked for the two SC032/SC038 target folders, the existing V4 staging WebPs, the electronics-store location staging files, and known cross-level store-source alternatives. Live readback `fetch_file(encoding=base64)` of all four staged WebP paths confirmed the original Git blob SHA and identical Base64 for SC032 versus SC038 in each media type. Base64 whitespace removed before decoded length checks. Previous authenticated binary-upload/round-trip record was checked; no new upload is required.

Also opened the original physical user ZIP `hsk6.zip` and the previously QA-verified V4 physical WebP ZIP with Pillow. Exact raw Git SHA plus SHA256, dimensions and mode were independently confirmed:
- **Donor SC035 BG:** 720×1280 RGB, 199694 bytes, `b0ba989e06045ea92a0c4fd6ebf580877f4acc48`.
- **Donor SC035 FG:** 720×1280 RGBA, 134182 bytes, `dd7b43d996a33e40ff2c5cf86b5c4fa297238061`.
- **V4 right-only staging FG (both scenes):** 720×1280 RGBA, 84614 bytes, `84631be9ed27a64a29e134e84037919b23277440`; checked normalized remote Base64 112820 chars.
- **V4 staging preview (both scenes):** 720×1280 RGB, 215124 bytes, `ca8c43043c628d2b69ef7e59625bca49f1586533`; checked normalized remote Base64 286832 chars.

Actual V4 actor-mask remeasurement on unchanged original Zhang Wei and Chen Yu WebPs confirmed **0 simultaneous alpha≥80 actor–FG and actor–actor pixels**. Chen Yu still has **1196 low-alpha FG contacts**, equivalent to **47.54594 fully opaque pixels**, with visible alpha≥80 foot endpoints at y=1203 / 1200. This is acceptable staging proxy information only, not camera equivalence.

## High-resolution alternative candidates searched

| Candidate | Real BG/FG source Git SHA | Dimensions | Evaluation |
| --- | --- | --- | --- |
| **HSK6_SC035** | BG `b0ba989e06045ea92a0c4fd6ebf580877f4acc48`; FG `dd7b43d996a33e40ff2c5cf86b5c4fa297238061` | **720×1280** | Native-size electronics-shop source, **camera equivalence not proved** |
| `staging/.../locations/LOC_ELECTRONICS_STORE_001` | **Same exact two BG/FG blobs as SC035** | **720×1280** | Not a new independent geometry source; its location `qa_manifest.json` has `QA_PENDING` and `accepted=false` |
| **HSK3_SC042 / HSK5_SC002** | BG `bc540d14e120afa06e8766a9e574c41470211a6a`; FG `0bf5404580c38c70f8c185e9b9a45d1dc62bfc56` | **360×640** | Physical WebP headers reread from GitHub; different scene perspective and below native target size |
| **HSK5_SC008** | BG `c0a8cd2fdace1ed57ca5690ae030b00e5b3d0549`; FG `71931bdfc24c20f853887c612cdc4c14608df917` | **576×1024** | Physical WebP headers reread from GitHub; different FG/camera and below native target size |

**Scope limitation:** These are previously identified electronics-store candidates checked against the current repo tree, not an exhaustive assertion that no other image exists outside this repo or library.

## Numeric camera proof — still absent

The GitHub tree contains **no** `approved_numeric_camera_evidence.json`, `camera_matrix.json`, or approved target homography/ground-plane geometry for `CAM_HSK6_SC032_01` and `CAM_HSK6_SC038_01`. The donor SC035's four-line Hough intersection median `(379.25,396.25)` is a single-camera 2D image proxy, not independently calibrated target camera proof. Both target `visual_grounding.json` records approve scene-context and location matching but explicitly retain `layerPlan.approved=false`, `cameraCalibrationVerified=false`.

SC032 and SC038 remain **different locked dialogue scenes** even though their V4 staging pixels match. Both have missing target-specific BG/FG and production preview binaries:
`sc032_bg.webp`, `sc032_fg.webp`, `sc032_preview.webp`, `sc038_bg.webp`, `sc038_fg.webp`, `sc038_preview.webp`.

**Production decision: HOLD.** Do not rename/copy the SC035 donor or V4 staging WebPs into target canonical paths, upscale sub-HD alternatives or generate unsupported target art. Existing V4 staging files, all canonical source art, SC026 and other HOLDs, `LOCKS.md`, Golden and accepted counters stay untouched. Cross-level Zhang Wei visual audit remains P999 final task, not started.

**Next evidence necessary:** source geometry for each distinct target camera; independently reviewed at least four corresponding ground-plane points with numerical reprojection tolerances **or** a separately approved native target camera BG; compatible FG object depth and face/gesture/floor/safe-area visual QA; physical four-layer source SHA/decodes and final single-frame preview. Only then perform authenticated binary promotion and exact SHA backread. No GitHub Actions, no force-push, all commits `[skip ci]`.
