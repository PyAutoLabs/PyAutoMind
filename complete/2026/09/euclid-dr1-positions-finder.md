Model-guided multiple-image finder for euclid DR1 (phase 2/3 of the positions work), plus the tooling to roll it out: the production positions writer (SNR >= 3 peaks, 0.7" de-dup, the #103 gate, pair floor) lives in a shared pure-numpy module used by `segmentation.py`, `util.py` and the gate; `scripts/tools/rewrite_positions.py` and `segmentation.write_positions` overwrite `positions.json` with a `positions_segmentation_v1.json` backup. The SIE solver loop is kept as a diagnostic only; flux-ratio and NIR-colour rules failed on the sample and were not shipped.

Merged 2026-09-25 (human `/prm`):
- PyAutoLabs/euclid_strong_lens_modeling_pipeline#106 — merged as 94f9244 (stacked on #104, main merged in at 64a173c). pytest 139 PASS (not slow; 9 new rewrite_positions tests) at 53cc0d3; 150/150 regression identical to the human-approved old-vs-new comparison (100 easy + 50 penalty-locked lenses).

Overrides (recorded on #106, #105 and in active.md):
- Heart RED override — live user 2026-09-25 "Override, open the PR" (push + open PR; merge by human /prm). RED reasons: release validation FAILED (stage integrate); workspace validation not passing (4 failed, cloud#35579888156); manifest drift (7 mismatches vs repos.yaml).
- Red-CI merge override — human answered "Override: merge, file bug" in /prm. The only red leg (unit / smoke 3.12 + 3.13) was `tests/test_compute_latent_variable.py::test_latent_euclid_variables_traces_under_jax_jit`, also red on main since a89a468 (#104 merge; stack drift, not this PR). Bug draft filed: `draft/bug/euclid/latent_total_source_flux_jax_vs_numpy_regression.md`.

**Rollout NOT done — in-progress data operation, not code.** The human-approved rollout overwrites `positions.json` for every DR1 lens (backup `positions_segmentation_v1.json`). At close-out RAL array 350731 is rewriting the first 250 dr1_sep1_rest tiles (priority pass). Still to come: the full dr1_sep1_rest + dr1_sep1_top1000 CPU array pass and the rsync of rest positions back to the local euclid_dr1 clone, driven from the main session. Do not treat DR1 positions as rewritten until that lands.

Follow-ups: phase 3 `draft/research/euclid/euclid_dr1_positions_gate_remodel_run.md` (run the gate over DR1 and submit the remodel set) is unblocked; it should run on the rewritten positions.

## Original prompt

# euclid_dr1: model-guided multiple-image finder (compute, fit, solve, reconcile loop)

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
Difficulty: hard
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-24
Issued: 2026-09-24
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/105
Related: euclid-dr1-positions-gate (#103, PR #104) — phase 1; this phase refactors the gate's numpy tracer and quick fit into a shared module, so it stacks on `feature/euclid-dr1-positions-gate` until #104 merges
Witness: on the 10-lens calibration sample (euclid_dr1 `inspect/positions_sample/`, human-approved 2026-09-24) the new finder returns the 5 good tiles' positions unchanged or as a traceable superset (quick-fit s_min <= 0.1"), and on the 5 locked tiles removes the nucleus position (Tile102008208, Tile102014701), the neighbour (Tile102014701, Tile102022005), adds a model-predicted counter-image or sends the tile to review (Tile102012741), and breaks Tile102023528 (probably not a lens) to no positions or a review flag; unit tests cover each reconcile rule; then the census witness: over the 14,032-tile census the fraction failing the gate's quick-fit trace drops from 16.6% (2,325 tiles) and no SNR < 2 counter-image is emitted without a model prediction behind it.

Phase 2 of the positions work (phase 1: #103 positions gate, PR #104). Root cause found 2026-09-24: 59-80% of the offending near-centre "multiple images" have source-flux SNR < 3. `preprocess/segmentation.py:151 compute_positions` and `util.py:55 _compute_positions_from_source_flux` (identical copies) take SNR > 3 local maxima of segmentation/source_flux.fits, then walk the counter-image SNR threshold down in 0.1 steps all the way to 0, with an "opposite side" test that flips sign per axis about the cutout origin (0,0) rather than the lens light centre. No lens model is consulted; the phase 1 gate consults one but only ever removes positions. Research: euclid_dr1 `inspect/positions_census/research/` (A_central_radius.md "Separate finding", B_final_method.md, SYNTHESIS.md).

## Approved plan (human, 2026-09-24)

Method: alternate between the flux map and a lens model until the position set is stable.

1. **Compute.** Local maxima of source_flux with SNR >= 2 (floor), excluding a 0.15" disc around the brightest lens-flux pixel (the light centre, same definition as the gate). Peaks with SNR in [1, 2) are kept aside as *weak* candidates.
2. **Fit.** The gate's fixed-centre SIE + external shear quick fit (positions_gate.py `source_positions`, `_chi2_fit`, `_sep_fit`) to the current set gives a mass model and a source position beta (mean of the traced positions).
3. **Solve.** Forward-solve beta through the model on a fine image-plane grid over the mask (pure numpy: minima of |theta - alpha(theta) - beta|, refined per minimum, residual < 0.02", magnification from the numeric Jacobian). A numpy stand-in for al.PointSolver so the finder stays seconds per tile with no PyAutoLens import in preprocess.
4. **Reconcile.** Match predicted images to observed peaks within r_match (~0.3"):
   - predicted image with a matching peak: keep;
   - predicted image with only a *weak* peak nearby: add it (the SNR walk-down now happens only where the model says a counter-image should be);
   - observed position with no predicted image near it: drop (nucleus, companion, neighbour, second source);
   - bright predicted image (|mu| large) over empty sky (SNR < 1): counts against the set.
5. **Iterate** 2-4 until the set is stable, cap 5 rounds. Non-convergence, an empty set after drops, or a set that traces only through an implausible model (gate's J cost) sends the tile to review with no positions or a large threshold. Threshold as the gate: T = min(max(2 s_final, 0.3"), 0.5").

Code: new pure-numpy module (e.g. `positions_finder.py` at the package root, or `preprocess/` if util's autolens import is too heavy) holding the tracer, quick fit, solver and reconcile loop; `segmentation.py`, `util.py` and `scripts/tools/positions_gate.py` all import it. The gate becomes "run the finder with the existing positions.json as the seed set", so existing and future tiles share one logic. Keep `positions_meta.json` as the output contract that `load_vis_dataset` already reads.

Tests (tests/): each reconcile rule on a synthetic SIE (add weak counter-image, drop unplaceable position, empty-sky penalty), the solver against `source_positions` round trips on a synthetic quad and double, convergence cap, and parity between the segmentation and util writers.

Calibration sample (human-approved 2026-09-24): euclid_dr1 `inspect/positions_sample/` (README.md, contact_sheet_good.png, contact_sheet_locked.png, locked_screening.md). Good five from Success_100 (Tile102022524 quad, Tile102164113 quad, Tile102034991 triple, Tile102015991 double, Tile102022507 double; May prelim delivery). Locked five: Tile102008208 (nucleus + one-sided arc), Tile102014701 (nucleus + neighbour), Tile102023528 (one-sided arc, counter-image missed; human: may not be a lens at all, should break to no positions or a huge threshold, a stress test), Tile102012741 (two peaks on one arc, no counter-image), Tile102022005 (unrelated neighbour). Three multi-galaxy lenses were removed as out of scope (removed_mgl/); runner-ups in locked_screening.md. The screening's MGL pre-filter (red second peak >= 0.25 of the lens inside the image radius) is a phase 3 candidate for sizing the out-of-scope fraction.

Sequencing: PR #104 open and green, unmerged (human merge via /prm). Branch `feature/euclid-dr1-positions-finder` off `feature/euclid-dr1-positions-gate`, own worktree; retarget to main after #104 merges. Issue title `feat: model-guided multiple-image finder (compute/solve/reconcile loop)`.
