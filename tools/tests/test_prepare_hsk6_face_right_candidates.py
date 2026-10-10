"""Offline checks for HSK6 face-right candidate repair; never starts Actions."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import prepare_hsk6_face_right_candidates as prep


class HSK6CandidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        source_specs = {}
        for identity, (name, _sha, outfit) in prep.SOURCES.items():
            filename = self.root / name
            filename.parent.mkdir(parents=True, exist_ok=True)
            image = Image.new("RGBA", (600, 900), (0, 0, 0, 0))
            ImageDraw.Draw(image).rectangle((40, 100, 170, 800),
                                            fill=(100, 130, 200, 255))
            image.save(filename, "WEBP", lossless=True)
            source_specs[identity] = (name, prep.git_blob_sha1(filename), outfit)
        patcher = patch.object(prep, "SOURCES", source_specs)
        patcher.start()
        self.addCleanup(patcher.stop)
        pinned_scenes = {}
        for scene, actor_id in prep.SCENE_ACTORS.items():
            directory = self.root / f"content/hsk6/sc{scene:03d}"
            directory.mkdir(parents=True)
            manifest = {
                "sceneId": f"HSK6_SC{scene:03d}",
                "locationId": "LOC_TEST_001",
                "assets": {"characterA": f"assets/{prep.target_path(scene, actor_id, self.root).name}"},
                "characters": [
                    {"characterId": actor_id, "speechBubbleAnchor": "face_right",
                     "outfit": prep.SOURCES[actor_id][2]},
                    {"characterId": "CHAR_ZHANG_WEI_001", "speechBubbleAnchor": "face_left",
                     "outfit": "OUTFIT_ZHANG_WEI_CASUAL_01"},
                ],
            }
            (directory / "visual_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            pinned_scenes[f"{scene:03d}"] = {
                "sceneId": manifest["sceneId"],
                "locationId": manifest["locationId"],
                "characters": [
                    {key: actor.get(key) for key in
                     ("characterId", "outfit", "speechBubbleAnchor")}
                    for actor in manifest["characters"]
                ],
            }
        pins_file = self.root / "tools/hsk6_face_right_identity_pins.json"
        pins_file.parent.mkdir(parents=True, exist_ok=True)
        pins_file.write_text(json.dumps({"scenes": pinned_scenes}), encoding="utf-8")

    def test_missing_independent_identity_pins_blocks_all_outputs(self):
        (self.root / "tools/hsk6_face_right_identity_pins.json").unlink()
        with self.assertRaisesRegex(ValueError, "identity pin file missing"):
            prep.prepare(self.root)
        self.assertFalse(prep.target_path(1, prep.SCENE_ACTORS[1], self.root).exists())

    def test_secondary_actor_identity_drift_blocks_all_outputs(self):
        manifest = self.root / "content/hsk6/sc039/visual_manifest.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["characters"][1]["characterId"] = "CHAR_CHEN_YU_001"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "independent scene/identity"):
            prep.prepare(self.root)
        self.assertFalse(prep.target_path(1, prep.SCENE_ACTORS[1], self.root).exists())

    def test_locked_location_drift_blocks_all_outputs(self):
        manifest = self.root / "content/hsk6/sc019/visual_manifest.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["locationId"] = "LOC_WRONG_001"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "independent scene/identity"):
            prep.prepare(self.root)
        self.assertFalse(prep.target_path(1, prep.SCENE_ACTORS[1], self.root).exists())

    def test_20_candidates_preserve_character_pixels_and_alpha(self):
        outputs = prep.prepare(self.root)
        self.assertEqual(len(outputs), 20)
        for scene, identity in prep.SCENE_ACTORS.items():
            target = prep.target_path(scene, identity, self.root)
            with Image.open(target) as im:
                self.assertEqual(im.size, (600, 900))
                rgba = im.convert("RGBA")
                self.assertEqual(rgba.getpixel((490, 300))[3], 255)
                self.assertEqual(rgba.getpixel((80, 300))[3], 0)

    def test_refuses_to_overwrite_any_existing_actor(self):
        target = prep.target_path(1, prep.SCENE_ACTORS[1], self.root)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"do not overwrite")
        with self.assertRaisesRegex(FileExistsError, "must not be overwritten"):
            prep.prepare(self.root)
        self.assertEqual(target.read_bytes(), b"do not overwrite")

    def test_invalid_wardrobe_stops_before_first_write(self):
        scene = 39
        manifest = self.root / f"content/hsk6/sc{scene:03d}/visual_manifest.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["characters"][0]["outfit"] = "OUTFIT_WRONG"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "drift"):
            prep.prepare(self.root)
        self.assertFalse(prep.target_path(1, prep.SCENE_ACTORS[1], self.root).exists())

    def test_bad_sha_blocks_all_candidates(self):
        spec = prep.SOURCES["CHAR_WANG_MING_001"]
        prep.SOURCES["CHAR_WANG_MING_001"] = (spec[0], "0" * 40, spec[2])
        with self.assertRaisesRegex(ValueError, "missing/mismatched"):
            prep.prepare(self.root)
        self.assertFalse(prep.target_path(1, prep.SCENE_ACTORS[1], self.root).exists())


if __name__ == "__main__":
    unittest.main()
