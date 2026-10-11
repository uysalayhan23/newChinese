#!/usr/bin/env python3
"""One-pass, Actions-free HSK6 physical WebP staging (never auto-accepts).

Local checkout of uysalayhan23/newChinese at main, with Git and Pillow:
    python tools/run_hsk6_visual_staging.py
    python tools/run_hsk6_visual_staging.py --publish

Runs both repository HSK6 unittest suites BEFORE any image writes. Verifies
all SHA-pinned inputs and identity/outfit/orientation manifests. Produces
20 mirrored face-right candidates, then 16 exact 720x1280 four-layer previews.
--publish commits only these QA-pending outputs + provenance manifests and
pushes main with [skip ci]. No GitHub Actions. No accepted-status changes.

The runner needs a local checkout with real binary WebPs. It cannot fix a
missing checkout, network restrictions, or supply missing human visual QA.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image

from compose_hsk6_ready_previews import (
    READY, TARGET, compose, preflight as preview_preflight, checked_git,
    git_blob_sha1, read_manifest,
)
from prepare_hsk6_face_right_candidates import (
    SCENE_ACTORS, SOURCES, prepare, preflight as actor_preflight,
    target_path,
)

ROOT = Path(__file__).resolve().parents[1]


def run_tests(root: Path) -> None:
    for pattern in (
        "test_prepare_hsk6_face_right_candidates.py",
        "test_compose_hsk6_ready_previews.py",
    ):
        print(f"RUNNING {pattern}", flush=True)
        subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s",
             "tools/tests", "-p", pattern, "-v"],
            cwd=root, check=True,
        )


def check_checkout(root: Path) -> None:
    top = Path(checked_git(root, "rev-parse", "--show-toplevel",
                           capture=True)).resolve()
    if top != root.resolve():
        raise ValueError("runner must execute inside its exact Git checkout")
    if checked_git(root, "branch", "--show-current", capture=True) != "main":
        raise ValueError("only main branch may be published")
    remote = checked_git(root, "remote", "get-url", "origin", capture=True)
    if not remote.rstrip("/").removesuffix(".git").endswith(
            "uysalayhan23/newChinese"):
        raise ValueError("origin must point to uysalayhan23/newChinese")
    if checked_git(root, "status", "--porcelain", "--untracked-files=all",
                   capture=True):
        raise ValueError("working tree must be clean before staging")


def audit_preview(scene: int, root: Path, file: Path) -> None:
    directory, manifest = read_manifest(scene, root)
    expected = {
        role: git_blob_sha1(directory / manifest["assets"][role])
        for role in ("background", "characterA", "characterB", "foreground")
    }
    if (manifest.get("previewComposition") or {}).get("inputBlobs") != expected:
        raise ValueError(f"SC{scene:03d}: preview source SHA provenance drift")
    if (manifest.get("previewComposition") or {}).get("previewBlob") != git_blob_sha1(file):
        raise ValueError(f"SC{scene:03d}: preview output SHA provenance drift")
    with Image.open(file) as image:
        if image.format != "WEBP" or image.size != TARGET:
            raise ValueError(f"SC{scene:03d}: expected exact 720x1280 WebP")
        image.verify()


def stage(root: Path) -> list[Path]:
    # Fail-closed full-source preflight before any new files are written.
    actor_preflight(root, overwrite=False)
    for scene in READY:
        preview_preflight(scene, root)

    outputs: list[Path] = []
    actor_results = prepare(root, overwrite=False)
    if len(actor_results) != 20:
        raise ValueError("20 mirrored canonical candidate outputs are required")
    for scene, identity in SCENE_ACTORS.items():
        actor = target_path(scene, identity, root)
        if not actor.is_file():
            raise ValueError(f"SC{scene:03d}: face-right candidate missing")
        outputs.append(actor)

    for scene in READY:
        preview, manifest_path = compose(scene, root)
        audit_preview(scene, root, preview)
        outputs.extend((preview, manifest_path))
        print(f"HSK6_SC{scene:03d}: physical QA-pending 720x1280 preview",
              flush=True)
    print("20 actor candidates + 16 previews created; visual identity and "
          "continuity QA still pending (zero accepted automatically).", flush=True)
    return outputs


def publish(root: Path, outputs: list[Path]) -> None:
    paths = sorted({str(p.relative_to(root)) for p in outputs})
    checked_git(root, "add", "--", *paths)
    staged = checked_git(root, "diff", "--cached", "--name-only", capture=True)
    unexpected = set(staged.splitlines()) - set(paths)
    if unexpected:
        raise ValueError(f"unexpected staged files: {sorted(unexpected)}")
    if not staged:
        print("NO CHANGES: binary outputs already at current main HEAD")
        return
    checked_git(root, "commit", "-m",
                "Stage 20 HSK6 canonical actor and 16 preview QA candidates [skip ci]")
    checked_git(root, "push", "origin", "main")
    print("PUSHED QA-pending WebP candidates; no scene accepted.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true",
                        help="Commit and push QA-pending images; no acceptance")
    args = parser.parse_args()
    check_checkout(ROOT)
    run_tests(ROOT)
    outputs = stage(ROOT)
    if args.publish:
        publish(ROOT, outputs)
    else:
        print("PREPARED LOCALLY. Use --publish from a clean checkout to push.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        sys.exit(1)
