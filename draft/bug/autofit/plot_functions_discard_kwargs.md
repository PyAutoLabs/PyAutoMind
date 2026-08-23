# `autofit.plot` functions accept `**kwargs` and silently discard them

Type: bug
Target: autofit
Repos:
- PyAutoFit
- autofit_workspace
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-07 (backfilled from git)

Filed 2026-08-07, found while fixing `docs/api/plot.rst`
(complete/2026/08/pyautofit_plot_rst_dead_plotters.md). Deliberately left out of
that PR: it is a library/workspace defect, not a docs one, and the docs change
was docs-only by design.

## The defect

All five public `autofit.plot` functions take `**kwargs` in their signature and
**never reference it in the body**. Verified mechanically — `kwargs` appears in
`autofit/non_linear/plot/{samples_plotters,nest_plotters,mle_plotters}.py` only
on the `def` lines:

- `corner_cornerpy(samples, path=None, filename="corner", format="show", **kwargs)`
- `corner_anesthetic(samples, path=None, filename="corner_anesthetic", format="show", **kwargs)`
- `subplot_parameters(...)`, `log_likelihood_vs_iteration(...)`,
  `figure_of_merit_vs_iteration(...)` — same shape

`corner_cornerpy` calls the underlying library with a **fixed** argument set:

```python
corner.corner(
    data=data,
    weight_list=samples.weight_list,
    labels=samples.model.parameter_labels_with_superscripts_latex,
    range=_corner_range_from(data),
)
```

So a caller's customization is accepted without error and has no effect. The
failure mode is the bad one: **silent**. No `TypeError`, no warning, just a plot
that ignores what you asked for.

## Why it matters — the workspace teaches the broken idiom

`autofit_workspace/scripts/plot/*.py` passes long kwarg lists as though they
were forwarded, and says so in prose: *"In all the examples below, we use the
`kwargs` of this function to pass in any of the input parameters that are
described in the API docs."* That claim is false today.

Silently-discarded kwargs at those call sites (counted 2026-08-07):

| script | discarded kwargs |
|---|---|
| `scripts/plot/emcee_plotter.py` | 30 |
| `scripts/plot/dynesty_plotter.py` | 19 |
| `scripts/plot/zeus_plotter.py` | 16 |
| `scripts/plot/nautilus_plotter.py` | 11 |
| **total** | **76** |

A user following the plot tutorials sets `bins`, `smooth`, `show_titles`,
`truths`, … and sees none of them applied. The tutorials are the documentation
for this API, so this is the primary way the behaviour is encountered.

## The decision to make (why supervised, not auto)

Two coherent fixes; picking one is a judgement about the intended surface:

1. **Forward them** — pass `**kwargs` through to `corner.corner` /
   `anesthetic` / matplotlib. Matches what the workspace already claims and
   makes the existing tutorials correct as written. Watch the collisions:
   `corner_cornerpy` already sets `data`, `weight_list`, `labels` and `range`
   explicitly, and `range` in particular is computed by `_corner_range_from`
   to dodge corner's "no dynamic range" crash on degenerate columns — a
   user-supplied `range` must not silently reintroduce that. Decide precedence
   (caller wins / library wins) and state it.
2. **Drop `**kwargs`** from the signatures and correct the workspace scripts +
   prose. Honest, and callers get a loud `TypeError` instead of silence — but
   it removes customization the tutorials imply exists, so it is the bigger
   user-facing change.

Either way the workspace scripts and their prose need updating in the same
wave, so this is a paired PyAutoFit + autofit_workspace task.

## Verify

- A call passing a non-default kwarg (e.g. `bins=5`) visibly changes the
  output figure (fix 1), or raises `TypeError` (fix 2).
- The four `scripts/plot/*.py` tutorials and their surrounding prose agree with
  whichever behaviour was chosen — no script still passes an argument that does
  nothing.
- Degenerate-column input (every sample equal, e.g. a `PYAUTO_TEST_MODE=1` run)
  still does not crash `corner`, i.e. the `_corner_range_from` guard survives.

<!-- Grounding: verified against PyAutoFit main at 75bbc76a1 by reading the
     three plot modules and counting kwargs at the workspace call sites. The
     docs page that surfaced it is docs/api/plot.rst, rewritten in PyAutoFit#1455. -->
