#!/usr/bin/env python3
"""Actions-free canonical HSK5 preview preparation and optional publication.

From an up-to-date checkout of uysalayhan23/newChinese (main):
    python tools/prepare_hsk5_sc031_sc040.py
    python tools/prepare_hsk5_sc031_sc040.py --publish

Requires Python 3, Pillow and local Git/network access. --publish pushes *only*
the four generated previews and their source-blob provenance manifests.
It never marks visual acceptance complete. Manual image/continuity QA and
scene-bound review receipts are required before --accept can be run.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

from compose_hsk5_sc031_sc040 import (
    TARGET, canonical_scene_issues, git_blob_sha1, load_scene,
    read_json, required_paths, compose,
)
from fetch_hsk5_sc031_sc040 import transfer

ROOT = Path(__file__).resolve().parents[1]
SCENES = (31, 34, 36, 40)
ROLES = ("background", "characterA", "characterB", "foreground")


def run(*args: str, capture: bool = False) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, check=True,
                            capture_output=capture)
    return result.stdout.strip() if capture else ""


def ensure_clean_main() -> None:
    top = Path(run("git", "rev-parse", "--show-toplevel", capture=True)).resolve()
    if top != ROOT.resolve():
        raise RuntimeError("Script is not running in the expected repository checkout")
    branch = run("git", "branch", "--show-current", capture=True)
    if branch != "main":
        raise RuntimeError(f"Expected main, found {branch!r}")
    dirty = run("git", "status", "--porcelain", "--untracked-files=all",
                capture=True)
    if dirty:
        raise RuntimeError(
            "Working tree must be clean to avoid overwriting unrelated changes. "
            "Commit/stash them before rerunning. First changed path: " +
            dirty.splitlines()[0])


def run_offline_tests() -> None:
    for pattern in ("test_fetch_hsk5_sc031_sc040.py",
                    "test_hsk5_sc031_sc040.py"):
        print(f"RUNNING offline regression tests: {pattern}", flush=True)
        run(sys.executable, "-m", "unittest", "discover",
            "-s", "tools/tests", "-p", pattern, "-v")


def audit_preview(scene: int) -> tuple[Path, Path]:
    directory, manifest, _ = load_scene(scene)
    issues = canonical_scene_issues(scene, manifest)
    paths = required_paths(directory, manifest)
    record = manifest.get("previewComposition") or {}
    inputs = record.get("inputBlobs") or {}
    for role in ROLES:
        p = paths[role]
        if not p.is_file():
            issues.append(f"{role} is physically missing")
            continue
        if inputs.get(role) != git_blob_sha1(p):
            issues.append(f"{role} SHA differs from recorded composition provenance")
    preview = paths["preview"]
    if not preview.is_file():
        issues.append("preview is physically missing")
    else:
        with Image.open(preview) as image:
            if image.format != "WEBP" or image.size != TARGET:
                issues.append(f"preview format/dimensions invalid: {image.format} {image.size}")
            image.verify()
        if record.get("previewBlob") != git_blob_sha1(preview):
            issues.append("preview SHA differs from recorded composition provenance")
    if issues:
        raise RuntimeError(f"HSK5_SC{scene:03d} failed physical preview QA: " +
                           "; ".join(issues))
    return preview, directory / "visual_manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true",
                        help="Commit/push four verified generated previews with [skip ci]; acceptance remains pending")
    args = parser.parse_args()
    ensure_clean_main()
    run_offline_tests()
    print("FETCHING or verifying SHA-pinned canonical WebP source layers", flush=True)
    transfer(ROOT, list(SCENES), os.environ.get("GITHUB_TOKEN"))
    changed = []
    for scene in SCENES:
        outcome = compose(scene, replace=False, approvals={})
        print(f"HSK5_SC{scene:03d}: {outcome}", flush=True)
        if not (outcome.startswith("CREATED:") or
                outcome.startswith("SKIPPED:")):
            raise RuntimeError(f"HSK5_SC{scene:03d} could not be composed: {outcome}")
        changed.extend(audit_preview(scene))
    print("Four previews passed physical WebP/dimension/blob checks; "
          "visual identity/continuity approval is STILL PENDING.", flush=True)
    if args.publish:
        run("git", "add", "--", *(str(p.relative_to(ROOT)) for p in changed))
        staged = run("git", "diff", "--cached", "--name-only", capture=True)
        if staged:
            run("git", "commit", "-m",
                "Stage canonical HSK5 SC031/034/036/040 previews for visual QA [skip ci]")
            run("git", "push", "origin", "main")
            print("PUSHED four preview files/manifests; batch and accepted status unchanged.", flush=True)
        else:
            print("NO CHANGES: GitHub already has current preview and provenance.", flush=True)
    else:
        print("PREPARED locally only. Use --publish to push. No acceptance was written.", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.CalledProcessError, OSError, ValueError) as exc:
        print(f"PREPARATION BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)
