"""Offline synthetic regression checks for HSK5 SC031-SC040 compositor.

Run explicitly on a local checkout:
    python -m unittest discover -s tools/tests -p 'test_hsk5_sc031_sc040.py'

No GitHub Actions, network, canonical files, or real acceptance are involved.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

TOOLS = Path(__file__).resolve().parents[1]
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import compose_hsk5_sc031_sc040 as module  # noqa: E402


class SyntheticCompositorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / "content/hsk5/sc034"
        self.assets = self.directory / "assets"
        self.assets.mkdir(parents=True)
        self.old_root = module.ROOT
        module.ROOT = self.root
        self.addCleanup(setattr, module, "ROOT", self.old_root)
        self.files = {
            "background": "assets/hsk5_sc034_bg.webp",
            "characterA": "assets/hsk5_sc034_char_zhang_wei.webp",
            "characterB": "assets/hsk5_sc034_char_chen_yu.webp",
            "foreground": "assets/hsk5_sc034_fg.webp",
            "preview": "assets/hsk5_sc034_preview.webp",
        }
        self.manifest = {
            "sceneId": "HSK5_SC034",
            "locationId": "LOC_COMMUNITY_CENTER_001",
            "assets": self.files,
            "characters": [
                {"characterId": "CHAR_ZHANG_WEI_001",
                 "speechBubbleAnchor": "face_right"},
                {"characterId": "CHAR_CHEN_YU_001",
                 "speechBubbleAnchor": "face_left"},
            ],
        }
        (self.directory / "visual_manifest.json").write_text(
            json.dumps(self.manifest), encoding="utf-8")
        (self.directory / "media_status.json").write_text(
            json.dumps({"sceneId": "HSK5_SC034", "visual": {"status": "pending"}}),
            encoding="utf-8")
        self.bg_file = self.directory / self.files["background"]
        Image.new("RGB", (941, 1672), (190, 207, 208)).save(
            self.bg_file, "WEBP", quality=95)
        fg = Image.new("RGBA", (941, 1672), (0, 0, 0, 0))
        ImageDraw.Draw(fg).rectangle((0, 1600, 941, 1672),
                                      fill=(70, 60, 35, 160))
        fg.save(self.directory / self.files["foreground"], "WEBP")
        for name, shape, color in [
            ("characterA", (600, 900), (130, 65, 80, 255)),
            ("characterB", (600, 1066), (60, 95, 120, 255)),
        ]:
            actor = Image.new("RGBA", shape, (0, 0, 0, 0))
            ImageDraw.Draw(actor).ellipse((80, 30, shape[0] - 80, shape[1] - 30),
                                          fill=color)
            actor.save(self.directory / self.files[name], "WEBP")

    def test_produces_real_720_by_1280_webp_with_matching_provenance(self):
        result = module.compose(34, replace=False, approvals={})
        self.assertTrue(result.startswith("CREATED:"), result)
        preview = self.directory / self.files["preview"]
        self.assertTrue(preview.is_file())
        with Image.open(preview) as img:
            self.assertEqual(img.size, (720, 1280))
            self.assertEqual(img.format, "WEBP")
        manifest = json.loads(
            (self.directory / "visual_manifest.json").read_text(encoding="utf-8"))
        record = manifest["previewComposition"]
        self.assertEqual(record["previewBlob"], module.git_blob_sha1(preview))
        self.assertEqual(set(record["inputBlobs"]), {
            "background", "characterA", "characterB", "foreground"})
        self.assertEqual(
            record["inputBlobs"]["background"], module.git_blob_sha1(self.bg_file))

    def test_no_background_upscaling_is_permitted(self):
        Image.new("RGB", (540, 960), (200, 200, 200)).save(
            self.bg_file, "WEBP")
        result = module.compose(34, replace=False, approvals={})
        self.assertIn("genuine HD", result)
        self.assertFalse((self.directory / self.files["preview"]).exists())

    def test_transparent_empty_character_is_rejected(self):
        actor = self.directory / self.files["characterA"]
        Image.new("RGBA", (600, 900), (0, 0, 0, 0)).save(actor, "WEBP")
        result = module.compose(34, replace=False, approvals={})
        self.assertIn("not a usable transparent cutout", result)
        self.assertFalse((self.directory / self.files["preview"]).exists())

    def test_missing_visual_review_never_passes_acceptance(self):
        self.assertTrue(module.compose(34, replace=False, approvals={}).startswith(
            "CREATED:"))
        # Synthetic characters must never be mistaken for real canonical blobs.
        issues = module.verify_assets(34, module.read_json(
            self.directory / "visual_manifest.json"), {}, {})
        self.assertTrue(any("character identity/orientation" in s for s in issues))
        self.assertTrue(any("visual review" in s for s in issues))

    def test_modified_source_invalidates_preview_provenance(self):
        self.assertTrue(module.compose(34, replace=False, approvals={}).startswith(
            "CREATED:"))
        Image.new("RGB", (941, 1672), (31, 60, 100)).save(
            self.bg_file, "WEBP")
        issues = module.verify_assets(34, module.read_json(
            self.directory / "visual_manifest.json"), {}, {})
        self.assertTrue(any("provenance missing or stale" in s for s in issues))


if __name__ == "__main__":
    unittest.main()
