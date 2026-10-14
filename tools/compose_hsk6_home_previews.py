#!/usr/bin/env python3
"""Offline SC013/SC019 *staging-only* candidate composer. Never changes scene assets or manifests.

Usage: python tools/compose_hsk6_home_previews.py
Requires Pillow and the four existing WebP layers per scene.\nCandidate output needs human depth and identity QA; do NOT accept automatically.
"""
from __future__ import annotations

import hashlib
import json
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SIZE = (720, 1280)
SCENES = ("013", "019")
EXPECTED = {
    "background": "86c8e17e3e63a3acbf5d2ce4e205e191627cdcba",
    "characterA": "1944d13b2565d618ad183da64fd33ef68a11191a",
    "characterB": "717828100874a371def695365e29b7c946147b4d",
    "foreground": "6acadbee8403b5d78e0042431eec7af75fc94248",
}

def git_sha(payload: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()

def load_layer(path: Path, expected: str) -> Image.Image:
    payload = path.read_bytes()
    actual = git_sha(payload)
    if actual != expected:
        raise ValueError(f"{path}: Git blob SHA mismatch {actual} != {expected}")
    with Image.open(BytesIO(payload)) as im:
        if im.format != "WEBP":
            raise ValueError(f"{path}: not WebP")
        return im.convert("RGBA")

def contain(image: Image.Image, target_height: int) -> Image.Image:
    width = max(1, round(image.width * target_height / image.height))
    return image.resize((width, target_height), Image.Resampling.LANCZOS)

def build(number: str) -> dict:
    scene = f"hsk6_sc{number}"
    directory = ROOT / "content" / "hsk6" / f"sc{number}"
    manifest = json.loads((directory / "visual_manifest.json").read_text(encoding="utf-8"))
    if manifest["sceneId"] != f"HSK6_SC{number}" or manifest["locationId"] != "LOC_ZHANG_HOME_001":
        raise ValueError(f"{scene}: scene/location lock mismatch")
    assets = directory / "assets"
    layers = {}
    for role, blob_sha in EXPECTED.items():
        path = assets / manifest["assets"][role]
        layers[role] = load_layer(path, blob_sha)

    bg = layers["background"].resize(SIZE, Image.Resampling.LANCZOS)
    canvas = bg.copy()
    # Place the intended two speaking characters facing one another.
    for role, x_frac in (("characterA", 0.29), ("characterB", 0.69)):
        actor = contain(layers[role], round(SIZE[1] * 0.52))
        x = round(SIZE[0] * x_frac - actor.width / 2)
        y = SIZE[1] - actor.height
        if x < 0 or x + actor.width > SIZE[0]:
            raise ValueError(f"{scene}: {role} would be clipped: x={x}, width={actor.width}")
        canvas.alpha_composite(actor, (x, y))
    fg = layers["foreground"].resize(SIZE, Image.Resampling.LANCZOS)
    canvas.alpha_composite(fg)
    output = BytesIO()
    canvas.convert("RGB").save(output, "WEBP", quality=92, method=6)
    payload = output.getvalue()
    with Image.open(BytesIO(payload)) as decoded:
        if decoded.format != "WEBP" or decoded.size != SIZE:
            raise ValueError(f"{scene}: invalid output")
    dest = ROOT / "staging" / "hsk6" / "qa_pending" / f"sc{number}" / f"{scene}_deterministic_candidate.webp"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise FileExistsError(f"Refusing to overwrite existing preview: {dest}")
    dest.write_bytes(payload)
    return {"scene": manifest["sceneId"], "preview": str(dest.relative_to(ROOT)),
            "gitBlob": git_sha(payload), "sha256": hashlib.sha256(payload).hexdigest(),
            "size": list(SIZE), "inputBlobs": EXPECTED.copy(), "acceptance": "QA_PENDING_DEPTH_AND_IDENTITY", "productionAssetsUnchanged": True}

def main() -> int:
    try:
        # Preflight both scenes before producing any output.
        for number in SCENES:
            scene_dir = ROOT / "content" / "hsk6" / f"sc{number}"
            manifest = json.loads((scene_dir / "visual_manifest.json").read_text(encoding="utf-8"))
            for role, expected in EXPECTED.items():
                path = scene_dir / "assets" / manifest["assets"][role]
                if git_sha(path.read_bytes()) != expected:
                    raise ValueError(f"{number}/{role}: missing or hash-mismatched source")
            if (ROOT / "staging" / "hsk6" / "qa_pending" / f"sc{number}" / f"hsk6_sc{number}_deterministic_candidate.webp").exists():
                raise FileExistsError(f"{number}: staging candidate already exists; will not overwrite")
        result = [build(n) for n in SCENES]
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"BLOCKED (no acceptance changes): {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
