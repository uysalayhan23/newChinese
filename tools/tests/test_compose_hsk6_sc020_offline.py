"""SC020 wrapper guards: synthetic unit tests, no Actions or production writes."""
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

# Tests the SC020 lock and correct delegation to the independently tested
# compose_hsk6_odd11_staging source checker and compositor.
engine = types.ModuleType("compose_hsk6_odd11_staging")
engine.source_check = lambda root, scene, pin: {"verified": True}
engine.stage = lambda scene, layers, root, pin: (root / "candidate.webp", root / "candidate.qa.json")
sys.modules.setdefault("compose_hsk6_odd11_staging", engine)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compose_hsk6_sc020_offline as module


class SC020LockTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.base = self.root / "content/hsk6/sc020"
        (self.base / "assets").mkdir(parents=True)
        self.scene = {"sceneId": "HSK6_SC020", "locationId": "LOC_PUBLIC_LIBRARY_001",
                      "characterIds": ["CHAR_ZHANG_WEI_001", "CHAR_LI_NA_001"]}
        self.write_scene()

    def write_scene(self):
        (self.base / "scene.json").write_text(json.dumps(self.scene), encoding="utf-8")

    def test_delegates_with_exact_canonical_pins(self):
        with patch.object(module, "source_check", return_value={"verified": True}) as check, \
             patch.object(module, "stage", return_value=(self.root / "candidate.webp", self.root / "qa.json")) as stage:
            output, report = module.compose(self.root)
        self.assertEqual(output, self.root / "candidate.webp")
        self.assertEqual(report, self.root / "qa.json")
        check.assert_called_once_with(self.root, "020", module.PIN)
        stage.assert_called_once_with("020", {"verified": True}, self.root, module.PIN)
        self.assertEqual(len(module.PIN["assets"]), 4)

    def test_wrong_location_fails_closed(self):
        self.scene["locationId"] = "WRONG"
        self.write_scene()
        with self.assertRaisesRegex(ValueError, "location"):
            module.compose(self.root)

    def test_wrong_characters_fail_closed(self):
        self.scene["characterIds"] = ["CHAR_LIU_MEI_001", "CHAR_ZHANG_WEI_001"]
        self.write_scene()
        with self.assertRaisesRegex(ValueError, "speaker identity"):
            module.compose(self.root)

    def test_existing_production_preview_blocks(self):
        (self.base / "assets/hsk6_sc020_preview.webp").write_bytes(b"existing")
        with self.assertRaises(FileExistsError):
            module.compose(self.root)


if __name__ == "__main__":
    unittest.main()
