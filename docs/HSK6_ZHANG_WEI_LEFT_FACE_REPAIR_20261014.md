# HSK6 odd-scene Zhang Wei canonical-left publication — 2026-10-14

Source commit: `8e492e69e9751ccb34ce964f109cdb11242139e7`. Branch: `main`.

## Checked original reference and candidate
- Exact approved source: `content/hsk6/sc002/assets/hsk6_sc002_char_zhang_wei.webp`, Git blob `44a7a521b7fa64466111c30f6830904081c3767d`.
- Independent Pillow transformation: ImageOps.mirror(original.convert("RGBA")); WebP lossless method 6; verified `600x900` and nontrivial RGBA alpha.
- Pixel-exact mirror verification passed. Candidate Git blob `717828100874a371def695365e29b7c946147b4d`; SHA-256 `4db0a2bb2988f204f0c979e95d9e626fc1a65e702e2d2a21b2611c107249cd2a`. GitHub create_blob returned this exact SHA.
- 20 live odd-scene `visual_manifest.json` character identities, canonical outfit, facing anchors, scene locations, metadata and unchanged pending statuses were checked against `tools/hsk6_face_right_identity_pins.json`; each old characterB was `316717c873fade2a1e98564bdf6ac037e354e` (unapproved).

## Atomic publication scope
- 20 characterB WebP paths only, pointing at exact Git blob `717828100874a371def695365e29b7c946147b4d`.
- `content/visual_quality_gate.json`: append **only** the candidate SHA-256 under each of the 20 odd HSK6 scene IDs. Existing SHA-256 entries for ten previously approved Liu Mei / Chen Yu characterA files preserved.
- No global approved blob SHA changes, no identity rule relaxation. `identityRegeneration.status` remains `required`.
- 16 existing even/later preview WebPs and provenance, all current scene visual manifests, dialogue/scene data, original sources, and pending acceptance statuses were untouched.

## Pending next gates
- Seven four-layer odd scenes: SC003, SC005, SC009, SC015, SC021, SC025, SC027. Preview production and independently reviewed physical 720x1280 QA needed; do not claim full-scene acceptance.
- Thirteen odd scenes lack both BG and FG: SC001, SC007, SC011, SC013, SC017, SC019, SC023, SC029, SC031, SC033, SC035, SC037, SC039. These are not preview-ready.
- CharacterA rights/canonical approvals remain as previously validated.

No GitHub Actions, force push, temporary branches, or full scene acceptance.
