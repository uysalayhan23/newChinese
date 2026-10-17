# HSK6 SC026/032/038 — physical V3 staging WebP upload; SC032/038 FG shift feasibility HOLD (2026-10-17)

Base `a971edc2fac38dc282dea502236339dcfc79648a`, `uysalayhan23/newChinese/main`. This record documents actual WebP transport to **QA-PENDING STAGING ONLY**, not promotion or final visual acceptance.

## Exact physical WebP staging upload

Two UNIQUE original locally decoded V3 candidate WebPs were transported using exact Base64 from the physically checked Pillow RGB 720×1280 files and `create_blob(base64)`. GitHub returned the EXPECTED immutable blob SHA for both images (SHA verified before any tree change):
- **SC026:** `363694` bytes, SHA-256 `52ad32504d743de4508306eae7319ca036d728afd902bd879311a6b78b4defe9`, Git blob `9fd2fdb63ee437a741ca43a47ba2defdd6ce7c83`.
- **SC032/SC038:** `215396` bytes each, SHA-256 `8ee78c592a10324fb906caf7daf0a58cc5cfc588c28005468000f8c2ac70b3e4`, one shared byte-identical blob `1226b4b39bfe0bbdef938ea392488c071fa251e4`.

Paths newly added:
- `staging/hsk6/qa_pending/sc026/hsk6_sc026_safe_placement_v3_staging.webp`
- `staging/hsk6/qa_pending/sc032/hsk6_sc032_safe_placement_v3_staging.webp`
- `staging/hsk6/qa_pending/sc038/hsk6_sc038_safe_placement_v3_staging.webp`

The three staging JSON QA records from previous `a971edc2` already pin these source references, exact WebP blobs, positions and original vs V3 alpha/foot measurements. The original 4 source WebPs per scene remain untouched. Exact GitHub round-trip by path and SHA MUST be independently checked after the new commit; **do not claim that check based solely on this text**.

## New exact pixel locality / feasibility

Real original 720×1280 RGB BG, both unchanged RGBA characters and unaltered donor FG were decoded from user-provided `hsk6.zip` and the existing V2 sidecars. Under the exact pre-existing crop/Lanczos/alpha>=80 compositing method, moving character A at fixed vertical (+1px) position for SC032/SC038 across **73 horizontal shifts from -32 to +40px** yielded:
- Best shift with **zero actor–actor alpha collisions:** `dx=+4,dy=+1` (V3), with **726 FG-intersection pixels**, one overlap region bounding `x=82..110,y=785..833`.
- At `dx=+5`: 685 FG pixels but 2 actor-collision pixels.
- At `dx=+6`: 642 FG pixels but 10 actor-collision pixels.
- **No** tested x-only fixed-foot configuration eliminates BOTH collisions without changing source art, scale, B position or foreground. This is a *scope-limited feasibility result*, not proof that no art solution could exist.

The 726 pixels occur beside the left-side shop counter in a speaking-arm area; this needs visual hand/gesture/FG geometry review. Do NOT disguise by deleting source foreground or actor alpha. The store donor has location match but donor camera ID `CAM_HSK6_SC035_01` differs from target `CAM_HSK6_SC032_01` and `CAM_HSK6_SC038_01`; exact perspective calibration, ground-plane vanishing geometry and layerPlan approval remain missing. **The production target BG+FG pair for each scene (6 files overall) and three production previews do not exist.** Canonical four-layer acceptance is not established. SC026's V3 FG overlap=0 in this fixed proxy but cannot certify calibrated geometry either.

## Safeguards

- Production `content/hsk6/sc026|032|038/assets` untouched; 40/50 existing previews preserved.
- `visual_grounding.json` scene context/location approvals retained; `layerPlan.approved=false` and `visualQa` HOLD unchanged.
- No source WebP, LOCKS, scene dialogue, audio, status counters, accepted image or Golden demo changed.
- **P999** HSK1–HSK6 Zhang Wei comparison is LAST, user deferred; do not start.
- Other HSK6 HOLDs unaffected. No Actions, `[skip ci]`, no force push.

**Decision:** `V3_SOURCE_AND_BINARY_STAGING_PASS; SC032_038_FG_GESTURE_AND_CAMERA_HOLD; CANONICAL_BGFG_MISSING; PRODUCTION_NOT_PROMOTED`. Required next: approved per-scene BG/FG camera reconstruction and safe foreground with natural gesture occlusion, independently verified before promoting any production binary.
