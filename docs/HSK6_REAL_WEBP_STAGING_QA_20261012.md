# HSK6 real canonical WebP staging QA — 2026-10-12

Repository: `uysalayhan23/newChinese`, branch `main`.

## Real binary transfer completed
- The user supplied `NewChinese_HSK6_15_Canonical_WebP.zip` (2,460,509 bytes).
- All 15 canonical WebPs were extracted into an isolated Pillow staging workspace.
- **15/15 source Git blob SHA-1 values verified** against the source manifest.
- **64/64 scene-specific preview input SHA references verified** for the sixteen four-layer scene setups.
- All source images decoded as actual WebP via Pillow 12.3.0.

## Produced in local staging (NOT YET pushed as binary Git blobs)
- **16/16** physical preview images at exactly 720 x 1280 WebP, derived deterministically from background, character A, character B and foreground. SHA provenance recorded in staging manifests.
- **20/20** physical, lossless `face_right` character WebP candidates produced by horizontal mirroring of three pinned canonical sources (Wang Ming, Liu Mei, Chen Yu).
- An independent offline integration QA suite against real source bytes passed **7/7 tests**, including source SHA, 16 preview provenance, and per-pixel equality of 20 mirrored candidates.
- Manual inspection contact sheets exist in the isolated staging artifact, but that inspection does NOT constitute full canonical character acceptance.

## Identity quality-gate exceptions
Live `content/visual_quality_gate.json` reports `identityRegeneration.status=required`. Four preview scenes reference source character SHAs not in `approvedCanonicalGitBlobSha1`:
- **HSK6_SC041**
- **HSK6_SC043**
- **HSK6_SC047**
- **HSK6_SC049**

The other **12 previews** pass the present automated source-identity whitelist check and physical checks, but should remain QA-pending until full visual approval.

All 20 mirrored character files are **candidates only**. Their generated SHA values are not automatically approved canonical identities. Do not update scene/batch acceptance merely because their physical and pixel-mirroring QA passed.

## Safe publishing boundary
This document records the actual local production and gate results. Binary WebP outputs are not yet committed to the GitHub repository because the connected GitHub write API requires the image bytes as in-call base64, and no supported cross-runtime binary upload bridge was confirmed. The staged ZIPs can be supplied to the user; do not claim remote media publication before verifying GitHub blob SHAs.

Do not run GitHub Actions. Use `[skip ci]` in commit messages. Preserve locked scene dialogue, locations, identity pins, and source canonical layers.
