# HSK6 odd-scenes: canonical BG/FG audit and conditional reuse — 2026-10-14

Repo: `uysalayhan23/newChinese`, `main`. Baseline report: `docs/HSK6_ODD7_PREVIEW_REAL_QA_20261014.md`.

## SHA-verified seven preview publication

HSK6_SC003, SC005, SC009, SC015, SC021, SC025 and SC027 were rebuilt independently with Pillow from actual source WebP bytes, following BG → character A → character B → FG and 720×1280 WebP encoding. The seven physically produced outputs matched **7/7** exact target Git blob SHA values specified in the baseline report (five unique blobs); actor overlap was 94px. They were committed with scene-specific `previewComposition.inputBlobs` and `previewBlob` while all original manifest fields and pending acceptance states were retained. All seven were re-fetched from `main` and **7/7** remote SHA/provenance checks passed. Commit `f20d2b397dee8e8c835928a905c8965ba60d28b3`. These seven are **QA-pending**, not full scene acceptance.

## Exact-location source verification for the remaining thirteen

The target scene location IDs were cross-checked against `locations/LOC_*/visual_bible.json`, historical HSK production batch location mappings, canonical source scene manifests, and the actual GitHub BG/FG blobs.

| Location | HSK6 missing odd scenes | Evaluated historical source | Native size | Decision |
|---|---|---|---|---|
| `LOC_ZHANG_OFFICE_001` | SC001, SC007, SC031, SC037 | HSK4/5_SC001 BG `9c660be...`, FG `8c5f452...` | 540×960 | HOLD: below 720×1280 |
| `LOC_PUBLIC_LIBRARY_001` | SC011, SC017, SC033, SC039 | HSK5_SC023 BG `e56a214...`, FG `32632b6...` | 576×1024 | HOLD: below 720×1280 |
| `LOC_ZHANG_HOME_001` | SC013, SC019 | **HSK5_SC024** BG `86c8e17...`, FG `6acadbee...` | **768×1365** | **PASS for BG/FG reuse only** |
| `LOC_NEIGHBORHOOD_001` | SC023, SC029 | HSK3_SC022 BG `b3dc36b...`, FG `623a5e4...` | 540×960 | HOLD: below 720×1280 |
| `LOC_ELECTRONICS_STORE_001` | SC035 | HSK3_SC023 BG `c0a8cd2...`, FG `71931bdf...` | 576×1024 | HOLD: below 720×1280 |

Alternate sources were checked, including HSK2_SC032 Zhang Home (941×1672 BG/FG) and HSK5_SC024. The former visually focuses on a packed travel bag and dominates the foreground, making it mismatched to HSK6_SC013/SC019's home learning dialogue; **not reused**. The latter shows a warm contemporary Hangzhou home living room consistent with the locked `LOC_ZHANG_HOME_001` visual bible and the two HSK6 scenes. Its source `visual_manifest.json` declares `visual-assets-complete`, `qualityBlocked=[]` and specifically lists `background` and `foreground` as preserved canonical layers. `visual_grounding.json` contains approved `locationMatch` and `layerPlan` sourcing from HSK2_SC049.

## Safely staged BG/FG (no preview acceptance)

Only four new scene asset paths are bound to **the exact pre-existing Git objects**, no re-encoding:
- SC013 BG and SC019 BG → `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba`
- SC013 FG and SC019 FG → `6acadbee8403b5d78e0042431eec7af75fc94248`

Both source images are 768×1365 WebP; the FG uses an alpha-capable VP8X container. Their actual visual content was inspected. The HSK6 manifest asset paths already reference these filenames; original manifests, all characterA/B layers and 23 previously staged HSK6 preview files remain UNCHANGED. SC013/019 remain visual-assets-pending until independent four-layer preview visual QA.

**Still missing BG/FG:** eleven odd-numbered HSK6 scenes (SC001, 007, 011, 017, 023, 029, 031, 033, 035, 037, 039), 22 physical assets. Do not upscale low-resolution historical sources or substitute mismatched locations merely to satisfy counters. Additional higher-resolution canonical source or quality-preserving new assets are needed.

All commits `[skip ci]`. No GitHub Actions, force-push, branch creation, changes to locked dialogue/identity, or automatic scene acceptance.
