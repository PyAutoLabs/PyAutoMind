## demo-subplot-fit-interferometer-combined
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/555
- completed: 2026-09-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/558 (merge 4aed6195)
- summary: |
    `scripts/multi_dataset/plot.py` gains an interferometer arc mirroring its imaging arc: the datacube
    reference cube (auto-simulated by `scripts/interferometer/features/datacube/simulator.py`) is loaded
    as four `Interferometer` objects with `TransformerDFT`, each channel is fitted with its own true
    `tracer.json`, and `aplt.subplot_fit_interferometer_combined(fit_list=fit_list)` is called on those
    four genuinely distinct fits (own visibilities, noise realisation, source intensity and centre) —
    never `[fit, fit]`. Opening docstring, `__Contents__` and `__Visualizer__` extended (the `Visualizer`
    writes `fit_combined.png` for a multi-dataset interferometer fit). `multi_dataset/plot.py` added to
    `smoke_tests.txt` so the witness is CI-enforced; `scripts/multi_dataset/README.md` line updated;
    notebook and catalogue regenerated. Witness held: local smoke-profile run exit 0 (~12 s, datacube
    auto-simulation ~6 s), a full-visualization probe confirmed the call with 4 fits, CI smoke 3.12 +
    3.13 green on b9894c7c.
- premise-corrections: |
    The prompt named `scripts/multi/`; the folder is `scripts/multi_dataset/`. It also proposed
    `multi_dataset/features/imaging_and_interferometer/` as the "real multi-interferometer fit context",
    but that example fits ONE interferometer plus ONE imaging dataset and cannot supply a `fit_list` of
    interferometer fits. The datacube feature (`scripts/interferometer/features/datacube/`) is the
    workspace's real list-of-`Interferometer` context, and the library docstring names datacube channels
    as the function's primary case (`autolens/interferometer/model/plotter.py` calls it to write
    `fit_combined.png`). Reaching across topics for the dataset is explained in one sentence of prose.
- trap: |
    `PyAutoMind/scripts/ledger_merge.py classify` hangs (>120 s) when run with uncommitted changes in
    the tree; commit first, then classify — it returns instantly. Also the `dataset.fits` the imaging
    arc of `plot.py` writes to the workspace root is untracked and not gitignored: delete it before
    `git add -A`.
- session: |
    web-github (session clone /home/user/autolens_workspace, no task worktree, no `gh`; GitHub via
    the MCP surface). Fable planned and reviewed, Opus authored the prose; one unverifiable claim
    (a physical reason for the missing `_log10` variant) trimmed at review. The five PyAuto library
    mains were cloned read-only and pip-installed into the session venv to run the smoke profile
    locally; the Heart CLI was absent so the smoke run stood as the readiness gate. Shadow row
    (tier notify, stage 1, merged-unchanged) appended at close-out.

## Original prompt

# Demo `subplot_fit_interferometer_combined` in a multi-dataset example

Type: docs
Target: workspaces
Repos:
- autolens_workspace
Themes:
- visualization
Difficulty: medium
Autonomy: safe
Priority: normal
Status: active
Consequence: notify
Witness: `aplt.subplot_fit_interferometer_combined` is called from a multi-dataset interferometer example under `autolens_workspace/scripts/multi/` with a `fit_list` of genuinely distinct fits (not `[fit, fit]`), and that script runs to completion under the smoke profile.
Review-minutes: 0
Unattended: ready
Filed: 2026-09-09
Issued: 2026-09-17

Split from `plot_coverage_followups.md` on 2026-09-09 (item 1 of 4). That file
was a container of four independent follow-ups and said so — "do **not**
bulk-issue them as a series" — so it has been split into one prompt per item and
archived.

## Why

PyAutoLens#668 **exported** `aplt.subplot_fit_interferometer_combined` for API
symmetry — imaging's `subplot_fit_combined` was exported, the interferometer
equivalent was not — but nothing demonstrates it.

## What

It takes a `fit_list`, so its home is a multi-dataset interferometer example,
not the single-fit `scripts/interferometer/plot.py`. Passing `[fit, fit]` there
would teach a wrong idiom (the same reasoning that kept the `*_x1_plane` pair
out of the originating task).

Candidate home: `autolens_workspace/scripts/multi/` — `multi/plot.py` already
demonstrates the imaging combined subplots (`subplot_fit_combined`,
`subplot_fit_combined_log10`), and `multi/features/imaging_and_interferometer/`
provides a real multi-interferometer fit context.

- @autolens_workspace
