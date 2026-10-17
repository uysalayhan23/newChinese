# HSK6 SC032 / SC038 — real V4 rerun, floor corridor and alternate-camera source rejection (2026-10-17)

Repository: `uysalayhan23/newChinese` `main`, verified starting HEAD `1d0dfc05366f12d61fb8085d235ebbec5e849abf`. This is **QA evidence only**. Neither target has a scene-specific canonical background/foreground nor approved production preview. No production media/counters/LOCKS changes.

## Actual binary V4 source rebuild and checks

Used the user's original physical `hsk6.zip`, original physical V3 staging ZIP and the **original V4 Pillow generator script**, executed again. The outputs matched the previously materialized user V4 staging archive for **both SC032 and SC038 byte-for-byte**:

| Binary, both scenes | Real encoded bytes | Git blob SHA | Actual Pillow dimensions |
|---|---:|---|---|
| V4 right-only FG | 84614 | `84631be9ed27a64a29e134e84037919b23277440` | 720×1280 RGBA |
| V4 PREVIEW | 215124 | `ca8c43043c628d2b69ef7e59625bca49f1586533` | 720×1280 RGB |

Original SC035 donor BG `b0ba989e06045ea92a0c4fd6ebf580877f4acc48`, donor FG `dd7b43d996a33e40ff2c5cf86b5c4fa297238061`, source Zhang Wei `44a7a521b7fa64466111c30f6830904081c3767d` and Chen Yu `ee14b09ae3c8cc4f5e539a54884798900f2ad85b` also matched the raw ZIP data / current GitHub source tree.

The **V4 whole-object reassignment** (omit complete left FG component because the left counter already appears in immutable BG, preserve full right FG object) again achieves **0 actor A/FG alpha≥80 intersections, 0 actor B/FG intersections and 0 actor–actor intersections**; earlier exact V3 value was 726 overlapped hand pixels. Original source and V4 candidate binaries were not edited.

## New independent foot/camera screen-space measurement

Using real source alpha and original exact staged crop/placement dimensions, independently measured with threshold alpha≥80:
- Zhang Wei: visible end y=1203; ground-band shoe x range 148..359.
- Chen Yu: visible end y=1200; shoe x range 579..628. The older report gave y=1203/1203 using a different nonzero-alpha criterion. This **is a threshold distinction**, not newly altered foot artwork.
- Re-evaluated previously detected donor SC035 background ground/counter line segments. Their four intersection median is **(379.25,396.25)** px. At y=1203, the two corridor-edge proxies imply x≈**150.14..680.24** px. Zhang Wei's left-most shoe alpha extends about **2.14 px** left of this approximate corridor edge; Chen Yu's measured shoe range lies inside. A 2-px deviation in a Hough-derived line is within plausible line-selection uncertainty. **No camera or foot geometry acceptance** follows from this observation.

The tool's true-image QA overlay and reproduction script are in downloadable non-production QA bundle `HSK6_SC032_SC038_V4_FLOOR_GROUNDING_QA_ONLY_20261017.zip`, SHA256 `038b7951a67c14e5f454df5c87f8047df36933ae23f176c61bbef5076b637da3`. Bundle includes donor-labelled BG, unchanged canonical character WebPs, V4 foreground, V4 preview for each target. It must **NOT** be presented as canonical source upload.

## Tested other electronics-store source cameras — no promotion

Physically inspected GitHub `fetch_file(base64)` for HSK3_SC042 BG/FG (also identical HSK5_SC002) and HSK5_SC008 BG/FG. Parsed actual RIFF/WebP dimensions from original bytes:
- HSK3_SC042 / HSK5_SC002: **360×640 BG and RGBA FG**, different shop shelves/windows and large bottom foreground accessory table. BG `bc540d14e120afa06e8766a9e574c41470211a6a`, FG `0bf5404580c38c70f8c185e9b9a45d1dc62bfc56`.
- HSK5_SC008: **576×1024 BG and RGBA FG**, different shop framing and a broad bottom product-counter FG. BG `c0a8cd2fdace1ed57ca5690ae030b00e5b3d0549`, FG `71931bdfc24c20f853887c612cdc4c14608df917`.

Both alternatives are **below actual 720×1280**, have distinct foreground/depth and camera framing, and lack independent target-camera matching approval. Upscaling would not add real detail; neither qualifies as a safe canonical source substitute for SC032/038.

## GitHub binary gate remains HOLD

Direct GitHub blob queries for exact V4 FG `84631be9...` and preview `ca8c4304...` both returned **404**, and recursive `main` tree contains none of the four target canonical BG/FG/preview paths. Real local bytes were **not** submitted to `create_blob(base64)` in this pass: the authenticated GitHub connector does not accept a container filepath and no verified source-bytes bridge exists. Local exact SHA != GitHub upload PASS.

- `SC032`: dialogue/Location Bible grounding approved, **layerPlan=false**, V4 staging physical PASS; camera homography, numeric target preset, target BG/FG, production preview **HOLD**.
- `SC038`: separately same condition; identical staging artwork does not approve a distinct `CAM_HSK6_SC038_01` camera.
- SC026 and other HOLD/LOCKS unchanged. The global Zhang Wei HSK1–HSK6 identity audit stays LAST `P999`, unstarted.

**Next release gate:** obtain an independently grounded target-camera source image or approved camera equivalence with numeric / geometric evidence; create four actual scene-specific source layers; check floor contact, fixed objects, faces/hands occlusion and safe zones; then upload exact verified WebPs and round-trip SHA through GitHub before any acceptance claim. No Actions, only `[skip ci]`, no force push.
