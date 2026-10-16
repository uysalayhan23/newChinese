# HSK6 missing preview triage — 2026-10-16

Baseline main HEAD: `ed7d140c7fbd32607d546a1f3ca037b351595ca5`. Source: user's original HSK6 zip; actual Pillow decode and raw Git blob SHA checks. **No production promotion or acceptance change.**

## 18 missing production previews
- **Source complete (5):** SC011, SC013, SC017, SC019, SC020; all four WebP layers physically available and decoded.
- **Missing both BG and FG (13):** SC004, SC010, SC014, SC016, SC026, SC032, SC034, SC036, SC038, SC040, SC042, SC045, SC048. Character layers are present, but new preview cannot be truthfully completed without actual scene-specific background and foreground.
- **Protect existing local staging:** SC011 and SC017 share physical 720x1280 candidate blob SHA `d292165b0ba5b65094822be2a6054460ab615c54`; SC020 shadow-v3 staging candidate 720x1280 SHA `76dbd4ece57386d3ac71bbd7ecb9b0c4c7fee68b`. No regeneration needed.
- **Keep SC013/SC019 HOLD:** existing source BG and FG decode at 768x1365, and prior candidate from those sources is likewise 768x1365 and has unresolved coffee-table/feet depth conflict; resizing is not a substitute for geometric QA.
- Repo recursive Git tree (19,139 entries, not truncated) includes historical SC011/SC017 staging preview candidates with *other* SHAs but **not** the exact `d292165...` binary. Do not substitute a different blob for the validated local candidate without separate QA.

## Decision
Prioritize sources for the 13 missing BG/FG pairs instead of creating synthetic/borrowed assets. Retain already validated SC011/SC017/SC020 staging files; no production upload until a real binary write and subsequent SHA verification is possible. Full scene acceptance cannot follow from source presence alone. Existing SC021 and SC022 production previews remain untouched. Protect LOCKS, scenes, dialogues and canonical layers; GitHub Actions not run. Documentation-only commit uses `[skip ci]`.
