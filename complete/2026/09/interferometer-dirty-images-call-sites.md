## interferometer-dirty-images-call-sites
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/556
- completed: 2026-09-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/557
- summary: |
    Switched every `aplt.subplot_fit_dirty_images(` call in autolens_workspace's
    interferometer examples to the autolens-bound
    `aplt.subplot_fit_interferometer_dirty_images(` (PyAutoLens#670), which
    derives the tracer's critical curves from the fit and overlays them on the
    Dirty Model Image panel. 10 code call sites in 9 scripts (interferometer
    plot/fit/modeling, five features/*/fit.py, the multi_dataset
    imaging_and_interferometer modeling example), arguments untouched; the four
    docstrings that name the function updated with one sentence about the
    overlay; the 9 notebook mirrors regenerated with the PyAutoHands generator.
    Merged unchanged at e794ffd (head 26d73f1f, one commit).
- findings: |
    - The prompt's count was stale: main had 10 call sites, not 11, and five
      `features/*/fit.py` (shapelets sits under `features/advanced/`), not four;
      the multi-dataset script lives under `scripts/multi_dataset/`, not
      `scripts/multi/`. Re-verifying against main before editing, as the prompt
      asked, is what caught it.
    - `scripts/interferometer/plot.py` also mentions `subplot_fit_dirty_images`
      as the `config/visualize/plots.yaml` key under `fit_interferometer:`. That
      is a config key, not the function, and the key is unchanged, so that line
      stays and a bare grep for the old name under `scripts/` still returns it.
    - The released autolens 2026.9.15.1 already exports the new name, so no
      library PR and no pending-release gate; the PR carried `pending-release`
      by convention only.
    - Witness basis: a spy on `_compute_critical_curve_lines` during the new
      plotter's render on the simulated `simple` fit returned one curve
      (261 points) and the PNG shows it on the Dirty Model Image panel only;
      the autogalaxy-bound function has no `image_plane_lines` argument, so it
      never drew one.
- traps: |
    - Web session, `--auto` at effective level supervised: implementation
      delegated to an Opus subagent, review read by a different model
      (Fable). The review faculty script reports "no reviewable diff" on
      uncommitted work; the working-tree diff had to be read directly.
    - `scripts/interferometer/fit.py` needs the optional `nufftax` package to
      run locally (the default JAX-native NUFFT); install it before a local
      smoke run or the simulator subprocess fails on import.
    - Two parallel Bash calls that `cd` into different clones crossed working
      directories in this session; use `git -C` and absolute paths for
      multi-repo close-out steps.
- worktree: n/a — web-github session clones; local branch cleanup outstanding on a laptop checkout (nothing to delete on the remote)

## Original prompt

# Switch 11 workspace call sites to `subplot_fit_interferometer_dirty_images`

Type: docs
Target: workspaces
Repos:
- autolens_workspace
Themes:
- visualization
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: active
Issued: 2026-09-17
Consequence: notify
Witness: After the sweep a grep for `subplot_fit_dirty_images` under `autolens_workspace/scripts/` returns nothing, all 11 named sites call `subplot_fit_interferometer_dirty_images`, and each regenerated figure carries the auto-derived critical-curve overlay the autogalaxy-bound version did not draw. The call-site count and the `fit=fit`-only claim are re-verified against current main first.
Review-minutes: 0
Unattended: ready
Filed: 2026-09-09

Split from `plot_coverage_followups.md` on 2026-09-09 (the remaining sub-item of
item 4 of 4). That file was a container of four independent follow-ups and said
so — "do **not** bulk-issue them as a series" — so it has been split into one
prompt per item and archived. **Item 4's own finding already shipped**
(2026-07-30, PyAutoLens#670, `339867e2c`); this prompt carries only the
workspace sweep it deferred.

## Why

PyAutoLens#670 added `subplot_fit_interferometer_dirty_images` — autolens's own
version, which with `image_plane_lines=None` auto-derives the tracer's critical
curves from the fit (`_compute_critical_curve_lines`) and overlays them on the
dirty model image. `subplot_fit_dirty_images` was deliberately **left bound to
autogalaxy's** version, because the signatures diverge
(`residuals_symmetric_cmap` vs `image_plane_lines`) and rebinding would be a
behaviour change rather than an additive export.

## What

`autolens_workspace` still calls the autogalaxy-bound `aplt.subplot_fit_dirty_images`
at 11 sites:

- `scripts/interferometer/{fit,modeling,plot}.py`
- four `scripts/interferometer/features/*/fit.py`
- `scripts/multi/features/imaging_and_interferometer/modeling.py`

All pass `fit=fit` only (none pass `residuals_symmetric_cmap`), so all 11 can be
switched to the new name and would gain critical-curve overlays for free.

Deferred from the originating task because it is a **visual change across 11
lens examples** and deserves its own review pass — which is why this is
`supervised`: the figures change, and a human should look at them.

Re-verify the call-site count and the "all pass `fit=fit` only" claim against
current `main` before editing; the finding was recorded 2026-07-30.

- @autolens_workspace
