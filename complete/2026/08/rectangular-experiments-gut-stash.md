Repaired `autolens_workspace_developer` against two PyAutoArray mesh changes it had
fallen behind, and condemned the experiments the first made unrunnable.

**PR:** PyAutoLabs/autolens_workspace_developer#132 (merged 2026-08-27, `1b8ef33`)
**Issue:** #131 · 24 files, +82/-1834

## What shipped

**Condemned (14 files)** — each imported a class deleted by the 2026-07-23 consolidation
(PyAutoArray#402/#403) and had been unrunnable since: `rect_adapt_duo/` (rotated-vs-spline
demo + simulator + bundled dataset), `searches_minimal/probe_grad_pix_adapt_image.py`, both
`jax_profiling/misc/pixelization_spline_*` scripts and their `spline_vs_linear` results.
Catalogued in `condemned.md` as `autolens_workspace_developer/rectangular-spline-rotated-experiments`;
committed deletion on a pushed repo, so `archive-ref: n/a` and the record pins pre-delete
SHA `9ae0502`. No Gut ref pushed, nothing to void.

**Renamed (9 files)** — date-checked per `git blame`, never swept by name, following the rule
`08d5d86` wrote into `jax_profiling/gradient/README.md`: pre-2026-07-23 lines are rank-CDF
(`RectangularBilinearAdapt*`), later ones kernel-CDF (`RectangularRTUAdapt*`).

## Three corrections to the filed prompt

1. **Its stated rename target did not exist.** The prompt (filed 2026-07-24) said rename to
   `RectangularAdapt{Density,Image}` — names the 2026-08-21 split (PyAutoArray#461, `f9aceea3`)
   had already deleted. Ignoring that would have produced import errors, not fixes.
2. **Following it literally would have destroyed a working comparison.**
   `plotting_alignment/kernel_cdf_alignment.py` compares a rank-CDF arm against a kernel-CDF
   arm; collapsing both onto one plain name makes it compare a mesh with itself.
3. **"Drop the now-redundant `bandwidth=`" was wrong** — it is still a live parameter on the
   RTU meshes, so dropping it would have been a silent behaviour change.

## Found while editing, beyond the prompt's scope

- The prompt's file list missed three broken files, incl. `slam_pipeline/light_dark_mge.py`,
  a live SLaM pipeline script that had not imported since 2026-07-23. Also two
  `source_science/results/*/RESULTS.md` records.
- `kernel_cdf_alignment.py` was broken *below* the class names: it imported
  `interpolator.rectangular_kernel`, a module #461 merged away, and dispatched its arms on
  `"kernel" in label` — a string test the relabel would have silently mis-routed. Both arms
  now call the single `adaptive_rectangular_transformed_grid_from` with
  `transform=interpolator.transform`, read off the mapper. Behaviour-preserving:
  `_transforms_from` ignores `mesh_pixels`/`bandwidth`/`n_knots` on the rank path.
- `searches_minimal/pix_multi_start.py` printed `bandwidth=0.1` hard-coded while running
  `PIX_BANDWIDTH`, so every non-default sweep in the #117 Stage-3 campaign logged the wrong
  bandwidth. Worth re-reading any conclusion in `pix_prodigy_findings.md` that rests on one.

## Verification

The repo is developer-tier — no `.github/workflows`, no smoke suite, and these scripts run
full fits — so verification was static and by callee probe against installed
`autoarray 2026.8.17.1`: every `al.mesh.*` symbol resolves; the rewritten import and its
kwargs bind; all five mesh constructor forms construct; `interpolator_kwargs` confirmed to
return `{"transform": "rank"}` for both Bilinear meshes; no reference to a deleted path
survives. No likelihood values changed.

## Ship gate

Merged under an **explicit human override of Heart RED** (`release validation FAILED
(stage integrate)`, score 40). The corrective-PR exception authorised earlier covers push and
PR-open only, so the merge was a human decision above that contract, recorded on the PR and
in `active.md`.

That RED is unrelated and still open: `f0ef8f2` regenerated 4 of the 6
`imaging/jax_likelihood/rectangular*` constants in `autolens_workspace_test` and skipped the
MGE pair (`rectangular_mge.py`, `rectangular_mge_rtu.py`); their `multi_dataset` twins were
repinned and pass in the same run. Follow-up task, not started.

## Original prompt

# autolens_workspace_developer rectangular experiments — Gut stash + rename

Type: maintenance
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
- PyAutoGut
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-07-24 (backfilled from git)
Issued: 2026-08-27

## Context (split from rectangular-mesh-consolidation, PyAutoArray#402, closed 2026-07-24)

The consolidation deleted the spline/rotated/kernel-named rectangular classes
from PyAutoArray (#403). `autolens_workspace_developer` still holds the
experiment scripts that used them; the repo was claimed by
`blackjax-smc-gradient-kernel` at wrap-up time (23 dirty files), so this
cleanup was deferred. File issued when that claim releases and the repo is
clean.

## Task

1. **Stash to PyAutoGut** (condemned-material lifecycle — durable recoverable
   refs) the spline/rotated experiments now that their library classes are
   gone:
   - `rect_adapt_duo/` (rotated-vs-spline demo `compare_meshes.py` +
     `simulator.py` + bundled `dataset/` — `RectangularRotatedAdaptImage` /
     `RectangularSplineAdaptImage`, live nowhere else);
   - `searches_minimal/probe_grad_pix_adapt_image.py` (tests the deleted
     `RectangularSplineAdapt*`);
   - `jax_profiling/misc/pixelization_spline_vs_linear.py` +
     `pixelization_spline_fit_comparison.py` + their `results/jit/imaging/spline_vs_linear*`.
2. **Rename kernel-named survivors to the plain names** (the classes still
   exist, just renamed): `searches_minimal/probe_grad_pix.py`,
   `pix_multi_start.py`, `plotting_alignment/kernel_cdf_alignment.py`
   (`RectangularKernelAdapt{Density,Image}` → `RectangularAdapt{Density,Image}`,
   drop any now-redundant `bandwidth=`/default handling).
3. **Update** `jax_profiling/gradient/README.md` rows to the consolidated
   naming (the linear-mesh staircase rows stay as history; the kernel rows are
   now just "the adaptive rectangular mesh"). See the completion record's
   bandwidth note (optimal h is config-dependent) for the README caveat.

## Constraints

- The `blackjax-smc-gradient-kernel` claim is RELEASED (worktree removed 2026-07-24;
  the parked task was shelved as superseded 2026-08-18), so this is no longer
  blocked — but verify the repo is clean before starting (23 dirty files at wrap-up).
- Developer repo (doc-light, not CI-gated like the workspaces); still verify
  renamed scripts import cleanly against merged main.
- Copy any gitignored products out before any worktree teardown.
