# HSK6_SC013 / HSK6_SC019 — home depth HOLD, 2026-10-16

Repository: `uysalayhan23/newChinese`, branch `main`. Source: user-provided original `hsk6.zip`; actual Pillow WebP decode and Git-blob SHA-1 inventory. Baseline main HEAD before recording: `ba273873dfa99fbc905ea17b78d0012b874216cb`.

## Verified canonical source identity
- Both scene manifests use `LOC_ZHANG_HOME_001` and remain `visual-assets-pending`.
- Both background WebPs have the same Git blob SHA: `86c8e17e3e63a3acbf5d2ce4e205e191627cdcba`.
- Both foreground WebPs have the same Git blob SHA: `6acadbee8403b5d78e0042431eec7af75fc94248`.
- Both Liu Mei WebPs share SHA `1944d13b2565d618ad183da64fd33ef68a11191a`.
- Both Zhang Wei WebPs share SHA `717828100874a371def695365e29b7c946147b4d`.
- Neither SC013 nor SC019 has a production preview in the user-provided source archive.

## Search for alternative source geometry within uploaded HSK6
The exact location is referenced by SC013, SC016, SC019, SC042, SC045 and SC048.
Only SC013 and SC019 contain physical BG/FG files. The BG/FG SHA pairs are identical, so swapping their foregrounds cannot create a different depth model. The other four scene folders lack physical BG/FG assets. This result applies **only to the uploaded HSK6 source archive**; it does not prove that no alternative asset exists elsewhere.

## Visual acceptance blocker
Pillow composites from original four layers still place standing character feet implausibly in relation to foreground coffee-table geometry. Reusing the identical foreground cannot resolve that mismatch. The result is not visually acceptable, even if WebP files physically decode.

**Decision: HOLD — no production promotion, no canonical source replacement and no scene acceptance.** A compatible camera/foreground or canonical pose with correct floor-plane occlusion requires independent visual review. Avoid faked masking, restyling or silent source changes.

This is an audit-only documentation commit. GitHub Actions must not be run. LOCKS, scene/dialogue content, and canonical WebP assets remain unchanged.
