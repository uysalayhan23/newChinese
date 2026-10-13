# HSK6 face_right characterA audit — 2026-10-13

Repository: `uysalayhan23/newChinese` main. GitHub Actions were not used.

## Visual and physical findings
All 20 odd-numbered HSK6 target scene manifests and visual production queues were checked for character identity, locked outfit, location and the `face_right` direction requirement.

- Wang Ming, 10 scenes (SC001, SC003, SC005, SC007, SC009, SC031, SC033, SC035, SC037, SC039): **REJECT** the mechanically mirrored candidate because it faces LEFT; select instead the existing exact approved canonical source `067fcfe261c52adebc383f5551d7ed365abd747e`, which faces RIGHT. Character is dressed in `OUTFIT_WANG_MING_WORK_01` and preserves handedness without changing any pixel. The source is already listed in `approvedCanonicalGitBlobSha1`. This commit stages only these 10 missing characterA layers.
- Liu Mei, 5 scenes (SC011, SC013, SC015, SC017, SC019): the mirrored candidate faces RIGHT and retains the approved source identity, casual outfit, green notebook, anatomical silhouette and transparent background. Candidate blob `1944d13b2565d618ad183da64fd33ef68a11191a`, SHA-256 `a91cc9592d1269b3140bcc9acebc516d383c4013f469088a3c360db08845c834`. Pixel-exact horizontal reflection passed 5/5. **Asset-level visual QA PASS; remote publishing pending**.
- Chen Yu, 5 scenes (SC021, SC023, SC025, SC027, SC029): the mirrored candidate faces RIGHT and retains the approved source identity, casual outfit, anatomical silhouette, symmetric two-hand conversational gesture and transparent background. Candidate blob `55885be8637e7df4b7ff300a710ed9d1b6f78847`, SHA-256 `5097459fdf98cd4e4701edf7820f8ac9601178b1fcb4b3c747c6c2f2bb431956`. Pixel-exact horizontal reflection passed 5/5. **Asset-level visual QA PASS; remote publishing pending**.

All 20 image targets were absent on `main` before this audit. The candidate source WebPs were independently decoded in Pillow; dimensions, alpha bounds, per-pixel mirroring and Git blob SHA were checked.

## Acceptance boundary
- **Do not mark any full HSK6 scene accepted** based only on characterA, as other layers, scene preview and full scene quality may still be pending.
- The 16 existing HSK6 preview WebPs and their provenance were not altered.
- For the Liu Mei and Chen Yu *mirrored* files, new blob SHAs are not present in the current global canonical allowlist. When physically published, require independent exact-SHA review and optionally per-scene `approvedCharacterSha256` entries; do not globally approve a transformation without review.
- Do not substitute the left-facing mirrored Wang Ming outputs for the right-facing approved canonical source.

All writes must include `[skip ci]`; do not start GitHub Actions or force-push.

## 2026-10-13 publication and scene-specific identity approval

The ten previously-pending mirrored characterA layers were physically stored as exact GitHub WebP blobs with verified SHA-1, checked for Pillow decoding, intact RGBA alpha and pixel-exact mirroring from the pinned canonical sources, and reviewed for right-facing orientation and locked outfits.

- Liu Mei: SC011/013/015/017/019 — blob `1944d13b2565d618ad183da64fd33ef68a11191a`, per-scene SHA-256 `a91cc9592d1269b3140bcc9acebc516d383c4013f469088a3c360db08845c834`.
- Chen Yu: SC021/023/025/027/029 — blob `55885be8637e7df4b7ff300a710ed9d1b6f78847`, per-scene SHA-256 `5097459fdf98cd4e4701edf7820f8ac9601178b1fcb4b3c747c6c2f2bb431956`.

All ten characterA paths and **only** their ten scene-specific `approvedCharacterSha256[HSK6_SCxxx]` array entries were committed atomically on `main` with `[skip ci]`. The global approved canonical blob list, all twenty visual manifests, all sixteen preview files, dialogue, camera and lighting metadata, and all scene acceptance statuses remain untouched. `identityRegeneration.status` remains `required` for other assets; the SHA-256 exception is limited to the ten exact files and scene IDs. No Actions were triggered. Remaining scene BG/FG/preview QA is a separate acceptance gate.
