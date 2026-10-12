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
**SUPERSEDED / DO NOT APPLY ITS MANIFESTS:** The earlier `NewChinese_HSK6_12_Previews_Repo_Ready_STAGING.zip` contained 12 reconstructed `visual_manifest.json` files. Those files preserve only a subset of the real repository's fields, and would delete protected metadata such as `cameraPreset`, `lightingPreset`, and `activeSpeakerBubble` if uploaded as replacements. The 12 WebP files in that archive passed CRC, SHA, Pillow and exact 720x1280 checks, but the accompanying manifest files are UNSAFE for direct overwrite. All outputs remain staging-only and QA-pending.

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


## 2026-10-12 safe package revision: preserve full scene manifests

The replacement `NewChinese_HSK6_12_Previews_SAFE_STAGING.zip` contains:
- Twelve original physical preview WebP files only, in exact `content/hsk6/scNNN/assets/` relative paths;
- `preview_provenance_patches.json` containing *only* per-scene `previewComposition` additions and expected WebP SHA;
- `SHA_VERIFICATION.json` and a safety README;
- **Zero replacement `visual_manifest.json` files**.

Local QA re-checked all 12 WebP files as 720x1280, validated their Git blob SHA-1 values and source provenance, and verified ZIP CRC. There are 7 unique preview blobs across the 12 scenes.

**Mandatory publication ordering:** (1) physically upload each preview binary and verify its exact GitHub-returned blob SHA; (2) fetch that scene's CURRENT live `visual_manifest.json` from `main`, preserving all existing fields; (3) merge ONLY the relevant `previewComposition` field, then update with `[skip ci]` under SHA concurrency protection. Never replace full manifests from either staging ZIP. Preserve all character, location, camera, lighting, active-speaker, status and locked dialogue metadata.

As of this report, no physical preview WebP has been verified uploaded to the remote. Do not mark any scene as accepted solely on these technical checks. The four identity-blocked previews and 20 unaccepted face-right candidates remain out of this safe media package. GitHub Actions not used.


## 2026-10-12 verified remote binary upload closure (supersedes pending statements above)

**12/12 physical preview WebPs are now present on GitHub `main`.** This supersedes earlier historical notes in this report that said the previews had not been uploaded.

1. The actual WebP bytes were bridged from the local Pillow output to GitHub's base64 `create_blob` API, using temporary conversation-file reads. All **7/7 unique Git blob SHA-1 values matched exactly**, with no binary regeneration.
2. A 12-entry Git tree was built on the existing repository tree and committed to `main` as **`1d21d29b8f062ae07e0a17ff302b6e1fd2912c26`**: `Stage 12 SHA-verified HSK6 720x1280 preview WebPs for QA [skip ci]`.
3. All 12 preview files were re-fetched from GitHub `main` using `encoding=base64` and their remote SHA values checked against the physical locally generated preview SHAs (**12/12 PASS**).
4. The CURRENT existing 12 `visual_manifest.json` files were separately fetched from `main`; scene IDs, location, characters, wardrobe and orientation were checked against independent locks; `previewComposition` was appended without altering existing fields. Commit **`e17f373a9927597227a6dda23ea8901a57feb889`**: `Record provenance for 12 staged HSK6 previews without changing scene acceptance [skip ci]`.
5. All 12 remote manifests were fetched again and verified with **12/12 provenance PASS**, retaining `cameraPreset`, `lightingPreset`, `activeSpeakerBubble`, `characters`, `locationId`, and scene `status="visual-assets-pending"`.

**Remote-stage scenes:** HSK6_SC002, SC006, SC008, SC012, SC018, SC022, SC024, SC028, SC030, SC044, SC046, SC050. Exactly 12 previews at 720x1280 WebP; 7 unique binary blobs. These are physical QA-staged previews, **not accepted scene closures**.

**Still blocked:** SC041, SC043, SC047, SC049 require independent canonical identity approval/repair before the previews can pass the quality gate. The 20 mirrored `face_right` candidate WebPs remain generated locally but **unapproved** for visual handedness/pose/continuity; they were NOT published to GitHub. Do not bypass the gate or overwrite locked sources.

All commits used `[skip ci]`; no GitHub Actions were invoked.
