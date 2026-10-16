# HSK6 SC011/SC017 preview promotion gate — 2026-10-16

Base main HEAD: `c63670ef17b7b60a0ea704a003b1bf1258c2d4d6`. Sources: user-uploaded original HSK6 archive, local Pillow compositor, and GitHub directory SHA inventory.

Both scenes' canonical sources match exact Git blobs:
- background `8c3e7732156ba04375c846af6633475264b229a2`
- Liu Mei `1944d13b2565d618ad183da64fd33ef68a11191a`
- Zhang Wei `717828100874a371def695365e29b7c946147b4d`
- foreground `01c2add740504ca62d55e2226c53d8993e74fcc7`

Pillow physically decoded locally composed **both** 720×1280 WebP staging images. Because input blobs are identical and deterministic composition parameters match, the two preview blobs match exactly, Git blob SHA `d292165b0ba5b65094822be2a6054460ab615c54`, file length 238350 bytes. Visual review under the user's tolerant policy: identifiable Liu Mei and Zhang Wei, correct scene, usable silhouettes; minor photoreal/CGI difference is not a reason to regenerate. Staging asset QA suitable for promotion review.

**Production upload NOT performed:** Connected GitHub interface can create base64 blobs, but there is no verified binary bridge from the local Pillow file to that GitHub action in this session. Do not label production previews present or full scenes accepted before upload SHA verification. No manifests, LOCKS or canonical assets were changed.

SC020 shadow-v3 candidate remains a 720×1280 staging-only preview; preserve its previously documented QA and do not regenerate. SC021 existing preview remains unchanged. SC022 railing occlusion and apparent-scale issues require scene-specific geometric review; do not treat a minor style tolerance as permission to ignore a severe spatial mismatch.

No GitHub Actions. Audit-only commit uses `[skip ci]`. No acceptance counters changed.
