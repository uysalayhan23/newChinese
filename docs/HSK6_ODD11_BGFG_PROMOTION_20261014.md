# HSK6 exact-location BG/FG production promotion — 2026-10-14

Scope: `uysalayhan23/newChinese`, branch `main`. **BG/FG-only asset QA**, not full scene acceptance.

## Evidence
- Sources: physical 720×1280 WebP images in staging; local Git blob SHAs matched the 22 staged GitHub paths and 8 unique sources.
- Backgrounds: office, public library, Hangzhou neighborhood and electronics store visually checked against corresponding `locations/LOC_*/visual_bible.json` rules.
- Foregrounds: RGBA alpha checkerboard and BG+FG composites visually inspected. Dark/color-striped RGB in *fully transparent pixels* is not visible in alpha composites. All four composites show clean natural occlusion.
- Pixel test in visible FG regions (alpha >=128) comparing FG RGB against the corresponding BG produced zero pixels above mean absolute difference 20 for office/library/electronics, 302/65027 for neighborhood (edge anti-aliasing), consistent with BG-derived cutouts.
- Reused the **existing staging Git blob SHA objects**, no re-encoding, no new generated identities, no changes to original canonical faces or scripts.
- Manifest `locationId` and BG/FG target asset names checked for each of 11 scenes, with unchanged camera/character IDs.
- Each location shares an identical pair across its target scenes, preserving intra-location layout continuity.

| Location | Scenes | BG SHA | FG SHA | FG placement |
|---|---|---|---|---|
| LOC_ZHANG_OFFICE_001 | SC001, SC007, SC031, SC037 | `df52de129130d06220c250afabec250caf218541` | `ab49f2892127f49189bc800d6e8cd444feb37a15` | plant lower left; natural occlusion |
| LOC_PUBLIC_LIBRARY_001 | SC011, SC017, SC033, SC039 | `8c3e7732156ba04375c846af6633475264b229a2` | `01c2add740504ca62d55e2226c53d8993e74fcc7` | bookshelves at right edge; natural side occlusion |
| LOC_NEIGHBORHOOD_001 | SC023, SC029 | `a0fda64fd0732d378d2648a48d058edfb4fca015` | `5da1b87d0e43673ce2259c2759c88569f8cae81e` | tree canopy upper right, planter/bench left; no central obstruction |
| LOC_ELECTRONICS_STORE_001 | SC035 | `b0ba989e06045ea92a0c4fd6ebf580877f4acc48` | `dd7b43d996a33e40ff2c5cf86b5c4fa297238061` | counter edges left/right, free central walkway |

**22 files promoted to `content/hsk6/sc*/assets/`: 11 backgrounds, 11 foregrounds.**

## QA boundary
- `background=PASS` / `foreground=PASS` refers to **exact-location layer structure/format/composite** only.
- Character pose/size, face direction, lighting on the subject, scene-by-scene preview, and continuity with adjacent SCs remain pending until actual **full character composites** are reviewed.
- All 11 `visual_manifest.json` and `media_status.json` retain pending statuses; do not change `acceptedScenes`, complete flags, audio, dialogue, or locked content.
- `HSK6_SC013`/`HSK6_SC019` remain staged preview candidates; AI-assisted previews are NOT canonical pixel-preserving character composites. Do not mark `accepted` without additional identity comparison.
- QA staging files left unchanged as an audit trail.
- No workflows manually dispatched. Commit uses `[skip ci]` to avoid Actions minutes. No force push.

## Source SHA table
LOC_ZHANG_OFFICE_001: BG `df52de129130d06220c250afabec250caf218541` / FG `ab49f2892127f49189bc800d6e8cd444feb37a15`.
LOC_PUBLIC_LIBRARY_001: BG `8c3e7732156ba04375c846af6633475264b229a2` / FG `01c2add740504ca62d55e2226c53d8993e74fcc7`.
LOC_NEIGHBORHOOD_001: BG `a0fda64fd0732d378d2648a48d058edfb4fca015` / FG `5da1b87d0e43673ce2259c2759c88569f8cae81e`.
LOC_ELECTRONICS_STORE_001: BG `b0ba989e06045ea92a0c4fd6ebf580877f4acc48` / FG `dd7b43d996a33e40ff2c5cf86b5c4fa297238061`.
