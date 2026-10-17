# HSK6 SC026 / SC032 / SC038 — independent four-source staging camera / floor / foreground audit (2026-10-17)

Repository: `uysalayhan23/newChinese`, `main`. Parent SHA: `22cac8abc4ae13edd981b5bed9a24184322eb417`. Text-only QA evidence, not a production asset release.

## Inputs and physical source verification

Locally examined actual uploaded binary archives:
- `hsk6.zip`, 231,732,632 bytes, SHA-256 `3bbfad7f8133fd542c7b431e195dc689f72886fd4d0ec235ff5a71a580d319db`.
- `NewChinese_HSK6_SC026_SC032_SC038_STAGE_V2_QA_BUNDLE_20261016.zip`, 1,093,810 bytes, SHA-256 `aee2e3900a03c56c6617059fa60e0f385447bd4499015cae05085630c292968e`.
- Pillow 12.3.0 + NumPy decoded the genuine RGB donor BG, both RGBA source characters, RGBA FG and V2 RGB preview for **each scene**. Verified exact Git blob SHA for all four sources and each candidate preview against source QA sidecars and current GitHub tree.
- All three staged previews are 720×1280 RGB. Exact source pixels remain unchanged.
- Staging V2 previews themselves are **not GitHub production files**; no new preview, donor layer, or scene acceptance status was promoted.

## Truly independent foreground / actor geometry measurements

The script cropped each original actor's actual nontransparent alpha bounding box, resized it using Pillow Lanczos to the old V2 placement dimensions, then compared that reprojected actor alpha mask to the donor FG's unchanged RGBA alpha. A pixel was counted as foreground overlap when both alpha values were >=80. These are explicitly **proxy masks**; they do not exactly reproduce all stages of the V2 compositor, nor prove camera perspective.

| Scene | Staging Git blob | Actual visible feet end A/B (px y) | FG head overlap for A (new ROI) | FG torso overlap for A (new ROI) | Opaque A–B collision | Final gate |
|---|---|---|---|---|---|---|
| SC026 | `ceca83f32fe89c510844de4820c22c379f207f88` | 1202 / 1208 (6 px difference) | 0.774783% | 0% | 0 px | HOLD |
| SC032 | `5398498273bbf47abaa10445f9775f71304dff0b` | 1202 / 1203 (1 px difference) | 0% | 2.039655% | 0 px | HOLD |
| SC038 | **byte-identical SC032** `5398498273bbf47abaa10445f9775f71304dff0b` | 1202 / 1203 (1 px difference) | 0% | 2.039655% | 0 px | HOLD |

**Important ROI qualification:** The earlier V2 sidecar measured head and torso with *different region masks*: SC026 A head 0.3127%, torso 0.1226%; SC032/038 A head 0.3414%, torso 1.4960%. Independent method above divides each character's rectangular placement into first 25% (head) and 25–75% (torso), then intersects with the real actor silhouette, so the percentages are **not directly comparable** to those earlier acceptance cutoffs. The larger new SC026 head and SC032/038 torso ratios identify regions for review; they do **not** prove source pixels changed or retroactively negate a test using a different ROI.

**Foot baseline qualification:** The old staging metadata places both actor crop rectangles at bottom y=1210, but the alpha crop image boundary contains transparent fringe. Actual reprojected visible alpha pixels end at 1202/1208 in SC026, and 1202/1203 in SC032/038. A shared rectangle bottom alone does not establish identical natural ground contact.

Additional foreground alpha>=80 pixel coverage is 7.3377% of SC026 frame, 9.3607% of SC032 and SC038 frame. For SC026 coverage is above midframe mostly top/middle; for electronics store mostly middle (shelf/counter). Actor-vs-actor alpha80 collisions = 0, foreground still needs eyes/hands and real camera-depth visual review.

### Camera/perspective gate

SC026 camera preset `CAM_HSK6_SC026_01` differs from SC023 donor preset `CAM_HSK6_SC023_01`; SC032/038 camera presets differ from SC035. No calibrated projection/vanishing point, ground plane or proven source-to-target camera transform is supplied with these strings. Shared location and light match is insufficient to justify an immutable donor layer copy.

The production target folders still have **no scene-specific BG/FG binaries** (six missing) and no production previews (three missing); `visual_grounding.json` records scene-context and Location Bible approval, but `layerPlan.approved=false` and each `visualQa` remains HOLD. Global HSK1–HSK6 Zhang Wei identity comparison stays **last task P999** at user request, untouched. The distinct *local* actor/scale issue remains an unresolved gate, not an instruction to modify actors.

### Committed non-production staging evidence

- `staging/hsk6/qa_pending/sc026/independent_four_layer_mask_qa_20261017.json`
- `staging/hsk6/qa_pending/sc032/independent_four_layer_mask_qa_20261017.json`
- `staging/hsk6/qa_pending/sc038/independent_four_layer_mask_qa_20261017.json`

Local reproducibility package `NewChinese_HSK6_SC026_032_038_FOUR_LAYER_QA_STAGING_20261017.zip` contains full independent pixel-count JSON, masks-over-BG diagnostics, and the exact Python/Pillow QA script. The ZIP is an attached local QA deliverable, **not** represented as uploaded to GitHub. Onward: physically resolve target BG/FG camera alignment and actor/FG natural contact in staging, then only promote files whose complete four-layer evidence passes. Existing other HSK6 HOLDs remain protected.

No GitHub Actions, no lock or canonical source changes; commit `[skip ci]`, no force-push.
