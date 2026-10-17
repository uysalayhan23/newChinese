# HSK6 SC026 / SC032 / SC038 — scene context and location grounding closure; 4-layer camera hold (2026-10-17)

Base `8a4c075347bc124b9aff23905649689a55791b01` on `uysalayhan23/newChinese/main`. Scope: strictly text-only scene grounding and QA evidence, no art/manifest/status/counter/LOCKS edits.

## New evidence, exact physical WebP and Git source SHA

Read all 108 locked dialogue lines from GitHub for SC026/032/038 (36 per scene, 18 lines per speaker, character/voice mapping intact), three scene+visual manifests, two Location Bibles, prior donor-approved grounding, and previous/next scene location metadata. All input `scene.json`, `dialogue.json`, `visual_manifest.json` SHA values are pinned in each new `visual_grounding.json`.

Actual WebPs of donor background, foreground, both target actors, and the V2 staging preview for each scene were independently decoded using Pillow from original `hsk6.zip` and `NewChinese_HSK6_SC026_SC032_SC038_STAGE_V2_QA_BUNDLE_20261016.zip`. Exact Git blob hashes matched source QA sidecars and remote tree pins (4/4 source layers per scene). Each preview is RGB 720×1280; actor alpha and FG transparency physically verified. **This is staging source verification only**, not the missing scene BG/FG existing in production.

| Scene | Donor | Staging preview Git SHA | Actual source hashes | V2 adult actor relative image-height ratio | FG alpha >=80 distribution (top/middle/bottom thirds) |
| --- | --- | --- | --- | --- | --- |
| SC026 | SC023 | `ceca83f32fe89c510844de4820c22c379f207f88` | all 4/4 PASS | 0.8293 | 15.1932% / 6.8026% / 0% |
| SC032 | SC035 | `5398498273bbf47abaa10445f9775f71304dff0b` | all 4/4 PASS | 0.8100 | 2.3237% / 21.9796% / 3.7656% |
| SC038 | SC035 | `5398498273bbf47abaa10445f9775f71304dff0b` | all 4/4 PASS | 0.8100 | 2.3237% / 21.9796% / 3.7656% |

Real preview visual side-by-side review shows background identity with the same-location donor, without evidence that the scene-specific camera presets are calibrated. Pixel region occupancy quantifies where foreground art is non-transparent, **not** photographic perspective. The earlier QA sidecar reports actor A FG head overlaps 0.3127% for SC026 and 0.3414% for SC032/038, torso/gesture overlaps 0.1226% and 1.4960%, and shared actor foot baseline y=1210; these are **sidecar measurements**, not independently recalculated in this pass. Do not infer actor identity or floor-plane validity from shared feet lines.

## LOCKED_STEP_17 two-stage approvals — limited scope

Three new files:
- `content/hsk6/sc026/visual_grounding.json`
- `content/hsk6/sc032/visual_grounding.json`
- `content/hsk6/sc038/visual_grounding.json`

For **each**: `sceneContext.status=approved` (all 36 locked lines, topic/tone/cast/mood, no mandatory prop interaction, previous/next transitions) and `locationMatch.status=approved` with `approvedForLayerPlanning=true`, limited to location and dialogue metadata. This is **permission to plan**, not permission to import a donor layer or to accept production art.

All three `layerPlan.approved=false` and `visualQa.status=HOLD_BGFG_CAMERA_SCALE_PRODUCTION_NOT_APPROVED`. Target `CAM_HSK6_SC026_01`, `CAM_HSK6_SC032_01`, `CAM_HSK6_SC038_01` are distinct from donor presets `CAM_HSK6_SC023_01` and `CAM_HSK6_SC035_01`. No intrinsic calibrated camera parameters or ground-plane source proof currently establishes an exact copy mapping. Six target BG/FG files and all three production previews are still physically absent. The Zhang Wei *global* HSK1–HSK6 character comparison remains **the last queue item** (`P999`), not started, as the user requested; the local actor source pixels were not modified.

### HOLD and next gate

- Source / staging physical checks: **PASS**, exact checked scope above.
- SC026 / SC032 / SC038 scene-context and location grounding from locked dialogue: **APPROVED**, metadata scope only.
- Final 4-layer plan, canonical BG/FG camera/scale and foreground occlusion, scene image identity, scene acceptance: **HOLD**. No production pass.
- Next: establish camera-calibrated source BG/FG or camera-equivalent donor evidence, independently verify actor footprint and scene-specific foreground occlusion; only then approve a 4-layer plan, source final art, and regenerate single 9:16 preview without replacing protected image binaries.
- SC013/019 home geometry, SC020 shadow v3, SC022 railing and SC016/042/045/048 HOME missing sources remain HOLD.

Existing 40/50 preview path count unchanged; no `visual_manifest.json`, `media_status.json`, LOCKS, dialogue, canonical artwork or accepted counters modified. No GitHub Actions; commit `[skip ci]`, force-push forbidden.
