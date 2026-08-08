# fix-workspace-start-here-colab-links

- shipped: 2026-07-24
- commit: autolens_workspace `897465a6` — "docs: link Colab introduction to workspace start"
- repos:
  - autolens_workspace (verified)
  - autogalaxy_workspace / PyAutoLens / PyAutoGalaxy / euclid_strong_lens_modeling_pipeline (in the prompt's scope, NOT verified here — see below)

## Summary

The "try PyAutoLens in a web browser without installing it" Colab links pointed
at the topic-specific `notebooks/imaging/start_here.ipynb` rather than the
workspace's own root `start_here.ipynb`, dropping new users into the imaging
tutorial instead of the overall introduction.

Verified on `autolens_workspace` `main`, `README.md`:

```
- [PyAutoLens on Google Colab](https://colab.research.google.com/github/PyAutoLabs/autolens_workspace/blob/<tag>/start_here.ipynb): try PyAutoLens in a web browser without installing it.
```

and the "New Users" section link below it, both now resolving to the root
notebook. The tag component is kept current by the release job's
"bump Colab URL tag refs" step.

The topic-specific links in `start_here.py` (`imaging/start_here.ipynb`,
`interferometer/`, `point_source/`, `group/`, `cluster/`) are **correctly left
pointing at their own notebooks** — the prompt explicitly asked to preserve
links that describe the imaging-specific tutorial, and those are a deliberate
directory listing.

## Scope caveat — do not read this as fully verified

The prompt named five repos. Only `autolens_workspace` was checked when this
record was reconstructed. The PyAutoGalaxy side was called out in the original
request ("this is prob required for PyAutoGalaxy too") and has **not** been
confirmed here. If a stale introductory Colab link turns up in
`autogalaxy_workspace`, the PyAutoLens/PyAutoGalaxy docs, or
`euclid_strong_lens_modeling_pipeline`, treat it as unfinished scope of this
task rather than a new bug.

## Bookkeeping note

Reconstructed 2026-08-08 during the orphaned-prompt triage
(`draft/maintenance/pyautomind/active_prompt_orphan_triage.md`). Dated from the
fixing commit; no ship-time record exists.

## Original prompt

# Fix workspace-level `start_here.py` Colab links

Type: docs
Target: workspaces
Repos:
- PyAutoLens
- PyAutoGalaxy
- autolens_workspace
- autogalaxy_workspace
- euclid_strong_lens_modeling_pipeline
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Correct Google Colab URLs described as the introductory PyAutoLens or
PyAutoGalaxy Jupyter Notebook so that they open each workspace's root
`start_here.ipynb`, generated from the overall workspace `start_here.py`, not
the topic-specific `notebooks/imaging/start_here.ipynb`. Scan other `README.md`
and documentation files for the same incorrect target and update matching
introductory links, while preserving links that explicitly describe the
imaging-specific tutorial.

Verify that both root `start_here.py` sources use the correct product-specific
`setup_colab` call and that the corresponding generated `start_here.ipynb`
notebooks contain the same setup before routing users to them.

## Original request

> The URL to this should not be imaging/start_here.py but the overall workspace start_here.py, The introduction Jupyter Notebook on Google Colab: try PyAutoLens in a web browser (without installation)., update it and scan other README.md and docs for the same issue

> make sure the examples we are routing to has the right setup_colab

> this is prob requied for PyautoGalaxy too
