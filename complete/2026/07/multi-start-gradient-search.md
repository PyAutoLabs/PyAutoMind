## multi-start-gradient-search
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1369 (closed)
- completed: 2026-07-14
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1370 (merged 63cd4e22, squash)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/43 (merged 0a81c457, squash)
- repos: PyAutoFit, autofit_workspace_test
- summary: Phase 1 of promoting the benchmark-winning multi-start gradient MAP optimizer to first-class PyAutoFit searches. AbstractMultiStartGradient(AbstractMLE) + af.MultiStartAdam/MultiStartADABelief/MultiStartLion (distinct class per optax rule, mirroring AbstractBFGS→BFGS/LBFGS): N broad multi-starts vmapped over the af.Fitness seam, fixed self-normalised optax step per start, best-basin MAP + per-start diagnostics via standard samples/result; optax added to the jax extra. Library unit tests numpy-only; JAX end-to-end truth-basin validation in autofit_workspace_test (scripts/searches/MultiStartAdam.py, recovers 1D Gaussian 50/25/10). --auto parked on Heart RED, resumed human-present after RED→YELLOW ack. Phases 2 (config/defaults) + 3 (workspace examples) not yet issued. See project_multi_start_gradient_search_promotion.

## Original prompt

# Multi-start gradient MAP search — core search + samples/result (Phase 1)

Type: feature
Target: PyAutoFit
Repos:
- @PyAutoFit
- @autofit_workspace_test
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Phase 1 of promoting the multi-start gradient MAP optimizer (benchmark winner,
autolens_workspace_developer PR#96+#98, Phase-3 complete) to first-class PyAutoFit
searches. This phase ships the core search machinery and the samples/result
contract; config/packaged-defaults and workspace examples are follow-up phases
(see "Follow-up phases" below) and must not be issued until this one nears
shipping.

## What to build

Add JAX/optax multi-start gradient MAP searches to PyAutoFit under
`autofit/non_linear/search/mle/multi_start_gradient/search.py`, mirroring the
existing `AbstractBFGS → BFGS/LBFGS` idiom in `mle/bfgs/search.py`:

- `class AbstractMultiStartGradient(AbstractMLE)` — owns the shared algorithm:
  N broad multi-starts on the **unconstrained** parameterization, a **batched
  (vmapped) value_and_grad** step over the standard `af.Fitness` seam, a fixed
  self-normalised optax update per start, best-basin tracking, and per-start
  basin diagnostics. The local optax rule and the start count `N` are
  first-class configurable knobs (`n_starts`, `n_steps`, `learning_rate`,
  broad-start bounds). Class attributes fix the optax factory + default lr.
- `class MultiStartAdam(AbstractMultiStartGradient)` — `optax.adam`, lr 1e-2
  (certified best).
- `class MultiStartADABelief(AbstractMultiStartGradient)` — `optax.adabelief`,
  lr 1e-2 (tied best).
- `class MultiStartLion(AbstractMultiStartGradient)` — `optax.lion`, lr 1e-3
  (sign-based → ~10× smaller lr; already in the reference `_OPT_FACTORY`).

Export `af.MultiStartAdam`, `af.MultiStartADABelief`, `af.MultiStartLion` in
`autofit/__init__.py` alongside `Drawer` / `BFGS` / `LBFGS`.

Return the best-basin MAP point **plus per-start basin diagnostics** through
PyAutoFit's standard search / `Samples` / `Result` contract (follow the
`samples_via_internal_from` pattern in `mle/bfgs/search.py`), with search-internal
save/resume.

## Port source (algorithm only — not the lens objective)

Port the *algorithm* from `autolens_workspace_developer/searches_minimal/`
`gpu_multi_start_adam.py` + `_grad_setup.py`: the unconstrained z-transform,
robust finite-gradient start generation, and batched `value_and_grad` N-start
loop. PyAutoFit **must not** import autoarray/autogalaxy/autolens — the reference
builds an autolens-specific MGE objective, but here the objective is the
library-agnostic seam that already exists:

- Objective: `af.Fitness(model, analysis, fom_is_log_likelihood=False)` — already
  exposes `_jit` / `_vmap` / `_grad` and honours `analysis._use_jax`. Use the
  vmapped path (`use_jax_vmap`) for the batched value_and_grad.
- Unconstrained transform: `model.vector_from_unit_vector(u, xp=jnp)` (already
  jax-traceable). Draw broad starts in unit space, keep only finite-gradient
  starts.

## Testing (JAX stays out of PyAutoFit unit tests)

Library unit tests are numpy-only: unit-test the non-JAX plumbing (start
generation / filtering, `Samples` construction, search-internal save/resume,
config parsing) with a simple/mocked objective. The real JAX/optax end-to-end
fit (recovers the truth basin on an imaging-style likelihood; cross-backend
parity) belongs in **autofit_workspace_test**, not `test_autofit/`.

`optax` becomes a runtime dependency for these searches (currently only `jax`
via `autoconf[jax]`); wire it into `pyproject.toml` and guard the import so a
non-jax install fails with a clear "install optax" message rather than at import
time.

## Out of scope (explicit)

Line-search / second-order methods (L-BFGS / BFGS / NCG / LM / Gauss-Newton) all
failed the benchmark on the NNLS-kinked objective — explicitly out of scope.

## Follow-up phases (do NOT issue yet)

- Phase 2 — config + packaged defaults: promote the optax rule / `N` / lr /
  step-count knobs to first-class packaged config defaults (mirror into autoconf
  packaged defaults) and any output/visualization config keys.
- Phase 3 — workspace examples (autofit_workspace): example running the search on
  an imaging lens fit, with Opus-authored tutorial prose.

<!-- Phase 1 split from feature/autofit/promote_the_multi_start_gradient_map_optimizer.md on 2026-07-14 -->
