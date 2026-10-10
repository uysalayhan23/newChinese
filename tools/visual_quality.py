from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUALITY_GATE_PATH = ROOT / "content" / "visual_quality_gate.json"

MIN_DIMS = {
    "background": (540, 960),
    "foreground": (540, 960),
    "preview": (720, 1280),
    "character": (500, 750),
}


def webp_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    if chunk == b"VP8X":
        return (
            1 + int.from_bytes(data[24:27], "little"),
            1 + int.from_bytes(data[27:30], "little"),
        )
    if chunk == b"VP8L" and len(data) >= 25:
        b1, b2, b3, b4 = data[21:25]
        return (
            1 + (((b2 & 0x3F) << 8) | b1),
            1 + (((b4 & 0x0F) << 10) | (b3 << 2) | (b2 >> 6)),
        )
    if chunk == b"VP8 ":
        pos = data.find(b"\x9d\x01\x2a", 20)
        if pos >= 0 and pos + 7 <= len(data):
            return (
                struct.unpack_from("<H", data, pos + 3)[0] & 0x3FFF,
                struct.unpack_from("<H", data, pos + 5)[0] & 0x3FFF,
            )
    return None


def asset_role(rel: str) -> str | None:
    name = Path(rel).name.lower()
    if name.endswith("_bg.webp"):
        return "background"
    if name.endswith("_fg.webp"):
        return "foreground"
    if name.endswith("_preview.webp"):
        return "preview"
    if "_char_" in name and name.endswith(".webp"):
        return "character"
    return None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_gate() -> dict:
    if not QUALITY_GATE_PATH.is_file():
        return {}
    return json.loads(QUALITY_GATE_PATH.read_text(encoding="utf-8"))


def identity_blocked(scene_id: str, rel: str, path: Path, gate: dict) -> bool:
    rule = gate.get("identityRegeneration") or {}
    if rule.get("status") != "required" or asset_role(rel) != "character":
        return False
    match = re.fullmatch(r"HSK([1-6])_SC(\d{3})", scene_id)
    if not match:
        return False
    level, scene = map(int, match.groups())
    if not (level > 5 or (level == 5 and scene >= 6)):
        return False
    approved = (rule.get("approvedCharacterSha256") or {}).get(scene_id) or []
    return sha256(path) not in approved


def visual_quality_blocks(scene_id: str, scene_dir: Path, required: list[str]) -> list[dict]:
    gate = load_gate()
    blocks: list[dict] = []
    existing = {rel: scene_dir / rel for rel in required if (scene_dir / rel).is_file()}

    for rel, path in existing.items():
        role = asset_role(rel)
        if not role:
            continue
        dims = webp_dimensions(path)
        if dims is None:
            blocks.append({"asset": rel, "reason": "invalid_or_unreadable_webp"})
            continue
        min_w, min_h = MIN_DIMS[role]
        if dims[0] < min_w or dims[1] < min_h:
            blocks.append({
                "asset": rel,
                "reason": "below_minimum_resolution",
                "actual": [dims[0], dims[1]],
                "minimum": [min_w, min_h],
            })
        if identity_blocked(scene_id, rel, path, gate):
            blocks.append({
                "asset": rel,
                "reason": "identity_regeneration_required_after_HSK5_SC005",
            })

    bg_rel = next((r for r in existing if asset_role(r) == "background"), None)
    preview_rel = next((r for r in existing if asset_role(r) == "preview"), None)
    if bg_rel and preview_rel and existing[bg_rel].read_bytes() == existing[preview_rel].read_bytes():
        blocks.append({"asset": preview_rel, "reason": "preview_is_byte_identical_to_background"})

    for item in (gate.get("manualBlocks") or {}).get(scene_id) or []:
        if item not in blocks:
            blocks.append(item)
    return blocks
