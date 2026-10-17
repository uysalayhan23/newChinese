# HSK6 SC032/038 V4 — independent binary rerun and camera / staging gate (2026-10-17)

Repository `uysalayhan23/newChinese/main`, verified baseline `4b5f9fce4287cca2a0258fbe80b18b94ff8ca2f1`. **QA-only / HOLD; this is not a media promotion or final scene acceptance.**

## Newly repeated physical proof

Opened the user's original V4 physical ZIP (**1,800,978 B**, SHA-256 `35db68ad9b30060baca5c55b8a53c6abe1b790bf603a9c94561fdffde0802701`) with ZIP CRC verification. All four real source V4 WebPs Pillow-decoded with exact RGB/RGBA 720×1280 dimensions and Git blob SHA/sha256 matches.

Independently **executed** the user's original `prepare_hsk6_sc032_038_counter_depth_candidate_20261017.py` using the original `hsk6.zip` and physical V3 staging ZIP. Real SC035 donor BG/FG and target Zhang Wei/Chen Yu character source SHA pins matched the untouched source WebPs. The original GitHub-pinned V3 WebP was re-created byte-for-byte, then **all four V4 outputs matched the original V4 archive byte-for-byte**. Both scene FG candidates are identical 84,614-B RGBA WebPs (Git blob `84631be9ed27a64a29e134e84037919b23277440`) and both preview candidates are identical 215,124-B RGB WebPs (Git blob `ca8c43043c628d2b69ef7e59625bca49f1586533`).

The original FG has two entirely disjoint depth objects at x=0..122 and x=617..719, with x=123..616 fully transparent. This target-only *staging hypothesis* keeps the entire right FG island and leaves the left counter visible solely in the unchanged donor BG. No hand-specific masking or canonical source pixel rewrite was performed. Actor-A FG intersection `726 → 0` pixels at alpha>=80; actor-B FG intersection and actor-vs-actor collision remain 0; visible foot endings y=1203/1203. The left counter overlay/BG RGB delta mean=0.2851, p95=2 and max=16; none of these automatically proves physical camera calibration.

## Camera, target BG and four-layer scene decision

SC035 reference camera ID `CAM_HSK6_SC035_01` differs from `CAM_HSK6_SC032_01` and `CAM_HSK6_SC038_01`. Neither the GitHub source inventory nor targeted search revealed a validated numeric projection calibration, ground-plane homography, or source-to-target camera-equivalence proof. Matching the electronics-store Location Bible is **location compatibility, not camera equivalence**. Both targets still lack their own canonical BG/FG, neither final four-layer layer plan nor preview/application acceptance is approved. V4 only solves the tested hand/FG occlusion.

**Disposition:** 4/4 local binary reproducibility PASS; V4 staging geometry-proxy PASS; camera, target canonical BG/FG, local actor/scale, four-layer production and full scene acceptance **HOLD**. No production art, source character, manifest, acceptance status or LOCKS modified.

## Exact GitHub binary upload status

Four desired **staging-only** target filenames and per-asset SHA pins are in `staging/hsk6/qa_pending/SC032_SC038_V4_BINARY_TRANSFER_GATE_20261017.json`. This current audit **has not uploaded the real V4 WebP blobs**: the connected GitHub API accepts Base64 data, but this session lacks a verified bridge from actual local binary files to its `content` argument. Local verified SHA is not a GitHub byte-for-byte round-trip. Until exact Git blobs have been created and each path has been read back by GitHub, transport status must be **PENDING**. Do not substitute text or donor binary art or report false PASS.

SC026 and other HSK6 HOLDs preserved. Global Zhang Wei HSK1–HSK6 comparison remains last queue task P999, not started. No Actions; only a documentation + JSON staging gate commit with `[skip ci]` and no force-push.
