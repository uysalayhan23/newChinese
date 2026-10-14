# HSK6 SC013/SC019 canonical face and depth follow-up — 2026-10-14

Branch: `main`. This document supersedes older staging-only statements about the BG/FG 22-file gap.

## Verified separate results

1. **Eleven other HSK6 scenes:** exactly 22 layer WebPs, 11 BG + 11 FG, now present in production `content/hsk6/sc*/assets`. The Git tree at commit `db30eefb7b34b60379d9de4fd6054156e01b1cc5` matches all 22 prior staging Git blob SHAs. Source/location/alpha composite QA passed. These 11 scenes remain **visual-assets-pending**; no complete previews or scene acceptance is asserted. See `docs/HSK6_ODD11_BGFG_PROMOTION_20261014.md`.
2. **SC013/SC019:** original canonical BG, Liu Mei, Zhang Wei and FG still have the same four immutable Git blob SHA values in both scenes:
   - BG `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba`
   - Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`
   - Zhang Wei `717828100874a371def695365e29b7c946147b4d`
   - FG `6acadbee8403b5d78e0042431eec7af75fc94248`

## Strict preview acceptance result

The staged depth-corrected scene preview candidates have physically valid 720×1280 WebP formatting and improved depth, but they are generative recompositions rather than unchanged canonical source pixels. Therefore **facial identity provenance is not proven**; neither is approved as the final preview.

A separate local deterministic candidate using the original canonical characters and BG (`hsk6_sc013_canonical_identity_depth_review_v4.webp`, **local only, not a GitHub asset**) was visually inspected. It preserves the original character cutouts, but the foreground coffee-table/feet occlusion remains unnatural. **Do not promote or accept it.**

### Gate state
- SC013/SC019: `SOURCE_IDENTITY_PRESERVED`, `FINAL_PREVIEW_HOLD`.
- Full-scene visual QA and previous/current/next scene continuity: **PENDING**.
- Do not modify either canonical character, manifest acceptance flag, dialogue, or previous successful scene content to force closure.

## Correct next requirement

Produce a realistic FG depth layer based on the canonical living room while retaining canonical faces, stage a deterministic four-layer composite with physically grounded feet, verify face-right/face-left orientation and locked outfit, and visually compare against adjacent scenes. Only then publish a final `hsk6_sc013_preview.webp` / `hsk6_sc019_preview.webp` and advance acceptance flags.

The 22 promoted BG/FG pairs for other scenes need character/FG composite preview checks before declaring their scenes accepted.

No Actions dispatch. Commits use `[skip ci]`.
