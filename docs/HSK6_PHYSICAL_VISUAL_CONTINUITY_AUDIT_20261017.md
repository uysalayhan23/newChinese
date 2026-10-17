# HSK6 — physical WebP, visual and canonical continuity audit (2026-10-17)

Repository: `uysalayhan23/newChinese`, branch `main`. Verified baseline HEAD: `0e21bb20b91033684e98f9f8e72bbc0fa3e50fdb`.
Sources: the user's original `hsk6.zip`, the user's six-preview transfer ZIP, existing SC011/SC017 staging WebPs, and the SC026/032/038 staging-v2 QA bundle. Local Pillow decoded actual binary WebPs. GitHub `main` recursive Git tree was returned with `truncated=false`; production preview Git blob SHAs were compared against raw source ZIP bytes. This is an audit-only record, **not** production asset promotion or final application acceptance.

## Physical and manifest QA

- Original `hsk6.zip` SHA-256: `3bbfad7f8133fd542c7b431e195dc689f72886fd4d0ec235ff5a71a580d319db`.
- Original archive: character 100/100, background 37/37, foreground 37/37, original preview 32/32, each WebP physically decoded by Pillow. Additional six preview WebPs from previously promoted transfer ZIP: 6/6 physically decoded. **212/212 binary decodes PASS**. All 38 previews decode as RGB 720×1280; character/FG layers have nonempty RGBA alpha channels; background layers are RGB.
- All **50/50** original archive `scene.json` and `visual_manifest.json` pairs agreed on scene ID, location ID, and character ID set. No asset name-to-character manifest mismatch detected in the original archive.
- Remote `main`: **38/50** production preview file paths exist; the 38 Git blob SHAs match the original archive's 32 previews plus the six exact transfer files, including SC036 blob `ffc9a603e2bd34bf1cf3ced7a76f6a854cf0b6d9`. These checks establish binary identity, not final visual acceptance.
- **12 missing production previews:** SC011, SC013, SC016, SC017, SC019, SC020, SC026, SC032, SC038, SC042, SC045, SC048.
- Source 100 character WebPs across 50 scenes map to **10 unique blob SHAs**: Zhang Wei 3 variants, Liu Mei 2, Li Na 2, Chen Yu 2, Wang Ming 1. Reuse counts are not themselves a visual identity acceptance.
- The six newly present preview files SC004/010/014/034/036/040 still lack original per-scene BG/FG binaries in the user's HSK6 archive. Preview existence alone does not satisfy complete four-layer canonical asset or application acceptance.

## Ordered visual QA gates

1. **SC011 / SC017 — staging asset QA PASS; production missing.** Exact same four source blob SHAs, correct library location and identifiable Liu Mei/Zhang Wei. The two *existing* 720×1280 RGB staging WebPs were Pillow-decoded; both 238,350 bytes, Git blob SHA `d292165b0ba5b65094822be2a6054460ab615c54`, SHA-256 `087bc81e520646e2d95879a303a1fb0baee60e14151d71a34ba8a39e014e252f`. Visual composite inspection: visible hands/faces and credible floor contact. Minor CGI/photo style gap is tolerated under the existing policy. No production preview uploaded; no full scene acceptance.
2. **SC013 / SC019 — HOLD_DEPTH.** Both original home source pairs decode at 768×1365, with identical source BG/FG SHA. The coffee-table foreground and actor foot-plane contradiction remains. Resizing, swapping identical FG, or unsupported masking cannot fix it. No promotion.
3. **SC020 — STAGING/HOLD.** Four canonical sources decode. An original shadowless staging candidate was also physically decoded at 720×1280 (blob `a370d6dc40816df83493fdf946e49242b7315239`). Previously recorded shadow-v3 candidate `76dbd4ece57386d3ac71bbd7ecb9b0c4c7fee68b` is preserved as an earlier local-QA finding; its exact v3 binary was **not freshly re-decoded in this audit**. No production preview and no application PASS.
4. **SC021 — existing production preview preserved.** Original four source WebPs and 720×1280 RGB production preview decode, preview SHA `2cab32aad9acbf8e4f2ec682b8b8d7d38c4d01c4`. Visual inspection found no obvious major floor-depth contradiction. This is not full application acceptance.
5. **SC022 — HOLD_GEOMETRY despite existing preview.** All four layers and 720×1280 preview decode, blob `56f465a61f2e58c1d437f9098c66f6f126a2fc55`. Detailed preview inspection: the stone railing hides much of Zhang Wei's body and his apparent scale relative to Liu Mei remains implausible. Do not waive this as a minor style difference; protect canonical layers until real perspective/occlusion QA succeeds.
6. **SC026 / SC032 / SC038 — staging-v2 asset QA PASS; production missing.** Previously prepared foreground-safe reposition candidate WebPs were newly Pillow-decoded as 720×1280 RGB, and exact Git blob SHA matched bundle sidecars: SC026 `ceca83f32fe89c510844de4820c22c379f207f88`, SC032/SC038 `5398498273bbf47abaa10445f9775f71304dff0b`. Prior proxy alpha overlap gates passed, but these proxies cannot prove natural depth or canonical BG/FG completeness. No promotion.
7. **SC016 / SC042 / SC045 / SC048 — HOLD_HOME_BGFG.** No original per-scene home BG/FG in uploaded archive, and existing SC013/019 home geometry cannot be safely reused. SC045 additionally uses one-off Li Na and Zhang Wei source blob variants (`052e3d74becb…`, `316717c873fa…`) relative to neighboring scenes; identity/outfit continuity requires scene-specific review, with no assumed defect solely from uniqueness.

## Non-negotiable gates and next actions

- Do not alter `LOCKS.md`, `LOCKED_STEP_01–20`, Golden Demo V1, canonical source WebPs, scene/dialogue manifests, media-status files, production previews, acceptance counters, or unrelated scenes based on this audit.
- Next preview candidates for **separate binary-write + SHA and visual promotion gates**: SC011 and SC017; then SC026/032/038 only after physical per-scene layer completeness and scene-specific review. Keep SC020 shadow-v3 staged; resolve SC013/019 home geometry and SC022 railing/scale independently. Four other home scenes stay HOLD.
- No GitHub Actions. Commits must include `[skip ci]`. No force-push, extra branch, or claim of full application PASS without end-to-end evidence.

**Outcome:** physical integrity PASS for listed binaries; remote 38 preview SHA matches; staging candidates as specified; no new full-scene acceptance.
