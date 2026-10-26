# HSK6 SC045 visual candidate — QA PENDING

This directory contains review-only visual sources, NOT canonical runtime assets.

## Targeted foreground correction (2026-10-26)

- BG and both character WebPs remain byte-for-byte unchanged from the prior review package.
- FG now contains isolated, soft-focus near-camera foliage restricted to the lower-right border (720x1280, transparent elsewhere). It is no longer blank.
- FG visible pixels (>5 alpha): 10,162. Bounding rectangle: (610,1043)-(720,1260).
- FG overlaps neither character alpha mask; faces and speaking gestures remain uncovered.
- Updated Preview composites BG, Zhang Wei, Li Na and the repaired FG at 720x1280.
- The lossless Pillow composite is pixel-exact against the four original and revised layers. Review Preview uses WebP quality 75 (mean absolute channel error 2.55/255 vs the lossless composite), with visual inspection.
- Positive tests: nonempty FG, zero character overlap, 720x1280, valid transparent layer, composite reconstruction.
- Negative tests: blank FG rejected; FG artificially covering the speaker face rejected.

## Still pending — DO NOT MARK COMPLETE

- The generated faces in the candidate do not yet have proven approval against the across-HSK canonical character identity and CGI style.
- The changed BG/camera geometry is not formally accepted for Zhang Wei's home.
- Runtime files in content/hsk6/sc045/assets and visual/media status must remain untouched.
- Golden, historical COMPLETE, HOLD, and REVIEW locks remain unchanged.
