# HSK6 home preview acceptance gate — 2026-10-14

Repository: `uysalayhan23/newChinese`, branch `main`.

## SC013 / SC019 — QA HOLD
- Current GitHub scene folders contain the four canonical WebP layers but **no** `hsk6_sc013_preview.webp` / `hsk6_sc019_preview.webp`.
- Local canonical input Git blob SHAs: background `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba`, Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`, Zhang Wei `717828100874a371def695365e29b7c946147b4d`, foreground `6acadbee8403b5d78e0042431eec7af75fc94248`.
- A locally produced 720x1280 candidate was visually inspected. Both characters have recognizable outfits and faces, but the lower-body placement and table/foreground occlusion are **spatially implausible**: characters appear to stand on/in front of the coffee table. This fails full visual acceptance even though file decode, native dimension and source SHAs pass.
- **Decision:** QA HOLD, no scene acceptance, no fabricated preview publication or manifest status changes. A further local composite needs physically plausible floor/perspective/foreground occlusion and full visual review. `tools/compose_hsk6_home_previews.py` is a draft, not an accepted renderer.

## Other 11 odd HSK6 scenes — exact physical gap (live main directory enumeration)
| Location ID | Scenes | Missing files |
|---|---|---|
| LOC_ZHANG_OFFICE_001 | SC001 SC007 SC031 SC037 | 8 BG/FG |
| LOC_PUBLIC_LIBRARY_001 | SC011 SC017 SC033 SC039 | 8 BG/FG |
| LOC_NEIGHBORHOOD_001 | SC023 SC029 | 4 BG/FG |
| LOC_ELECTRONICS_STORE_001 | SC035 | 2 BG/FG |
| **Total** | **11 scenes** | **22 BG/FG** |

The character layers exist in all 11 scenes. For these locations, legacy BG/FG references measured 540x960 or 576x1024 and have been previously placed on HOLD; do not upscale or borrow unrelated rooms to satisfy completion counters.

## Preservation
No changes to canonical input layers, 300/300 locked dialogue, visual manifest acceptance or approved identity assets. Actions must not run; use `[skip ci]` when committing. This record is a review/audit, not successful image publication.
