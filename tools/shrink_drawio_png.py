"""Re-export draw.io PNGs wider than MAX_WIDTH pixels at MAX_WIDTH.

Uses the draw.io desktop CLI, which renders the diagram stored inside the PNG
again and embeds the diagram source in the new file, so it stays editable.
Multi-page diagrams are skipped, because the embedded export keeps one page only.

Usage: python tools/shrink_drawio_png.py images/x.dio.png ...
Set DRAWIO to the draw.io executable if it is not in the default macOS location.
Exits 1 if any file was changed or could not be processed (pre-commit convention).
"""
import os
import re
import struct
import subprocess
import sys
import tempfile
import urllib.parse

MAX_WIDTH = 2000
DRAWIO = os.environ.get("DRAWIO", "/Applications/draw.io.app/Contents/MacOS/draw.io")


def png_info(path):
    """Return (width, number of diagram pages in an embedded mxfile)."""
    with open(path, "rb") as f:
        png = f.read()
    (width,) = struct.unpack(">I", png[16:20])
    pages, i = 1, 8
    while i < len(png):
        (n,) = struct.unpack(">I", png[i : i + 4])
        if png[i + 4 : i + 8] == b"tEXt" and png[i + 8 : i + 15] == b"mxfile\0":
            xml = urllib.parse.unquote(png[i + 15 : i + 8 + n].decode("latin1"))
            pages = max(1, len(re.findall(r"<diagram[ >]", xml)))
        i += 12 + n
    return width, pages


def main(paths):
    failed = False
    for path in paths:
        width, pages = png_info(path)
        if width <= MAX_WIDTH:
            continue
        if pages > 1:
            print(f"skipped {path}: {pages} pages, re-export manually")
            continue
        if not os.path.exists(DRAWIO):
            print(f"{path} is {width} px wide; draw.io CLI not found at {DRAWIO}")
            failed = True
            continue
        fd, tmp = tempfile.mkstemp(suffix=".png", dir=os.path.dirname(path) or ".")
        os.close(fd)
        subprocess.run(
            [DRAWIO, "-x", "-f", "png", "-e", "--width", str(MAX_WIDTH), "-o", tmp, path],
            capture_output=True,
        )
        if os.path.getsize(tmp) == 0 or png_info(tmp)[0] != MAX_WIDTH:
            print(f"failed to re-export {path}")
            os.remove(tmp)
            failed = True
            continue
        os.replace(tmp, path)
        print(f"re-exported {path}: {width} -> {MAX_WIDTH} px")
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
