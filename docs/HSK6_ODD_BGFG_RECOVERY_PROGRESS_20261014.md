# HSK6 SC013 / SC019: physically staged preview candidates — 2026-10-14

Branch: `main`. Publication is **QA_PENDING**, not accepted scene completion.

Two actual 720×1280 RGB WebP blobs were uploaded through the authenticated GitHub Git blob API and linked into the Git tree at:

| Scene | Staging path | Git blob SHA | Bytes |
|---|---|---|---:|
| SC013 | `staging/hsk6/qa_pending/sc013/hsk6_sc013_depth_corrected_candidate.webp` | `00662ad233744133acd005594648383f3d6cc578` | 172472 |
| SC019 | `staging/hsk6/qa_pending/sc019/hsk6_sc019_depth_corrected_candidate.webp` | `aa10238394b62960d3f983781abcdd0d7121a650` | 188362 |

Both Git server blob SHAs were independently checked against the local exact WebP bytes before tree publication.

**Visual depth QA:** Previous table-grounding artifact corrected; each visibly features exactly Liu Mei and Zhang Wei on a room rug in front of sofa, coffee table in foreground, no split layout, no text/logos.

**Canonical lock:** These are AI-assisted recompositions, not deterministic alpha composites. Their character identities and continuity remain `QA_PENDING`; the original accepted canonical source images and all HSK6 scene `visual_manifest.json` files remain UNCHANGED. They must not replace production preview assets or count as scene accepted until exact character identity and source-level QA pass.

Exact canonical source BG/FG blobs already assigned to both scenes remain unchanged: BG `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba`, FG `6acadbee8403b5d78e0042431eec7af75fc94248`, Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`, Zhang Wei `717828100874a371def695365e29b7c946147b4d`.

## Remaining 11 odd-scene exact-location source investigation

All 22 BG/FG target scene files remain physically missing from `content/hsk6/scXXX/assets`.

- `LOC_ZHANG_OFFICE_001`: SC001/007/031/037 (8 assets). Historical canonical source HSK3/4/5_SC001/041/044/050 BG `9c660be22cdd428e2a90862be84176defa615899` and FG `8c5f4525102a9c486917a0c5d13d7f5a6062f151`, native 540×960: **HOLD**.
- `LOC_PUBLIC_LIBRARY_001`: SC011/017/033/039 (8 assets). Historical HSK3_SC011 and HSK5_SC023/026/029 BG `e56a214bd8135e1130f6dabd6595bdc1a242b921`, FG `32632b6a4f27e6212381ed82c9084fb17543484b`, native 576×1024: **HOLD**.
- `LOC_NEIGHBORHOOD_001`: SC023/029 (4 assets). HSK3_SC022/026 and HSK5_SC032/035/038 BG `b3dc36b60ee3b552f398ef5707e2e9992eab0eff`, FG `623a5e4c5a311b1d3a54c64d06aee74f903aa588`, native 540×960: **HOLD**.
- `LOC_ELECTRONICS_STORE_001`: SC035 (2 assets). HSK3_SC023 and HSK2_SC029 BG `c0a8cd2fdace1ed57ca5690ae030b00e5b3d0549`, FG `71931bdfc24c20f853887c612cdc4c14608df917`, native 576×1024: **HOLD**.

Native sizes are from existing `docs/HSK6_ODD13_BGFG_SOURCE_AUDIT_20261014.md`. Additional historical 25628-byte HSK2_SC025 electronics source and 23404-byte HSK2_SC021 library source also exist, but are not promoted without sufficient native-resolution evidence and explicit visual acceptance. No upscaling of low-resolution originals, no unrelated location substitution, no manufactured `PASS` counter.

No GitHub Actions dispatched, only `[skip ci]` commit.
