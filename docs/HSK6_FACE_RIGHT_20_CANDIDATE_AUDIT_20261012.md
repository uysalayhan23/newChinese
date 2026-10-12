# HSK6 SC001–SC039 face_right candidate audit — 2026-10-12

Repository: `uysalayhan23/newChinese`; active branch: `main`.

## Completed physical and canonical source checks

Source archive: user-supplied `NewChinese_HSK6_15_Canonical_WebP.zip`, 15/15 real WebP Git blob SHA matches verified in Pillow.

Twenty local `face_right` candidates were generated losslessly from three approved source identities. An independent Pillow comparison against the canonical source image flipped horizontally (`ImageOps.mirror(source.convert("RGBA"))`) found:
- **20/20**: fully pixel-identical RGBA, including transparent pixels.
- **20/20**: WebP decoded and usable alpha.
- **20/20**: independent manifest identity/outfit/location/`speechBubbleAnchor` preflight passed at staging time.

| Identity | Scenes | Approved canonical source | Generated candidate Git blob SHA | Source-pixel comparison | Gate |
|---|---|---|---|---|---|
| Wang Ming | SC001,003,005,007,009,031,033,035,037,039 (10) | `067fcfe261c52adebc383f5551d7ed365abd747e` | `6f01b2a15fda3aa13192b6cb81fdfd4a4be8ad13` | 10/10 PASS | REVIEW REQUIRED |
| Liu Mei | SC011,013,015,017,019 (5) | `eea4742918bf5b78f222b54631de8f71a4c824a7` | `1944d13b2565d618ad183da64fd33ef68a11191a` | 5/5 PASS | REVIEW REQUIRED |
| Chen Yu | SC021,023,025,027,029 (5) | `ee14b09ae3c8cc4f5e539a54884798900f2ad85b` | `55885be8637e7df4b7ff300a710ed9d1b6f78847` | 5/5 PASS | REVIEW REQUIRED |

## Why the candidates are NOT published or accepted

Live `content/visual_quality_gate.json` retains `identityRegeneration.status="required"` from HSK5_SC006 forward. **None of the three new mirrored output SHAs** is currently listed in `approvedCanonicalGitBlobSha1`; `approvedCharacterSha256` has no scene-specific overrides.

A pixel-perfect mirror guarantees physical image fidelity but **does not independently establish canonical face orientation**, gesture handedness, clothing continuity or narrative placement. In particular, `speechBubbleAnchor="face_right"` is manifest metadata and should not be inferred from the mere fact an image was mirrored. A side-by-side contact sheet of the original and mirrored characters is in the staging artifacts. The three candidate source orientations require independent acceptance; changing the canonical allowlist solely to pass automation would bypass the quality gate.

Result: **20 candidate physical QA PASS / 0 accepted / 0 published**. No quality-gate whitelist or locked character bible modifications are authorized by this technical test alone.

## Four repaired previews and original 12 retained

One atomic, non-forced `main` commit `c251eaaea3b8b646dfec29a459acd66a724bab49` linked two new physical preview blobs across SC041,043,047,049 and relinked eight character-layer paths to two **already approved canonical** source SHAs; updated the four live manifests and one source-pin manifest (17 changed paths, `[skip ci]`).

Re-fetched all four repaired scene assets and manifests from remote GitHub: **4/4 preview SHA, character source SHA, per-scene pin and retained camera/lighting/speaker metadata PASS**. The prior **12/12** GitHub previews were also fetched and their exact original blob SHAs preserved.

All 16 HSK6 previews now physically exist on `main`; scene acceptance fields remain pending. GitHub Actions were not run.

## Next safe gate

Perform individualized orientation, anatomy/gesture, silhouette, outfit, face and scene-continuity review for Wang Ming, Liu Mei, and Chen Yu. Only after documented visual acceptance consider explicit canonical authorization of the 3 candidate SHA values (or replacing with already-approved correctly oriented canonical sources), then publish 20 destination paths and verify exact remote blob SHAs. Do not auto-approve from mirror/pixel checks.
