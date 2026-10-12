"""Offline test for canonical WebP REST-to-Pillow importer. No Actions."""
import base64
import hashlib
import json
import sys
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from import_hsk6_canonical_webps import decode_verified_webp, import_pinned_sources


class CanonicalImportTests(unittest.TestCase):
    def setUp(self):
        buf = BytesIO()
        Image.new("RGBA", (30, 40), (5, 6, 7, 25)).save(buf, "WEBP", lossless=True)
        self.raw = buf.getvalue()
        self.b64 = base64.b64encode(self.raw).decode("ascii")
        self.sha = hashlib.sha1(f"blob {len(self.raw)}\\0".encode().replace(b"\\0", b"\\x00") + self.raw).hexdigest()

    def test_valid_webp(self):
        self.assertEqual(decode_verified_webp(self.b64, self.sha), self.raw)

    def test_wrong_sha(self):
        with self.assertRaisesRegex(ValueError, "SHA mismatch"):
            decode_verified_webp(self.b64, "0" * 40)

    def test_invalid_base64(self):
        with self.assertRaises(Exception):
            decode_verified_webp("invalid&", self.sha)

    def test_not_a_webp(self):
        raw = b"not-webp"
        sha = hashlib.sha1(f"blob {len(raw)}\\0".encode().replace(b"\\0", b"\\x00") + raw).hexdigest()
        with self.assertRaises(Exception):
            decode_verified_webp(base64.b64encode(raw).decode(), sha)

    def test_deduplicated_scene_write(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            pins = root / "pins.json"
            pins.write_text(json.dumps({"scenes": {"002": {"a.webp": self.sha}, "006": {"b.webp": self.sha}}}))
            with patch("import_hsk6_canonical_webps.fetch_verified_webp", return_value=self.raw) as fetch:
                result = import_pinned_sources(pins, root, "owner/repo")
                self.assertEqual(result, {"unique_blobs": 1, "materialized": 2})
                self.assertEqual(fetch.call_count, 1)
                self.assertEqual((root / "content/hsk6/sc002/assets/a.webp").read_bytes(), self.raw)


if __name__ == "__main__":
    unittest.main()
