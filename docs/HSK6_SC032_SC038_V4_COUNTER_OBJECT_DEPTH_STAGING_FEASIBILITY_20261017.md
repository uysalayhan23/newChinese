# HSK6_SC032/SC038 V4 whole-object foreground depth alternative — real Pillow QA, camera HOLD (2026-10-17)

Repository `uysalayhan23/newChinese/main`, starting HEAD `4081704d21ca2c30c6541874b5b38f44f0e2cda7`. **Local-only QA staging**. This audit does NOT mark production complete, alter any canonical asset or authorize a new camera. SC026 remains unchanged/HOLD. The HSK1–HSK6 global Zhang Wei identity review stays LAST (P999), not started.

## Source and V3 provenance (actual binary)
- Fetched remote GitHub V3 SHA pins `1226b4b39bfe0bbdef938ea392488c071fa251e4` for both SC032 and SC038 (RGB 720×1280, 215396 bytes). Read locally available independently provided physical V3 ZIP, verified both physical WebPs decode with Pillow and bytes hash to the *same Git blob SHA*. Re-rendered the exact original `hsk6.zip` four layers with V3 positions, reproducing the immutable V3 WEBP **byte-for-byte**.
- Original donor SC035 BG Git blob `b0ba989e06045ea92a0c4fd6ebf580877f4acc48`, donor FG Git blob `dd7b43d996a33e40ff2c5cf86b5c4fa297238061`, source Zhang Wei `44a7a521b7fa64466111c30f6830904081c3767d`, Chen Yu `ee14b09ae3c8cc4f5e539a54884798900f2ad85b`. All source hashes checked against raw bytes. No original binary changed.

## Geometry finding: two entirely disjoint counter FG objects
Full donor FG nonzero-alpha x ranges are **0–122 (left cabinet)** and **617–719 (right cabinet)**. The 494-column x=123..616 gap has exactly zero original alpha. Original donor BG **already contains the complete visible left cabinet**, therefore a physically valid *depth allocation hypothesis* is: left cabinet stays in immutable BG behind actors; right counter remains the foreground. This removes the **entire** separate left FG object—there is **no pixel-by-pixel hand masking**, patching, inpainting, actor erase or hand-specific clipping.

An entirely *new, target-only local staging FG* (720×1280 RGBA, lossless WebP) was derived, preserving the right RGBA component pixel-for-pixel in visible-alpha pixels. Original BG and original donor FG binary files remain untouched. Original V3 actor positions and dimensions unchanged; generated new V4 single-image staging preview (720×1280 RGB WebP). This is only a camera/depth proposal, not an acceptance of a new canonical target FG.

### Real V3 → V4 pixel QA (Pillow)

| Metric | V3 | V4 candidate |
|---|---:|---:|
| Left outstretched hand overlapped by FG at alpha >=80 | 726 pixels, x82..110,y785..833 | **0 pixels** |
| Actor–actor alpha>=80 overlap | 0 | 0 |
| Actor B vs FG | 0 | 0 |
| Visible feet A/B y | 1203 / 1203 | 1203 / 1203 |
| Right FG component pixel identity | source | **preserved** |

When comparing the *unchanged BG* to the complete donor FG overlay within the removed left component (x0..122), average absolute RGB-channel difference is **0.2851** levels, 95th percentile **2**, maximum **16** (8-bit RGB). Thus the BG already closely reproduces the cabinet; no empty hole was exposed by object-level depth reassignment. The V4 preview's decoded bitmap differs from lossy V3 at 80104 pixel locations including lossy re-encoding effects; that is **not** an exact camera/screen equality test.

The staging variant regenerated a second time from the exact same physical sources with **byte-identical outputs** for FG and preview for both scenes. SC032 and SC038 are byte-identical *source/image hypotheses*, but remain distinct dialogue/camera scenes.

| Staging binary | Bytes | Git blob SHA |
|---|---:|---|
| new RGBA right-only FG (both) | 84614 | `84631be9ed27a64a29e134e84037919b23277440` |
| new RGB 720×1280 V4 preview (both) | 215124 | `ca8c43043c628d2b69ef7e59625bca49f1586533` |

**Transfer status:** These newly generated WebPs are in the locally verified downloadable `NewChinese_HSK6_SC032_SC038_V4_COUNTER_DEPTH_QA_20261017.zip`. They have **NOT** been uploaded as binary GitHub blobs. GitHub only receives *text-only provenance QA sidecars* and this report. No false transfer/pass claim.

## Production/LOCKED_STEP_17 gates, still HOLD
- Staging hand occlusion resolution **PASS** for the tested whole-object depth hypothesis only.
- New scene-specific optical camera **HOLD**: donor preset `CAM_HSK6_SC035_01` differs from targets `CAM_HSK6_SC032_01`/`CAM_HSK6_SC038_01`; source camera matrices/homography, perspective floor-plane and canonical BG geometry are not proved. Merely leaving objects in BG cannot prove proper target camera.
- The *target* canonical BG/FG paths for each are still missing, and production previews still missing. `layerPlan.approved=false`, `visualQa` HOLD. A new foreground candidate does not magically supply target canonical approval.
- Local canonical actor adult portrayal/scale was not changed or waived. Full HSK1–HSK6 Zhang Wei continuity is deferred to last P999. No acceptance counts changed, and SC026's original V3 staging pass with camera HOLD is preserved.
- No Actions, no force-push; documentation-only commit `[skip ci]`.

Next: independently approve target camera/ground-plane and object depth semantics from visually suitable source art; verify exact source-to-target target camera parameters/occlusion; then perform four-layer final staging/QA and only produce/publish accepted scene BG/FG/PREVIEW binaries. Other HSK6 HOLDs remain.
