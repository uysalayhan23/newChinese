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
MINIMUMS = {"background": (720, 1280), "foreground": (540, 960),
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


def verify_assets(number: int, manifest: dict, approvals: dict) -> list[str]:
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
    return issues


def compose(number: int, *, replace: bool) -> str:
    if number in LIU_MEI_FACE_RIGHT:
        return "BLOCKED: canonical Liu Mei face_right image needs separate approval"
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
        if actor.getextrema()[3][0] == 255:
            return f"BLOCKED: {key} layer is entirely opaque (not a cutout)"
        height = round(TARGET[1] * 0.76)
        width = round(actor.width * height / actor.height)
        actor = actor.resize((width, height), Image.Resampling.LANCZOS)
        x = round(TARGET[0] * x_fraction - width / 2)
        y = TARGET[1] - height
        if x < 0 or x + width > TARGET[0]:
            return f"BLOCKED: {key} exceeds canvas bounds"
        canvas.alpha_composite(actor, (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "WEBP", quality=92, method=6)
    return f"CREATED: {output.relative_to(ROOT)} {TARGET[0]}x{TARGET[1]}"


def accept(approvals: dict) -> list[str]:
    batch = read_json(BATCH)
    queue = read_json(QUEUE)
    notes = []
    all_ok = 0
    for number in SCENES:
        directory, manifest, media = load_scene(number)
        issues = verify_assets(number, manifest, approvals)
        scene_id = f"HSK5_SC{number:03d}"
        if issues:
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
        queue["hsk5Progress"]["sc031_sc040"].get("remaining", {}).pop(f"sc{number:03d}", None)
        notes.append(f"{scene_id}: ACCEPTED")
    for entry in batch["scenes"]:
        status = read_json(scene_dir(int(entry["sceneId"][-3:])) / "media_status.json")
        if status["visual"]["status"] == "complete":
            all_ok += 1
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
    args = parser.parse_args()
    if not args.compose and not args.accept:
        parser.error("Select --compose or --accept")
    if any(scene not in SCENES for scene in args.scenes):
        parser.error("Only HSK5 SC031-SC040 are supported")
    approvals = read_json(args.face_right_approvals) if args.face_right_approvals else {}
    if args.compose:
        for n in args.scenes:
            print(f"HSK5_SC{n:03d}: {compose(n, replace=args.replace)}")
    if args.accept:
        for line in accept(approvals):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
