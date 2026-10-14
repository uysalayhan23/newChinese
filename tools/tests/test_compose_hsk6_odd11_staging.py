"""Synthetic offline tests; never touch the real repository or canonical files."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import compose_hsk6_odd11_staging as c


class Odd11PreviewTest(unittest.TestCase):
    def setUp(self):
        self.work=tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.root=Path(self.work.name)
        self.base=self.root/"content/hsk6/sc001"
        (self.base/"assets").mkdir(parents=True)
        self.paths={
            "background":"assets/hsk6_sc001_bg.webp",
            "characterA":"assets/hsk6_sc001_char_wang_ming.webp",
            "characterB":"assets/hsk6_sc001_char_zhang_wei.webp",
            "foreground":"assets/hsk6_sc001_fg.webp",
            "preview":"assets/hsk6_sc001_preview.webp",
        }
        self.manifest={
            "sceneId":"HSK6_SC001","locationId":"LOC_ZHANG_OFFICE_001",
            "characters":[
                {"characterId":"CHAR_WANG_MING_001","outfit":"OUTFIT_WANG_MING_WORK_01","speechBubbleAnchor":"face_right"},
                {"characterId":"CHAR_ZHANG_WEI_001","outfit":"OUTFIT_ZHANG_WEI_CASUAL_01","speechBubbleAnchor":"face_left"}
            ],"assets":self.paths,"status":"visual-assets-pending"
        }
        self.write_image_assets()
        (self.base/"visual_manifest.json").write_text(json.dumps(self.manifest),encoding="utf-8")
        self.set_pins()

    def write_image_assets(self):
        Image.new("RGB",c.SIZE,(190,170,140)).save(self.base/self.paths["background"],"WEBP")
        for key,color in (("characterA",(255,50,20,255)),("characterB",(20,20,255,255))):
            a=Image.new("RGBA",(650,1024),(0,0,0,0))
            ImageDraw.Draw(a).rectangle((140,50,500,1000),fill=color)
            a.save(self.base/self.paths[key],"WEBP")
        fg=Image.new("RGBA",c.SIZE,(0,0,0,0))
        ImageDraw.Draw(fg).rectangle((0,1100,720,1279),fill=(20,70,20,255))
        fg.save(self.base/self.paths["foreground"],"WEBP")

    def set_pins(self):
        self.pin={
            "sceneId":self.manifest["sceneId"],
            "locationId":self.manifest["locationId"],
            "characters":self.manifest["characters"],
            "assets":{k:{"path":str((self.base/self.paths[k]).relative_to(self.root)),
                          "sha":c.blob_sha((self.base/self.paths[k]).read_bytes())}
                      for k in c.ROLES}
        }
        pins=self.root/"tools"/"hsk6_odd11_preview_pins.json"
        pins.parent.mkdir(exist_ok=True)
        pins.write_text(json.dumps({"scenes":{"001":self.pin}}),encoding="utf-8")

    def test_produces_staged_webp_without_changing_manifest(self):
        old=(self.base/"visual_manifest.json").read_bytes()
        code=c.main(["--root",str(self.root),"--scenes","001"])
        self.assertEqual(code,0)
        target=self.root/"staging/hsk6/qa_pending/sc001"
        out=target/"hsk6_sc001_canonical_composite_candidate.webp"
        report=json.loads((target/"hsk6_sc001_canonical_composite_candidate.qa.json").read_text())
        with Image.open(out) as im:
            self.assertEqual(im.format,"WEBP")
            self.assertEqual(im.size,c.SIZE)
        self.assertEqual(out.read_bytes() and c.blob_sha(out.read_bytes()),report["previewGitBlob"])
        self.assertFalse(report["accepted"])
        self.assertEqual((self.base/"visual_manifest.json").read_bytes(),old)
        self.assertFalse((self.base/self.paths["preview"]).exists())
        self.assertEqual(len(report["sourceGitBlobs"]),4)

    def test_source_sha_mismatch_fails_closed(self):
        (self.base/self.paths["characterA"]).write_bytes(b"wrong")
        with self.assertRaisesRegex(ValueError,"SHA mismatch"):
            c.main(["--root",str(self.root),"--scenes","001"])
        self.assertFalse((self.root/"staging").exists())

    def test_location_identity_change_fails_closed(self):
        m=json.loads((self.base/"visual_manifest.json").read_text())
        m["locationId"]="WRONG"
        (self.base/"visual_manifest.json").write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError,"drift"):
            c.main(["--root",str(self.root),"--scenes","001"])

    def test_pin_wardrobe_change_fails_closed(self):
        m=json.loads((self.base/"visual_manifest.json").read_text())
        m["characters"][0]["outfit"]="OUTFIT_BAD"
        (self.base/"visual_manifest.json").write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError,"drift"):
            c.main(["--root",str(self.root),"--scenes","001"])

    def test_opaque_foreground_fails_closed(self):
        Image.new("RGBA",c.SIZE,(0,0,0,255)).save(self.base/self.paths["foreground"],"WEBP")
        self.set_pins()
        with self.assertRaisesRegex(ValueError,"missing transparency channel|unusable alpha"):
            c.main(["--root",str(self.root),"--scenes","001"])

    def test_refuse_replacing_existing_candidate(self):
        c.main(["--root",str(self.root),"--scenes","001"])
        with self.assertRaises(FileExistsError):
            c.main(["--root",str(self.root),"--scenes","001"])


if __name__=="__main__":
    unittest.main()