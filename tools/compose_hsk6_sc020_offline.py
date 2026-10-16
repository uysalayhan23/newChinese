#!/usr/bin/env python3
"""Stage a SHA-locked HSK6_SC020 candidate from four canonical WebPs.

Requires a local checkout containing the real binary assets and Pillow:
    python tools/compose_hsk6_sc020_offline.py

Uses the repository's tested four-layer compositor and foreground-occlusion
guards; writes ONLY staging/hsk6/qa_pending/sc020. Never publishes or accepts.
No network, Actions, or GitHub operations.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from compose_hsk6_odd11_staging import source_check, stage

ROOT = Path(__file__).resolve().parents[1]
SCENE = "020"
CHARACTERS = [
    {"characterId": "CHAR_ZHANG_WEI_001", "outfit": "OUTFIT_ZHANG_WEI_CASUAL_01", "speechBubbleAnchor": "face_right"},
    {"characterId": "CHAR_LI_NA_001", "outfit": "OUTFIT_LI_NA_CASUAL_01", "speechBubbleAnchor": "face_left"},
]
PIN = {
    "sceneId": "HSK6_SC020",
    "locationId": "LOC_PUBLIC_LIBRARY_001",
    "characters": CHARACTERS,
    "assets": {
        "background": {"path": "content/hsk6/sc020/assets/hsk6_sc020_bg.webp", "sha": "8c3e7732156ba04375c846af6633475264b229a2"},
        "characterA": {"path": "content/hsk6/sc020/assets/hsk6_sc020_char_zhang_wei.webp", "sha": "44a7a521b7fa64466111c30f6830904081c3767d"},
        "characterB": {"path": "content/hsk6/sc020/assets/hsk6_sc020_char_li_na.webp", "sha": "a02f88b5075f6cb590d8c0f23219b0e5fa3e80d0"},
        "foreground": {"path": "content/hsk6/sc020/assets/hsk6_sc020_fg.webp", "sha": "01c2add740504ca62d55e2226c53d8993e74fcc7"},
    },
}


def compose(root: Path = ROOT) -> tuple[Path, Path]:
    scene_dir = root / "content/hsk6/sc020"
    scene = json.loads((scene_dir / "scene.json").read_text(encoding="utf-8"))
    if (scene.get("sceneId") != PIN["sceneId"] or
            scene.get("locationId") != PIN["locationId"] or
            scene.get("characterIds") != [x["characterId"] for x in CHARACTERS]):
        raise ValueError("SC020 scene / location / speaker identity drift")
    if (scene_dir / "assets/hsk6_sc020_preview.webp").exists():
        raise FileExistsError("Production preview exists: refuse overwrite")
    layers = source_check(root, SCENE, PIN)
    return stage(SCENE, layers, root, PIN)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    output, report = compose(args.root.resolve())
    print(f"SC020 staged: {output}\nPhysical QA evidence: {report}\nHuman visual QA: PENDING; accepted=false")


if __name__ == "__main__":
    main()
