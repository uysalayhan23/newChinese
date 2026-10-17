# HSK6 SC032/038 V4 physical WebP pixel recheck — 2026-10-17

Base GitHub main HEAD `80a485075c5a5cc39692e66c76030528c6733253`. QA-only / HOLD. This document does not approve production image assets.

## Actually executed and checked

Read original `hsk6.zip`, the original V3 physical staging ZIP and `NewChinese_HSK6_SC032_SC038_V4_COUNTER_DEPTH_QA_20261017.zip`. The V4 archive passed CRC and SHA256 `35db68ad9b30060baca5c55b8a53c6abe1b790bf603a9c94561fdffde0802701`. Independently ran the original V4 Pillow script **twice** against original source binaries. Both runs reproduced both SC032 and SC038 FG/preview WebPs exactly byte-for-byte against the original ZIP; source SHA pins and exact original V3 recomposition passed.

| V4 output, byte-identical between SC032/038 | Bytes | Mode/dimensions | Exact Git blob SHA |
|---|---:|---|---|
| Whole-object right-counter-only staging FG | 84,614 | WEBP RGBA 720×1280 | `84631be9ed27a64a29e134e84037919b23277440` |
| Scene staging composite preview | 215,124 | WEBP RGB 720×1280 | `ca8c43043c628d2b69ef7e59625bca49f1586533` |

New independent alpha>=80 pixel check: original SC035 donor FG had separate left x=0..122 and right x=617..719 object islands, separated by zero-alpha columns 123..616. The new QA staging FG omits the **whole left object** (33,617 alpha>=80 pixels), preserving the **entire right object** (52,651 alpha>=80 pixels). Original source BG already depicts the left cabinet; no hand-specific erasure or source-art replacement was done.

Actor-A speaking hand/FG overlap **726 → 0 pixels**, B/FG overlap **0**, actor collision **0**, and both visible foot bottoms stay at y=1203 in this exact staging mask method. V3→V4 preview re-encoding has small RGB quantization differences beyond the changed left object; alpha and source integrity conclusions rely on original source masks and direct lossless FG comparison, not RGB preview equality.

## Unclosed camera, source, and transfer gates

- `CAM_HSK6_SC035_01` donor and target `CAM_HSK6_SC032_01` / `CAM_HSK6_SC038_01` are distinct preset IDs with **no validated scene-to-scene camera projection, lens/ground-plane calibration or homography** in the reviewed evidence. Same Location Bible, floor contact and reduced hand masking are **not** camera equivalence evidence.
- SC032/SC038 scene-specific canonical BG + FG binary files and production previews are still missing; the original BG/FG and two actor source WebPs, LOCKS, accepted art and current `layerPlan.approved=false` and scene HOLD must stay untouched. SC026 also retains separate camera/BGFG HOLD.
- The real verified V4 blob SHAs were checked against GitHub Git blob API and both returned **404 Not Found** at this check; local V4 physical binary verification is **not** a GitHub upload. GitHub staging V4 transfer and full binary readback are still **PENDING**. Do not claim upload, use a fabricated SHA, write Base64 text as WebP, or promote V4 into runtime content paths without actual binary receipt.
- Local QA artifact: `NewChinese_HSK6_SC032_SC038_V4_VERIFIED_STAGING_NOT_PRODUCTION_20261017.zip` (990,207 B, SHA256 `893b9973724419e04fa03d3df5609e18cbf4f053dee174d17624e820f5cea7d8`) contains both real scene FG/preview WebPs, independent measurements, scripts and comparison.
- Global Zhang Wei HSK1–HSK6 identity comparison remains the **last** queued P999 task, not started.

**Decision:** `LOCAL_STAGING_V4_PHYSICAL_AND_GESTURE_PROXY_PASS / GITHUB_V4_BINARY_TRANSFER_PENDING / CAMERA_AND_CANONICAL_BGFG_HOLD / PRODUCTION_NOT_PROMOTED`.

Document-only change. No Action run requested or started; `[skip ci]`; no force push. Preview production inventory remains **40/50**.
