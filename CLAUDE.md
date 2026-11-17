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
- Slides and lecture notes (HTML/PDF) render from the same cells. Slide type
  `skip` shows a cell only in the lecture notes. Content between the fence cells
  `::: {.content-hidden unless-profile="interactive"}` and `:::` (both `skip`)
  shows only in the slides. Prefer one version that works in both (e.g. a
  different heading) over two separate versions.

## Terminology in the text

- "lecture notes" for the written material ("these lecture notes", "the first part of these lecture notes"). Not "book", although Quarto builds it as one.
- "course" for the teaching event: lectures, workshops, exam ("toward the end of the course").

## Writing lecture content

- Learning goals go in a `::: {.callout-tip}` box ("After this lecture, students
  will be able to:"). "Learning goals revisited" is prose in the past tense
  ("We defined ...", "We analyzed ..."), not nested bullets.
- Bibliographical and historical remarks that are general, or that shaped the
  lecture as a whole, go in a footnote to the opening statement, not in a
  section at the end. A source for a specific definition, result, or figure is
  cited in the text where it is used.
- Footnote labels must be unique across all notebooks, exercises included. The
  PDF merges every chapter into one document, and a reused label makes every
  reference show the last definition. Prefix labels with the chapter topic
  (e.g. `[^tipping-tau]`, `[^resilience-sources]`).
- Open each major transition with the question it answers ("Can we do better
  than simulating forward?", "How does the stability analysis extend to
  multi-dimensional systems?").
- Never reuse a symbol for two meanings in one lecture. General matrix entries
  are $A_{ij}$, so that $a, b, \dots$ stay free for model parameters. When
  renaming a symbol, also update the exercise notebook (`XX.YYex`).
- When a new symbol relates to an earlier one, state the relation where it is
  used (e.g. "$a = 1-r < 0$").
- Show derivations step by step; do not write "solve" or "yields" over a
  skipped step. State the purpose of a computation before the computation
  (e.g. "$|\lambda|$ decides whether oscillations shrink or grow").
- One idea per slide: function definitions and long derivations start a new
  subslide; split derivations across slides rather than crowding one.
- Refer to DeepDives as "the DeepDives", not "below": slides skip them.
- For a model with a common textbook name in another form, use the descriptive
  name in the text and give the textbook form in a footnote.
- A lecture has 90 minutes. When revising, estimate the time per section. Cut
  content that repeats an idea in a different framing (e.g. a section on
  oscillations from delays right after the cases for $|a|$). Optional material
  goes into a DeepDive, not onto the slides.
- Code cells stay visible in the slides: they are executed live in class. Never
  set a code cell to `skip` or `notes` to save space. A code cell copied from an
  earlier lecture is not walked through line by line, so it may overflow the
  slide height.
- Place an abstract claim where students can already see it concretely (e.g.
  "changing the feedback strength beats changing the stock" right after the
  experiment with halved and doubled rates and the closed-form solution).
- Show a model's equations on the slide. A check question ("Is this a linear
  system?") can lead into the next section.

