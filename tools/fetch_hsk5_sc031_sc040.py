#!/usr/bin/env python3
"""Fetch SHA-pinned canonical WebPs to a checkout; never start GitHub Actions.

    python tools/fetch_hsk5_sc031_sc040.py
    python tools/compose_hsk5_sc031_sc040.py --compose --scenes 31 34 36 40

Requires network access from the host running this script, not GitHub Actions.
Does not touch accepted previews or Git metadata; does not commit/push.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "uysalayhan23/newChinese"
SOURCE_REF = "main"
CANONICAL = {
    "community_bg": "6ba20dfb8423743e855c90dcd4212a17a866e9b7",
    "city_park_bg": "d6dc8b286b482c84716db61f550b2aafa08aec5c",
    "zhang_wei": "44a7a521b7fa64466111c30f6830904081c3767d",
    "liu_mei_face_left": "eea4742918bf5b78f222b54631de8f71a4c824a7",
    "chen_yu_face_left": "ee14b09ae3c8cc4f5e539a54884798900f2ad85b",
    "community_fg": "6b1f41e98c50cd53e5bd32b5e14c0976c5de32ed",
    "city_park_fg": "7fd1642711f0b3e70da53902f0a7fd4949f0f4b8",
}
SCENE_LAYERS = {
    31: ("community_bg", "zhang_wei", "liu_mei_face_left", "community_fg"),
    34: ("community_bg", "zhang_wei", "chen_yu_face_left", "community_fg"),
    36: ("city_park_bg", "zhang_wei", "chen_yu_face_left", "city_park_fg"),
    40: ("community_bg", "zhang_wei", "chen_yu_face_left", "community_fg"),
}
ASSET_NAMES = {
    "community_bg": "bg", "city_park_bg": "bg",
    "zhang_wei": "char_zhang_wei", "liu_mei_face_left": "char_liu_mei",
    "chen_yu_face_left": "char_chen_yu",
    "community_fg": "fg", "city_park_fg": "fg",
}


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def validate_webp(data: bytes) -> None:
    if not (len(data) > 30 and data[:4] == b"RIFF"
            and data[8:12] == b"WEBP"
            and int.from_bytes(data[4:8], "little") + 8 <= len(data)):
        raise ValueError("Invalid or truncated RIFF/WebP")


def fetch(path: str, token: str | None) -> bytes:
    if token:
        url = (f"https://api.github.com/repos/{REPOSITORY}/contents/"
               f"{quote(path)}?ref={SOURCE_REF}")
        req = Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.raw+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "newChinese-canonical-asset-fetcher",
        })
    else:
        url = f"https://raw.githubusercontent.com/{REPOSITORY}/{SOURCE_REF}/{quote(path)}"
        req = Request(url, headers={"User-Agent": "newChinese-canonical-asset-fetcher"})
    with urlopen(req, timeout=30) as response:
        return response.read()


def transfer(root: Path, scenes: list[int], token: str | None) -> int:
    downloaded = skipped = 0
    for scene in scenes:
        for layer in SCENE_LAYERS[scene]:
            filename = f"hsk5_sc{scene:03d}_{ASSET_NAMES[layer]}.webp"
            path = Path(f"content/hsk5/sc{scene:03d}/assets") / filename
            target = root / path
            expected = CANONICAL[layer]
            if target.exists():
                existing = target.read_bytes()
                if blob_sha(existing) != expected:
                    raise ValueError(f"STOP: refusing to replace non-canonical asset: {path}")
                validate_webp(existing)
                skipped += 1
                print(f"VERIFIED {path}")
                continue
            data = fetch(path.as_posix(), token)
            validate_webp(data)
            actual = blob_sha(data)
            if actual != expected:
                raise ValueError(f"STOP: Git blob SHA mismatch for {path}: {actual} != {expected}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temp:
                temp.write(data)
                name = temp.name
            os.replace(name, target)
            downloaded += 1
            print(f"DOWNLOADED {path} ({len(data)} bytes, {actual})")
    print(f"Canonical assets: {downloaded} transferred; {skipped} already verified")
    return downloaded


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--scenes", type=int, nargs="+", default=[31, 34, 36, 40],
                        choices=sorted(SCENE_LAYERS))
    args = parser.parse_args()
    try:
        transfer(args.root.resolve(), args.scenes, os.environ.get("GITHUB_TOKEN"))
    except (HTTPError, URLError, OSError, ValueError) as exc:
        parser.exit(1, f"TRANSFER FAILED (no files counted as accepted): {exc}\n")


if __name__ == "__main__":
    main()
