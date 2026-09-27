# Point-source source-plane chi-squared campaign — phase 2d: analysis-declared gradient_mode

Type: feature
Target: autofit
Repos:
- PyAutoFit
- PyAutoLens
- autolens_profiling
Themes:
- point-source
- profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Epic: point-source-cpu-speed
Lane: any
Filed: 2026-09-27
Issued: 2026-09-27
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1648
Parent-record: complete/2026/09/point-source-source-plane-p2c.md
Campaign: draft/research/autolens_profiling/point_source_source_plane_chi_squared_speed.md

Phase 2d of the campaign prompt above (retained in `draft/`). Plan approved by the human 2026-09-27;
full plan on PyAutoFit#1648.

## Context

Phase 2b (#327) and phase 2c (#331) measured the gradient of the source-plane point-source
likelihood. Computing it in forward mode (`jax.jacfwd` over the flat parameter vector) instead of
reverse mode (`jax.value_and_grad`):
- is 2–4.5× faster;
- compiles up to 8× faster (80 s → ≤ 11 s at 24 parameters);
- keeps that lead through 24 free parameters, and the lead grows with model size.

The cause is structural: this likelihood contains an inner forward-mode lensing Hessian, so reverse
mode runs reverse-over-forward through every mass profile. You chose (2026-09-27) to make the mode
an **analysis-declared default with a search override**, not an `n_params` threshold. This phase puts
that into the libraries. The default stays `"reverse"` everywhere except `AnalysisPoint`, so
nothing changes for any other analysis.

## Design

**PyAutoFit**
1. New helper module `autofit/jax/gradient.py`:
   - `GRADIENT_MODES = ("reverse", "forward")`;
   - `resolve_gradient_mode(analysis, override=None) -> str`. The override wins, otherwise
     `getattr(analysis, "gradient_mode", "reverse")`. An unknown value raises a clear `ValueError`.
   - `value_and_grad_from(func, mode) -> callable` returning `(value, grad)` with the same contract
     as `jax.value_and_grad(func)`:
     - reverse → `jax.value_and_grad(func)`;
     - forward → `jax.jacfwd(lambda v: (func(v), func(v)), has_aux=True)`, swapped to
       `(value, grad)`. This is exactly the phase-2b/2c `fwd` route, over the flat vector.
   - `grad_from(func, mode)`: the gradient-only counterpart, for `Fitness._grad`.
2. `af.Analysis`: class attribute `gradient_mode = "reverse"`, with a docstring saying when to
   declare `"forward"`: when the likelihood contains an inner forward-mode derivative and has few
   parameters. The docstring points to the phase-2c result.
3. `Fitness` (`autofit/non_linear/fitness.py`): an optional `gradient_mode=None` constructor argument.
   `_grad` (`:917`) builds through `grad_from(self.call, resolve_gradient_mode(self.analysis,
   self.gradient_mode))`. The existing `log_on_first_compile` wrapper and the pickling strip of
   `_grad` (`:833`) stay unchanged.
4. `MultiStartGradient` (`autofit/non_linear/search/mle/multi_start_gradient/search.py`): a new
   keyword `gradient_mode: Optional[str] = None`, stored and documented, with validation at
   construction.
   - The mode is resolved against the analysis at fit time.
   - Both `jax.value_and_grad` sites (`:974` physical objective; `:1072` scaler/bijector stepped
     objective) go through `value_and_grad_from(..., mode)`.
   - The downstream code is unchanged: `_value_and_grad_finite`, the vmap at `:1089`, batching,
     `_broad_starts`, `value_and_grad_single=jax.jit(_value_and_grad)` at `:1256`.
   - The resolved mode is logged once at search start and recorded in the search's output metadata.
5. **Out of scope:** blackjax NUTS/SMC (they differentiate the log-density themselves; a later
   step), graphical/EP factor gradients, and changing any default other than `AnalysisPoint`'s.

**PyAutoLens**
6. `AnalysisPoint` (`autolens/point/model/analysis.py:36`): `gradient_mode = "forward"`, with a
   docstring citing autolens_profiling #327/#331. Users override per search with
   `af.MultiStartGradient(gradient_mode="reverse")`.

**Memory caveat (documented):** forward mode carries one tangent per free parameter, so under vmap
its memory scales with `n_starts × n_params`. This is why it is analysis-declared rather than
global. The `MultiStartGradient` docstring says so next to `batch_size`.

## Tests

- **PyAutoFit (`test_autofit/`):**
  - helper parity: forward ≡ reverse value and gradient on a toy JAX analysis (Gaussian model) at
    several vectors, rtol 1e-10;
  - `resolve_gradient_mode`: analysis default, override precedence, invalid value raises;
  - `Fitness.grad` honours the mode;
  - `MultiStartGradient` with `gradient_mode="forward"` vs `"reverse"` on the toy model with the same
    seed gives the same result to tolerance, including the scaler/bijector path;
  - invalid keyword raises at construction.
  - Existing `test_multi_start_gradient.py` stays green.
- **PyAutoLens (`test_autolens/point/`):**
  - `AnalysisPoint.gradient_mode == "forward"`;
  - forward ≡ reverse gradient of a `FitPositionsSourceSolved` likelihood through `Fitness`
    (registered model; non-zero, finite; PRNGKey sweep 0..15);
  - one short `MultiStartGradient` point-source fit that runs in forward mode end-to-end.
- Full PyAutoFit and PyAutoLens suites; GPU regression check on the RAL A100 (the multi-start
  point-source test in forward and reverse mode) before ship.

## Workspace follow-up (after the library PRs merge)

- autolens_profiling: `scripts/point_source_source/likelihood_breakdown/gradient_mode_library_ab.py`.
  It runs the *real* `MultiStartGradient` step on the phase-2c L5 and L24 rungs with
  `gradient_mode="forward"` vs `"reverse"`, on RAL gpu-node CPU + A100. It confirms the phase-2b/2c
  gain arrives through the library path. It also adds a campaign-note section.
- autolens_workspace: no script change needed, because the default flips inside `AnalysisPoint`.
  If a point-source gradient example exists, add a one-line comment on the new keyword.

## Execution

- Task `point-source-gradient-mode`; new Mind prompt `active/point_source_source_plane_phase_2d.md`.
  Issue on PyAutoFit, cross-referenced from PyAutoLens.
- Branch `feature/point-source-gradient-mode` in PyAutoFit, PyAutoLens and (later) autolens_profiling,
  under worktree `~/Code/PyAutoLabs-wt/point-source-gradient-mode`.
- **Parallel claims (approval requested with this plan):**
  - PyAutoLens is claimed by `workspace-config-cleanup` (its Lens PR is already merged, awaiting
    release) and by `pointsolver-mcs-headroom` (point solver). This phase touches only
    `autolens/point/model/analysis.py` plus a new test.
  - autolens_profiling is claimed by `pointsolver-mcs-headroom` and `interferometer-mesh-numba-p2`.
    The follow-up touches only a new cell, its results and the source-plane note.
  - PyAutoFit is unclaimed.
- Order: `/start_library` → implement (Opus subagent, progress file + Monitor) → `/ship_library`
  (PyAutoFit PR first, PyAutoLens PR depends on it) → `/start_workspace` for the profiling
  follow-up → `/ship_workspace`.
- Related: `jax-grad-nan-zero-components` (PyAutoGalaxy#631) is already fixing the NaN-at-zero
  gradients found in phase 2c, and is not touched here.

## Verification

- `pytest test_autofit` and `pytest test_autolens` green in the worktree. The new tests fail on
  unfixed main first (e.g. `AnalysisPoint.gradient_mode` missing).
- RAL A100: the point-source multi-start test in both modes, results identical to tolerance.
- The workspace follow-up rows show the forward-mode speed-up through `MultiStartGradient` itself.
