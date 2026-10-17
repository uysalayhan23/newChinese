# HSK6 SC026 / SC032 / SC038 — locked dialogue-grounding draft and QA gates (2026-10-17)

Repository `uysalayhan23/newChinese`, `main`; validated source HEAD `0455b540b59b5ca62af1978c327521c8e258b624`.
**DRAFT / HOLD / NO PRODUCTION PROMOTION.** This review does not approve `visual_grounding.json` or a layer plan. It preserves `LOCKED_STEP_17_VISUAL_SYSTEM.md`, all scene/dialogue content, accepted canonical layers, manifest/status and full-scene acceptance counts.

## Source-based review completed

Read all **36/36 locked `dialogue.json` lines** for each of the three scenes (108 total); `status=locked-reference`; speakers each alternate with **18/18 lines**, each with their prescribed Zhang Wei/Liu Mei or Zhang Wei/Chen Yu voice ID. `scene.json`, `visual_manifest.json`, `visual_production_queue.json` and matching Location Bibles were read for each. This is a source/role/metadata audit, not proof of scene-specific camera calibration.

| Scene | Dialogue topic and evidence | Characters | Manifest location and authoritative Bible | Adjacent scene boundaries |
| --- | --- | --- | --- | --- |
| HSK6_SC026 | `人口流动`, `L001` / `L019` / `L033`: population mobility, changing perspectives, weighing consequences | Zhang Wei (`CHAR_ZHANG_WEI_001`), Liu Mei (`CHAR_LIU_MEI_001`) | `LOC_NEIGHBORHOOD_001`, `locations/LOC_NEIGHBORHOOD_001/visual_bible.json`: tree-lined Hangzhou residential street, small park, storefronts | `SC025 LOC_WEST_LAKE_001` → `SC026` → `SC027 LOC_COMMUNITY_CENTER_001` |
| HSK6_SC032 | `人类判断的价值`, `L001` / `L019` / `L024`: human judgment, trustworthy facts, justice, long-term impact | Zhang Wei (`CHAR_ZHANG_WEI_001`), Chen Yu (`CHAR_CHEN_YU_001`) | `LOC_ELECTRONICS_STORE_001`, `locations/LOC_ELECTRONICS_STORE_001/visual_bible.json`: mobile-accessory and headphone displays, device demonstration tables, neat shelves | `SC031 LOC_ZHANG_OFFICE_001` → `SC032` → `SC033 LOC_PUBLIC_LIBRARY_001` |
| HSK6_SC038 | `数字身份`, `L001` / `L019` / `L033`: digital identity, evaluating evidence and responsible decisions | Zhang Wei (`CHAR_ZHANG_WEI_001`), Chen Yu (`CHAR_CHEN_YU_001`) | `LOC_ELECTRONICS_STORE_001`, same location bible but **independent** scene/camera ID | `SC037 LOC_ZHANG_OFFICE_001` → `SC038` → `SC039 LOC_PUBLIC_LIBRARY_001` |

### A. Candidate Scene Context Grounding — REVIEW_PENDING (not approved)

- **Purpose/mood:** all three are 36-line reflective HSK6 dialogues, calm/analytical/respectful tone and two adult conversational actors. Main physical action: face-to-face spoken discussion with non-obscuring natural small hand gestures. The locked text does **not** establish a required physical prop interaction such as picking up a phone, pointing at an object or walking; do not invent such an action.
- **Visible surroundings** are *location-based staging candidates*, not dialogue-mandated props. SC026: tree-lined sidewalk and nearby residential storefronts; SC032/038: consumer-electronics displays and accessory shelving. No baked readable signage or subtitles.
- **Continuity:** preceding and following scenes use different locations. Do not carry over cameras, lighting poses or outfits merely because Zhang Wei recurs.
- **Mobile composition:** single 720×1280 textless vertical preview derived from BG+two transparent characters+subtle RGBA FG only, faces/hands/gestures visible; bubble is an app overlay. These constraints are locked requirements, not independent visual PASS.

### B. Candidate Location Matching — REVIEW_PENDING, approvedForLayerPlanning=false

The scene ID, scene/manifest location and visual production queue agree for each target. The reflective locked dialogue does not contradict its specified location, but does not independently prove a particular camera preset. Prior `SC023` (neighborhood) and `SC035` (electronics store) have source-grounded same-location layers, **not interchangeable scene-specific approval**:

| Target | Reference BG Git blob | Reference FG Git blob | Required independent camera |
| --- | --- | --- | --- |
| SC026 (donor SC023) | `a0fda64fd0732d378d2648a48d058edfb4fca015` | `5da1b87d0e43673ce2259c2759c88569f8cae81e` | `CAM_HSK6_SC026_01` vs donor `CAM_HSK6_SC023_01` |
| SC032 / SC038 (donor SC035) | `b0ba989e06045ea92a0c4fd6ebf580877f4acc48` | `dd7b43d996a33e40ff2c5cf86b5c4fa297238061` | `CAM_HSK6_SC032_01` and `CAM_HSK6_SC038_01` vs donor `CAM_HSK6_SC035_01` |

**Unresolved gates:** SC026/SC032/SC038 target BG and FG binary files are missing (six paths); production previews missing (three paths). Physical staging 720×1280 candidates and pre-existing FG alpha-overlap proxy PASS do not prove camera depth, adult canonical character appearance, apparent height, foreground occlusion or completion. No `content/hsk6/sc026|032|038/visual_grounding.json` approval files exist at source HEAD. Therefore **no approved layer plan** may be generated yet under `LOCKED_STEP_17`.

### Next immediate work, without the deferred global character comparison

1. Independent QA review/approval of these scene-specific context and location candidates; verify exact dialogue evidence and adjacent-scene boundaries.
2. **Then** draft/approve camera-calibrated BG/characterA/characterB/FG/PREVIEW layer plans. Verify actual floor plane, alpha occlusion and UI safe areas with real files before producing/publishing final source BG/FG.
3. Keep SC026/032/038 `HOLD`; retain SC013/019 home depth, SC020 shadow-v3 staging, SC022 railing/scale and SC016/042/045/048 missing-home BG/FG HOLD.
4. The cross-level Zhang Wei HSK1–HSK6 visual comparison is **not** this phase: user explicitly moved it to the very end of `content/visual_regeneration_queue.json` as `P999_FINAL_HSK1_HSK6_ZHANG_WEI_CANONICAL_VISUAL_REVIEW` (priority 999, not started). Do not quietly begin, regenerate or overwrite any actor sources now.

No Actions or force-push. All commits `[skip ci]`. Scene acceptance and production preview count stay unchanged at 40/50.
