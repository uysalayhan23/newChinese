import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_hsk6_032_038_camera_gate import preflight

class CameraGateTests(unittest.TestCase):
    def fixture(self, root, sc):
        b = Path(root) / 'content' / 'hsk6' / f'sc{sc}'
        b.mkdir(parents=True)
        manifest = {'sceneId': f'HSK6_SC{sc}', 'locationId': 'LOC_ELECTRONICS_STORE_001',
                    'cameraPreset': f'CAM_HSK6_SC{sc}_01',
                    'assets': {k: f'assets/hsk6_sc{sc}_{k}.webp'
                               for k in ('background', 'characterA', 'characterB', 'foreground', 'preview')}}
        grounding = {'sceneContext': {'status': 'approved'},
                     'locationMatch': {'status': 'approved', 'approvedForLayerPlanning': True},
                     'layerPlan': {'environmentCandidate': {'targetCameraPreset': f'CAM_HSK6_SC{sc}_01',
                                                            'donorCameraPreset': 'CAM_HSK6_SC035_01',
                                                            'cameraCalibrationVerified': False,
                                                            'donorReuseApproved': False}}}
        (b/'visual_manifest.json').write_text(json.dumps(manifest))
        (b/'visual_grounding.json').write_text(json.dumps(grounding))
        return b, grounding

    def test_missing_canonical_layers_stays_hold(self):
        with TemporaryDirectory() as d:
            self.fixture(d, '032')
            r = preflight(Path(d), '032')
            self.assertEqual(r['status'], 'HOLD')
            self.assertIn('BACKGROUND_WEBP_MISSING', r['blockers'])
            self.assertIn('FOREGROUND_WEBP_MISSING', r['blockers'])

    def test_camera_flags_alone_do_not_open_gate(self):
        with TemporaryDirectory() as d:
            b, g = self.fixture(d, '038')
            g['layerPlan']['environmentCandidate']['cameraCalibrationVerified'] = True
            g['layerPlan']['environmentCandidate']['donorReuseApproved'] = True
            (b/'visual_grounding.json').write_text(json.dumps(g))
            self.assertIn('TARGET_CAMERA_GROUND_PLANE_NOT_VERIFIED', preflight(Path(d), '038')['blockers'])

    def test_actor_sha_drift_stays_hold(self):
        with TemporaryDirectory() as d:
            b, _ = self.fixture(d, '032')
            (b/'assets').mkdir()
            (b/'assets/hsk6_sc032_characterA.webp').write_bytes(b'RIFFabcdWEBPfake')
            r = preflight(Path(d), '032')
            self.assertIn('CHARACTERA_CANONICAL_SHA_MISMATCH', r['blockers'])
            self.assertFalse(r['automaticSceneAcceptance'])

    def test_other_scene_is_rejected(self):
        with self.assertRaises(ValueError):
            preflight(Path('.'), '026')

if __name__ == '__main__':
    unittest.main()
