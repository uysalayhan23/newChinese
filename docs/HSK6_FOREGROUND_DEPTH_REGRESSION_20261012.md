# HSK6 preview foreground depth regression — 2026-10-12

## Scope
Verification of foreground/character compositing order after commits `a0801377abf1f105f433564d684c5fd9a00fadfb` and `d07ad537ea41294faee357c99fa4e669c6bff69a`.

## Synthetic Pillow execution: PASS
Executed on an isolated Python environment with Pillow 12.3.0. Recreated the regression test's synthetic fixtures:
- Target: 720×1280; input foreground: 941×1672, alpha 120 in the bottom rectangle; actor: 600×900 transparent PNG-like RGBA fixture containing a red ellipse.
- At preview pixel (205,1200), **old** composition (BG → FG → actor) produced RGB (200,80,100).
- At preview pixel (205,1200), **corrected** composition (BG → actor → FG) produced RGB (141,73,74).
- The new test's predicate `red < 185` FAILS on the old ordering and PASSES on the corrected ordering.
- These pixel measurements validate the ordering regression fixture; they do **not** constitute execution of the complete repository unittest suite.

## Not executed
- Physical canonical WebP integration tests, image visual QA and the complete repository Python suites could not be run against the repository's actual binary input files. GitHub connector binary blob decoding failed and direct GitHub DNS/network access was unavailable.
- No scene or media acceptance status was changed.

## Operational constraints
No Actions used; no locked, canonical binary or scene content changed; commit uses [skip ci].
