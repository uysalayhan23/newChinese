# HSK6 character continuity and SC020 shadow v3 QA — 2026-10-16

Repository `uysalayhan23/newChinese`; baseline `91a26a35d9665b7d22c93e23c721cafaa06c45c4`. Scope: user-supplied original HSK6 zip and local Pillow tests. Audit-only. No production asset or canonical source changes.

## Continuity findings
100 real character WebPs across all 50 HSK6 scenes reduce to 10 distinct Git blob SHA values. Zhang Wei has three, Liu Mei two, Li Na two, Chen Yu two and Wang Ming one. SC011 and SC017 reuse Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a` and Zhang Wei `717828100874a371def695365e29b7c946147b4d`; SC022 uses Liu Mei `eea4742918bf5b78f222b54631de8f71a4c824a7` and Zhang Wei `44a7a521b7fa64466111c30f6830904081c3767d`.

Existing HSK6 alternatives were composited and visually compared. SC011/017's realistic Liu Mei versus stylized CGI Zhang Wei mismatch persists. Substituting SC022's pair would affect odd-scene visual continuity. SC022's existing pair is a staging reference, not a continuity acceptance. None of SC011, SC017 or SC022 is newly accepted.

## SC020 v3 staging candidate (local; not uploaded to production)
- Method: compact soft elliptical contact shadows **beneath** independently composited canonical actors; source WebP bytes unchanged.
- Four source blob SHAs: BG `8c3e7732156ba04375c846af6633475264b229a2`, Zhang Wei `44a7a521b7fa64466111c30f6830904081c3767d`, Li Na `a02f88b5075f6cb590d8c0f23219b0e5fa3e80d0`, FG `01c2add740504ca62d55e2226c53d8993e74fcc7`.
- Candidate: `staging/hsk6/qa_pending/sc020/sc020_contact_shadow_refined_v3.webp` in local QA workspace (not GitHub).
- Git blob SHA of local candidate: `76dbd4ece57386d3ac71bbd7ecb9b0c4c7fee68b`.
- SHA-256: `4e49ba20f227aaa7e30b6022f14783566809526a2819d44d945d5b7482467138`.
- Actual Pillow validation: lossless WebP 720×1280 physically decoded; pixel-for-pixel RGB equality of recomposed frame and decoded WebP; 0 altered pixels in fully opaque source actor regions; 16,779 changed pixels versus shadowless composite.
- Visual QA: foot contact modestly improved; CGI/photographic environment stylistic conflict remains. `accepted=false`, `HOLD_STYLE_AND_SCENE_VISUAL_QA`.

## SC013 and SC019
See `docs/HSK6_SC013_SC019_HOME_DEPTH_HOLD_20261016.md`. Both retain their depth/coffee-table HOLD. No alternative physically present home BG/FG was established in uploaded HSK6, and no compositing trick was promoted.

**Gate:** Do not change `visual_manifest.json`, `media_status.json`, acceptance counts, locked dialogues, canonical assets, or production previews on this evidence. GitHub Actions prohibited without explicit user permission. Commit message uses `[skip ci]`.
