"""Offline tests for four-layer HSK6 720x1280 preview QA staging."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compose_hsk6_ready_previews as p


class HSK6PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.scene = 2
        self.base = self.root / "content/hsk6/sc002"
        self.assets = self.base / "assets"
        self.assets.mkdir(parents=True)
        self.files = {
            "background": "assets/hsk6_sc002_bg.webp",
            "characterA": "assets/hsk6_sc002_char_zhang_wei.webp",
            "characterB": "assets/hsk6_sc002_char_wang_ming.webp",
            "foreground": "assets/hsk6_sc002_fg.webp",
            "preview": "assets/hsk6_sc002_preview.webp",
        }
        self.manifest = {
            "sceneId": "HSK6_SC002",
            "locationId": "LOC_WEST_LAKE_001",
            "assets": self.files,
            "characters": [
                {"characterId": "CHAR_ZHANG_WEI_001", "speechBubbleAnchor": "face_right"},
                {"characterId": "CHAR_WANG_MING_001", "speechBubbleAnchor": "face_left"},
            ],
            "status": "visual-assets-pending",
        }
        pth = self.base / "visual_manifest.json"
        pth.write_text(json.dumps(self.manifest), encoding="utf-8")
        Image.new("RGB", (941, 1672), (180, 200, 150)).save(
            self.base / self.files["background"], "WEBP")
        fg = Image.new("RGBA", (941, 1672), (0, 0, 0, 0))
        ImageDraw.Draw(fg).rectangle((0, 1450, 941, 1671),
                                      fill=(75, 65, 45, 120))
        fg.save(self.base / self.files["foreground"], "WEBP")
        for role, color in [("characterA", (200, 80, 100, 255)),
                            ("characterB", (60, 100, 180, 255))]:
            actor = Image.new("RGBA", (600, 900), (0, 0, 0, 0))
            ImageDraw.Draw(actor).ellipse((85, 25, 510, 880), fill=color)
            actor.save(self.base / self.files[role], "WEBP")
        pins = {Path(filename).name: p.git_blob_sha1(self.base / filename)
                for role, filename in self.files.items() if role != "preview"}
        tools_dir = self.root / "tools"
        tools_dir.mkdir()
        (tools_dir / "hsk6_ready_preview_blobs.json").write_text(
            json.dumps({"scenes": {"002": pins}}), encoding="utf-8")
        (tools_dir / "hsk6_ready_preview_identity_pins.json").write_text(
            json.dumps({"scenes": {"002": {
                "sceneId": "HSK6_SC002",
                "locationId": self.manifest["locationId"],
                "characters": [
                    {key: actor.get(key) for key in
                     ("characterId", "outfit", "speechBubbleAnchor")}
                    for actor in self.manifest["characters"]
                ],
            }}}), encoding="utf-8")

    def test_generates_physical_720x1280_webp_but_not_acceptance(self):
        preview, manifest = p.compose(2, self.root)
        self.assertTrue(preview.is_file())
        with Image.open(preview) as img:
            self.assertEqual(img.size, p.TARGET)
            self.assertEqual(img.format, "WEBP")
        recorded = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(recorded["status"], "visual-assets-pending")
        self.assertEqual(recorded["previewComposition"]["previewBlob"],
                         p.git_blob_sha1(preview))
        self.assertEqual(len(recorded["previewComposition"]["inputBlobs"]), 4)

    def test_refuses_unpinned_face_direction_change(self):
        changed = json.loads((self.base / "visual_manifest.json").read_text())
        changed["characters"][0]["speechBubbleAnchor"] = "face_left"
        (self.base / "visual_manifest.json").write_text(json.dumps(changed))
        with self.assertRaisesRegex(ValueError, "facing drift"):
            p.compose(2, self.root)
        self.assertFalse((self.base / self.files["preview"]).exists())

    def test_refuses_unpinned_outfit_change(self):
        changed = json.loads((self.base / "visual_manifest.json").read_text())
        changed["characters"][0]["outfit"] = "OUTFIT_UNAPPROVED"
        (self.base / "visual_manifest.json").write_text(json.dumps(changed))
        with self.assertRaisesRegex(ValueError, "outfit/facing drift"):
            p.compose(2, self.root)

    def test_refuses_unpinned_location_change(self):
        changed = json.loads((self.base / "visual_manifest.json").read_text())
        changed["locationId"] = "LOC_INCORRECT_001"
        (self.base / "visual_manifest.json").write_text(json.dumps(changed))
        with self.assertRaisesRegex(ValueError, "locked scene/location"):
            p.compose(2, self.root)

    def test_refuses_missing_identity_pins(self):
        (self.root / "tools/hsk6_ready_preview_identity_pins.json").unlink()
        with self.assertRaisesRegex(ValueError, "identity/outfit/facing pin file"):
            p.compose(2, self.root)

    def test_reuses_unchanged_preview_only_with_provenance(self):
        preview, _ = p.compose(2, self.root)
        old = preview.read_bytes()
        second, _ = p.compose(2, self.root)
        self.assertEqual(old, second.read_bytes())

    def test_refuses_low_resolution_foreground(self):
        Image.new("RGBA", (540, 960), (0, 0, 0, 0)).save(
            self.base / self.files["foreground"], "WEBP")
        with self.assertRaisesRegex(ValueError, "low resolution"):
            p.compose(2, self.root)
        self.assertFalse((self.base / self.files["preview"]).exists())

    def test_refuses_manifest_actor_identity_mismatch(self):
        m = self.manifest.copy()
        m["characters"] = [*self.manifest["characters"]]
        m["characters"][0] = {"characterId": "CHAR_CHEN_YU_001"}
        (self.base / "visual_manifest.json").write_text(
            json.dumps(m), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "locked scene/location/identity/outfit/facing drift"):
            p.compose(2, self.root)
        self.assertFalse((self.base / self.files["preview"]).exists())

    def test_detects_changed_canonical_blob_before_composing(self):
        Image.new("RGB", (941, 1672), (25, 80, 100)).save(
            self.base / self.files["background"], "WEBP")
        with self.assertRaisesRegex(ValueError, "canonical source blob SHA drift"):
            p.compose(2, self.root)
        self.assertFalse((self.base / self.files["preview"]).exists())

    def test_rejects_missing_pinset(self):
        (self.root / "tools/hsk6_ready_preview_blobs.json").unlink()
        with self.assertRaisesRegex(ValueError, "pinned canonical source SHA"):
            p.compose(2, self.root)

    def test_rejects_non_ready_scene(self):
        with self.assertRaises(ValueError):
            p.compose(1, self.root)


if __name__ == "__main__":
    unittest.main()
