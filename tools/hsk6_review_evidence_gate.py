#!/usr/bin/env python3
"""Reject stale UIAutomator hierarchies and Android splash-only screenshots."""
import argparse
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path


def validate_hierarchy(path, marker, mode):
    nodes = [n for n in ET.parse(path).getroot().iter("node")
             if marker in n.attrib.get("content-desc", "")]
    if len(nodes) != 1:
        raise ValueError(f"Expected one {marker} marker, found {len(nodes)}")
    match = re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]",
                         nodes[0].attrib.get("bounds", ""))
    if not match:
        raise ValueError("Missing scene bounds")
    x1, y1, x2, y2 = map(int, match.groups())
    w, h = x2 - x1, y2 - y1
    if w < 300 or h < 300:
        raise ValueError(f"Unusable scene bounds {w}x{h}")
    if mode == "expanded" and h < 1200:
        raise ValueError(f"Expanded scene still compact: {w}x{h}")
    if mode == "compact" and h >= 1200:
        raise ValueError(f"Compact scene unexpectedly expanded: {w}x{h}")
    return w, h


def validate_pixels(path):
    data = Path(path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG screenshot")
    pos, chunks, width, height, channels = 8, [], 0, 0, 0
    while pos + 12 <= len(data):
        size = struct.unpack_from(">I", data, pos)[0]
        kind = data[pos+4:pos+8]
        chunk = data[pos+8:pos+8+size]
        if len(chunk) != size:
            raise ValueError("Truncated PNG chunk")
        if kind == b"IHDR":
            width, height, depth, color, comp, filt, interlace = struct.unpack(">IIBBBBB", chunk)
            if depth != 8 or color not in (2, 6) or interlace:
                raise ValueError("Unsupported screenshot PNG format")
            channels = 4 if color == 6 else 3
        elif kind == b"IDAT":
            chunks.append(chunk)
        elif kind == b"IEND":
            break
        pos += size + 12
    if width < 600 or height < 1000 or not chunks:
        raise ValueError(f"Unexpected screenshot size {width}x{height}")
    stride = width * channels
    raw = zlib.decompress(b"".join(chunks))
    if len(raw) != height * (stride + 1):
        raise ValueError("Invalid PNG payload size")
    prev = bytearray(stride)
    colored = sampled = 0
    offset = 0
    for y in range(height):
        filter_type = raw[offset]
        row = bytearray(raw[offset+1:offset+1+stride])
        offset += stride + 1
        for i in range(stride):
            a = row[i-channels] if i >= channels else 0
            b = prev[i]
            c = prev[i-channels] if i >= channels else 0
            if filter_type == 1:
                row[i] = (row[i] + a) & 255
            elif filter_type == 2:
                row[i] = (row[i] + b) & 255
            elif filter_type == 3:
                row[i] = (row[i] + (a+b)//2) & 255
            elif filter_type == 4:
                p = a+b-c
                da, db, dc = abs(p-a), abs(p-b), abs(p-c)
                pred = a if da <= db and da <= dc else b if db <= dc else c
                row[i] = (row[i] + pred) & 255
            elif filter_type != 0:
                raise ValueError(f"Invalid PNG filter {filter_type}")
        if int(height*.08) <= y <= int(height*.24) and y % 16 == 0:
            for x in range(int(width*.40), int(width*.61), 12):
                r, g, b = row[x*channels:x*channels+3]
                sampled += 1
                if max(r,g,b)-min(r,g,b) >= 20 and min(r,g,b) < 220:
                    colored += 1
        prev = row
    ratio = colored / max(sampled, 1)
    if ratio < .15:
        raise ValueError(f"Top-center scene pixels absent ({ratio:.1%}); splash/stale framebuffer")
    return ratio


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--xml", required=True)
    p.add_argument("--png")
    p.add_argument("--scene", choices=("042", "048"), required=True)
    p.add_argument("--speaker", choices=("zhang", "li"), required=True)
    p.add_argument("--mode", choices=("compact", "expanded"), required=True)
    a = p.parse_args()
    marker = f"SC{a.scene}_REVIEW_READY_{a.speaker.upper()}"
    w, h = validate_hierarchy(a.xml, marker, a.mode)
    ratio = validate_pixels(a.png) if a.png else None
    print(f"{marker} {a.mode}: {w}x{h}" +
          (f", colored={ratio:.1%}" if ratio is not None else ", UI-only"))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, ET.ParseError, OSError, zlib.error) as exc:
        print(f"REVIEW_NOT_PASS: {exc}", file=sys.stderr)
        sys.exit(1)
