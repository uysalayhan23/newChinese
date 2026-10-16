# HSK6 tolerance-based visual reassessment — 2026-10-16

Repository: `uysalayhan23/newChinese`, `main`. Baseline: `4ba09eb2bdb81e04c20eaef5e6b6f4f0ba0d7ae7`. Audit source: original user-provided `hsk6.zip`. Local Pillow decoded all 22 physical WebP files across HSK6 SC011, SC017, SC020, SC021 and SC022 (four layers each, plus previews for SC021 and SC022). Git blob SHA calculated from raw local bytes. Local SC020 staged preview is separate from the 22 production source WebPs.

## Updated user acceptance policy
Minor stylistic differences in shading, photorealism, lighting, color, and texture **alone** do not require re-generation if the characters remain identifiable, outfits/scene continuity reasonable, and physical files and composition are valid. Do not silently relax character identity, wrong location, foreground geometry, missing previews, or exact physical validation requirements. Full application acceptance remains separate from asset QA.

## Scene gates
- **SC011 / SC017:** both use the same physically decoded canonical library BG `8c3e7732156ba04375c846af6633475264b229a2`, FG `01c2add740504ca62d55e2226c53d8993e74fcc7`, Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`, Zhang Wei `717828100874a371def695365e29b7c946147b4d`. Minor CGI-versus-realism style difference is **not an independent replacement trigger**. Both production preview files are absent. Retain characters and scene metadata; finish a physically and visually valid preview before promotion.
- **SC020:** four canonical sources physically decode and agree with previously locked blob SHAs. The 720×1280 shadow-v3 preview exists in local QA staging but not as a production preview. Minor photorealism gap is tolerable in principle; foreground contact and overall scene still require final preview-specific QA. Do not overwrite canonical originals.
- **SC021:** four WebP source layers and 720×1280 preview physically decode. Existing preview blob: `2cab32aad9acbf8e4f2ec682b8b8d7d38c4d01c4`. The moderate visual stylistic difference alone does not warrant regeneration. Reuse is preferred subject to scene-specific occlusion and application acceptance.
- **SC022:** four WebP source layers and 720×1280 preview physically decode. Existing preview blob: `56f465a61f2e58c1d437f9098c66f6f126a2fc55`. Preserve canonical pair. Verify railing occlusion and actor apparent scale separately: these are spatial factors, not merely superficial style changes.

**Disposition:** no automatic full-scene PASS, no acceptance count changes, no mutation of visual manifests, media status, scene/dialogue, production artwork, LOCKS, or canonical identity. Do not run GitHub Actions. Text-only audit commit uses `[skip ci]`.
