"""Fetch pinned GitHub canonical WebPs directly within the Pillow Python runtime.

Requires that this Python runtime itself have GitHub network access.
Never starts GitHub Actions, accepts candidates, or modifies the remote repo.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image


def decode_verified_webp(payload: str, expected_sha: str) -> bytes:
    raw = base64.b64decode(payload, validate=True)
    calculated = hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()
    if calculated != expected_sha:
        raise ValueError(f"Canonical blob SHA mismatch: {calculated} != {expected_sha}")
    with Image.open(BytesIO(raw)) as im:
        if im.format != "WEBP":
            raise ValueError("Canonical blob is not WebP")
        im.load()
    return raw


def fetch_verified_webp(repo: str, ref: str, path: str, expected_sha: str, token: str = "") -> bytes:
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "newchinese-canonical-webp-importer"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        obj = json.load(response)
    if obj.get("sha") != expected_sha or obj.get("encoding") != "base64":
        raise ValueError(f"GitHub content metadata mismatch: {path}")
    return decode_verified_webp("".join(obj["content"].split()), expected_sha)


def import_pinned_sources(pin_file: Path, root: Path, repo: str, ref: str = "main", token: str = "") -> dict:
    pins = json.loads(pin_file.read_text(encoding="utf-8"))["scenes"]
    cache = {}
    written = []
    for scene, layers in sorted(pins.items()):
        for name, expected_sha in layers.items():
            path = f"content/hsk6/sc{scene}/assets/{name}"
            if expected_sha not in cache:
                cache[expected_sha] = fetch_verified_webp(repo, ref, path, expected_sha, token)
            destination = root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(cache[expected_sha])
            written.append(path)
    return {"unique_blobs": len(cache), "materialized": len(written)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pins", type=Path, default=Path("tools/hsk6_ready_preview_blobs.json"))
    parser.add_argument("--output-root", type=Path, default=Path("."))
    parser.add_argument("--repo", default="uysalayhan23/newChinese")
    parser.add_argument("--ref", default="main")
    args = parser.parse_args()
    result = import_pinned_sources(args.pins, args.output_root, args.repo, args.ref, os.environ.get("GITHUB_TOKEN", ""))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
