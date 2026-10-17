# HSK6_SC032 / SC038 — exact V4 binary status and fail-closed canonical camera preflight (2026-10-17)

Baseline uysalayhan23/newChinese/main: c5445a36ad401b0d9d752acf4e7d958a6c85a87f. Documentation and read-only validation code only.

## Grounded real WebP evidence

- From physical NewChinese_HSK6_SC032_SC038_V4_VERIFIED_STAGING_NOT_PRODUCTION_20261017.zip: scene-specific V4 FG (RGBA, 720x1280, 84,614 bytes) SHA-256 c79a0c4dbfbc6807a94c598afd378682213894fd992356fcfe3cd3b66bcb62aa, Git blob 84631be9ed27a64a29e134e84037919b23277440; V4 preview (RGB, 720x1280, 215,124 bytes) SHA-256 5a69c580d7a85d160eae0602f956440b3800bd39dd07b80363c13de05f6bc5bc, Git blob ca8c43043c628d2b69ef7e59625bca49f1586533. Repeated for both scenes: binary SHA and decode PASS within the local QA archive.
- Fresh GitHub GET /git/blobs/84631... and /git/blobs/ca8c... returned 404. No create_blob(base64) nor GitHub backread success for either V4 exact binary. Do NOT mark V4 GitHub transport PASS or refer to the local ZIP as GitHub-staged WebP.
- Recursive remote Git tree untruncated, 40/50 HSK6 production previews. In both SC032 and SC038 content/assets the two pinned character WebPs physically exist; both BG + FG + preview are absent. Four requested BG/FG files absent.
- V4 object-level FG right-counter-only redesign fixes an old 726-pixel speaking-hand overlap in SC035 donor camera and preserves right FG object pixel content. This does not prove different scene camera presets CAM_HSK6_SC032_01 or CAM_HSK6_SC038_01 are equivalent to CAM_HSK6_SC035_01. Existing Hough floor-corridor vanishing estimate (379.25,396.25) is a proxy **within donor** and no independently approved numeric target camera proof is present.
- Alternate HSK3_SC042 / HSK5_SC002 360x640 and HSK5_SC008 576x1024 electronics-store sources remain below required 720x1280 physical resolution and camera/FG geometry differs; unverified upscale/copy is prohibited.

## Newly added deterministic, read-only release guard

- tools/verify_hsk6_032_038_camera_gate.py scans each scene's approved dialogue/location grounding and camera metadata; requires separately recorded approved target-camera numeric evidence, physical BG+2 actor+FG+preview at the exact manifest paths, Pillow physical decode and mode/size, and pinned actor Git blob SHA. It checks optional V4 staging SHA separately.
- tools/tests/test_verify_hsk6_032_038_camera_gate.py covers missing layers, false camera approval, actor SHA tampering, and unrelated scene rejection. Offline 4/4 synthetic-fixture tests passed for the tested local gate implementation. The newly committed exact file has NOT been exercised on a full remote repo checkout and must not be called an end-to-end PASS.
- A provided numeric-camera JSON is inspected for declared per-landmark reprojection errors and independent approval fields; the script does not itself reconstruct a homography or replace independent visual inspection. Even with every mechanical check complete, its best outcome is preflight only, never full scene/art acceptance.
- Example offline command (no Actions): python tools/verify_hsk6_032_038_camera_gate.py --repo .
- Example offline tests: python -m unittest discover -s tools/tests -p test_verify_hsk6_032_038_camera_gate.py

## Required next source/production steps

1. Independently establish a target-camera coordinate system, actual target BG image, and source-to-target ground-plane landmarks for EACH scene (SC032 and SC038 separately). An opaque cameraPreset ID or donor vanishing point alone is not numeric camera equivalence.
2. Produce scene-correct, textless 720x1280 empty-scene BG and one-object-depth RGBA FG; verify original canonical actor WebPs, 0 face/hand/torso FG cover, floor contact and safe-area geometry. All four true layer files must pass before deriving final preview.
3. Upload only SHA-pinned actual binary media through authenticated GitHub create_blob, commit with [skip ci], and re-read the binary for exact Git SHA / byte identity before changing visual complete status; do not substitute Base64-text files as .webp.
4. SC026, remaining HSK6 HOLDs, locked dialogues/media, LOCKS and accepted canonical pixels preserved. Zhang Wei all-level visual comparison remains P999 final deferred task.

Current disposition: V4 local physical FG + preview QA PASS; target camera homography and canonical BG/FG release HOLD; GitHub V4 binary transfer UNVERIFIED; scene acceptance HOLD. No Actions and no force push.
