# Visual QA Rebaseline — HSK1 through HSK5_SC005

Status: **ACTIVE REPAIR GATE**

Physical 5/5 WebP presence alone no longer proves visual acceptance.

## Locked user decision

- Audit character identity continuity from HSK1 through HSK5_SC005.
- Regenerate/rebase all character layers from HSK5_SC006 onward against canonical identities.
- Audit BG and FG from HSK1 onward and repair blurred/low-resolution/placeholder assets.
- GitHub Actions must not be used.

## Confirmed defects

- HSK1_SC020 background: 320x180 — blocked.
- HSK1_SC028 preview: 120x213 — blocked.
- HSK1_SC011 foreground: 1x1 placeholder/transparent asset — below the new required-FG quality floor.
- HSK3_SC002 reused breakroom BG/FG: 360x640 — below quality floor.
- HSK3_SC013 Zhang Wei character: 160x284 — blocked.
- HSK4_SC002/004/006/008/010 previews are byte-identical to their backgrounds — invalid composite previews.
- HSK5_SC005 canonical references: Zhang Wei 600x900 and Wang Ming 507x900 — character floor PASS.
- HSK5_SC006 starts the mandatory post-baseline character regeneration zone.

## Quality floors

- BG >= 540x960
- FG >= 540x960
- PREVIEW >= 720x1280
- CHAR >= 500x750
- PREVIEW may never be byte-identical to BG.
- A quality-blocked scene remains visual pending.

## Repair order

1. HSK1 low-resolution/placeholder BG-FG-PREVIEW.
2. HSK1_SC031-SC050 character identity review.
3. HSK2_SC001-SC010 character rebaseline and low-resolution repairs.
4. HSK3/HSK4 low-resolution reuse repair and invalid preview reconstruction.
5. HSK5_SC001-SC005 final baseline confirmation.
6. HSK5_SC006 onward full character regeneration/rebase.
7. Complete HSK5/HSK6 only after the quality gate passes.
8. Recreate english-learning from repaired Chinese main.
