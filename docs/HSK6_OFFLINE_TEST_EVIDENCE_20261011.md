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

## Live GitHub pin verification and unified local runner — 2026-10-11

Verified against the live `uysalayhan23/newChinese` `main` Git tree **after** the current SHA-pinning commits:
- 16 HSK6 four-layer preview scenes × 4 assets = **64/64 source blob SHAs match** `tools/hsk6_ready_preview_blobs.json` (no drift).
- **16/16** HSK6 preview scene ID, location ID, ordered characters, outfits, and speech/face directions match `tools/hsk6_ready_preview_identity_pins.json`.
- **20/20** proposed canonical face-right actor scene ID, location ID, ordered characters, outfits, and directions match `tools/hsk6_face_right_identity_pins.json`.
- Existing HSK6_SC041 and SC047 preview candidates share SHA `824ed1f02e5f3a15b5889cc7db5e4349c5a4f68f` and are **941×1672 source reuse**, not newly composed exact 720×1280 WebPs. 14 of the 16 preview-ready scenes have no preview file.

`tools/run_hsk6_visual_staging.py` was committed to unify the two **existing** production tools into one local `main` checkout operation. It runs the original offline test suites, performs a fail-closed preflight, produces 20 lossless face-right cutout candidates and 16 exact 720×1280 previews, then (with `--publish`) commits/pushes only those outputs plus their SHA-provenance manifests. It does **not** mark scenes visually accepted.

The isolated Python environment cannot fetch private canonical GitHub binaries due to unavailable DNS/network routing. No new canonical visual binaries were generated, uploaded, or accepted by the runner in this session. Static connector-side SHA/identity verification **does not count** as successful execution of the original offline Python test suites or independent rendered visual QA. Prior isolated synthetic replays are separate evidence.

Run from a **clean local clone** with Pillow installed, Git remote `origin` matching `uysalayhan23/newChinese`, and a verified `main` checkout:

```bash
python tools/run_hsk6_visual_staging.py --publish
```

All commit messages include `[skip ci]`. No GitHub Actions were executed. Status remains HSK6 **128/250 physically present, 0/50 visually accepted**.
