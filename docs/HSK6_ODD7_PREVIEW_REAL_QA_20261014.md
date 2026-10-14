# HSK6 odd-scene 7-preview physical QA and 13-scene BG/FG inventory — 2026-10-14

Repository: `uysalayhan23/newChinese`, branch `main`.
Approved characterB publication SHA: `717828100874a371def695365e29b7c946147b4d`, scoped approved SHA-256: `4db0a2bb2988f204f0c979e95d9e626fc1a65e702e2d2a21b2611c107249cd2a`.
Publication commit: `d08e33aa17f729ca9be98e948858cb71393e142a`, 20 characterB paths + gate + immutable QA notes. **No preview assets or scene manifest statuses changed.**

## Seven genuine QA-pending preview outputs

Local independent Pillow integration reconstructed previews from exact SHA-verified source WebP bytes:
- BG/FG: GitHub scene-specific existing blobs matched the source-archive's canonical SHA-1 values for cafe, West Lake, and community center.
- Character A: existing reviewed right-facing Wang Ming `067fcfe...`, Liu Mei `1944d13...`, Chen Yu `55885be...` depending on each locked scene.
- Character B: the published lossless left-facing Zhang Wei `717828100874a371def695365e29b7c946147b4d`, independently recomputed from the approved `44a7a521...`.
- Composition order: BG → characterA → characterB → FG. Pillow LANCZOS scaling to exact `720x1280`, 92 WebP quality with method 6.
- SHA, true WebP decoding, RGB mode, dimensions, nontrivial source alpha, exact four-input provenance, and actor bounding-box overlap 94px (at or below 101px tolerance) passed for **7/7** outputs. Five unique preview Git blobs.
- The actual seven-scene contact sheet was visually inspected: two intended characters, recognizable canonical style/wardrobe, right-facing character A versus left-facing Zhang Wei B, no gross anatomical errors or incorrect front/back depth seen. This is *candidate-level QA*, not full-scene acceptance.

| Scene | Preview candidate Git blob SHA | Source/location |
|---|---|---|
| HSK6_SC003 | `0a38fd3b246b18908e291e34f5ae6ffb3c04bd95` | Cafe |
| HSK6_SC005 | `0699a12e840cce23701062465c37f51022b2b954` | West Lake |
| HSK6_SC009 | `0a38fd3b246b18908e291e34f5ae6ffb3c04bd95` | Cafe |
| HSK6_SC015 | `70a1f487d25f8121c74824238a9f26c7e3f4721a` | Community center |
| HSK6_SC021 | `2cab32aad9acbf8e4f2ec682b8b8d7d38c4d01c4` | Community center |
| HSK6_SC025 | `0b21ff8f51ef72eb2ccd47c549303c5654fd7666` | West Lake |
| HSK6_SC027 | `2cab32aad9acbf8e4f2ec682b8b8d7d38c4d01c4` | Community center |

The seven newly produced preview candidates remain **local QA_PENDING artifacts**, not committed GitHub scene preview files. Do not register them as accepted or update visual_manifest before physical publication and independent locked-scene/continuity review. The 16 pre-existing approved-for-staging preview blobs remain untouched.

## Remaining thirteen odd scenes: real remote BG/FG absence

All thirteen scene `assets` directories were checked live against GitHub `main`. Both `*_bg.webp` and `*_fg.webp` are missing in every scene:

| Locked location | Missing scenes | Count |
|---|---|---:|
| `LOC_ZHANG_OFFICE_001` | SC001, SC007, SC031, SC037 | 4 |
| `LOC_PUBLIC_LIBRARY_001` | SC011, SC017, SC033, SC039 | 4 |
| `LOC_ZHANG_HOME_001` | SC013, SC019 | 2 |
| `LOC_NEIGHBORHOOD_001` | SC023, SC029 | 2 |
| `LOC_ELECTRONICS_STORE_001` | SC035 | 1 |
| **Total** | **13 missing BG + 13 missing FG** | **26 assets** |

Only canonical assets matching those **exact** locked location IDs may be proposed for reuse. Do not substitute lake/cafe/community BG/FG in office, library, home, neighborhood or electronics store scenes solely because the resolution is correct.

## Preserved locks and next decisions

- Confirmed the new atomically published characterB paths and twenty scoped SHA-256 gate entries in the live commit diff; ten pre-existing Liu Mei/Chen Yu SHA-256 entries were preserved.
- Existing sixteen HSK6 preview provenance and image paths were not modified by the characterB commit; `identityRegeneration.status=required` and global approved Git blob allowlist unchanged.
- Existing scene statuses remain pending and all 300 locked dialogue scenes untouched; no GitHub Actions or force push.
- Next: independently review source/location reference assets for the five missing location types; upload only verified canonical BG/FG and validate previews for the remaining thirteen. The seven QA-pending previews can be physically published with input provenance in a separate guarded `[skip ci]` step when independently accepted for staging.
