from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "visual_regeneration_queue.json"


def main() -> int:
    items = []
    for level in range(1, 7):
        level_dir = ROOT / "content" / f"hsk{level}"
        if not level_dir.is_dir():
            continue
        for scene in range(1, 51):
            if level < 5 or (level == 5 and scene <= 5):
                continue
            scene_dir = level_dir / f"sc{scene:03d}"
            manifest_path = scene_dir / "visual_manifest.json"
            if not manifest_path.is_file():
                continue
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for char in manifest.get("characters") or []:
                cid = char.get("characterId")
                if not cid:
                    continue
                short = cid.removeprefix("CHAR_").removesuffix("_001").lower()
                rel = f"assets/hsk{level}_sc{scene:03d}_char_{short}.webp"
                items.append({
                    "sceneId": f"HSK{level}_SC{scene:03d}",
                    "characterId": cid,
                    "outfit": char.get("outfit"),
                    "speechBubbleAnchor": char.get("speechBubbleAnchor"),
                    "target": rel,
                    "status": "regenerate_required",
                    "canonicalRule": "match approved HSK1-HSK5_SC005 identity baseline",
                    "maturityLock": f"HSK{level}",
                })

    out = {
        "policy": "HSK5_SC006 onward character layers require regeneration/re-approval.",
        "items": items,
        "total": len(items),
        "complete": 0,
        "pending": len(items),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Character regeneration queue: {len(items)} pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
