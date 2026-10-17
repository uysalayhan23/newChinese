# HSK6 SC032 / SC038 — actual V4 GitHub WebP staging round-trip; camera and canonical BG/FG HOLD (2026-10-17)

Repository `uysalayhan23/newChinese`, `main`. Verified input HEAD `dc91ba11c52e5ffed4f0f3f2dec34a9199c75f48`; binary-only fast-forward commit `c058e932d49e730d842280df675f4c5123cd071c` uses `[skip ci]`. **Scope: staging-only physically verified binary promotion, never production or visual-scene acceptance.**

## Physical original source and exact GitHub upload evidence

- Source: the exact, earlier independently decoded and SHA-pinned `NewChinese_HSK6_SC032_SC038_V4_VERIFIED_STAGING_NOT_PRODUCTION_20261017.zip`. ZIP and physical WebP source checks were previously documented; both FG WebPs are byte-identical and both RGB PREVIEW WebPs are byte-identical. No source art was regenerated or changed here.
- Lossless V4 right-counter-only foreground: **RGBA 720×1280, 84,614 bytes**, local Git blob SHA `84631be9ed27a64a29e134e84037919b23277440`, SHA256 `c79a0c4dbfbc6807a94c598afd378682213894fd992356fcfe3cd3b66bcb62aa`.
- V4 composite preview: **RGB 720×1280, 215,124 bytes**, local Git blob SHA `ca8c43043c628d2b69ef7e59625bca49f1586533`, SHA256 `5a69c580d7a85d160eae0602f956440b3800bd39dd07b80363c13de05f6bc5bc`.
- Created actual authenticated GitHub Git blobs by `create_blob(base64)` with exact local file byte Base64. GitHub returned **exactly** both expected 40-digit blob SHA identifiers, not merely an API success response.
- Inserted **only four new staging WebP paths** (below), reusing those two SHA-pinned Git blob objects, and fast-forwarded `main` without force-push:
  - `staging/hsk6/qa_pending/sc032/hsk6_sc032_right_counter_only_fg_v4_STAGING.webp` → FG SHA `84631be9ed27a64a29e134e84037919b23277440`
  - `staging/hsk6/qa_pending/sc032/hsk6_sc032_right_counter_depth_preview_v4_STAGING.webp` → preview SHA `ca8c43043c628d2b69ef7e59625bca49f1586533`
  - `staging/hsk6/qa_pending/sc038/hsk6_sc038_right_counter_only_fg_v4_STAGING.webp` → FG SHA `84631be9ed27a64a29e134e84037919b23277440`
  - `staging/hsk6/qa_pending/sc038/hsk6_sc038_right_counter_depth_preview_v4_STAGING.webp` → preview SHA `ca8c43043c628d2b69ef7e59625bca49f1586533`
- **Independently re-read every staging path from GitHub with `fetch_file(encoding=base64, ref=c058e932...)`.** For all four returned files, `sha` exactly matched the expected Git blob SHA AND the returned Base64 content was character-for-character equal to the unchanged local source Base64, i.e. exact binary bytes after decoding. 112,820 Base64 chars (FG) and 286,832 (preview) in both scene folders. **Verified staging GitHub binary transport = PASS, 4/4.**
- Checked the binary-only commit's GitHub Actions query: **0 workflow runs**. It changed precisely the four staging paths. No production `content/hsk6/` WebP, locked dialogue, LOCKS, manifest or media-status mutation.

## Independent camera/ground-plane and target canonical source QA

At HEAD `c058e932d49e730d842280df675f4c5123cd071c`, full recursive Git tree was **not truncated**. `CAM_HSK6_SC032_01` and `CAM_HSK6_SC038_01` remain distinct from same-location SC035 reference `CAM_HSK6_SC035_01`; no `staging/hsk6/qa_pending/sc032|sc038/approved_numeric_camera_evidence.json` was present. The original target `visual_grounding.json` explicitly has `layerPlan.approved=false` and `cameraCalibrationVerified=false`. The only quantified donor perspective is an in-image 2D vanishing proxy; there is still no independently approved target camera transform, ground-plane calibration or scene-specific native target BG. **Camera equivalence = HOLD.** Scene topic and Location Bible agree, but do not prove projection identity.

All four scene-specific target **canonical BG/FG WebP** paths remain physically absent:
- `content/hsk6/sc032/assets/hsk6_sc032_bg.webp`, `hsk6_sc032_fg.webp`
- `content/hsk6/sc038/assets/hsk6_sc038_bg.webp`, `hsk6_sc038_fg.webp`

Both `hsk6_sc032_preview.webp` and `hsk6_sc038_preview.webp` are absent from production, as expected. Do not copy SC035 donor BG/FG into target canonical paths or promote same-location V4 staging artwork as accepted scene art. Previous real-source V4 whole-object FG QA removed 726-pixel speaking-hand obstruction (staging) while retaining fully visible right counter and leaving canonical pixels unchanged; this does **not** certify the missing camera.

## Read-only preflight reconciliation (this commit)

The existing `tools/verify_hsk6_032_038_camera_gate.py` still looked for `right_counter_only_fg_candidate_v4.webp`, a **local QA export filename**, while the newly committed staging FG uses `right_counter_only_fg_v4_STAGING.webp`. Updated that one lookup to the real GitHub staged filename. Existing PREVIEW lookup already matches. Added a synthetic regression test ensuring both staged names are discovered while intentionally bad binary SHA stays `HOLD`. **No tests were actually executed in this document-only/preflight-fix pass; the new test must not be represented as a test PASS.** The preflight remains fail-closed: numeric target-camera evidence and all physical canonical target layers must independently exist and pass even when V4 staging SHA verification succeeds.

## Unchanged release decisions

- **PASS:** exact binary identity and authenticated GitHub stage upload / four-path return comparison. **Not production.**
- **HOLD:** independently calibrated target camera; both target BG+FG, both target production previews; complete four-layer scene and camera/scale/foreground UI-safe area acceptance. Production preview inventory remains **40/50**.
- **Protected:** SC026 and remaining HSK6 HOLD scenes, `LOCKED_STEP_01..20` / `LOCKS.md`, Golden Demo reference, canonical actor identity and original source pixels, locked voices/dialogues, media and acceptance counters. Cross-level Zhang Wei HSK1–HSK6 review remains **P999 last, not started**.
- Next evidence needed: scene-specific target-camera matching approval with actual ground-plane landmarks, suitable real 720×1280 BG and RGBA FG, four-layer visual QA with face/gesture and floor contact, independent real source-to-GitHub SHA backread at **production paths** only after complete source QA. Actions explicitly unused, no force push, commits `[skip ci]`.
