# HSK6 SC026/032/038 — V3 physical staging GitHub round-trip & foreground-hand occlusion (2026-10-17)

Original source HEAD `a971edc2fac38dc282dea502236339dcfc79648a`; binary staging asset commit `3c353ff5835163472f27adbeef4443899a1e192b` on `uysalayhan23/newChinese/main`. This is exact transfer verification, NOT production approval.

## Real GitHub staging WebP round-trip: 3/3 PASS

Verified `create_blob(base64)` returned the exact SHA computed from the original, physically decoded Pillow RGB 720×1280 binaries. Attached three paths only under `staging/hsk6/qa_pending/` and committed once without force push. **After commit**, fetched each of the three GitHub file paths by immutable SHA ref with `encoding=base64`, compared the entire decoded source representation to the original Base64 byte-for-byte (whitespace-normalized for transport), and independently checked each returned Git blob SHA:

| Scene | Staging path under `staging/hsk6/qa_pending` | Bytes | Expected and returned Git blob SHA | Full Base64 equality |
|---|---|---:|---|---|
| SC026 | `sc026/hsk6_sc026_safe_placement_v3_staging.webp` | 363694 | `9fd2fdb63ee437a741ca43a47ba2defdd6ce7c83` | **PASS** |
| SC032 | `sc032/hsk6_sc032_safe_placement_v3_staging.webp` | 215396 | `1226b4b39bfe0bbdef938ea392488c071fa251e4` | **PASS** |
| SC038 | `sc038/hsk6_sc038_safe_placement_v3_staging.webp` | 215396 | `1226b4b39bfe0bbdef938ea392488c071fa251e4` | **PASS** |

SC032/038 physically share the one exact Git blob but have distinct staging paths and distinct dialogue/camera manifest IDs. The V3 candidate sources and source SHA pins are in `safe_placement_v3_binary_evidence_20261017.json` per scene. No runtime production WebP added.

## Exact FG issue is a speaking-hand occlusion, not a cosmetic numeric issue

Independently evaluated the original physical SC035 donor foreground alpha with the unchanged source actor A alpha at their V3 composited placement, threshold `alpha >=80`. **726 pixels** remain in one connected region `x=82..110, y=785..833` (inclusive). Visual cropping against the actual V3 scene confirms these pixels overlap Zhang Wei's **left outstretched speaking hand**, where a diagonal shop cabinet/counter edge occludes fingers/palm. Since `LOCKED_STEP_17_VISUAL_SYSTEM.md` prohibits masking faces/torsos/**speaking gestures**, this is a real foreground-geometry QA HOLD. The local QA PNG `HSK6_SC032_SC038_V3_FG_726PX_LOCALIZED_QA_20261017.png` colors exact collisions red; PNG is local evidence, not production art.

A constrained sweep of **73** actor-A horizontal offsets (`dx -32..40`) at unchanged actor scale, B position, FG and aligned visible foot baseline found:
- Best 0 actor-vs-actor collision position: V3 `dx=+4,dy=+1` with 726 foreground/hand intersection pixels.
- `dx=+5` reduces FG intersections to 685 but creates **2** actor collisions.
- `dx=+6` reduces FG intersections to 642 but creates **10** actor collisions.
- **No zero-foreground-and-zero-actor-collision solution within the constrained search.** This does not rule out genuinely new camera-correct art or approved geometric reconstruction. Do not hack around it with synthetic masking or silently change canonical FG, scale, actors or draw order.

### Remaining gates

SC026: V3 zero FG collision proxy and aligned visible feet, but camera/ground-plane and source BG/FG still HOLD. SC032/038: speaking hand covered by SC035 FG donor and no zero-constraint actor translation. All three target BG/FG canonical physical paths are missing (six absent) and all three production preview paths absent; donor camera IDs differ from targets. No camera intrinsics/extrinsics/homography were provided. `layerPlan.approved=false`, `visualQa` HOLD, original 40/50 production preview paths unchanged. User-deferred full HSK1–HSK6 Zhang Wei review remains the last `P999` queue item, not started.

Only a new closure document is committed here. Production assets, character sources, manifest, LOCKS, dialogue, audio, media_status and acceptance counters were not changed. GitHub Actions must not run; all commits use `[skip ci]`, no force push.
