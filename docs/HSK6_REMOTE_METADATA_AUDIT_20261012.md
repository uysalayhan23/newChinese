# HSK6 GitHub source and identity audit — 2026-10-12

Repository: `uysalayhan23/newChinese`, branch `main`.
Audited starting HEAD: `62e9ffce7de73ac6f1e70c58bf43ef0e0a5f0866`.

## PASS — remote repository checks
- 64/64 canonical source WebP Git blob SHA comparisons matched `tools/hsk6_ready_preview_blobs.json` for the 16 declared preview-ready scenes.
- 16/16 preview-ready scene manifests matched the independent scene/location/character/outfit/speechBubbleAnchor entries in `tools/hsk6_ready_preview_identity_pins.json`.
- 20/20 face-right candidate scene manifests matched the independent scene/location/character/outfit/speechBubbleAnchor entries in `tools/hsk6_face_right_identity_pins.json`.
- Total: 100/100 *repository metadata and source-hash checks* passed.

## NOT RUN / NOT ACCEPTED
- The 18/18 previously recorded Python unittest result was **not rerun** for this audit.
- Pillow is available in the audit execution environment (12.3.0), but direct Git network access failed (DNS for github.com unavailable), and the GitHub connector failed when decoding binary WebP blobs as UTF-8.
- Therefore no physical Pillow composition or image decode was performed and no visual/identity acceptance should be inferred.
- The following preview paths were absent from the GitHub tree: SC002, SC006, SC008, SC012, SC018, SC022, SC024, SC028, SC030, SC043, SC044, SC046, SC049, SC050 (14 paths).
- SC041/SC047 preview paths existed but were **not** independently checked for 720x1280 resolution in this audit.
- No face-right image candidates were generated, and no visual status/acceptance was changed.

## Constraints
No GitHub Actions runs were started. LOCKS, scene content, canonical binary assets and existing visual statuses remain unchanged. This audit is a factual record of *remote SHA and manifest comparisons*, not evidence of end-to-end media QA.
