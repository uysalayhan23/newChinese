# HSK6 SC032/038 V4 physical recheck, attempted GitHub transport and calibrated-camera BG/FG HOLD (2026-10-17)

Repository: `uysalayhan23/newChinese`, `main`, preaudit HEAD `9cb2eb5a93c726459eb34c10b1520dd978fd62e7`. **QA-only text/metadata commit; no WebP promotion.**

## Actual V4 source and byte comparison
Unzipped physical Library snapshot `NewChinese_HSK6_SC032_SC038_V4_COUNTER_DEPTH_QA_20261017.zip` (1,800,978 B, SHA256 `35db68ad9b30060baca5c55b8a53c6abe1b790bf603a9c94561fdffde0802701`) and independent verified copy `NewChinese_HSK6_SC032_SC038_V4_VERIFIED_STAGING_NOT_PRODUCTION_20261017.zip` (990,207 B, SHA256 `893b9973724419e04fa03d3df5609e18cbf4f053dee174d17624e820f5cea7d8`). Both ZIP CRC checks PASS. All four physically stored V4 WebPs decode with Pillow. The two target FGs are byte-identical; likewise the two target PREVIEWs.

- V4 **FG** RGBA WebP 720×1280, **84,614 bytes**, exact Git blob `84631be9ed27a64a29e134e84037919b23277440`, SHA256 `c79a0c4dbfbc6807a94c598afd378682213894fd992356fcfe3cd3b66bcb62aa`.
- V4 **preview** RGB WebP 720×1280, **215,124 bytes**, exact Git blob `ca8c43043c628d2b69ef7e59625bca49f1586533`, SHA256 `5a69c580d7a85d160eae0602f956440b3800bd39dd07b80363c13de05f6bc5bc`.
- Original source archive `hsk6.zip` BG `b0ba989e06045ea92a0c4fd6ebf580877f4acc48`, FG `dd7b43d996a33e40ff2c5cf86b5c4fa297238061`, Zhang Wei `44a7a521b7fa64466111c30f6830904081c3767d`, Chen Yu `ee14b09ae3c8cc4f5e539a54884798900f2ad85b` again match remote source SHA; the originals remain byte-for-byte unchanged.
- Independently decoded original donor FG and new V4 FG to RGBA and compared **all actual visible-right FG RGBA pixels** and right-region alpha, without trusting preview encoder equality. Original left cabinet: 40,417 positive-alpha pixels / 33,617 alpha>=80. New V4 left: **0**; middle alpha **0**. Original and V4 right: 63,211 positive-alpha / 52,651 alpha>=80, **zero changed visible-right RGBA pixels and zero changed right alpha pixels**. The original BG already contains left-cabinet geometry. This PASS is limited to a **whole-object foreground-depth staging alternative**; no actor or canonical pixels were overwritten.
- Earlier controlled actor collision check V3→V4 was 726→0 overlapped speaking-hand pixels and actor-to-actor 0; it is prior evidence, not independently rerun in this pass.

## Binary transport — NOT verified
- Actual local V4 bytes were inspected and their exact Base64 text was prepared locally for a potential `create_blob(encoding=base64)` upload. However, connected GitHub write calls do **not** directly accept the local file path, and there is no verified trusted connector bridge of those exact bytes into the authenticated Base64 `content` parameter here. A file view / export or re-encoded image is *not* a byte-preserving Git upload.
- Queried GitHub exact blob GET for both expected SHAs on this HEAD: **404 NOT FOUND for both**. No `create_blob` success, tree insertion, commit of binary WebPs or byte-for-byte GitHub backread was observed. Thus **BINARY_TRANSPORT_HOLD**. `staging/hsk6/qa_pending/SC032_SC038_V4_BINARY_TRANSFER_GATE_20261017.json` records the exact four desired staging-only paths, their original SHA pins and this attempt.
- Strictly **do not claim GitHub V4 upload PASS**, do not place Base64 text at a `.webp` path and do not copy identical V4 staging candidates into production `content` paths without camera and canonical QA.

## Target-camera/canonical remediation
`CAM_HSK6_SC035_01` donor and target IDs `CAM_HSK6_SC032_01` / `CAM_HSK6_SC038_01` differ. Neither scene+visual manifests nor available camera-oriented repository search provided a calibrated perspective transform, camera parameters, ground-plane calibration or target-specific camera-equivalence signoff. Identical Location Bible (`LOC_ELECTRONICS_STORE_001`), right-FG pixel conservation, adjusted hands and y=1203 foot endpoints cannot substantiate that equivalence.

For **each SC032 and SC038**, the canonical target BG/FG and production preview paths remain missing. Follow `LOCKED_STEP_17`: source physically grounded target-camera BG, transparent canonical actor A/B and depth-correct FG; validate vanishing-line/floor-plane geometry, real alpha occlusion and mobile UI safe areas; independently reproduce single-scene preview; only then consider approved layer plan, canonical publishing, counters. No stage art promoted on metadata-only location match.

**Decisions:** exact local V4 source + foreground separation **PASS**; Github binary upload, source-specific camera, canonical BG/FG, full four-layer acceptance **HOLD**. SC026 remains independently HOLD, all other HSK6 HOLD preserved. Global Zhang Wei cross-level review remains final P999 task, not started. No Actions, no force push, `[skip ci]`.
