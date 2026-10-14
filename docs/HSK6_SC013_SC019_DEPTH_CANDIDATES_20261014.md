# HSK6 SC013/SC019 — depth-corrected preview candidate evidence (2026-10-14)

Repository: `uysalayhan23/newChinese`, branch `main`.

## Input verification

The four canonical WebP files were supplied in the conversation and independently checked against the exact Git blob hashes currently referenced by both scene asset folders:

| Role | Git blob SHA |
|---|---|
| `background` | `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba` |
| `characterA` (Liu Mei) | `1944d13b2565d618ad183da64fd33ef68a11191a` |
| `characterB` (Zhang Wei) | `717828100874a371def695365e29b7c946147b4d` |
| `foreground` | `6acadbee8403b5d78e0042431eec7af75fc94248` |

## Local candidate files — not yet published to GitHub

Two improved visuals were generated from the references, resized via Pillow with Lanczos resampling and physically encoded to WebP at 720×1280:

| Scene | Local filename | Bytes | SHA-256 | Local Git blob SHA |
|---|---|---:|---|---|
| SC013 | `hsk6_sc013_depth_corrected_candidate.webp` | 172472 | `e34fe931f2570267bdeabdfd0a6913a22bf1cb84625edbbf820096c16a1cb40f` | `00662ad233744133acd005594648383f3d6cc578` |
| SC019 | `hsk6_sc019_depth_corrected_candidate.webp` | 188362 | `368ee9fb9c5eb85045ef56e446348c04f626c3bdc4f5c1ff780a7b4bf371aaed` | `aa10238394b62960d3f983781abcdd0d7121a650` |

The previews now show Liu Mei and Zhang Wei on a rug in front of the sofa with the coffee table clearly in the foreground, rather than apparently standing on the coffee table. Only two visible characters, intended outfit palettes, textless/logoless portrait scene, and coherent foreground depth were observed.

**CRITICAL QA CLASSIFICATION: `DEPTH_VISUAL_CANDIDATE_PASS`, `CANONICAL_IDENTITY_AND_PROVENANCE_PENDING`.** These are AI-assisted *recompositions*, **not deterministic alpha composites of unchanged canonical RGBA pixels**. Facial identity and any other differences against locked characters must be reviewed before adoption; visual quality alone does not authorize canonical acceptance. Neither SHA above refers to a published GitHub blob unless a future actual upload is separately confirmed. Scene manifests and counters remain unchanged.

## Still missing exact-location BG/FG

- `LOC_ZHANG_OFFICE_001`: SC001/SC007/SC031/SC037 → 8 physical files.
- `LOC_PUBLIC_LIBRARY_001`: SC011/SC017/SC033/SC039 → 8 physical files.
- `LOC_NEIGHBORHOOD_001`: SC023/SC029 → 4 physical files.
- `LOC_ELECTRONICS_STORE_001`: SC035 → 2 physical files.

**Total: 22**. Historical sources of 540×960 or 576×1024 remain unsuitable for direct 720×1280 acceptance without approved high-resolution replacements. The exact visual bibles in `locations/LOC_*/visual_bible.json` remain binding. No unrelated scene substitution or fabricated quality passes.

## Tool and environment boundary

GitHub admin/push rights are live, but an isolated local image processing container cannot send its generated binary files directly through the GitHub connector's `create_blob(content=base64)` action. Publishing requires a supported binary bridge; no pretend successful upload. All visual files and dialogue locks stay untouched by this audit. Do not trigger GitHub Actions; commit messages include `[skip ci]`.
