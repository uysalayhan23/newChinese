# HSK6 missing BG/FG: exact-location reuse audit (2026-10-16)

Baseline main `62d71743651ef405f5d0c9d7776c07dea435811f`. Sources: uploaded `hsk6.zip` decoded using Pillow, GitHub main recursive tree (not truncated), and repository location `visual_bible.json` documents. No source mutation and no production promotion.

| Exact location | Missing BG/FG scenes | Existing physically decoded BG/FG source | Preliminary result |
|---|---|---|---|
| `LOC_ZHANG_OFFICE_001` | SC004, SC010, SC034, SC040 | SC001 (also SC007/031/037), 720×1280 RGB background and RGBA foreground | same-location **candidate**, scene-specific camera/occlusion pending |
| `LOC_PUBLIC_LIBRARY_001` | SC014, SC036 | SC011 (also SC017/020/033/039), 720×1280 RGB background and RGBA foreground | same-location **candidate**, scene-specific camera/occlusion pending |
| `LOC_NEIGHBORHOOD_001` | SC026 | SC023 (also SC029), 720×1280 RGB background and RGBA foreground | same-location **candidate**, scene-specific camera/occlusion pending |
| `LOC_ELECTRONICS_STORE_001` | SC032, SC038 | SC035, 720×1280 RGB background and RGBA foreground | same-location **candidate**, scene-specific camera/occlusion pending |
| `LOC_ZHANG_HOME_001` | SC016, SC042, SC045, SC048 | SC013/019, 768×1365, identical BG/FG blob pair | **HOLD**: pre-existing coffee-table, foot placement and depth contradiction; no safe unreviewed reuse |

The location visual bibles confirm office light-wood desks/windows, library shelving/study area, tree-lined neighborhood, electronics-shop displays, and compact home identity, respectively. Exact location and source decode do **not** by themselves certify a matching camera, pose or foreground geometry.

For the **9 non-home scenes** no newly generated BG/FG is justified before testing existing SHA-pinned candidates in staging. For the **4 home scenes**, existing BG/FG may not be promoted merely by resizing or copying: spatial consistency remains unresolved. Existing SC011/017/020 staged previews and SC013/019 HOLD conclusions are protected. No application acceptance count changed; no new production WebP committed. Canonical character and scene files, LOCKS and dialogues untouched. Do not run GitHub Actions. Documentation-only commit uses `[skip ci]`.
