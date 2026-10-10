#!/usr/bin/env python3
"""Deterministic, fail-closed HSK5 SC031-SC040 visual repair (no GitHub Actions).

From a checked-out repository:
    python tools/compose_hsk5_sc031_sc040.py --compose
    python tools/compose_hsk5_sc031_sc040.py --accept

--compose writes only scene-specific preview WebP files. --accept updates status
metadata only after five physical assets and canonical identity rules pass.
Face-right Liu Mei scenes require separately verified per-scene SHA-1 approval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from visual_quality import git_blob_sha1, visual_quality_blocks, webp_dimensions

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "production_batches/HSK5_SC031_SC040.json"
QUEUE = ROOT / "content/visual_regeneration_queue.json"
MASTER = ROOT / "MASTER_EXECUTION_STEPS.md"
SCENES = tuple(range(31, 41))
PREVIEW_ONLY = (31, 32, 34, 36, 38, 40)
LIU_MEI_FACE_RIGHT = (33, 35, 37, 39)
TARGET = (720, 1280)
MINIMUMS = {"background": (720, 1280), "foreground": (720, 1280),
            "characterA": (500, 750), "characterB": (500, 750),
            "preview": TARGET}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def scene_dir(number: int) -> Path:
    return ROOT / "content/hsk5" / f"sc{number:03d}"


def load_scene(number: int) -> tuple[Path, dict, dict]:
    directory = scene_dir(number)
    return directory, read_json(directory / "visual_manifest.json"), read_json(directory / "media_status.json")


def required_paths(directory: Path, manifest: dict) -> dict[str, Path]:
    return {role: directory / relative for role, relative in manifest["assets"].items()}


def verify_assets(number: int, manifest: dict, approvals: dict, reviews: dict) -> list[str]:
    directory = scene_dir(number)
    paths = required_paths(directory, manifest)
    issues = []
    for role, path in paths.items():
        if not path.is_file():
            issues.append(f"{role}: missing {path.name}")
            continue
        size = webp_dimensions(path)
        if size is None:
            issues.append(f"{role}: invalid WebP")
            continue
        minimum = MINIMUMS[role]
        if size[0] < minimum[0] or size[1] < minimum[1]:
            issues.append(f"{role}: {size} below {minimum}")
    record = manifest.get("previewComposition") or {}
    inputs = record.get("inputBlobs") or {}
    for role in ("background", "characterA", "characterB", "foreground"):
        path = paths[role]
        if path.is_file() and inputs.get(role) != git_blob_sha1(path):
            issues.append(f"{role}: preview composition provenance missing or stale")
    preview = paths["preview"]
    if preview.is_file() and record.get("previewBlob") != git_blob_sha1(preview):
        issues.append("preview: compositor output does not match recorded blob")
    required = list(manifest["assets"].values())
    for block in visual_quality_blocks(f"HSK5_SC{number:03d}", directory, required):
        issues.append(f"{block['asset']}: {block['reason']}")
    if number in LIU_MEI_FACE_RIGHT:
        char_spec = next((s for s in manifest["characters"]
                          if s["characterId"] == "CHAR_LIU_MEI_001"), None)
        if not char_spec or char_spec.get("speechBubbleAnchor") != "face_right":
            issues.append("Liu Mei face_right orientation manifest mismatch")
        layer = paths.get("characterA")
        actual = git_blob_sha1(layer) if layer and layer.is_file() else None
        approved = approvals.get(f"HSK5_SC{number:03d}")
        if not approved or actual != approved:
            issues.append("Liu Mei face_right: explicit approved per-scene blob SHA required")
    # Technical checks cannot judge identity, readability, occlusion or story.
    # Bind visual approval to the actual preview bytes, preventing stale review reuse.
    review = reviews.get(f"HSK5_SC{number:03d}") or {}
    preview_path = paths["preview"]
    if not preview_path.is_file() or review.get("previewBlob") != git_blob_sha1(preview_path):
        issues.append("preview: exact-blob visual review approval required")
    for field in ("identity", "foregroundOrdering", "continuity", "textless", "sharpness"):
        if review.get(field) is not True:
            issues.append(f"preview: visual review {field} not approved")
    return issues


def compose(number: int, *, replace: bool, approvals: dict) -> str:
    if number in LIU_MEI_FACE_RIGHT:
        approved = approvals.get(f"HSK5_SC{number:03d}")
        layer = scene_dir(number) / f"assets/hsk5_sc{number:03d}_char_liu_mei.webp"
        if not approved or not layer.is_file() or git_blob_sha1(layer) != approved:
            return "BLOCKED: canonical Liu Mei face_right image needs explicit blob approval"
    directory, manifest, _ = load_scene(number)
    paths = required_paths(directory, manifest)
    output = paths["preview"]
    if output.exists() and not replace:
        existing_size = webp_dimensions(output)
        if existing_size and existing_size[0] >= TARGET[0] and existing_size[1] >= TARGET[1]:
            return "SKIPPED: existing preview meets minimum dimensions; use --replace to recompose"
        # Low-resolution previews must be replaced automatically after successful composition.
    for key in ("background", "characterA", "characterB", "foreground"):
        if not paths[key].is_file():
            return f"BLOCKED: missing {key}"
    bg_size = webp_dimensions(paths["background"])
    if not bg_size or min(bg_size[0] / TARGET[0], bg_size[1] / TARGET[1]) < 1:
        return f"BLOCKED: BG {bg_size} requires genuine HD source (no upscaling)"
    with Image.open(paths["background"]) as bg:
        canvas = bg.convert("RGBA").resize(TARGET, Image.Resampling.LANCZOS)
    with Image.open(paths["foreground"]) as fg:
        overlay = fg.convert("RGBA").resize(TARGET, Image.Resampling.LANCZOS)
        canvas.alpha_composite(overlay)
    for key, x_fraction in (("characterA", 0.34), ("characterB", 0.67)):
        with Image.open(paths[key]) as image:
            actor = image.convert("RGBA")
        alpha_min, alpha_max = actor.getextrema()[3]
        if alpha_min == 255 or alpha_max == 0:
            return f"BLOCKED: {key} layer is not a usable transparent cutout"
        # Keep source aspect ratio and keep the full canonical silhouette on-canvas.
        # The legacy 76%-height rule clipped the 600x900 left actor at x=0.34.
        target_height = round(TARGET[1] * 0.70)
        width_limit = round(TARGET[0] * 0.75)
        scale = min(target_height / actor.height, width_limit / actor.width)
        height = max(1, round(actor.height * scale))
        width = max(1, round(actor.width * scale))
        actor = actor.resize((width, height), Image.Resampling.LANCZOS)
        x = max(0, min(TARGET[0] - width,
                       round(TARGET[0] * x_fraction - width / 2)))
        y = TARGET[1] - height
        if width > TARGET[0] or height > TARGET[1]:
            return f"BLOCKED: {key} exceeds canvas bounds"
        canvas.alpha_composite(actor, (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "WEBP", quality=92, method=6)
    manifest["previewComposition"] = {
        "method": "deterministic_alpha_composite_v1",
        "inputBlobs": {key: git_blob_sha1(paths[key])
                       for key in ("background", "characterA", "characterB", "foreground")},
        "previewBlob": git_blob_sha1(output),
    }
    write_json(directory / "visual_manifest.json", manifest)
    return f"CREATED: {output.relative_to(ROOT)} {TARGET[0]}x{TARGET[1]}"


def accept(approvals: dict, reviews: dict) -> list[str]:
    batch = read_json(BATCH)
    queue = read_json(QUEUE)
    notes = []
    verified_scenes = set()
    for number in SCENES:
        directory, manifest, media = load_scene(number)
        issues = verify_assets(number, manifest, approvals, reviews)
        scene_id = f"HSK5_SC{number:03d}"
        if issues:
            # A stale complete label must not survive a failed re-audit.
            entry = next(s for s in batch["scenes"] if s["sceneId"] == scene_id)
            entry["status"] = "audio_complete_visual_pending"
            notes.append(f"{scene_id}: PENDING ({'; '.join(issues)})")
            continue
        media["visual"]["status"] = "complete"
        for field in ("missing", "qualityBlocked", "remainingAudit", "regenerationRequired"):
            if field in media["visual"]:
                media["visual"][field] = []
        manifest["status"] = "visual-assets-complete"
        manifest["qualityBlocked"] = []
        if "regeneration" in manifest:
            manifest["regeneration"]["required"] = []
        manifest["validation"] = {"status": "passed", "method": "physical-five-webp-plus-identity-audit"}
        media["visual"]["validation"] = manifest["validation"]
        write_json(directory / "media_status.json", media)
        write_json(directory / "visual_manifest.json", manifest)
        entry = next(s for s in batch["scenes"] if s["sceneId"] == scene_id)
        entry["status"] = "complete"
        verified_scenes.add(number)
        queue["hsk5Progress"]["sc031_sc040"].get("remaining", {}).pop(f"sc{number:03d}", None)
        notes.append(f"{scene_id}: ACCEPTED")
    # Never count stale metadata as accepted; only scenes verified in this run.
    all_ok = len(verified_scenes)
    batch["progress"]["visualComplete"] = all_ok
    batch["progress"]["acceptedScenes"] = all_ok
    batch["status"] = "complete" if all_ok == 10 else "in_progress"
    progress = queue["hsk5Progress"]["sc031_sc040"]
    progress["visualComplete"] = all_ok
    progress["accepted"] = all_ok
    if all_ok == 10:
        progress["status"] = "complete"
    batch.setdefault("notes", []).append(
        f"Physical visual rebaseline audit: {all_ok}/10, remaining scenes not marked complete."
    )
    write_json(BATCH, batch)
    write_json(QUEUE, queue)
    summary = f"- HSK5_SC031–SC040 visual rebaseline: {all_ok}/10 passed physical WebP and identity QA."
    master = MASTER.read_text(encoding="utf-8")
    if summary not in master:
        MASTER.write_text(master.rstrip() + "\n" + summary + "\n", encoding="utf-8")
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compose", action="store_true")
    parser.add_argument("--accept", action="store_true")
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--scenes", nargs="*", type=int, default=list(PREVIEW_ONLY))
    parser.add_argument("--face-right-approvals", type=Path,
                        help="JSON mapping HSK5_SC033/035/037/039 to visually approved SHA-1 blobs")
    parser.add_argument("--visual-review", type=Path,
                        help="JSON mapping scene ID to exact preview blob and identity/ordering/continuity/textless/sharpness approvals")
    args = parser.parse_args()
    if not args.compose and not args.accept:
        parser.error("Select --compose or --accept")
    if any(scene not in SCENES for scene in args.scenes):
        parser.error("Only HSK5 SC031-SC040 are supported")
    approvals = read_json(args.face_right_approvals) if args.face_right_approvals else {}
    reviews = read_json(args.visual_review) if args.visual_review else {}
    if args.compose:
        for n in args.scenes:
            print(f"HSK5_SC{n:03d}: {compose(n, replace=args.replace, approvals=approvals)}")
    if args.accept:
        for line in accept(approvals, reviews):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
