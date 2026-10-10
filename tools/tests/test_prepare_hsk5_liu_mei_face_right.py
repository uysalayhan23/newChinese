"""Isolated non-Actions QA tests for Liu Mei canonical mirror candidates."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import prepare_hsk5_liu_mei_face_right as module


class LiuMeiCandidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.webp"
        rgba = Image.new("RGBA", (800, 1320), (0, 0, 0, 0))
        ImageDraw.Draw(rgba).rectangle((60, 300, 260, 1100),
                                       fill=(160, 90, 100, 255))
        rgba.save(self.source, "WEBP", lossless=True)
        self.addCleanup(patch.stopall)
        patch.object(module, "ROOT", self.root).start()
        patch.object(module, "SOURCE", self.source).start()
        patch.object(module, "EXPECTED_SOURCE",
                     module.git_blob_sha1(self.source)).start()
        for scene in module.SCENES:
            target, manifest = module.candidate_paths(scene)
            target.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({"sceneId": f"HSK5_SC{scene:03d}",
                                             "characters": [
                {"characterId": "CHAR_LIU_MEI_001",
                 "speechBubbleAnchor": "face_right"},
                {"characterId": "CHAR_ZHANG_WEI_001",
                 "speechBubbleAnchor": "face_left"},
            ]}), encoding="utf-8")

    def test_mirrors_canonical_pixels_and_preserves_alpha(self):
        lines = module.prepare()
        self.assertEqual(len(lines), 4)
        for scene in module.SCENES:
            target, _ = module.candidate_paths(scene)
            self.assertTrue(target.exists())
            with Image.open(target) as img:
                self.assertEqual(img.size, (800, 1320))
                rgba = img.convert("RGBA")
                self.assertEqual(rgba.getpixel((700, 600))[3], 255)
                self.assertEqual(rgba.getpixel((120, 600))[3], 0)

    def test_does_not_overwrite_unapproved_existing_layer(self):
        target, _ = module.candidate_paths(33)
        target.write_bytes(b"never replace an existing character layer")
        lines = module.prepare()
        self.assertIn("SKIPPED", lines[0])
        self.assertEqual(target.read_bytes(),
                         b"never replace an existing character layer")

    def test_wrong_canonical_source_sha_blocks_all_outputs(self):
        module.EXPECTED_SOURCE = "0" * 40
        with self.assertRaisesRegex(ValueError, "source identity mismatch"):
            module.prepare()
        self.assertFalse(module.candidate_paths(33)[0].exists())

    def test_wrong_manifest_orientation_fails_closed(self):
        target, manifest = module.candidate_paths(35)
        body = json.loads(manifest.read_text(encoding="utf-8"))
        body["characters"][0]["speechBubbleAnchor"] = "face_left"
        manifest.write_text(json.dumps(body), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "does not require"):
            module.prepare()
        self.assertFalse(target.exists())
        # Atomic preflight: SC033 must not have been written either.
        self.assertFalse(module.candidate_paths(33)[0].exists())


if __name__ == "__main__":
    unittest.main()
