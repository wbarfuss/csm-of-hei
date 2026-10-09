# Building and maintaining these lecture notes

This file covers rendering, publishing, and the git conventions of this repository. Readers who only want to work through the material do not need any of it; the [README](README.md) is the place to start.

## Python environment

The environment used to write and run the notebooks is defined in `PyEnv-IntegratedWriting.yml`:

```bash
conda env create -f PyEnv-IntegratedWriting.yml
conda activate iw
```

## Rendering the lecture notes

Assuming you have installed the [Quarto CLI](https://quarto.org/docs/get-started/) and cloned or copied the [repository](https://github.com/wbarfuss/csm-of-hei) to your local machine, you can render these lecture notes by running the following command in the terminal:

```bash
quarto render .
```

The output (web version and book PDF) is written to `__output/`, as set in `_quarto.yml`. Notebooks are not re-executed; Quarto uses the outputs stored in them.

### Slides and standalone PDFs per lecture

Each lecture notebook ends with build commands, stored as markdown cells so they do not run by accident:

- `jupyter nbconvert ... --to slides` writes the slides to `__slides/`.
- `quarto render ... --to pdf --profile standalone` writes a standalone PDF to `__scripts/`.

To run one, switch the cell to code, run it, and switch it back to markdown. Do not commit it as a code cell: its output (the full build log) would be stored in the notebook.

## README

`README.md` is generated from `index.ipynb`, which is also the preface of the book (required in the Quarto Book project type). Edit `index.ipynb`, then run:

```bash
quarto convert index.ipynb        # convert into Quarto markdown
tail -n +10 index.qmd > README.md  # remove some metadata
rm index.qmd                      # remove the intermediate file
```

## Publishing to GitHub Pages

Publishing is automatic. Every push to `main` runs the workflow `.github/workflows/publish.yml` on GitHub, which:

1. runs all pre-commit hooks as a check (job `checks`);
2. renders the book, web version and PDF, with `quarto render .`, using the outputs stored in the notebooks; notebooks are not executed (job `build`);
3. deploys the result to <https://wbarfuss.github.io/csm-of-hei/> (job `deploy`).

The workflow can also be started by hand under *Actions → Publish → Run workflow* on GitHub. The repository setting *Settings → Pages → Source* must be *GitHub Actions*.

Do not use `quarto publish gh-pages`. It commits every rendered site, including the book PDF, to a `gh-pages` branch, which made the repository grow by about 60 MB per publish.

## Git conventions: pre-commit hooks

This repository uses [pre-commit](https://pre-commit.com) to check every commit. To install the hooks once per clone, run:

```bash
pre-commit install --allow-missing-config
```

The hooks then run on every `git commit`. To run them on all files at once:

```bash
pre-commit run --all-files
```

If a hook modifies a file, the commit stops; stage the changes with `git add` and commit again. If a hook rejects a file, the commit stops and the file has to be unstaged or the commit overridden (see below).

| Hook | What it does |
|---|---|
| `nb-clean` | Removes notebook metadata, empty cells, and execution counts; keeps outputs and the `slideshow` and `tags` cell metadata. |
| `strip-png-metadata` | Runs `tools/strip_nb_png_metadata.py`. Removes the Matplotlib version stored inside each figure and the random ids of interactive widgets. Without it, re-running a notebook under a new Matplotlib version changes every figure in git, even when the pixels are identical. |
| `shrink-drawio-png` | Runs `tools/shrink_drawio_png.py`. Re-exports draw.io PNGs (`*.dio.png`, `*.drawio.png`) wider than 2000 px at 2000 px, using the draw.io desktop app. The diagram stays embedded and editable; the whitespace around it is kept. 2000 px is enough for a projector, high-resolution screens, and the PDF. Multi-page diagrams are skipped. If draw.io is not installed at `/Applications/draw.io.app`, set the `DRAWIO` environment variable to its executable. |
| `forbid-generated` | Rejects PDFs, draw.io backups (`.bkp`), and anything in `__output/`, `__scripts/`, `__slides/`. These are build outputs. |
| `check-added-large-files` | Rejects new files larger than 3 MB. Files already tracked are not checked when they change. |
| `check-merge-conflict` | Rejects files that still contain merge-conflict markers. |

### Why generated and large files are blocked

A file committed once stays in the git history permanently, even after it is deleted. Earlier versions of this repository committed lecture PDFs and draw.io backups before `.gitignore` covered them; they still take up space in every clone. `.gitignore` alone does not prevent this: it covers only the paths it lists, does not apply to files that are already tracked, and is bypassed by `git add -f`. For example, a failed standalone-PDF build leaves `XX_.pdf` in the repository root, which `.gitignore` does not cover.

### Overriding a hook

If a large file is intended, skip the size check for one commit:

```bash
SKIP=check-added-large-files git commit -m "..."
```

The same works for `forbid-generated`. If a PDF should be tracked permanently (for example a vector figure), add an `exclude:` pattern for it to the `forbid-generated` hook in `.pre-commit-config.yaml` instead of skipping the hook each time.

### Screenshots pasted into draw.io diagrams

A screenshot pasted into draw.io is stored at its full resolution inside the diagram, often 3–4 times larger than it is drawn. The `shrink-drawio-png` hook does not change this. After pasting large images, run:

```bash
python3 tools/shrink_drawio_embedded_images.py --dry-run images/x.dio.png  # show planned changes
python3 tools/shrink_drawio_embedded_images.py images/x.dio.png
```

It reduces each embedded image to twice the size at which it is drawn (or more, if the PNG export uses a larger scale), and re-renders the PNG at its current width. All pages and the diagram structure are kept. It requires ImageMagick (`magick`) and draw.io.

### Checking notebooks manually

To check a notebook with the same `nb-clean` settings outside of a commit:

```bash
nb-clean check --remove-all-notebook-metadata --remove-empty-cells --preserve-cell-outputs --preserve-cell-metadata slideshow tags -- index.ipynb
```

Replace `check` with `clean` to apply the changes.

### Editors

Save notebooks with JupyterLab or VS Code. Editors built on the nteract `runtimed` runtime fail on the `null` execution counts that `nb-clean` writes and replace the affected outputs with an error message.
