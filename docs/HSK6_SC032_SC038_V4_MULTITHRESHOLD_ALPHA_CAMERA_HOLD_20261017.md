# HSK6_SC032/SC038 — independent V4 multithreshold alpha-edge QA and camera/BGFG HOLD (2026-10-17)

Repo `uysalayhan23/newChinese/main`. Verified base HEAD `e3600b164c731f782b406bed29bd6b5f3bc060ad`. **Read-only real WebP recheck; this commit contains only two staging QA JSONs and this report**. Nothing in `content/` production art, LOCKS, dialogue, visual manifests, accepted statuses or P999 final task was changed.

## Real binary and exact source verification

Materialized physical `NewChinese_HSK6_SC032_SC038_V4_VERIFIED_STAGING_NOT_PRODUCTION_20261017.zip` (990207 B; SHA256 `893b9973724419e04fa03d3df5609e18cbf4f053dee174d17624e820f5cea7d8`) alongside source `hsk6.zip`. ZIP entries were read as real bytes, decoded with Pillow and checked against Git blob SHA derived from byte length and raw content, not merely PNG representation:

- Donor SC035 BG `b0ba989e06045ea92a0c4fd6ebf580877f4acc48`; original donor FG `dd7b43d996a33e40ff2c5cf86b5c4fa297238061`.
- Zhang Wei `44a7a521b7fa64466111c30f6830904081c3767d`, Chen Yu `ee14b09ae3c8cc4f5e539a54884798900f2ad85b`. Character source pixels untouched. Cross-level visual identity comparison deferred to user-requested final task P999.
- V4 whole-object right-only FG **RGBA 720×1280, 84614 B**, SHA `84631be9ed27a64a29e134e84037919b23277440`. V4 preview **RGB 720×1280, 215124 B**, SHA `ca8c43043c628d2b69ef7e59625bca49f1586533`.
- Source V4 SC032 and SC038 FG files are byte-identical, and both previews byte-identical, *but the target scene camera presets and locked dialogues remain distinct*.

## Additional independent mask thresholds (new real QA)

Recomputed both original actor silhouettes from alpha-cropped WebPs, Pillow Lanczos at the exact V3/V4 unchanged x/y/width/height. Measured intersections with actual V4 RGBA FG alpha and actor A–B alpha at all specified thresholds. For SC032 and SC038 **identical** figures:

| Alpha threshold | Zhang Wei vs V4 FG | Chen Yu vs V4 FG | Actor A–B |
| --- | ---: | ---: | ---: |
| >=1 | 0 | **1196** | 52 |
| >=8 | 0 | **558** | 3 |
| >=32 | 0 | **139** | 1 |
| >=80 | 0 | **0** | 0 |
| >=128 / >=192 / >=240 | 0 | 0 | 0 |

The previously quoted **0 intersections** is therefore true **only at alpha>=80 and stronger**, not for low-alpha antialias fringes. Chen Yu FG overlap at alpha-positive is bounded x=619..715, y=554..1004, but the substantive threshold>=8 area is x=623..633, y=637..746. Alpha>=32 overlap is x=628..631, y=657..721, i.e. a narrow soft edge near the counter/gesture. No confirmed opaque cover. In this entire alpha-positive overlap, the independently recomposed RGB image changes by mean **1.4214** gray levels per channel (out of 255), p95=5, max=21, and 25 pixels change by more than 10 in any channel. This is a subtle yet measurable edge, **not** a release PASS, nor justification to mask just the hand or retouch the protected original FG.

**Alpha-dependent foot endpoint:** the same unchanged source actor crop ends at y=1210/1209 (A/B, threshold>=1), y=1203/1200 (>=80), y=1202/1195 (>=240). Prior y=1203/1203 was based on a different visibility criterion; do not imply physical actor pose was changed. The image-space corridor estimate (donor vanishing proxy ~379.25,396.25) cannot certify target camera identity or target ground plane.

## Real GitHub camera and transfer checks

- Current `main` tree's four target canonical BG/FG files and two production previews are absent. V4 FG and preview Git blob GET each returned **404** for the *exact expected SHA* during this audit; no actual Base64 blob was created, committed or backread. Local ZIP and local SHA are **not** GitHub transfer PASS.
- Code search for `CAM_HSK6_SC032_01` and `CAM_HSK6_SC038_01` found no repository camera calibration definition. This does not prove an absolute absence of camera evidence; no independently approved per-scene target lens, homography or floor mapping is available in reviewed sources.
- V4 BG is an unchanged SC035 same-store reference, not a separately approved target-camera source. Four canonical target BG/FG paths remain missing, `layerPlan.approved=false`; a source-perspective match inside SC035 alone is insufficient for SC032 or SC038.
- **Scene disposition:** physical staged source integrity PASS; alpha>=80 occlusion proxy PASS, low-alpha edge flagged; *camera/ground plane, canonical BG/FG, binary GitHub transfer, complete four-layer scene acceptance* HOLD. Neither V4 stage media, nor source characters, nor SC026 or any other HOLD were changed. No image pixels edited or new camera presumptively adopted.

Next approved work: scene-specific camera/source geometry with independent floor/vanishing landmarks, assess faint right-counter halo against Chen Yu without actor-specific erase or artificial clipping, then regenerate compatible *real* BG/FG and four-layer preview; accept only verified real WebP GitHub roundtrip with proper camera/identity/occlusion evidence. No GitHub Actions; all commits `[skip ci]`, no force-push.
