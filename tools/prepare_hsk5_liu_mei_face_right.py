#!/usr/bin/env python3
"""Prepare canonical-identity Liu Mei face-right candidate assets for SC033/035/037/039.

Mirrors the physically approved existing face-left Liu Mei cutout; no character
regeneration or face re-interpretation. A mirror is a *candidate*, not proof
of artistic/continuity suitability. Does not set any scene to 'complete' and
does not issue manual approval receipts.

Usage from a checked-out repository (requires Pillow and the source WebP):
    python tools/prepare_hsk5_liu_mei_face_right.py
    python tools/prepare_hsk5_liu_mei_face_right.py --replace-candidates

The source is content/hsk5/sc031/assets/hsk5_sc031_char_liu_mei.webp,
pinned to its existing canonical Git blob SHA.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from PIL import Image, ImageOps

from visual_quality import git_blob_sha1, webp_dimensions

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content/hsk5/sc031/assets/hsk5_sc031_char_liu_mei.webp"
EXPECTED_SOURCE = "eea4742918bf5b78f222b54631de8f71a4c824a7"
SCENES = (33, 35, 37, 39)
MINIMUM = (720, 1280)


def candidate_paths(number: int) -> tuple[Path, Path]:
    directory = ROOT / f"content/hsk5/sc{number:03d}"
    return (directory / f"assets/hsk5_sc{number:03d}_char_liu_mei.webp",
            directory / "visual_manifest.json")


def prepare(replace_candidates: bool = False) -> list[str]:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"canonical left-facing asset is absent: {SOURCE}")
    actual = git_blob_sha1(SOURCE)
    if actual != EXPECTED_SOURCE:
        raise ValueError(f"source identity mismatch: {actual} != {EXPECTED_SOURCE}")
    dimensions = webp_dimensions(SOURCE)
    if dimensions is None or dimensions[0] < MINIMUM[0] or dimensions[1] < MINIMUM[1]:
        raise ValueError(f"canonical source resolution {dimensions} below {MINIMUM}")
    with Image.open(SOURCE) as source:
        rgba = source.convert("RGBA")
    if rgba.getextrema()[3][0] == 255 or rgba.getextrema()[3][1] == 0:
        raise ValueError("source must be a non-empty transparent cutout")
    candidate = ImageOps.mirror(rgba)
    # Preflight ALL scenes before mutating any file, avoiding partial batch writes
    # if a later scene has drifted from the locked character/scene manifest.
    for scene in SCENES:
        target, manifest_path = candidate_paths(scene)
        if not manifest_path.is_file():
            raise FileNotFoundError(f"manifest missing: {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        characters = manifest.get("characters") or []
        if (manifest.get("sceneId") != f"HSK5_SC{scene:03d}"
                or len(characters) != 2
                or characters[0].get("characterId") != "CHAR_LIU_MEI_001"
                or characters[0].get("speechBubbleAnchor") != "face_right"
                or characters[1].get("characterId") != "CHAR_ZHANG_WEI_001"
                or characters[1].get("speechBubbleAnchor") != "face_left"):
            raise ValueError(f"SC{scene:03d} does not match locked Liu Mei face_right scene")
    results = []
    for scene in SCENES:
        target, manifest_path = candidate_paths(scene)
        if target.exists() and not replace_candidates:
            results.append(f"SKIPPED: SC{scene:03d} already has a physical actor layer")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        candidate.save(target, "WEBP", lossless=True, method=6)
        with Image.open(target) as result:
            if result.format != "WEBP" or result.size != rgba.size:
                raise ValueError(f"written candidate failed WebP dimensions: {target}")
            result.verify()
        result_blob = git_blob_sha1(target)
        results.append(f"CREATED: SC{scene:03d} face_right candidate SHA {result_blob}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace-candidates", action="store_true",
                        help="Explicitly replace existing candidate files; never accept them automatically")
    args = parser.parse_args()
    for message in prepare(args.replace_candidates):
        print(message)
    print("PENDING: Independent visual identity, orientation, narrative and "
          "continuity QA. Do not mark complete or preapprove SHA receipts.")


if __name__ == "__main__":
    main()
