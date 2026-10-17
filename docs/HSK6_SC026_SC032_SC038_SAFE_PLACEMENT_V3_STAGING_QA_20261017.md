# HSK6 SC026/032/038 — reproducible safe-placement V3 staging, source-locked QA (2026-10-17)

Repository: `uysalayhan23/newChinese`, branch `main`. Exact base HEAD `f2e94dbc94827140e0ac5e33e81e19044652e128`. This is **QA-pending staging**, **NOT a production asset promotion**.

## Inputs and physical verification

Used the user's actual `hsk6.zip` WebP layer files and `NewChinese_HSK6_SC026_SC032_SC038_STAGE_V2_QA_BUNDLE_20261016.zip`. Pillow + NumPy independently decoded original 720×1280 RGB donor BG, 2 real transparent canonical character WebPs, original RGBA foreground, and V2 RGB staging preview for each scene. All 4 source layer Git blob SHAs per scene match the source ZIP and remote GitHub's immutable source object metadata.

For the new V3, the same source actor crop + Lanczos resize was preserved, and **only character A's crop placement was shifted**. The original source WebP bytes, actor resize dimensions, source foreground, source background and character B position were never modified. Recombined BG → CHAR_A → CHAR_B → FG and encoded new RGB 720×1280 WebPs. Physically decoded every resulting WebP and checked size/mode and SHA-256/Git blob. A separate full rerun produced **byte-identical** V3 WebPs for all three scenes.

### Before / after, independent alpha-mask ROI

| Scene | Move A | Visible foot-bottom difference old → V3 | FG alpha>=80 overlap with A old → V3 | Head FG overlap old → V3 | Torso FG overlap old → V3 | Actor collisions V3 | V3 git blob |
|---|---|---|---|---|---|---|---|
| SC026 | +8px right, +6px down | -6px → 0px | 117 → 0 pixels | 117 → 0 | 0 → 0 | 0 | `9fd2fdb63ee437a741ca43a47ba2defdd6ce7c83` |
| SC032 | +4px right, +1px down | -1px → 0px | 896 → 726 pixels | 0 → 0 | 896 → 726 | 0 | `1226b4b39bfe0bbdef938ea392488c071fa251e4` |
| SC038 | +4px right, +1px down | -1px → 0px | 896 → 726 pixels | 0 → 0 | 896 → 726 | 0 | `1226b4b39bfe0bbdef938ea392488c071fa251e4` |

The SC032/038 staging previews are byte-identical because source references and placement are identical, but **their dialogue topics and camera preset IDs are still independently locked**. The V3 soft-alpha actor collision mask also remained 0. Measurements are exact for this *algorithm and ROI*, not universal natural perspective evidence. Aligning source-alpha last-visible pixels does not independently prove matching floor plane or optical projection. The old V2 file was lossy WebP and V3 was newly recomposed; this audit does NOT claim lossless pixel equality of previous composites.

## Camera and acceptance gate — HOLD

Source manifest `CAM_HSK6_SC026_01` != donor `CAM_HSK6_SC023_01`; `CAM_HSK6_SC032_01` / `CAM_HSK6_SC038_01` != donor `CAM_HSK6_SC035_01`. No camera intrinsics/extrinsics, target ground-plane homography or validated corresponding vanishing lines were supplied. Shifting cutouts by a few pixels can reduce mask collision but cannot resolve optical camera or canonical adult-character style mismatch. Even after V3:
- SC026/032/038 production target BG/FG **all six files absent**.
- Target production preview **all three files absent**.
- Target `visual_grounding.json` has approved dialogue context + location, but `layerPlan.approved=false`; no art acceptance.
- SC032 and SC038 still have 726 FG-overlap pixels over actor A's torso ROI at alpha>=80.
- Scene-local actor/scale and real camera-depth QA remains HOLD. Per explicit user request, do NOT perform the global HSK1–HSK6 Zhang Wei identity comparison until final queued `P999` task.

### Artifacts

Physically prepared a local QA-only bundle `NewChinese_HSK6_SC026_032_038_STAGING_V3_SAFE_REPOSITION_20261017.zip`: three *real* candidate WebP files, three complete source-verified QA JSON sidecars, before/after QA comparison JPEGs, a reproducible Python/Pillow script, and a README. The ZIP is a conversation deliverable; **no V3 WebP binaries were uploaded as GitHub repository blobs**. The three smaller GitHub staging JSON files are pin/provenance records and do not imply media presence on GitHub.

**Disposition:** `V3_STAGING_POSITION_PROXY_PASS / CANONICAL_SOURCE_BGFG_CAMERA_AND_SCENE_VISUAL_HOLD`. Do not write these WebPs to `content/hsk6/scNNN/assets`, change manifest/status, acceptance or LOCKS based on these proxy metrics. Respect all other HSK6 HOLDs. GitHub Actions unused, GitHub commit `[skip ci]`, no force-push.
