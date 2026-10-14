# HSK6 exact-location BG/FG staging audit — 2026-10-14

Repository: `uysalayhan23/newChinese`, `main`.

## Actual completed operations
- Four high-resolution, portrait 720×1280 WebP background candidates, one each for office/library/neighborhood/electronics store, generated from location-specific visual-bible constraints.
- Four 720×1280 RGBA foreground candidates extracted as nonempty aligned masks from the matching newly generated backgrounds. **Depth occlusion is provisional and needs visual approval**.
- All eight original file-byte hashes verified locally and against GitHub-created blobs: **8/8 SHA-1 matches**.
- All eight source WebP paths present in `staging/hsk6/qa_pending/locations/LOC_*/`; GitHub directory listing verified.
- 11 scene-specific BG/FG candidate pairs (22 physically present WebP paths) now in `staging/hsk6/qa_pending/scNNN/`; GitHub directory listing verifies **22/22 files**. Git blobs are reused without re-encoding across scenes at the same exact location.
- Commit containing 11 scene pairs: `8cadbe1755c73f3c5b4e355c42bfe3ba16b56e5c`. Read-only Actions-run query for this commit returned `total_count=0`.

## Source pairs (real WebP, size 720×1280)
| Exact location | BG Git blob | FG Git blob | Scenes staged |
|---|---|---|---|
| `LOC_ZHANG_OFFICE_001` | `df52de129130d06220c250afabec250caf218541` | `ab49f2892127f49189bc800d6e8cd444feb37a15` | SC001, SC007, SC031, SC037 |
| `LOC_PUBLIC_LIBRARY_001` | `8c3e7732156ba04375c846af6633475264b229a2` | `01c2add740504ca62d55e2226c53d8993e74fcc7` | SC011, SC017, SC033, SC039 |
| `LOC_NEIGHBORHOOD_001` | `a0fda64fd0732d378d2648a48d058edfb4fca015` | `5da1b87d0e43673ce2259c2759c88569f8cae81e` | SC023, SC029 |
| `LOC_ELECTRONICS_STORE_001` | `b0ba989e06045ea92a0c4fd6ebf580877f4acc48` | `dd7b43d996a33e40ff2c5cf86b5c4fa297238061` | SC035 |

## Mandatory QA hold
**Staging existence does NOT equal production acceptance.** The production folders `content/hsk6/scNNN/assets` still lack these 22 BG/FG files. No production media counters, canonical manifests, or locked dialogues were modified. Current inspected scene statuses are `visual-assets-pending`.

New foreground depth masks must be inspected composited with each scene's **original approved character pixel layers** and scene-specific continuity. Backgrounds need visual comparison to exact `locations/LOC_*/visual_bible.json`, cinematic style, camera, lighting, and prior/next scenes. Only then promote BG/FG, compose preview deterministically, and mark an individual scene accepted.

## SC013 and SC019 separate acceptance hold
- Their four original canonical scene layers still exist under `content/hsk6/sc013/assets` and `sc019/assets`, with shared verified source SHAs: BG `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba`, Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`, Zhang Wei `717828100874a371def695365e29b7c946147b4d`, FG `6acadbee8403b5d78e0042431eec7af75fc94248`.
- Two depth-recomposed preview candidates exist separately in QA staging, not in production. They changed generated face pixels and cannot be certified as immutable canonical identity.
- An additional **pure four-layer deterministic Pillow composite** was locally tested. It preserved original character bytes but produced implausible table/feet depth. Thus **physical file checks may pass but final visual QA does not**.
- SC012/SC014 and SC018/SC020 visual manifests were inspected for adjacent locations, characters and outfit continuity. Zhang Wei's `OUTFIT_ZHANG_WEI_CASUAL_01` is consistently declared in adjacent scenes; this metadata check is **not** full scene visual continuity PASS.
- SC013 and SC019 remain `visual-assets-pending` until a pixel-provenance-safe and spatially plausible composition is reviewed.

## Preservation
No GitHub Actions manually invoked; commits contain `[skip ci]`. No new branch, force-push, change to production canonical character/BG/FG layers, locked dialogue or 300-scene structure. An inaccurate generated infographic claiming completed QA was discarded and never published.

**Next gate:** inspect each 11-scene foreground/actor depth composite, compare canonical face pixels, accept only demonstrably matching image layers, then promote staged assets to production on `main` via verified blob/tree/commit/ref without Actions.
