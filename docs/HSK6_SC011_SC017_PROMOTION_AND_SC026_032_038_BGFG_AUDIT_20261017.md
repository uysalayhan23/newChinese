# HSK6 SC011/017 binary promotion and SC026/032/038 canonical BG/FG gate — 2026-10-17

Repository: `uysalayhan23/newChinese`; branch `main`; base `223795b4ae90739b314fe783c8907c3cd9441b86`. This record documents exact WebP binary promotion and subsequent read-only visual/canonical checks. It is **not** full scene/application acceptance. No GitHub Actions and no source art/manifest/LOCKS mutations.

## SC011 / SC017 — completed exact binary upload

- Original, unchanged local candidate is physically decoded Pillow WEBP RGB **720×1280**, **238,350 bytes**, SHA-256 `087bc81e520646e2d95879a303a1fb0baee60e14151d71a34ba8a39e014e252f`.
- Both staging files are byte-identical. Their Git blob SHA is `d292165b0ba5b65094822be2a6054460ab615c54`.
- GitHub `create_blob(base64)` returned **exactly** that Git blob SHA. Only two target preview paths were inserted into a new tree: `content/hsk6/sc011/assets/hsk6_sc011_preview.webp` and `content/hsk6/sc017/assets/hsk6_sc017_preview.webp`.
- One fast-forward `main` commit `223795b4ae90739b314fe783c8907c3cd9441b86` (message contains `[skip ci]`), no force push. GitHub `fetch_file(encoding=base64)` round-trip was **byte-for-byte equal** to the original Base64 for **both** preview files; both returned the required blob SHA.
- Four canonical BG/character/FG source SHA pins for each scene are unchanged. Asset transport verification **PASS**; end-to-end scene acceptance and acceptance counts **unchanged**.
- After this upload, HSK6 production preview inventory is **40/50** paths. Still missing previews: SC013, SC016, SC019, SC020, SC026, SC032, SC038, SC042, SC045, SC048.

## SC026 / SC032 / SC038 — source BG/FG are still missing

The user's original HSK6 archive and fresh GitHub full recursive tree agree that **all six target paths** `hsk6_sc026_bg.webp`, `hsk6_sc026_fg.webp`, `hsk6_sc032_bg.webp`, `hsk6_sc032_fg.webp`, `hsk6_sc038_bg.webp`, `hsk6_sc038_fg.webp` are absent. Two actor WebPs exist for each target.

| Target | Location | Same-location donor | Donor BG blob | Donor FG blob |
|---|---|---|---|---|
| SC026 | `LOC_NEIGHBORHOOD_001` | SC023 (also SC029) | `a0fda64fd0732d378d2648a48d058edfb4fca015` | `5da1b87d0e43673ce2259c2759c88569f8cae81e` |
| SC032 / SC038 | `LOC_ELECTRONICS_STORE_001` | SC035 | `b0ba989e06045ea92a0c4fd6ebf580877f4acc48` | `dd7b43d996a33e40ff2c5cf86b5c4fa297238061` |

All four **donor** WebPs physically decode at 720×1280; RGB BG and RGBA FG. Their exact byte-derived Git blob SHA values match remote `main`. Location bibles permit the respective tree-lined street and store accessory-display continuity. All scenes use `LIGHT_WARM_NATURAL_01`, but **cameraPreset IDs differ by scene** (SC026 vs 023 and SC032/038 vs 035): same location/light alone does not certify perspective and occlusion.

### Existing local staging-v2 preview validation (not canonical assets)

| Scene | Decoded preview | WebP bytes | Git blob SHA | FG alpha-overlap proxy (actor A head; torso/gestures) |
|---|---|---:|---|---|
| SC026 | RGB 720×1280 | 330,982 | `ceca83f32fe89c510844de4820c22c379f207f88` | 0.3127%; 0.1226% |
| SC032 | RGB 720×1280 | 193,516 | `5398498273bbf47abaa10445f9775f71304dff0b` | 0.3414%; 1.4960% |
| SC038 | RGB 720×1280 | 193,516 | `5398498273bbf47abaa10445f9775f71304dff0b` | 0.3414%; 1.4960% |

Original staging-v2 sidecar QA reports 0 opaque actor collisions and proxy thresholds 0.5% head, 2% torso. Newly reopened the three actual WEBP staging binaries with Pillow and independently recomputed their Git blob SHA and SHA-256: **physical staging PASS**. SC032 and SC038 are byte-identical staging candidates. Manual side-by-side review of donors versus staging candidates shows matching location identity and unchanged source character artwork. Relative actor apparent scale and precise camera/foreground depth need final scene-specific review; alpha proxy PASS does **not** prove natural placement or authorize copying donor BG/FG into target canonical paths.

**Disposition:** `SC026/SC032/SC038 = STAGING_QA_PASS / CANONICAL_BGFG_MISSING / PRODUCTION_HOLD`. No donor copy, no target preview production upload, no alteration of original/accepted source or manifest, no acceptance-count change.

SC013/019 home-geometry HOLD, SC020 staging/HOLD, SC022 railing/scale HOLD and SC016/042/045/048 home BG/FG HOLD remain in force. The previously existing SC021 preview remains protected. GitHub Actions not requested or run. Commit contains `[skip ci]`.
