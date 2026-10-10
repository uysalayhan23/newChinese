# HSK6 Production Readiness & Verified Blockers, 2026-10-10

Repo `uysalayhan23/newChinese` main. User-authorized GitHub connector **read/write** available; GitHub Actions never invoked.

## Real outcomes

- 20/20 locked candidate scene manifests match expected face-right character ID, role, outfit and orientation.
- 16/16 ready preview scenes have 4 physical inputs each; all 64/64 Git blob SHA pins match `tools/hsk6_ready_preview_blobs.json`.
- 14 unique BG/FG/CHAR source blob WebP headers validated, all pass intended source resolution minimums.
- Two physical canonical-source preview WebPs added at HSK6_SC041 and HSK6_SC047, both exact reuses of accepted HSK2_SC040 preview blob `824ed1f02e5f3a15b5889cc7db5e4349c5a4f68f`. Source is **941×1672**, not the requested 720×1280. Their exact four layer Git blob SHAs, characters and outfits match HSK2_SC040. **Not accepted** until 720×1280 output + continuity/image QA.
- HSK6 physical state: **128/250 WebPs**, 122 missing. HSK6 accepted: **0/50**.
- `tools/hsk6_ready_preview_identity_pins.json` now independently protects 16 scene IDs, locations, both canonical actors, outfits and facing. The compositor checks this plus its independent 64 SHA source pins before encoding. Four further failure tests were committed to `test_compose_hsk6_ready_previews.py`, for a total of 11. They **have not been run locally** because this session cannot transfer the connector's repo images into its isolated Pillow runtime.
- Twelve preview-ready scenes `002,006,008,012,018,022,024,028,030,044,046,050` reuse Zhang Wei blob `44a7a521b7fa64466111c30f6830904081c3767d`, whose older accepted HSK2_SC001 manifest labels `OUTFIT_ZHANG_WEI_WORK_01`, while those HSK6 scenes label it `OUTFIT_ZHANG_WEI_CASUAL_01`. This metadata conflict may not be a visible clothing difference, but **must not silently pass wardrobe QA**.
- The 20 face-right character asset candidates have **not been physically created** and remain QA-pending.

## Gates

1. An Actions-free environment with a local checkout and Pillow decodes the actual canonical inputs.
2. Execute `python -m unittest discover -s tools/tests -p 'test_prepare_hsk6_face_right_candidates.py' -v` and `python -m unittest discover -s tools/tests -p 'test_compose_hsk6_ready_previews.py' -v`.
3. Generate actual 20 mirror **candidates** using `tools/prepare_hsk6_face_right_candidates.py` and 16 exact 720×1280 WebPs using `tools/compose_hsk6_ready_previews.py`. Upload/commit `[skip ci]` but do not auto-accept.
4. Confirm canonical appearance, wardrobe, facing, FG layering and previous→current→next narrative continuity by visual review, then close only passing scenes.

No lock, dialogue, story or canonical character bible has been modified in these operations.
