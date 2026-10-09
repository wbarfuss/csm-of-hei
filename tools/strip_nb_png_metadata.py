"""Remove run-dependent noise from notebook outputs, for git-friendly diffs.

- PNG outputs: drop text chunks (tEXt/zTXt/iTXt), which hold the Matplotlib
  version. Pixel data is untouched.
- ipywidget outputs: drop the widget-view reference (random model_id per run),
  keep the text/plain fallback.

Usage: python tools/strip_nb_png_metadata.py NOTEBOOK.ipynb ...
Exits 1 if any file was changed (pre-commit convention).
"""
import base64
import json
import struct
import sys

TEXT_CHUNKS = {b"tEXt", b"zTXt", b"iTXt"}
WIDGET_VIEW = "application/vnd.jupyter.widget-view+json"


def strip_png(b64):
    png = base64.b64decode(b64)
    out, i = [png[:8]], 8
    while i < len(png):
        (n,) = struct.unpack(">I", png[i : i + 4])
        if png[i + 4 : i + 8] not in TEXT_CHUNKS:
            out.append(png[i : i + 12 + n])
        i += 12 + n
    return base64.b64encode(b"".join(out)).decode("ascii")


def clean(nb):
    for cell in nb.get("cells", []):
        for output in cell.get("outputs", []):
            data = output.get("data", {})
            data.pop(WIDGET_VIEW, None)
            png = data.get("image/png")
            if png is not None:
                if isinstance(png, list):
                    png = "".join(png)
                trailing = "\n" if png.endswith("\n") else ""
                data["image/png"] = strip_png(png.strip()) + trailing
    return nb


def main(paths):
    changed = False
    for path in paths:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        new = json.dumps(clean(json.loads(raw)), indent=1, ensure_ascii=False) + "\n"
        if new != raw:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            print(f"cleaned {path}")
            changed = True
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
