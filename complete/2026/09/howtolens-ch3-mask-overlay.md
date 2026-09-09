Moved the two mask-overlay figures in HowToLens chapter 3 tutorial 3 below their
`apply_mask`, so the figure the prose introduces right after building an annular mask
actually draws the mask. HowToLens#79 MERGED 2026-09-09 (`5b51731`, head `eb8b26c`),
closing issue #78. Branch `feature/howtolens-ch3-mask-overlay`.

- issue: https://github.com/PyAutoLabs/HowToLens/issues/78
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/79
- completed: 2026-09-09

## The gap

`aplt.plot_array` derives its overlay one layer down (`autoarray/plot/array.py`,
`if mask is None: mask = auto_mask_edge(array)`), and `auto_mask_edge` returns `None`
for a fully-unmasked array. Two `plot_array` calls sat *above* their
`dataset.apply_mask(mask=mask)`, so each rendered a plain image directly under prose
announcing a mask. Not a crash — the tutorial ran green, which is why it survived from
before the 2026-08 `chapter_4_pixelizations` → `chapter_3_pixelizations` rename.

Confirmed on a live stack (autolens 2026.9.8.1) with the tutorial's own 0.5"/2.8"
annulus: `auto_mask_edge` goes `None` -> `(264, 2)` across `apply_mask`. The count
differs from the original report's `(156, 2)` only because that was measured under
`PYAUTO_SMALL_DATASETS`; qualitatively identical.

## What shipped

- **Site one fixed by moving `apply_mask` up, not the figure down** — the better of the
  two options, because the docstring "We now create the masked source-plane grid via the
  tracer" was itself introducing `apply_mask`, and now sits directly above the
  `lens_galaxy`/`tracer`/`source_plane_grid` block it actually describes. A
  pre-existing prose/code mismatch went with it. The mask docstring gained ", and apply
  it to the dataset"; the relocated figure got a two-line intro in the tutorial's voice.
- **Site two also lost a duplicate.** Its two `plot_array` calls were byte-identical
  figures — `dataset` was unchanged between them — so the second was both mask-less and
  redundant. Moved below `apply_mask`; the blanket docstring ("This code is doing all
  the same as above…") still read correctly and was left verbatim, with no docstring
  added so the block stays one notebook cell. The genuine raw-data figure before any
  mask exists is untouched.
- Both relocated figures retitled `"Image Data With Mask Applied"` — the canonical idiom
  (`autogalaxy_workspace/markdown/ellipse/fit.md`) — instead of the bare `"Data"` they
  inherited, which at site two would have left two identically-titled figures.
- 30 insertions / 15 deletions across 2 files: the script and its regenerated notebook.

## Evidence

- CI 7/7 green at merge: `smoke (3.12)`, `smoke (3.13)`, `smoke / changes`, `navigator /
  Catalogue staleness`, `navigator / Navigator paths + banner lint`, `navigator /
  Unbatched multi-start search check`, `tutorials-complete`. `mergeable_state: clean`.
- Ran locally before the PR under CI's exact smoke env (every default from
  `config/build/profile_smoke.yaml` + `MPLBACKEND=Agg`): exit 0, zero tracebacks. The
  script is not in `config/build/no_run.yaml`, so that is what CI executes.
- Second PyAutoHands regeneration on the swept tree a no-op — `git status` byte-identical
  between runs, md5sums of the notebook and both catalogue files unchanged.
- Notebook cell order verified by parsing the `.ipynb`: `apply_mask` (cell 9) -> new
  markdown intro (10) -> retitled `plot_array` (11) -> tracer prose (12) -> tracer code
  (13). No cell-id or execution-count churn.
- NOT verified: the rendered PNG was never eyeballed. What is verified is that
  `auto_mask_edge` returns a real edge array at the point each relocated call now runs.

## Traps and findings worth keeping

- **The catalogue regenerating byte-identical is correct, not a missed step.**
  `llms-full.txt` / `workspace_index.json` record each script's path, header summary and
  `__Contents__` section names — none of which a figure move changes. The generator
  rewrites both files (mtimes move, "Catalogue written … (50 scripts)") while the diff
  stays empty, so `navigator_check.yml` has nothing to flag.
- **`generate.py` needs `ipynb-py-convert` on PATH and nothing else.** It imports only
  stdlib plus `build_util`/`generate_autofit`, so notebook regeneration works in a cloud
  session with **no PyAuto library installed**. Two older records are now stale on this:
  `notebook-setup-notebook-regen-drift`'s trap ("ipynb-py-convert cannot pip-install on
  modern setuptools; vendor it into site-packages + a CLI shim") — `python3 -m pip
  install ipynb-py-convert` succeeded in seconds under Python 3.12 — and
  `howto-setup-notebook-audit`'s "PyAutoHands is not available in a cloud session", which
  clones anonymously and runs fine.
- **`autolens` does pip-install in a cloud session**, in under 170s, which makes the real
  smoke gate runnable locally rather than only on CI. Worth attempting on any
  workspace/tutorial task before declaring the gate CI-only.
- The generator **stages** the notebook it rewrites (`git add -f`), so a regenerated file
  is already in the index — check `git status` rather than assuming the tree is unstaged.
- HowToLens is a `category: howto` repo, not a library, so the `pending-release` label on
  #79 carries no Mind-side `pending-release:` obligation; it is the release build's own
  tracking and `/prm` never clears it.

## Bundle context

Sole implementation member of the auto `notebooks` bundle (2026-09-09, three independent
members). The other two closed without PRs, both because their premises had expired:

- `notebook_setup_notebook_drift_siblings` — already shipped 2026-08-07; retired the same
  day as this task to `complete/2026/08/notebook-setup-notebook-drift-siblings.md`.
- `multi_galaxy_package` — still blocked, left in `draft/`: its one remaining leg is the
  SDSS J1011+0143 real-data swap-in and MAST answers 403 to CONNECT through the session
  proxy (re-probed 2026-09-09, matching the 2026-07-26 finding).

Two of three bundle members were unstartable as written. **Re-measure a prompt's premise
before planning it** — that is what turned three tasks into one, and it cost one
`generate.py` run per repo plus one `curl`.

## Original prompt

# HowToLens ch4 tutorial 3: mask overlay is never actually drawn

Type: docs
Target: howtolens
Repos:
- HowToLens
Themes:
- notebooks
- visualization
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-04 (backfilled from git)
Issued: 2026-09-09

Spotted 2026-08-04 while fixing the sibling HowToGalaxy tutorial under
`plot-array-stale-kwargs` (HowToGalaxy#56). **Not a crash** — the tutorial runs
green, which is exactly why it has gone unnoticed.

## The gap

`HowToLens/scripts/chapter_3_pixelizations/tutorial_3_inversions.py` (chapter renamed from chapter_4_pixelizations in the 2026-08 restructure; line refs predate it) and
`:190` both do:

```python
aplt.plot_array(array=dataset.data, title="Data")
...
dataset = dataset.apply_mask(mask=mask)
```

The plot sits *before* `apply_mask`. `aplt.plot_array` derives its mask overlay
one layer down at `autoarray/plot/array.py:128`
(`if mask is None: mask = auto_mask_edge(array)`), and `auto_mask_edge` returns
`None` for a fully-unmasked array. Measured on the installed stack:

```
unmasked   -> mask.is_all_false: True  | auto_mask_edge: None
after mask -> mask.is_all_false: False | auto_mask_edge: (156, 2)
```

So the figure the prose introduces right after creating an annular mask shows
**no mask at all**. The reader is told about the mask and then shown a plain
image.

## Fix

Move each call below its `apply_mask`, matching what HowToGalaxy ch4 t3 now
does and the canonical idiom in
`autogalaxy_workspace/markdown/ellipse/fit.md:158` ("Image Data With Mask
Applied"). Check the surrounding prose still reads correctly in both places —
this is a teaching notebook, so the sentence order matters as much as the code.

Notebooks are **generated**: edit `scripts/` only, then regenerate
`notebooks/` + the navigator catalogue via PyAutoHands. Never hand-edit `.ipynb`.
