# HSK6 SC041/047 Exact-Source Preview Staging (2026-10-10)

- SHA-pinned West Lake canonical source: `HSK2_SC040` physical preview `824ed1f02e5f3a15b5889cc7db5e4349c5a4f68f` (**941×1672**, not 720×1280).
- HSK6_SC041 and HSK6_SC047 manifest character IDs, outfits, face direction and location match HSK2_SC040.
- All four staged source layers match HSK2_SC040's four Git blob SHAs, not just the setting or one character.
- Preview is staged by exact Git blob reuse. This is a **physical candidate**; requested 720×1280 pixel output has **not** been produced.
- Physical count moves from 126/250 to **128/250**, preview missing count to 48. Scene acceptance **remains 0/50**.
- Pending: exact 720×1280 render (do not upscale low-resolution source), independent visual/continuity QA, exact reviewed output SHA receipt, eventual scene acceptance.
- GitHub Actions must not be used; commits use `[skip ci]`.
