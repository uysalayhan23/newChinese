# HSK6 SC013/SC019 canonical-pixel preserving staging v5 — 2026-10-14

- Canonical inputs for both scenes share the same exact Git blobs: BG `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba`, Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`, Zhang Wei `717828100874a371def695365e29b7c946147b4d`, canonical FG `6acadbee8403b5d78e0042431eec7af75fc94248`.
- The v5 candidate is a *deterministic* Pillow resized RGBA layering using the canonical BG and both canonical characters. A masked region of the unchanged background photographic pixels is re-applied as a nearer foreground table/plant occlusion. This **does not use AI re-generation of either character**.
- Source actors are transformed by scale and placement only. Native canonical WebP blobs remain untouched.
- Actual 720×1280 RGB WebP; 177114 bytes; SHA-256 `228b25e248b6fe2af712db81a7a14b99dd1d6bed885ff62741b4e82fb73d3678`; Git blob SHA `e670ec0ddcfc3f0e094151789daa22b382ecf68f`. Both scenes intentionally share this exact photographic/character composition, since the four source layers share the same blobs.
- Local review: both hands within frame; no prior semitransparent sofa/legs ghost effect, coffee table visibly in front of actor lower bodies. **Depth perspective and cross-scene canonical quality are still QA_PENDING** because the source living-room image has limited visible floor and the cutout styling differs between Liu Mei and Zhang Wei.
- Storage: `staging/hsk6/qa_pending/sc013/hsk6_sc013_canonical_occlusion_v5_staging.webp` and `staging/hsk6/qa_pending/sc019/hsk6_sc019_canonical_occlusion_v5_staging.webp`.
- **Not production output and NOT accepted.** Do not alter `content/hsk6/sc013`, `content/hsk6/sc019` visual manifests, `media_status.json`, the character identity/canonical locks, dialogue, or completion counters. Preserved all earlier staging candidates.

No Actions manually dispatched. `[skip ci]` on commit.
