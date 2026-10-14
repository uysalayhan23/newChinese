#!/usr/bin/env python3
"""Offline SHA-pinned HSK6 odd-11 preview composer (staging only).

Preflight sources and locked identities. Never change canonical layers,
production previews, visual_manifest.json, media_status.json, or acceptance.
Requires Pillow. No network or GitHub Actions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SIZE = (720, 1280)
SCENES = ("001", "007", "011", "017", "023", "029",
          "031", "033", "035", "037", "039")
ROLES = ("background", "characterA", "characterB", "foreground")
PINFILE = Path("tools/hsk6_odd11_preview_pins.json")


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def source_check(root: Path, scene: str, pin: dict) -> dict[str, Image.Image]:
    base = root / "content" / "hsk6" / f"sc{scene}"
    manifest = json.loads((base / "visual_manifest.json").read_text("utf-8"))
    locked = {
        "sceneId": manifest.get("sceneId"),
        "locationId": manifest.get("locationId"),
        "characters": manifest.get("characters"),
    }
    expected = {
        "sceneId": pin["sceneId"],
        "locationId": pin["locationId"],
        "characters": pin["characters"],
    }
    if locked != expected or manifest.get("status") != "visual-assets-pending":
        raise ValueError(f"SC{scene}: scene, identity, outfit, direction or status drift")
    layers = {}
    for role in ROLES:
        item = pin["assets"][role]
        path = root / item["path"]
        if path != base / manifest["assets"][role]:
            raise ValueError(f"SC{scene}: {role} path lock changed")
        data = path.read_bytes()
        if blob_sha(data) != item["sha"]:
            raise ValueError(f"SC{scene}: {role} SHA mismatch")
        with Image.open(BytesIO(data)) as im:
            if im.format != "WEBP":
                raise ValueError(f"SC{scene}: {role} is not WebP")
            im.load()
            w,h = im.size
            if role in ("background","foreground") and (w,h) != SIZE:
                raise ValueError(f"SC{scene}: {role} is not 720x1280")
            if role.startswith("character") and (w<400 or h<600):
                raise ValueError(f"SC{scene}: low-resolution character {role}")
            if role != "background" and "A" not in im.getbands():
                raise ValueError(f"SC{scene}: {role} missing transparency channel")
            layer = im.convert("RGBA")
            if role != "background":
                low, high = layer.getchannel("A").getextrema()
                if low == 255 or high == 0:
                    raise ValueError(f"SC{scene}: {role} has unusable alpha")
            layers[role] = layer
    return layers



def guard_foreground_visibility(scene: str, foreground: Image.Image,
                                actor_masks: dict[str, tuple[int, int, Image.Image]]) -> dict:
    """Reject foreground covering canonical heads, torsos, or speaking gestures.

    Only opacity is compared; irrelevant colors hidden under transparency
    cannot fail QA. Deliberate bottom-leg floor/prop occlusion is permitted.
    This geometry check supplements, never replaces, human visual review.
    """
    fg_alpha = foreground.getchannel("A").point(lambda v: 255 if v >= 80 else 0)
    results = {}
    for role, (x, y, actor_alpha) in actor_masks.items():
        w, h = actor_alpha.size
        region_results = {}
        for region, fraction, limit in (("head", .30, .005),
                                        ("torso_and_gestures", .75, .02)):
            end = max(1, round(h * fraction))
            actor = actor_alpha.crop((0, 0, w, end)).point(
                lambda v: 255 if v >= 160 else 0)
            fg = fg_alpha.crop((x, y, x+w, y+end))
            opaque_actor = actor.histogram()[255]
            obscured = ImageChops.multiply(actor, fg).histogram()[255]
            rate = obscured / max(opaque_actor, 1)
            region_results[region] = round(rate, 6)
            if rate > limit:
                raise ValueError(
                    f"SC{scene}: foreground covers {role} {region} "
                    f"({rate:.2%} > {limit:.2%}); QA HOLD")
        results[role] = region_results
    return results

def stage(scene: str, layers: dict[str,Image.Image], root: Path,
          pin: dict) -> tuple[Path,Path]:
    target = root / "staging" / "hsk6" / "qa_pending" / f"sc{scene}"
    preview = target / f"hsk6_sc{scene}_canonical_composite_candidate.webp"
    report = target / f"hsk6_sc{scene}_canonical_composite_candidate.qa.json"
    if preview.exists() or report.exists():
        raise FileExistsError(f"SC{scene}: candidate already exists; refusing overwrite")
    canvas = layers["background"].copy()
    positions = {}
    actor_masks = {}
    for role,frac in (("characterA",.285),("characterB",.715)):
        actor=layers[role]
        bounds=actor.getchannel("A").getbbox()
        if bounds is None:
            raise ValueError(f"SC{scene}: actor silhouette invisible")
        actor=actor.crop(bounds)
        scale=min((SIZE[1]*.62)/actor.height, (SIZE[0]*.56)/actor.width)
        w=max(1,round(actor.width*scale))
        h=max(1,round(actor.height*scale))
        actor=actor.resize((w,h),Image.Resampling.LANCZOS)
        x=round(SIZE[0]*frac-w/2)
        x=max(0,min(SIZE[0]-w,x))
        y=SIZE[1]-round(SIZE[1]*.055)-h
        if y<0 or w>SIZE[0]:
            raise ValueError(f"SC{scene}: character geometry exceeds frame")
        positions[role]={"x":x,"y":y,"width":w,"height":h}
        actor_masks[role] = (x, y, actor.getchannel("A"))
        canvas.alpha_composite(actor,(x,y))
    a,b=(positions[r] for r in ("characterA","characterB"))
    overlap=max(0,min(a["x"]+a["width"],b["x"]+b["width"])-max(a["x"],b["x"]))
    if overlap>round(SIZE[0]*.21):
        raise ValueError(f"SC{scene}: actor overlap {overlap}px exceeds limit")
    visibility = guard_foreground_visibility(scene, layers["foreground"], actor_masks)
    canvas.alpha_composite(layers["foreground"])
    payload=BytesIO()
    canvas.convert("RGB").save(payload,"WEBP",quality=92,method=6)
    binary=payload.getvalue()
    with Image.open(BytesIO(binary)) as test:
        test.load()
        if test.format!="WEBP" or test.size!=SIZE:
            raise ValueError(f"SC{scene}: physical output validation failed")
    provenance={
        "sceneId":pin["sceneId"],"qaStatus":"PENDING_HUMAN_VISUAL_IDENTITY_DEPTH_CONTINUITY",
        "accepted":False,"productionFilesModified":False,
        "method":"canonical_4_layer_deterministic_compositor_staging_v1",
        "sourceGitBlobs":{r:pin["assets"][r]["sha"] for r in ROLES},
        "previewGitBlob":blob_sha(binary),"previewSha256":hashlib.sha256(binary).hexdigest(),
        "resolution":[*SIZE],"positions":positions,
        "foregroundVisibilityQA":visibility
    }
    target.mkdir(parents=True,exist_ok=True)
    preview.write_bytes(binary)
    report.write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return preview,report


def main(argv:list[str]|None=None)->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root",type=Path,default=ROOT)
    ap.add_argument("--scenes",nargs="*",default=list(SCENES))
    args=ap.parse_args(argv)
    if not args.scenes or any(s not in SCENES for s in args.scenes):
        ap.error("Only explicit HSK6 odd-11 scenes are allowed")
    pinned=json.loads((args.root/PINFILE).read_text("utf-8"))["scenes"]
    # Preflight every input before writing any candidate.
    prepared={}
    for scene in args.scenes:
        prepared[scene]=source_check(args.root,scene,pinned[scene])
        out=args.root/"staging"/"hsk6"/"qa_pending"/f"sc{scene}"
        if any((out/f"hsk6_sc{scene}_canonical_composite_candidate{suffix}").exists()
               for suffix in (".webp",".qa.json")):
            raise FileExistsError(f"SC{scene}: staging file already exists")
    for scene in args.scenes:
        preview,report=stage(scene,prepared[scene],args.root,pinned[scene])
        print(f"STAGED only: {preview.relative_to(args.root)}; {report.name}; ACCEPTED=false")
    return 0


if __name__=="__main__":
    raise SystemExit(main())