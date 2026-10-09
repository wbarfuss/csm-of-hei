# CLAUDE.md

Course materials: a Quarto book of Jupyter notebooks, published at
https://wbarfuss.github.io/csm-of-hei/. Read CONTRIBUTING.md first; it covers
rendering, publishing, the Python environment, and the pre-commit hooks.

## Rules that are not obvious from the files

- `README.md` is generated from `index.ipynb` (commands in CONTRIBUTING.md).
  Never edit `README.md` directly.
- The notebooks are taught live in JupyterLab with jupyterlab-slideshow. Keep the
  cell metadata `slideshow` and `tags`. Quarto attributes such as `{width=...}`
  have no effect there, so layout has to be fixed in the content itself.
- The build cells at the end of each lecture notebook are markdown on purpose.
  Never commit them as code cells or with output.
- Whitespace around draw.io figures is intended (it centers them in slides).
  Do not crop it.
- Never commit PDFs, `.bkp` files, or anything in `__output/`, `__scripts/`,
  `__slides/`. Never run `quarto publish gh-pages`; publishing runs through
  GitHub Actions on every push to `main`.
- When editing `.ipynb` files with a script, write the JSON with `indent=1`,
  `ensure_ascii=False` and a trailing newline (the format nb-clean produces),
  then run `pre-commit run --files <notebook>`.
- Uncommitted changes in a notebook are not necessarily intended edits.
  Re-running cells, running build cells, and saving with some editors also
  change notebooks. Compare against `HEAD` and ask before committing them.
