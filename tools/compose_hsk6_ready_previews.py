#!/usr/bin/env python3
"""Produce 720x1280 HSK6 QA-pending preview WebPs from 4 verified layers.

Only the 16 scenes already holding BG + CHAR_A + CHAR_B + FG are eligible by
default. This script never marks a scene accepted; independent visual QA is
required before any batch/manifest status transition.

From an up-to-date local checkout:
    python tools/compose_hsk6_ready_previews.py
    python tools/compose_hsk6_ready_previews.py --publish

--publish commits only scene-specific preview WebPs and their provenance
manifests with [skip ci]. No GitHub Actions or automation is invoked.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from PIL import Image

from visual_quality import git_blob_sha1, webp_dimensions

ROOT = Path(__file__).resolve().parents[1]
TARGET = (720, 1280)
READY = (2, 6, 8, 12, 18, 22, 24, 28, 30, 41, 43, 44, 46, 47, 49, 50)
ROLES = ("background", "characterA", "characterB", "foreground")


def read_manifest(scene: int, root: Path) -> tuple[Path, dict]:
    import json
    directory = root / f"content/hsk6/sc{scene:03d}"
    return directory, json.loads((directory / "visual_manifest.json").read_text(encoding="utf-8"))


def expected_character_filename(scene: int, character_id: str) -> str:
    slug = character_id.removeprefix("CHAR_").removesuffix("_001").lower()
    return f"assets/hsk6_sc{scene:03d}_char_{slug}.webp"


def preflight(scene: int, root: Path) -> tuple[dict, dict[str, Path], Path]:
    if scene not in READY:
        raise ValueError(f"HSK6_SC{scene:03d} is not in verified 4-layer staging")
    directory, manifest = read_manifest(scene, root)
    if manifest.get("sceneId") != f"HSK6_SC{scene:03d}":
        raise ValueError("scene identity mismatch")
    # Independent scene/character/outfit/orientation lock. Source SHA alone
    # does not prove wardrobe, facing or the correct narrative location.
    import json
    identity_file = root / "tools/hsk6_ready_preview_identity_pins.json"
    if not identity_file.is_file():
        raise ValueError("HSK6 identity/outfit/facing pin file is missing")
    identity_pin = json.loads(identity_file.read_text(encoding="utf-8")).get(
        "scenes", {}).get(f"{scene:03d}")
    actual = {
        "sceneId": manifest.get("sceneId"),
        "locationId": manifest.get("locationId"),
        "characters": [
            {field: actor.get(field) for field in
             ("characterId", "outfit", "speechBubbleAnchor")}
            for actor in (manifest.get("characters") or [])
        ],
    }
    if not identity_pin or actual != identity_pin:
        raise ValueError(f"HSK6_SC{scene:03d}: locked scene/location/identity/outfit/facing drift")
    chars = manifest.get("characters") or []
    if (len(chars) != 2 or
            any(manifest.get("assets", {}).get(f"character{letter}") !=
                expected_character_filename(scene, actor.get("characterId", ""))
                for letter, actor in zip(("A", "B"), chars))):
        raise ValueError("character identity/path mismatch")
    paths = {role: directory / manifest["assets"][role] for role in (*ROLES, "preview")}
    import json
    pinned_file = root / "tools/hsk6_ready_preview_blobs.json"
    if not pinned_file.is_file():
        raise ValueError("pinned canonical source SHA manifest is missing")
    scene_pins = json.loads(pinned_file.read_text(encoding="utf-8")).get(
        "scenes", {}).get(f"{scene:03d}")
    if not isinstance(scene_pins, dict) or len(scene_pins) != 4:
        raise ValueError(f"HSK6_SC{scene:03d}: incomplete source SHA pinset")
    for role in ROLES:
        p = paths[role]
        if not p.is_file():
            raise FileNotFoundError(f"missing {role}: {p}")
        dim = webp_dimensions(p)
        if not dim:
            raise ValueError(f"not WebP: {p}")
        minsize = TARGET if role in ("background", "foreground") else (500, 750)
        if dim[0] < minsize[0] or dim[1] < minsize[1]:
            raise ValueError(f"low resolution {role}: {dim}, required {minsize}")
        if scene_pins.get(p.name) != git_blob_sha1(p):
            raise ValueError(f"HSK6_SC{scene:03d}: {role} canonical source blob SHA drift")
    return manifest, paths, directory


def compose(scene: int, root: Path = ROOT, *, replace: bool = False) -> tuple[Path, Path]:
    manifest, paths, directory = preflight(scene, root)
    output = paths["preview"]
    record = manifest.get("previewComposition") or {}
    inputs = {role: git_blob_sha1(paths[role]) for role in ROLES}
    if (output.exists() and not replace
            and webp_dimensions(output) == TARGET
            and record.get("inputBlobs") == inputs
            and record.get("previewBlob") == git_blob_sha1(output)):
        return output, directory / "visual_manifest.json"
    with Image.open(paths["background"]) as bg:
        canvas = bg.convert("RGBA").resize(TARGET, Image.Resampling.LANCZOS)
    bounds = []
    for role, xc in (("characterA", 0.285), ("characterB", 0.715)):
        with Image.open(paths[role]) as img:
            layer = img.convert("RGBA")
        alpha_min, alpha_max = layer.getextrema()[3]
        if alpha_min == 255 or alpha_max == 0:
            raise ValueError(f"{role} must have a usable transparent silhouette")
        scale = min(round(TARGET[1] * .70) / layer.height,
                    round(TARGET[0] * .56) / layer.width)
        w, h = round(layer.width * scale), round(layer.height * scale)
        x = max(0, min(TARGET[0] - w, round(TARGET[0] * xc - w / 2)))
        y = TARGET[1] - h
        if bounds:
            prevx, prevw = bounds[-1]
            overlap = max(0, min(x + w, prevx + prevw) - max(x, prevx))
            if overlap > round(TARGET[0] * .14):
                raise ValueError(f"character bounding boxes overlap excessively: {overlap}px")
        bounds.append((x, w))
        canvas.alpha_composite(layer.resize((w, h), Image.Resampling.LANCZOS), (x, y))
    # Foreground is the nearest depth layer, so composite it after actors.
    with Image.open(paths["foreground"]) as fg:
        if fg.getbands()[-1] != "A":
            raise ValueError("foreground must have an alpha channel")
        overlay = fg.convert("RGBA").resize(TARGET, Image.Resampling.LANCZOS)
        alpha_min, alpha_max = overlay.getchannel("A").getextrema()
        if alpha_min == 255 or alpha_max == 0:
            raise ValueError("foreground must have a usable transparent depth layer")
        canvas.alpha_composite(overlay)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "WEBP", quality=92, method=6)
    with Image.open(output) as created:
        if created.format != "WEBP" or created.size != TARGET:
            raise ValueError("physical WebP output failed size/format verification")
        created.verify()
    manifest["previewComposition"] = {
        "method": "hsk6_deterministic_alpha_composite_v1",
        "inputBlobs": inputs, "previewBlob": git_blob_sha1(output),
    }
    import json
    manifest_file = directory / "visual_manifest.json"
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    return output, manifest_file


def checked_git(root: Path, *args: str, capture: bool = False) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, check=True,
                            capture_output=capture)
    return result.stdout.strip() if capture else ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true",
                        help="Commit/push only composed previews and provenance manifests")
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--scenes", type=int, nargs="*", default=list(READY))
    args = parser.parse_args()
    if args.publish:
        if checked_git(ROOT, "branch", "--show-current", capture=True) != "main":
            parser.error("publishing permitted only from main")
        if checked_git(ROOT, "status", "--porcelain", capture=True):
            parser.error("publishing requires a clean working tree")
    outputs = []
    for scene in args.scenes:
        output, manifest = compose(scene, replace=args.replace)
        outputs.extend((output, manifest))
        print(f"HSK6_SC{scene:03d}: physically staged {TARGET[0]}x{TARGET[1]} preview")
    if args.publish:
        checked_git(ROOT, "add", "--", *(str(p.relative_to(ROOT)) for p in outputs))
        if checked_git(ROOT, "diff", "--cached", "--name-only", capture=True):
            checked_git(ROOT, "commit", "-m",
                        "Stage HSK6 16 physical preview candidates for visual QA [skip ci]")
            checked_git(ROOT, "push", "origin", "main")
    print("All generated previews remain QA-pending; no scene was accepted.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        sys.exit(1)
