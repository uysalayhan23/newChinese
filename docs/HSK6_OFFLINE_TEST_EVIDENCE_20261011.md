# HSK6 canonical media production — offline test evidence (2026-10-11)

Repo: `uysalayhan23/newChinese`, branch `main`; no GitHub Actions executed.

## Confirmed changes on GitHub

- `tools/hsk6_face_right_identity_pins.json` now stores independent locked location, two-character identity, outfit and face-direction references for 20 candidate scenes: SC001/003/005/007/009, 011/013/015/017/019, 021/023/025/027/029 and 031/033/035/037/039.
- `tools/prepare_hsk6_face_right_candidates.py` now preflights **all 20 independent identity pins** before writing any candidate WebP. A manifest change affecting either actor, the location, wardrobe or orientation blocks the whole batch.
- `tools/tests/test_prepare_hsk6_face_right_candidates.py` gained tests for missing pins, incorrect second actor and location drift. It contains seven cases in total.

## Actual offline execution

The two GitHub-source Python algorithms and their test logic were reconstructed in an isolated, network-disabled local Python/Pillow working directory, with a limited locally implemented `visual_quality` helper exposing matching Git-blob-SHA and WebP-dimension algorithms. **These are local reconstructed test copies; this is not a byte-for-byte verification of a checked-out GitHub repository.**

| Offline suite | Result | Elapsed |
| --- | ---: | ---: |
| `test_prepare_hsk6_face_right_candidates.py` (20 synthetic mirror candidate cases) | 7/7 passed | 0.329s |
| `test_compose_hsk6_ready_previews.py` (synthetic alpha-composite, provenance, drift and size gates) | 11/11 passed | 2.358s |

`Pillow 12.3.0` used. The preview suite verified that its synthetic 720×1280 WebP was **physically saved and decoded**, while the status field remained pending; the mirror suite verified physically saved 600×900 transparent candidate layers. The tests use synthetic pixels, not any canonical character artwork.

## Production blockers — leave unaccepted

- This runtime can read canonical GitHub WebP blobs using the connected GitHub tools, but cannot reach GitHub from its isolated Python/Pillow container (DNS/network blocked). Binary GitHub WebP sources were **not transferred** into the actual Pillow run.
- Therefore **0 of the 20 requested canonical face-right WebP files and 0 of the 16 requested new exact 720×1280 preview WebPs were uploaded in this step**. The two previously staged HSK6_SC041/047 previews are 941×1672 candidates reused as exact source matches, not newly rendered 720×1280 previews.
- No scene has been accepted based on synthetic tests. HSK6 visual accepted remains `0/50`, physical WebP count remains `128/250`; HSK5 remains `226/250`. HSK6 pending HD BG/FG, candidate actors and previews remain open.
- Next steps require transfer of real source WebP bytes to image runtime, production of physical lossless face-right candidates and 720×1280 composites, publication through the connected GitHub write API, then image/identity/wardrobe/facing/continuity QA before updating `visual_manifest.json`, `media_status.json`, batch counters and queue.

All repository commits were made with `[skip ci]`, and no GitHub Actions were started.
