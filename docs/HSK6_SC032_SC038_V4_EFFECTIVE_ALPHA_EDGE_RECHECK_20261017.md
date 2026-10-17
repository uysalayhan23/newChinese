# HSK6 SC032 / SC038 — real V4 opacity-weighted FG edge QA, camera/scene BGFG HOLD (2026-10-17)

Repo `uysalayhan23/newChinese`, `main`; verified active HEAD `b8941efb82e51ff990c8e820ac9fc714cb25b4a5`. The user's earlier requested baseline `1d0dfc05366f12d61fb8085d235ebbec5e849abf` is an ancestor; advancing from actual HEAD avoids reverting concurrent QA. Scope **staging-only evidence**; canonical source/LOCKS/acceptance immutable.

## New independent *physical* QA

Loaded original user's `hsk6.zip` and `NewChinese_HSK6_SC032_SC038_V4_VERIFIED_STAGING_NOT_PRODUCTION_20261017.zip`. ZIP CRC and the exact six raw source Git blob SHA pins passed; both actor RGBA WebPs, donor RGB background, RGBA FG, V4 FG and V4 RGB preview physically decoded with Pillow. V4 actual binary pins for both scenes remain:

- FG: RGBA **720×1280**, **84,614 bytes**, exact Git SHA `84631be9ed27a64a29e134e84037919b23277440`, SHA256 `c79a0c4dbfbc6807a94c598afd378682213894fd992356fcfe3cd3b66bcb62aa`.
- PREVIEW: RGB **720×1280**, **215,124 bytes**, exact Git SHA `ca8c43043c628d2b69ef7e59625bca49f1586533`, SHA256 `5a69c580d7a85d160eae0602f956440b3800bd39dd07b80363c13de05f6bc5bc`.
- Both SC032 / SC038 FG binaries match *each other byte for byte*, and both previews similarly match. This does not merge two distinct locked dialogue and camera presets.

### Newly computed opacity-weighted overlap (not merely binary alpha threshold)

Reprojected real source actor alpha-crops using the existing exact source x,y,width,height: Zhang Wei (66,614,387,597) and Chen Yu (313,473,403,737) with Pillow Lanczos. For each overlapping pixel, computed `alpha(actor) × alpha(FG) / 255²`, summing to **fully opaque pixel equivalents**. Results per scene:

| Actor | Both alpha > 0 | Both alpha >= 32 | Both alpha >= 80 | Fully opaque pixel equivalents | Effective % of actor alpha mass |
| --- | ---: | ---: | ---: | ---: | ---: |
| Zhang Wei | **0** | 0 | **0** | **0** | 0 |
| Chen Yu | **1,196** | **139** | **0** | **47.5459** | **0.05016%** |

For Chen Yu, median foreground alpha across the 1,196 overlapping pixels was 12. The maximum FG alpha observed was 246 **where the actor alpha is correspondingly low**; do not conflate this with opaque facial/gesture masking. The V4 isolated whole-right-counter foreground has no proven high-opacity actor cover, but retains measurable soft-edge interaction. This is physical **staging edge QA** only; it is not a target camera/ground-plane proof or scene acceptance.

## Independent transfer check and immutable blockers

GitHub `fetch_blob` using the two precise V4 Git SHA values returned **404 NOT_FOUND** at this pass, so local SHA validation is **NOT** GitHub binary upload or backread PASS. No Base64 text was substituted for WebP and no production Git blob/tree/image was written.

- Target `CAM_HSK6_SC032_01` and `CAM_HSK6_SC038_01` are not proven numerically equivalent to donor `CAM_HSK6_SC035_01`. Donor image corridor vanishing estimate (~379.25,396.25) is only a within-image proxy; it cannot independently calibrate two absent target BG images.
- **Four scene-specific target canonical BG/FG files are physically missing**, and both production previews remain absent. Donor SC035 BG is reference-only. Lower-resolution HSK3_SC042 (360×640) and HSK5_SC008 (576×1024) alternate cameras were previously rejected; upscaling is not evidence.
- Both `layerPlan.approved=false`; maintain `HOLD_CAMERA_AND_CANONICAL_BGFG` and protect all SC026, other HOLDs, LOCKS, original voice/dialogues and Golden. Global Zhang Wei HSK1–HSK6 evaluation stays **last P999**, not begun.

**Next authorized step:** obtain verifiable scene-specific camera parameters / ground-plane landmarks and actual compatible 720×1280 scene BG/FG; repeat four-layer occlusion/safe-area checks; then and only then attempt exact GitHub WebP `create_blob(base64)`, readback and fast-forward `[skip ci]` promotion. No Actions and no force push.

Local reproducibility bundle `HSK6_SC032_SC038_V4_OPACITY_WEIGHTED_QA_ONLY_20261017.zip` contains the executed Pillow+NumPy QA script and original per-scene measurement JSONs. That local ZIP has **not** been uploaded as GitHub production imagery.
