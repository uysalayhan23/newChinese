#!/usr/bin/env python3
"""Offline physical QA for SC013/SC019 candidates; NEVER performs visual acceptance."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

EXPECTED = {
    "bg": "86c8e17e3e63a3acbf5d2ce4e205e191627cdcba",
    "char_liu_mei": "1944d13b2565d618ad183da64fd33ef68a11191a",
    "char_zhang_wei": "717828100874a371def695365e29b7c946147b4d",
    "fg": "6acadbee8403b5d78e0042431eec7af75fc94248",
}

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def examine(paths: list[Path], input_dir: Path, suffix: str) -> dict:
    sources = {}
    for name, expected in EXPECTED.items():
        path = input_dir / ("hsk6_sc013_" + name + ".webp")
        if not path.is_file():
            raise FileNotFoundError(path)
        payload = path.read_bytes()
        actual = git_blob_sha(payload)
        if actual != expected:
            raise ValueError(f"Canonical {name} mismatch: {actual}")
        with Image.open(path) as im:
            if im.format != "WEBP":
                raise ValueError(f"Canonical {name} not WebP")
            sources[name] = {"blob": actual, "size": list(im.size), "mode": im.mode}
    previews = []
    for scene in ("013", "019"):
        path = next((p for p in paths if p.name == f"hsk6_sc{scene}_{suffix}.webp"), None)
        if path is None:
            raise FileNotFoundError(f"hsk6_sc{scene}_{suffix}.webp")
        payload = path.read_bytes()
        with Image.open(path) as im:
            if im.format != "WEBP" or im.size != (720, 1280) or im.mode != "RGB":
                raise ValueError(f"{path.name}: bad WebP format/size/mode")
            im.load()
        previews.append({
            "scene": f"HSK6_SC{scene}", "filename": path.name,
            "bytes": len(payload), "gitBlob": git_blob_sha(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "physicalQA": "PASS", "depthVisualQA": "REVIEW_REQUIRED",
            "identityAndContinuityQA": "REVIEW_REQUIRED",
            "remotePublished": False, "accepted": False,
        })
    return {"canonicalInputSHA": sources, "previews": previews,
            "overall": "QA_PENDING",
            "reason": "Physical validation is not proof of scene depth, identity, continuity, or remote publication."}

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", type=Path, required=True)
    ap.add_argument("--candidate-dir", type=Path, required=True)
    ap.add_argument("--suffix", default="depth_corrected_candidate")
    args = ap.parse_args()
    print(json.dumps(examine(list(args.candidate_dir.glob("*.webp")),
                             args.source_dir, args.suffix), indent=2))

if __name__ == "__main__":
    main()
