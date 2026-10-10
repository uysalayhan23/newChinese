"""Offline unit tests for the canonical WebP transfer helper. No networking."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fetch_hsk5_sc031_sc040 as f


def make_webp():
    # Header-only fixture: transfer checks bytes/header; Pillow decoding is separate.
    payload = b"VP8 " + b"\x00" * 32
    return b"RIFF" + len(payload).to_bytes(4, "little") + b"WEBP" + payload


class TransferTests(unittest.TestCase):
    def test_blob_hash(self):
        data = b"test"
        expect = hashlib.sha1(b"blob 4\x00test").hexdigest()
        self.assertEqual(f.blob_sha(data), expect)

    def test_valid_and_truncated_webp(self):
        f.validate_webp(make_webp())
        with self.assertRaises(ValueError):
            f.validate_webp(make_webp()[:16])

    def test_all_four_assets_transferred_then_verified(self):
        data = make_webp()
        keys = f.SCENE_LAYERS[34]
        with tempfile.TemporaryDirectory() as p, patch.dict(
                f.CANONICAL, {k: f.blob_sha(data) for k in keys}):
            with patch.object(f, "fetch", return_value=data) as fetch:
                self.assertEqual(f.transfer(Path(p), [34], None), 4)
                self.assertEqual(fetch.call_count, 4)
                self.assertEqual(f.transfer(Path(p), [34], None), 0)
                self.assertEqual(fetch.call_count, 4)

    def test_never_overwrites_unknown_asset(self):
        with tempfile.TemporaryDirectory() as p:
            filename = Path(p) / "content/hsk5/sc034/assets/hsk5_sc034_bg.webp"
            filename.parent.mkdir(parents=True)
            filename.write_bytes(make_webp())
            with patch.object(f, "fetch") as fetch:
                with self.assertRaisesRegex(ValueError, "refusing to replace"):
                    f.transfer(Path(p), [34], None)
                fetch.assert_not_called()

    def test_rejects_sha_mismatch(self):
        with tempfile.TemporaryDirectory() as p, patch.object(
                f, "fetch", return_value=make_webp()):
            with self.assertRaisesRegex(ValueError, "SHA mismatch"):
                f.transfer(Path(p), [34], None)
            self.assertFalse((Path(p) / "content/hsk5/sc034/assets/hsk5_sc034_bg.webp").exists())


if __name__ == "__main__":
    unittest.main()
