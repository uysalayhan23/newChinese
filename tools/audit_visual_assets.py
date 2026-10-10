from __future__ import annotations

import json
from pathlib import Path

from visual_quality import asset_role, sha256, visual_quality_blocks, webp_dimensions

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    findings = []
    for level in range(1, 7):
        level_dir = ROOT / "content" / f"hsk{level}"
        if not level_dir.is_dir():
            continue
        for scene_dir in sorted(level_dir.glob("sc[0-9][0-9][0-9]")):
            media_path = scene_dir / "media_status.json"
            if not media_path.is_file():
                continue
            media = json.loads(media_path.read_text(encoding="utf-8"))
            scene_id = media.get("sceneId") or f"HSK{level}_{scene_dir.name.upper()}"
            required = (media.get("visual") or {}).get("required") or []
            blocks = visual_quality_blocks(scene_id, scene_dir, required)
            assets = []
            for rel in required:
                path = scene_dir / rel
                dims = webp_dimensions(path) if path.is_file() else None
                assets.append({
                    "asset": rel,
                    "exists": path.is_file(),
                    "role": asset_role(rel),
                    "dimensions": list(dims) if dims else None,
                    "sha256": sha256(path) if path.is_file() else None,
                })
            findings.append({
                "sceneId": scene_id,
                "status": "BLOCKED" if blocks else "PASS",
                "blocks": blocks,
                "assets": assets,
            })

    output = {
        "scenesAudited": len(findings),
        "blockedScenes": sum(item["status"] == "BLOCKED" for item in findings),
        "passedScenes": sum(item["status"] == "PASS" for item in findings),
        "findings": findings,
    }
    path = ROOT / "visual_quality_audit.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Visual QA: {output['passedScenes']} pass / "
        f"{output['blockedScenes']} blocked / {output['scenesAudited']} total"
    )
    return 1 if output["blockedScenes"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
