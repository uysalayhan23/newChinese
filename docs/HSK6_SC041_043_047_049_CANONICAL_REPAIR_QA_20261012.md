# HSK6 SC041 / SC043 / SC047 / SC049 — canonical repair QA staging (2026-10-12)

Repo: `uysalayhan23/newChinese`, target `main`. **No scene acceptance implied**.

## Root cause verified by real WebP inspection

All four existing source pairs use a recurring different Li Na + Zhang Wei design. Their character blob SHA values `052e3d74becbd8376eceeb96bf28adf417b6fbc8` (Li Na) and `316717c873fade2a1e98564bdf6ac037e7cc354e` (Zhang Wei) are NOT in `content/visual_quality_gate.json.identityRegeneration.approvedCanonicalGitBlobSha1`. The local decoded visual contact sheet shows these sources depart conspicuously from the verified HSK6_SC044/046/050 character designs.

Approved, original-byte canonical replacements already present in the repository:
- Li Na: `a02f88b5075f6cb590d8c0f23219b0e5fa3e80d0`, physical source `content/hsk6/sc012/assets/hsk6_sc012_char_li_na.webp` (1086×1448 with alpha).
- Zhang Wei: `44a7a521b7fa64466111c30f6830904081c3767d`, physical source `content/hsk6/sc002/assets/hsk6_sc002_char_zhang_wei.webp` (600×900 with alpha).

These source SHA values are on the existing approved list; no policy whitelist change is needed. Scene actor identities, outfits and `speechBubbleAnchor` settings remain unchanged.

## Local four-scene preview repair candidates

Deterministic, original-blob layers BG → Li Na → Zhang Wei → FG were composited in Pillow at 720×1280:
| Scenes | Location | BG / FG locked sources | Preview blob SHA | placement centers (Li Na, Zhang Wei) |
|---|---|---|---|---|
| SC041, SC047 | LOC_WEST_LAKE_001 | `25f85210...` / `5c82abba...` | `e09aa94f41e6f8be79dcf950a30f63ad88cd17ce` | (0.47, 0.79) |
| SC043, SC049 | LOC_CITY_PARK_001 | `d6dc8b28...` / `7fd16427...` | `768d90c9b2a4a5cc845860874c38d8a69a7364c1` | (0.29, 0.74) |

Both previews physically decoded as WebP at exactly 720×1280. Visual QA noted that at West Lake, part of Li Na's lower body is naturally occluded by the foreground railing; adjusted placement ensures her head/upper body remain visible. No source was mirrored; approved canonical SHA remains unchanged. All scenes still require final scene-level acceptance and repo publishing validation.

**Safe staging ZIP:** `NewChinese_HSK6_4_Canonical_Repair_SAFE_STAGING.zip` (12 scene-relative WebP files, four partial preview provenance patches, four source-pin patches, QA ledger). It is in the conversation artifact space; it has NOT been committed as binary media. NEVER overwrite full live `visual_manifest.json` files with patches. If publishing, move the two newly composed preview Git blobs to GitHub first; atomically map four preview paths plus eight reused approved canonical character blobs and merge the source pin/manifest changes into their CURRENT full content. Avoid intermediate inconsistent scene trees.

## Twenty face-right candidates — real offline QA

All 20 generated mirror candidates were checked against the real original canonical source bytes with Pillow/Numpy:
- 20/20 matching **alpha channels** pixel-for-pixel.
- 20/20 matching **visible RGB pixels** (where source alpha > 0).
- All output WebPs opened correctly with correct dimensions and transparency.
- Original SHA-pinned canonical sources are the approved Wang Ming, Liu Mei and Chen Yu assets.
- 20/20 remote `main` scene `visual_manifest.json` entries were fetched and matched the independent scene / location / characters / outfit / anchor pins.

Three unique candidate Git blob SHAs:
- Wang Ming: `6f01b2a15fda3aa13192b6cb81fdfd4a4be8ad13`
- Liu Mei and Chen Yu: `1944d13b2565d618ad183da64fd33ef68a11191a` / `55885be8637e7df4b7ff300a710ed9d1b6f78847` (map to their actual source identity by package ledger before remote upload)

**Important QA nuance:** Raw decoded RGBA arrays differ in RGB values of *fully transparent pixels*. WebP lossless re-encoding normalizes unseen color bytes. Visible RGB and alpha match exactly; calling full decoded RGBA byte equality PASS would be inaccurate.

**Canonical acceptance remains BLOCKED** for all 20 mirror variants. Their new Git SHA values are not on the approved identity list, and mere mirroring does not automatically authorize them. Inspect and approve identity/handedness/scene continuity before any publication. Do not change the identity quality gate as a shortcut.

## Protected remote status

The previously staged twelve scenes SC002, SC006, SC008, SC012, SC018, SC022, SC024, SC028, SC030, SC044, SC046, SC050 and their `previewComposition` records **must remain unchanged**. Existing scene statuses remain QA-pending.

**Actions forbidden:** No GitHub Actions were invoked. All repository commits use `[skip ci]`.
