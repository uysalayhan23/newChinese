# HSK6 SC013/SC019 local canonical preview QA — 2026-10-14

Repository: `uysalayhan23/newChinese`, branch `main`.

## Inputs (uploaded directly, exact Git blob SHA verified)
- BG `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba`, 768x1365
- Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`, 941x1672
- Zhang Wei `717828100874a371def695365e29b7c946147b4d`, 600x900
- FG `6acadbee8403b5d78e0042431eec7af75fc94248`, 768x1365, RGBA

## Independent local candidate
Composite order: BG, Liu Mei, Zhang Wei, foreground, using native foreground transparency; scale to 720x1280 and encode real WebP (Pillow quality 90, method 2). Local outputs:
- `hsk6_sc013_preview.webp`: 138164 bytes, 720x1280, Git blob SHA `19ad889508293e01a66e7bd1f8f0428d7856777e`.
- `hsk6_sc019_preview.webp`: 138164 bytes, same canonical source and blob SHA.

Visual inspection: exactly two correct supplied characters in warm home setting, both complete, no major clipping, correct depth ordering. They appear relatively small against the background; final visual style / continuity approval remains **QA_PENDING**.

**Important:** Preview binaries were generated in the conversation's isolated container, NOT committed to GitHub: the container has no GitHub network resolution and the GitHub connector does not accept local file paths. Existing scene manifests remain pending and unchanged. Do not treat candidate hash as published blob or set status complete. No Actions triggered.

Remaining 11 scenes requiring BG+FG: SC001, SC007, SC011, SC017, SC023, SC029, SC031, SC033, SC035, SC037, SC039 (22 files). Low-resolution historical sources remain on hold.
