"""Downscale raster images (e.g. pasted screenshots) embedded in draw.io PNGs.

Each embedded image is reduced to FACTOR times the size at which it is drawn
in the diagram (FACTOR is at least the scale of the PNG export, so no visible
resolution is lost). The PNG is then re-rendered at its current width with the
draw.io desktop CLI, which embeds the full diagram source again (all pages).
Requires ImageMagick (`magick`) and draw.io. Not a pre-commit hook; run it
manually on diagrams that contain large pasted images.

Usage: python tools/shrink_drawio_embedded_images.py [--dry-run] images/x.dio.png ...
Set DRAWIO to the draw.io executable if it is not in the default macOS location.
"""
import base64
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

FACTOR = 2.0
DRAWIO = os.environ.get("DRAWIO", "/Applications/draw.io.app/Contents/MacOS/draw.io")
PREFIX = "image=data:image/"


def png_width(path):
    with open(path, "rb") as f:
        return struct.unpack(">I", f.read(24)[16:20])[0]


def drawio(*args):
    subprocess.run([DRAWIO, "-x", *args], capture_output=True, check=True)


def render_scale(diagram, width_px):
    """Pixels per diagram unit of the exported first page."""
    xs = []
    for g in diagram.iter("mxGeometry"):
        if g.get("relative") == "1" or g.get("width") is None:
            continue
        x = float(g.get("x", 0))
        xs += [x, x + float(g.get("width"))]
    return width_px / (max(xs) - min(xs)) if xs else FACTOR


def resize(raw, fmt, w, h):
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, "in." + fmt), os.path.join(d, "out." + fmt)
        with open(src, "wb") as f:
            f.write(raw)
        subprocess.run(["magick", src, "-resize", f"{w}x{h}!", dst], check=True)
        with open(dst, "rb") as f:
            return f.read()


def image_size(raw, fmt):
    out = subprocess.run(
        ["magick", "identify", "-format", "%w %h", f"{fmt}:-"],
        input=raw, capture_output=True, check=True,
    ).stdout.split()
    return int(out[0]), int(out[1])


def shrink(path, dry_run):
    width_px = png_width(path)
    with tempfile.TemporaryDirectory() as d:
        xml_path = os.path.join(d, "diagram.drawio")
        drawio("-f", "xml", "--uncompressed", "-o", xml_path, path)
        tree = ET.parse(xml_path)
        diagrams = tree.getroot().findall("diagram")
        factor = max(FACTOR, render_scale(diagrams[0], width_px))
        before = after = 0
        for cell in tree.getroot().iter("mxCell"):
            style = cell.get("style", "")
            k = style.find(PREFIX)
            geometry = cell.find("mxGeometry")
            if k < 0 or geometry is None:
                continue
            end = style.find(";", k)
            end = len(style) if end < 0 else end
            fmt, _, b64 = style[k + len(PREFIX) : end].partition(",")
            raw = base64.b64decode(b64 + "=" * (-len(b64) % 4))
            w, h = image_size(raw, fmt)
            tw = math.ceil(float(geometry.get("width")) * factor)
            th = math.ceil(float(geometry.get("height")) * factor)
            s = max(tw / w, th / h)
            before += len(raw)
            if s >= 0.9:
                after += len(raw)
                continue
            nw, nh = round(w * s), round(h * s)
            new = raw if dry_run else resize(raw, fmt, nw, nh)
            after += len(new)
            print(f"  {w}x{h} -> {nw}x{nh}")
            if not dry_run:
                data = base64.b64encode(new).decode("ascii")
                cell.set("style", style[:k] + PREFIX + fmt + "," + data + style[end:])
        if dry_run or before == after:
            print(f"{path}: embedded images {before / 1e6:.2f} MB (no change written)")
            return False
        tree.write(xml_path, encoding="utf-8")
        out = os.path.join(d, "out.png")
        drawio("-f", "png", "-e", "--width", str(width_px), "-o", out, xml_path)
        if png_width(out) != width_px:
            raise RuntimeError(f"re-export of {path} failed")
        old_size = os.path.getsize(path)
        shutil.copyfile(out, path)
        print(f"{path}: embedded images {before / 1e6:.2f} -> {after / 1e6:.2f} MB, "
              f"file {old_size / 1e6:.2f} -> {os.path.getsize(path) / 1e6:.2f} MB")
        return True


if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry-run" in args
    for p in [a for a in args if a != "--dry-run"]:
        shrink(p, dry)
