# HSK6 SC032 / SC038 — stage-V4 real camera-floor proxy and per-scene canonical BG/FG gate (2026-10-17)

Repository `uysalayhan23/newChinese`, starting HEAD `6f1ac13ced03cfc473c534e4afe217b0fbb36ba3`. **QA-only; no production artwork, asset status, visual manifest, accepted images, or LOCKS changed.**

## New actual measurements

Reopened physical original user archive `hsk6.zip` and both existing local V4 staging WebPs from `NewChinese_HSK6_SC032_SC038_V4_COUNTER_DEPTH_QA_20261017.zip`. Pillow decoded BG, FG and V4 candidate; SHA and byte sizes match:
- Donor SC035 BG `b0ba989e06045ea92a0c4fd6ebf580877f4acc48`, original FG `dd7b43d996a33e40ff2c5cf86b5c4fa297238061`; target Zhang Wei `44a7a521b7fa64466111c30f6830904081c3767d`; Chen Yu `ee14b09ae3c8cc4f5e539a54884798900f2ad85b`.
- **V4 FG** same scene-wise bytes, RGBA 720×1280, 84,614 B, Git blob `84631be9ed27a64a29e134e84037919b23277440`.
- **V4 preview** same scene-wise bytes, RGB 720×1280, 215,124 B, Git blob `ca8c43043c628d2b69ef7e59625bca49f1586533`.
- Independently verified alpha of V4 FG: original left separate object alpha≥80 **33,617 pixels**, V4 left **0**; original right object **52,651 pixels alpha≥80** and visible right-region RGBA unchanged in V4. Left cabinet remains part of original SC035 BG. Source image bytes unchanged. Prior V3/V4 real mask QA measured hand/FG intersection **726→0** and foot y **1203/1203**. This rerun tested physical right-island pixel identity, not a new actor mask or character face QA.

### Newly measured image-space perspective (DONOR camera only)

OpenCV 4.13.0 deterministic Canny(50,150) and HoughLinesP on the original SC035 background region y=500..1249:
- Lines L1 (38,898)→(247,589), L2 (137,1249)→(209,997).
- Lines R1 (563,627)→(719,834), R2 (620,1047)→(698,1249).
- Pairwise intersections at x/y **(382.92,388.05), (371.86,404.39), (382.97,388.11), (375.57,414.00)**; median ≈**(379.25,396.25)** pixels.

The detected floor/counter corridor edges converge consistently **within the SC035 donor background**. Since V4 uses the original donor BG without geometric transformation, the *staging candidate* preserves donor perspective in that image space. A vanishing-point proxy from one image **does not** establish actual lens parameters, target ground-plane homography or equivalence to target `CAM_HSK6_SC032_01` and `CAM_HSK6_SC038_01`. Do not mark camera calibration PASS on this basis. These separate target scene IDs must each retain a distinct review record.

### Alternate canonical donor check — no unproven substitution

Live GitHub recursive tree shows HSK3_SC042 and HSK5_SC002 share the same electronics-store BG (`bc540d14e120afa06e8766a9e574c41470211a6a`), FG (`0bf5404580c38c70f8c185e9b9a45d1dc62bfc56`) and preview (`1d893f8b0db949bb999910e534c64433fbceeeed`) SHA. HSK5_SC008 uses **different** BG (`c0a8cd2fdace1ed57ca5690ae030b00e5b3d0549`), FG (`71931bdfc24c20f853887c612cdc4c14608df917`) and character asset SHAs but the **same preview blob** `1d893f8b0db949bb999910e534c64433fbceeeed`. Thus a scene metadata `visual-assets-complete` label is not itself a pixel-level camera/visual-continuity certification; older same-location candidates require fresh four-layer QA and are not promoted as replacements.

## Release-blocking status

| Gate | SC032 | SC038 |
| --- | --- | --- |
| Dialogue/context + Location Bible grounding | approved (metadata only) | approved (metadata only) |
| V4 FG whole-object depth / local binary SHA and WebP decode | PASS | PASS |
| V4 actual GitHub blob creation and binary backread | **NOT VERIFIED; exact two expected blobs still GitHub 404 at audited HEAD** | **NOT VERIFIED** |
| Numeric target camera calibration, scene-specific floor plane | HOLD | HOLD |
| Target canonical BG, FG, and production preview | **all missing** | **all missing** |
| Layer plan and application acceptance | HOLD | HOLD |

Do not mistake physical staging masks for a perspective transform. Need either independently verifiable per-scene target-camera geometry and a compatible original BG, or an explicitly reviewed scene-camera equivalence decision. Then produce target-specific canonical FG under full foreground/hand/face/foot occlusion QA, compose actual runtime four layers and preview, and only then upload binary assets and verify GitHub readback.

SC026 and all other established HOLDs are unchanged. Zhang Wei HSK1–HSK6 **global** identity comparison remains the last P999 queue task, not started. No Actions, force-push or arbitrary branch; `[skip ci]` commit. This record is audit evidence, not a completed repair.
