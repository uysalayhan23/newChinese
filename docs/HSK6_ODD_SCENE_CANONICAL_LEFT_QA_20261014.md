# HSK6 odd-scene Zhang Wei left-facing canonical audit — 2026-10-14

Repository: `uysalayhan23/newChinese`, branch `main`. GitHub Actions were not run.

## Previous accepted media preserved
- Live checks against HSK6_SC002/006/008/012/018/022/024/028/030/041/043/044/046/047/049/050 show **16/16 preview WebP SHA matches** their current `visual_manifest.json.previewComposition.previewBlob`. Existing camera, lighting and active-speaker metadata remain present; scene statuses remain pending.
- The 20 `face_right` characterA assets were published earlier: 10 Wang Ming exact approved Git blob `067fcfe261c52adebc383f5551d7ed365abd747e`, 5 Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`, 5 Chen Yu `55885be8637e7df4b7ff300a710ed9d1b6f78847`. Their prior SHA and scene-specific SHA-256 checks passed; later `74c890cd` changed only generator code, its tests, and audit docs.
- No previously published media or locked dialogue was changed by this report.

## New verified canonical Zhang Wei sources
- `content/hsk1/sc001/assets/hsk1_sc001_char_zhang_wei.webp` is approved Git blob `b617cef41d4adeb331f126284a2039dd33868a99`. This is **already left-facing** but visually has a backpack and an open blue overshirt; substituting it indiscriminately in HSK6 offices and homes risks wardrobe/accessory continuity.
- `content/hsk2/sc001/assets/hsk2_sc001_char_zhang_wei.webp` is approved Git blob `44a7a521b7fa64466111c30f6830904081c3767d`, reused by the existing even-scene HSK6 previews. Its normal pose is oriented right; an exact horizontal mirror preserves the approved face and clothing style while facing left.
- The currently used odd-scene characterB blob `316717c873fade2a1e98564bdf6ac037e7cc354e` is absent from the global approved SHA list. Its clothing/face differs from the accepted `44a7...` HSK6 continuity reference.

## New physically generated but UNPUBLISHED QA candidates
- Created one 600x900 transparent RGBA lossless-WebP left-facing Zhang Wei by horizontally mirroring the decoded approved `44a7...` source. Pixel-exact source-mirroring QA PASS; real WebP decode, full alpha range and physical dimensions PASS. **Candidate Git blob SHA**: `717828100874a371def695365e29b7c946147b4d`. **SHA-256**: `4db0a2bb2988f204f0c979e95d9e626fc1a65e702e2d2a21b2611c107249cd2a`. This hash is **not approved for production yet**.
- Inspected odd-scene remote asset trees. **7/20** already have BG + FG + characterA + characterB assets: `003,005,009,015,021,025,027`. The other 13 odd scenes lack BG and FG (see `docs/HSK6_FACE_RIGHT_POST_PUBLISH_AUDIT_20261013.md`).
- Locally composited **7/7 720x1280 WebP preview candidates** for these seven odd scenes, using pinned existing BG/FG, the accepted right-facing Wang Ming/Liu Mei/Chen Yu characterA layers and the new mirrored Zhang Wei characterB. Their image files are real, with 5 unique preview contents; the contact sheet was visually inspected for depth, anatomy, face direction and location consistency. **No image or pin/manifest was published** as a result of this work.
- Review-only local package `NewChinese_HSK6_7_Odd_Scenes_Review_ONLY.zip` contains the seven preview candidates, one mirrored Zhang Wei candidate and the local QA report. Not a GitHub acceptance or replacement manifest.

## Publishing conditions and next priority
1. Finish a trustworthy binary transfer for the mirrored Zhang Wei WebP and independently approve its exact SHA-256 for the required scene IDs. Do not use the backpack variant automatically.
2. Replace **only** the existing non-whitelisted `characterB` blobs on the 20 odd scenes through one guarded `[skip ci]` commit with necessary scene-specific SHA-256 whitelist entries. Preserve characters, outfits, scene manifests and acceptance statuses; do not relax global identity rules.
3. Validate the seven preview candidates against their exact remote source SHA pins before publishing previews and provenance; preview scene closure remains separately pending.
4. Supply or repair missing BG/FG in the remaining 13 odd scenes and perform full visual continuity QA.

This report documents staged QA only and does not assert running the updated original offline Python unittest suite. No Actions, force-push, or temporary branches were used.
