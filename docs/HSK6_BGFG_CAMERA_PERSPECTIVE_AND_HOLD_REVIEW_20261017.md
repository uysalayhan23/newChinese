# HSK6 SC026/032/038 — camera, depth and canonical BG/FG gate; remaining HOLD recheck (2026-10-17)

Repository: `uysalayhan23/newChinese`, `main`. Verified base HEAD `d9ed118f4b43407bf551a781846769c3cc35a5ce`.
**Audit-only.** This report does not authorize/perform reuse or production promotion, regenerate canonical pixels, modify any approved assets, alter acceptance counters, or change LOCKS/locked dialogues. No GitHub Actions.

## Evidence and gate definition

- Checked full remote Git tree with `truncated=false` (19,151 entries); read source manifests, scene dialogues, visual production queues, donor grounding and authoritative Location Bibles.
- Independently Pillow-decoded raw original `hsk6.zip` WebP assets, actual three staging-v2 previews from `NewChinese_HSK6_SC026_SC032_SC038_STAGE_V2_QA_BUNDLE_20261016.zip`, and separately the `sc020_contact_shadow_refined_v3.webp` staging binary. Calculated Git-blob SHA from real binary bytes.
- `LOCKED_STEP_17_VISUAL_SYSTEM.md` requires separately approved scene-context grounding from exact locked dialogue, location matching, layer planning, and all four physical scene-specific runtime layers **before** preview promotion. The donor SC023 and SC035 have `visual_grounding.json` approved; SC026, SC032 and SC038 **do not have** scene-specific `visual_grounding.json` at this HEAD. Donor approval does not transfer.
- All three target `visual_manifest.json` files remain `visual-assets-pending`. Target BG/FG binaries and production previews are absent. `cameraPreset` strings differ from donors (`CAM_HSK6_SC023_01` vs `CAM_HSK6_SC026_01`; `CAM_HSK6_SC035_01` vs `CAM_HSK6_SC032_01`/`CAM_HSK6_SC038_01`). Shared location/light IDs are not calibrated camera proof.

## Actual source / staging comparison

| Target | Exact-location donor BG / FG git SHA | Real staging WebP blob, geometry | FG alpha mask donor coverage | Foreground QA, two actor floor baseline |
| --- | --- | --- | --- | --- |
| SC026 | SC023: BG `a0fda64fd0732d378d2648a48d058edfb4fca015` / FG `5da1b87d0e43673ce2259c2759c88569f8cae81e` | 720×1280 RGB, 330982 bytes, `ceca83f32fe89c510844de4820c22c379f207f88` | nonzero alpha 8.58% of frame, >=80 alpha 7.34%, upper canopy/edge | v2 characterA head 0.3127%, torso/gesture 0.1226%; both foot baselines y=1210; heights 622 / 750 px (ratio 0.8293) |
| SC032 | SC035: BG `b0ba989e06045ea92a0c4fd6ebf580877f4acc48` / FG `dd7b43d996a33e40ff2c5cf86b5c4fa297238061` | 720×1280 RGB, 193516 bytes, `5398498273bbf47abaa10445f9775f71304dff0b` | nonzero alpha 11.24%, >=80 alpha 9.36%, shop display edges | v2 characterA head 0.3414%, torso/gesture 1.4960%; both baselines y=1210; heights 597 / 737 px (ratio 0.8100) |
| SC038 | identical source to SC032, same donor scene and source characters | byte-identical SC032 staging preview, Git blob `5398498273bbf47abaa10445f9775f71304dff0b` | same as SC032 | same as SC032 |

The foreground overlap values are preexisting staging sidecar metrics; foreground alpha coverage and actual WebP/blob decodes were checked independently in this audit. Thresholds are head <=0.5% and torso/gestures <=2%. The three staging outputs pass those *proxy* thresholds with no reported opaque actor collision. **These tests cannot prove camera perspective, floor-depth validity, or source BG/FG canonical authorization**; no production PASS is assigned.

### Continuity blocker requiring additional review

SC026/032/038 visual production queues explicitly require **two adult characters** and `CHAR_ZHANG_WEI_001`. Their source Zhang Wei WebP `44a7a521b7fa64466111c30f6830904081c3767d` (600×900 source image, blue sweater) appears visibly much younger/smaller than adult-appearing Zhang Wei variants in other HSK6 scenes; camera-relative apparent-height ratios are approximately 0.83 in SC026 and 0.81 in SC032/038 despite common foot baselines. This is an **identity / scale review flag**, not definitive proof of an age error from images alone. The same immutable source is reused in other existing scenes, so do **not** silently change it or override previously accepted content. Confirm canonical adult identity and outfit with full Character Bible/source approvals before promotion.

### Dialogue-specific context

- SC026 dialogue discusses `人口流动` (population mobility) at `LOC_NEIGHBORHOOD_001`, SC023 donor discusses `公共讨论中的耐心` at the same location. Neither excerpt independently requires a changed street-camera layout, but donor BG/FG approval cannot be assumed.
- SC032 dialogue discusses `人类判断的价值`, SC038 `数字身份`, with identical target speakers/locations `LOC_ELECTRONICS_STORE_001`; SC035 donor discusses `技术乐观与技术焦虑`. The shop location matches the Bible (phones/accessories, display tables, shelves), yet each scene's specific camera and gestures still require grounding.
- Existing PREVIEW is a derived QA image, not a substitute for physical runtime BG + A + B + FG layers.

**Disposition:** SC026/032/038 = `STAGING_V2_PHYSICAL_PASS; CANONICAL_BGFG_MISSING; GROUNDING_UNAPPROVED; CAMERA_AND_IDENTITY_QA_HOLD`. Do not copy/relabel donor layer SHA blobs into targets or upload staging candidates as production previews on this evidence.

## Remaining HSK6 HOLDs, ordered review

1. **SC013 / SC019 — HOLD_HOME_DEPTH**. Source BG `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba` and FG `6acadbee8403b5d78e0042431eec7af75fc94248` are identical in both, physically RGB/RGBA 768×1365. Original home coffee-table / foot-plane contradiction persists; no preview files; no resize, FG swap, or fake masking promotion.
2. **SC020 — STAGING_SHA_PASS / VISUAL_HOLD.** Newly decoded physical shadow-v3 staging WebP at RGB 720×1280, **957292 bytes**; Git blob `76dbd4ece57386d3ac71bbd7ecb9b0c4c7fee68b`, SHA256 `4e49ba20f227aaa7e30b6022f14783566809526a2819d44d945d5b7482467138`. Matches the prior exact sidecar. Canonical four source layers untouched. Contact-shadow test remains a staging-only pixel QA, not a final accept/release. Character visual age/scale/identity is still reviewable; do not treat superficial style tolerance as approval.
3. **SC022 — HOLD_RAILING_SCALE.** Existing production preview `56f465a61f2e58c1d437f9098c66f6f126a2fc55` physically exists; manual inspection confirms stone railing/flower foreground obscures much of Zhang Wei's lower body, with apparent actor-scale discontinuity. Keep unchanged pending actual perspective and occlusion repair.
4. **SC016 / SC042 / SC045 / SC048 — HOLD_HOME_BGFG.** Their original archives and GitHub scene target paths lack both scene-specific home BG and FG as well as previews. The only source home pair belongs to SC013/019 and retains unresolved incompatible table-depth geometry. Existing canonical actor sources decode and remain unchanged. SC045 uses distinct character variants (Li Na `052e3d74becb...`; Zhang Wei `316717c873fa...`) that need identity/outfit continuity verification; uniqueness alone does not equal failure.

Production inventory remains **40/50** preview paths; missing previews: SC013, SC016, SC019, SC020, SC026, SC032, SC038, SC042, SC045, SC048. No application-level acceptance count changes.

## Required next gates

(1) Scene-specific visual grounding of SC026/032/038 from locked dialogues and approved layer plans; (2) adult canonical actor/scale and camera perspective comparisons; (3) true scene-compatible BG and FG physical binary with separately verified visual geometry; (4) resulting four-layer compositing, source and destination SHA, facial/gesture occlusion, application safe-area QA. Stage first, then promote only on evidence. Resolve home table geometry, SC020 preview-specific identity/depth, and SC022 railing scale separately. Preserve all LOCKS and existing Golden/canonical records. No Actions; all doc-only commits `[skip ci]`.
