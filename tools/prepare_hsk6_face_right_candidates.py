#!/usr/bin/env python3
"""Build HSK6 face-right layers, reusing approved Wang Ming unmirrored.

No Actions, no image upscaling, no identity recreation, no metadata acceptance.
Run in the checked-out repository with Pillow installed:
    python tools/prepare_hsk6_face_right_candidates.py

A mirrored cutout is only a QA candidate. It must be visually checked for
handedness, pose, expression, wardrobe, continuity and identity before reuse.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageOps
from visual_quality import git_blob_sha1

ROOT = Path(__file__).resolve().parents[1]

# Canonical sources verified physically in GitHub on 2026-10-10.
SOURCES = {
    "CHAR_WANG_MING_001": (
        "content/hsk2/sc001/assets/hsk2_sc001_char_wang_ming.webp",
        "067fcfe261c52adebc383f5551d7ed365abd747e",
        "OUTFIT_WANG_MING_WORK_01",
    ),
    "CHAR_LIU_MEI_001": (
        "content/hsk5/sc031/assets/hsk5_sc031_char_liu_mei.webp",
        "eea4742918bf5b78f222b54631de8f71a4c824a7",
        "OUTFIT_LIU_MEI_CASUAL_01",
    ),
    "CHAR_CHEN_YU_001": (
        "content/hsk5/sc034/assets/hsk5_sc034_char_chen_yu.webp",
        "ee14b09ae3c8cc4f5e539a54884798900f2ad85b",
        "OUTFIT_CHEN_YU_CASUAL_01",
    ),
}

SCENE_ACTORS = {
    **{n: "CHAR_WANG_MING_001" for n in range(1, 10, 2)},
    **{n: "CHAR_LIU_MEI_001" for n in range(11, 20, 2)},
    **{n: "CHAR_CHEN_YU_001" for n in range(21, 30, 2)},
    **{n: "CHAR_WANG_MING_001" for n in range(31, 40, 2)},
}


def target_path(scene: int, character_id: str, root: Path) -> Path:
    actor_name = character_id.removeprefix("CHAR_").removesuffix("_001").lower()
    return root / f"content/hsk6/sc{scene:03d}/assets/hsk6_sc{scene:03d}_char_{actor_name}.webp"


def preflight(root: Path, overwrite: bool) -> dict[str, Image.Image]:
    """Check every source and manifest before touching any destination."""
    sources = {}
    for identity, (relative, expected_sha, _outfit) in SOURCES.items():
        path = root / relative
        if not path.is_file() or git_blob_sha1(path) != expected_sha:
            raise ValueError(f"missing/mismatched canonical face-left source for {identity}")
        with Image.open(path) as img:
            if img.format != "WEBP":
                raise ValueError(f"source is not WebP: {path}")
            if "A" not in img.getbands():
                raise ValueError(f"source must have an alpha channel: {path}")
            alpha_min, alpha_max = img.getchannel("A").getextrema()
            if alpha_min == 255 or alpha_max == 0:
                raise ValueError(f"source must have a usable transparent silhouette: {path}")
            sources[identity] = img.convert("RGBA").copy()
    pin_file = root / "tools/hsk6_face_right_identity_pins.json"
    if not pin_file.is_file():
        raise ValueError("independent HSK6 scene identity pin file missing")
    pins = json.loads(pin_file.read_text(encoding="utf-8")).get("scenes", {})
    if set(pins) != {f"{n:03d}" for n in SCENE_ACTORS}:
        raise ValueError("independent HSK6 scene identity pins incomplete")
    for scene, identity in SCENE_ACTORS.items():
        folder = root / f"content/hsk6/sc{scene:03d}"
        manifest = folder / "visual_manifest.json"
        if not manifest.is_file():
            raise FileNotFoundError(manifest)
        data = json.loads(manifest.read_text(encoding="utf-8"))
        actors = data.get("characters") or []
        locked_identity = {
            "sceneId": data.get("sceneId"),
            "locationId": data.get("locationId"),
            "characters": [
                {field: actor.get(field) for field in
                 ("characterId", "outfit", "speechBubbleAnchor")}
                for actor in actors
            ],
        }
        if locked_identity != pins[f"{scene:03d}"]:
            raise ValueError(f"HSK6_SC{scene:03d}: independent scene/identity/outfit/facing/location drift")
        if (data.get("sceneId") != f"HSK6_SC{scene:03d}" or len(actors) != 2
                or actors[0].get("characterId") != identity
                or actors[0].get("speechBubbleAnchor") != "face_right"
                or actors[0].get("outfit") != SOURCES[identity][2]):
            raise ValueError(f"HSK6_SC{scene:03d}: scene/identity/outfit/facing drift")
        if data.get("assets", {}).get("characterA") != (
            f"assets/{target_path(scene, identity, root).name}"
        ):
            raise ValueError(f"HSK6_SC{scene:03d}: manifest asset path drift")
        dest = target_path(scene, identity, root)
        if dest.exists() and not overwrite:
            raise FileExistsError(f"existing actor must not be overwritten: {dest}")
    return sources


def prepare(root: Path = ROOT, *, overwrite: bool = False) -> list[str]:
    source_images = preflight(root, overwrite)
    # The approved Wang Ming cutout already faces RIGHT. Mirroring it would
    # introduce an incorrect LEFT-facing candidate and lose its approved blob SHA.
    mirrored = {k: ImageOps.mirror(v) for k, v in source_images.items()
                if k != "CHAR_WANG_MING_001"}
    outputs = []
    for scene, identity in SCENE_ACTORS.items():
        destination = target_path(scene, identity, root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if identity == "CHAR_WANG_MING_001":
            # Exact byte reuse preserves canonical identity and orientation.
            shutil.copyfile(root / SOURCES[identity][0], destination)
        else:
            mirrored[identity].save(destination, "WEBP", lossless=True, method=6)
        with Image.open(destination) as decoded:
            if decoded.format != "WEBP" or decoded.size != source_images[identity].size:
                raise ValueError(f"candidate failed WebP verification: {destination}")
            decoded.verify()
        outputs.append(
            f"HSK6_SC{scene:03d}: candidate WebP sha={git_blob_sha1(destination)}"
        )
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace-candidates", action="store_true",
                        help="Explicitly overwrite existing unapproved candidate layers")
    args = parser.parse_args()
    for line in prepare(overwrite=args.replace_candidates):
        print(line)
    print("20 face-right layers staged. Wang Ming reuses approved canonical bytes;"
          " Liu Mei/Chen Yu mirrored outputs remain QA candidates. No scene accepted.")


if __name__ == "__main__":
    main()
