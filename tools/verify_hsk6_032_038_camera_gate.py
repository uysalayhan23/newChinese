#!/usr/bin/env python3
"""Read-only HSK6 SC032/SC038 release preflight; never promotes media or runs CI."""
from __future__ import annotations
import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path
from PIL import Image, UnidentifiedImageError

SCENES = ('032', '038')
ACTOR_PINS = {'characterA': '44a7a521b7fa64466111c30f6830904081c3767d',
              'characterB': 'ee14b09ae3c8cc4f5e539a54884798900f2ad85b'}
DONOR_PINS = {'background': 'b0ba989e06045ea92a0c4fd6ebf580877f4acc48',
              'foreground': 'dd7b43d996a33e40ff2c5cf86b5c4fa297238061'}
V4_PINS = {'fg': '84631be9ed27a64a29e134e84037919b23277440',
           'preview': 'ca8c43043c628d2b69ef7e59625bca49f1586533'}

def blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))

def preflight(root: Path, sc: str) -> dict:
    if sc not in SCENES:
        raise ValueError('Only HSK6_SC032 and SC038 supported')
    scene = f'HSK6_SC{sc}'
    base = root / 'content' / 'hsk6' / f'sc{sc}'
    blockers = []
    result = {'sceneId': scene, 'blockers': blockers, 'checks': {}}
    try:
        manifest = load_json(base / 'visual_manifest.json')
        grounding = load_json(base / 'visual_grounding.json')
    except (OSError, ValueError) as exc:
        blockers.append(f'SOURCE_MANIFEST_GROUNDING_INVALID:{type(exc).__name__}')
        result.update(status='HOLD', automaticSceneAcceptance=False)
        return result
    cam = grounding.get('layerPlan', {}).get('environmentCandidate', {})
    target_cam = f'CAM_HSK6_SC{sc}_01'
    donor_cam = 'CAM_HSK6_SC035_01'
    meta_ok = (manifest.get('sceneId') == scene and
               manifest.get('locationId') == 'LOC_ELECTRONICS_STORE_001' and
               manifest.get('cameraPreset') == target_cam and
               grounding.get('sceneContext', {}).get('status') == 'approved' and
               grounding.get('locationMatch', {}).get('status') == 'approved' and
               grounding.get('locationMatch', {}).get('approvedForLayerPlanning') is True and
               cam.get('targetCameraPreset') == target_cam and
               cam.get('donorCameraPreset') == donor_cam)
    result['checks']['grounding'] = bool(meta_ok)
    if not meta_ok:
        blockers.append('SCENE_GROUNDING_OR_CAMERA_METADATA_INVALID')
    evidence_path = root / 'staging' / 'hsk6' / 'qa_pending' / f'sc{sc}' / 'approved_numeric_camera_evidence.json'
    proof = {}
    if evidence_path.is_file():
        try:
            proof = load_json(evidence_path)
        except (OSError, ValueError):
            blockers.append('NUMERIC_CAMERA_EVIDENCE_INVALID_JSON')
    errors = proof.get('landmarkReprojectionErrorsPx')
    proof_ok = (proof.get('sceneId') == scene and
                proof.get('targetCameraPreset') == target_cam and
                proof.get('referenceDonorPreset') == donor_cam and
                proof.get('status') == 'independently_approved' and
                isinstance(errors, list) and len(errors) >= 4 and
                all(type(e) in (int, float) and 0 <= e <= 2 for e in errors) and
                isinstance(proof.get('sourceImageBlobSha'), str) and
                len(proof['sourceImageBlobSha']) == 40 and
                bool(proof.get('reviewEvidencePath')))
    camera_ok = (cam.get('cameraCalibrationVerified') is True and
                 cam.get('donorReuseApproved') is True and proof_ok)
    result['checks']['numericCameraProof'] = bool(camera_ok)
    if not camera_ok:
        blockers.append('TARGET_CAMERA_GROUND_PLANE_NOT_VERIFIED')
    assets = {}
    for kind in ('background', 'characterA', 'characterB', 'foreground', 'preview'):
        rel = manifest.get('assets', {}).get(kind)
        if not isinstance(rel, str) or not rel.startswith('assets/') or '..' in Path(rel).parts:
            blockers.append(f'{kind.upper()}_PATH_INVALID')
            continue
        p = base / rel
        if not p.is_file():
            blockers.append(f'{kind.upper()}_WEBP_MISSING')
            assets[kind] = {'present': False}
            continue
        raw = p.read_bytes()
        sha = blob_sha(p)
        valid = raw.startswith(b'RIFF') and raw[8:12] == b'WEBP'
        decoded = False
        try:
            with Image.open(BytesIO(raw)) as img:
                img.load()
                decoded = (img.size == (720, 1280) if kind in ('background', 'foreground', 'preview')
                           else img.width > 0 and img.height > 0)
                decoded &= (img.mode == 'RGBA' if kind in ('characterA', 'characterB', 'foreground')
                            else img.mode in ('RGB', 'RGBA'))
        except (UnidentifiedImageError, ValueError, OSError):
            pass
        assets[kind] = {'present': True, 'gitBlobSha': sha, 'webpPhysicalDecode': bool(valid and decoded)}
        if not valid or not decoded:
            blockers.append(f'{kind.upper()}_WEBP_PHYSICAL_INVALID')
        if kind in ACTOR_PINS and sha != ACTOR_PINS[kind]:
            blockers.append(f'{kind.upper()}_CANONICAL_SHA_MISMATCH')
        if kind in DONOR_PINS and sha == DONOR_PINS[kind] and not camera_ok:
            blockers.append(f'{kind.upper()}_DONOR_COPY_UNAPPROVED')
    result['checks']['physicalTargetAssets'] = assets
    stage = {}
    for kind, file in {'fg': f'hsk6_sc{sc}_right_counter_only_fg_candidate_v4.webp',
                       'preview': f'hsk6_sc{sc}_right_counter_depth_preview_v4_STAGING.webp'}.items():
        p = root / 'staging' / 'hsk6' / 'qa_pending' / f'sc{sc}' / file
        stage[kind] = {'present': p.is_file(), 'shaVerified': p.is_file() and blob_sha(p) == V4_PINS[kind]}
        if p.is_file() and not stage[kind]['shaVerified']:
            blockers.append(f'V4_{kind.upper()}_STAGING_SHA_MISMATCH')
    result['checks']['v4StagingOnly'] = stage
    result['status'] = 'HOLD' if blockers else 'PRECHECK_ONLY_INDEPENDENT_VISUAL_QA_STILL_REQUIRED'
    result['automaticSceneAcceptance'] = False
    result['productionWritePerformed'] = False
    return result

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--scenes', nargs='+', choices=SCENES, default=list(SCENES))
    args = parser.parse_args()
    checks = [preflight(args.repo, sc) for sc in args.scenes]
    print(json.dumps({'releasePreflight': checks}, ensure_ascii=False, indent=2))
    return 2 if any(x['status'] == 'HOLD' for x in checks) else 0

if __name__ == '__main__':
    raise SystemExit(main())
