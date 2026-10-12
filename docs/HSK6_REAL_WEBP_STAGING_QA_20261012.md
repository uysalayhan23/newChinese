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

## 2026-10-12 follow-up: repo-ready 12-preview package and remote blob check
A new staging ZIP, `NewChinese_HSK6_12_Previews_Repo_Ready_STAGING.zip`, contains exact repository-relative paths for **12 WebP preview files + 12 provenance `visual_manifest.json` files**, along with package QA metadata. The package passed a ZIP CRC check and each of the 12 physical previews was independently decoded with Pillow and checked against its staged SHA, byte count, and exact 720x1280 resolution. Scene `status` is preserved as pending; the package is NOT an acceptance marker.

| Scene | Local preview Git blob SHA-1 | Bytes |
|---|---|---:|
| HSK6_SC002 | `9d694d70648dc930525b15f0d48f43847fa07e71` | 292430 |
| HSK6_SC006 | `fd67897cd41de8702bf8391126d22aaf69a0f529` | 186932 |
| HSK6_SC008 | `9d694d70648dc930525b15f0d48f43847fa07e71` | 292430 |
| HSK6_SC012 | `f8c664bbfb3b8f5006a923dd3cb61c495f2133f9` | 167990 |
| HSK6_SC018 | `f8c664bbfb3b8f5006a923dd3cb61c495f2133f9` | 167990 |
| HSK6_SC022 | `56f465a61f2e58c1d437f9098c66f6f126a2fc55` | 289330 |
| HSK6_SC024 | `be64dcbdc7a74bcd0727cc3a3d7c103181d0cb76` | 170410 |
| HSK6_SC028 | `56f465a61f2e58c1d437f9098c66f6f126a2fc55` | 289330 |
| HSK6_SC030 | `be64dcbdc7a74bcd0727cc3a3d7c103181d0cb76` | 170410 |
| HSK6_SC044 | `e117ed2b699e1300e4b02e60356782ab385c9185` | 304096 |
| HSK6_SC046 | `4defc756632221415ce0cfb483d1effa55d6afc8` | 198434 |
| HSK6_SC050 | `e117ed2b699e1300e4b02e60356782ab385c9185` | 304096 |

These 12 paths contain **7 unique output WebP blobs**. A read-only GitHub `get blob by SHA` verification found **0/7 already exist** in the remote repository (all returned 404), so simply pointing a Git tree to those SHAs is not a valid publication method. Actual binary blob upload remains necessary. This is an explicit **remote upload pending** gate, not permission to commit simulated assets or overwrite canonical identity locks. GitHub Actions were not used.
