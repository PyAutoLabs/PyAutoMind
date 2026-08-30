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
