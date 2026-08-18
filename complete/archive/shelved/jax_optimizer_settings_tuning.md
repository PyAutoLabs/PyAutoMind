# Tune the JAX multi-start optimizers into a standard option (MGE + Sersic)

Type: experiment
Target: autolens_profiling
Repos:
- @autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: retired (2026-08-18 — superseded by the 2026-08-17 inference programme; human-confirmed)

## Retirement (2026-08-18 — do NOT start dev on this prompt)

The 2026-08-17 human-approved inference programme (autolens_profiling#134,
`results/notes/inference/PROGRAMME.md` via PRs #136/#137) owns and reframes
this prompt's core question:

1. **The settings question is answered or redesigned.** Settled evidence
   (PROGRAMME §1.2) established that basin selection, not settings, is the
   discriminator for gradient MAP — Adam's p_hit ≈ 0.18/start is already
   measured, and the carried-forward multi-start engine is the lr-free
   **Prodigy**, which eliminates this prompt's `learning_rate` axis entirely
   (that was the point of the shipped lr-free-multi-start-optimizers task).
   The surviving knob, `n_starts`, is exactly programme **Phase 3**'s
   reliability-curve question (n_starts {16, 64, 256} × ≥5 seeds vs
   Nautilus/NSS budgets), and **Gate B** makes the "standard, recommended
   option" call this prompt wanted — including the fallback classification
   as a local/initialized optimizer. This prompt's `batch_size`-is-inert
   note is already programme canon.
2. **The harness gaps this prompt scoped are Phase 1's outputs.** Truth
   scoring / basin metrics and a stable (target, config, seed, hardware) →
   metrics axis are the Phase 1 targets registry + schema v2, superseding
   the ad-hoc settings-grid extension of `sweep.py` proposed here.
3. **The docs deliverable is programme §6** (evidence cards → future user
   guides feeding workspace defaults).

**Delta deliberately dropped (human decision, 2026-08-18):** the **Sersic
lens + Sersic source model case** (a new `sersic` model type for
`_setup.py` as a lower-complexity parametric rung) is NOT carried forward —
programme targets v1 registers only mge / delaunay / knn / delaunay_matern /
delaunay_nn / slam_source_pix, and that stands. Do not re-file it from this
record.

**Tracker:** this task's GitHub issue **autolens_profiling#69** was closed
as superseded on 2026-08-18 (human-confirmed), pointing at PROGRAMME.md
Phases 1/3 and this record.

Goal: make the JAX gradient MAP optimizers (`af.MultiStartAdam` /
`MultiStartADABelief` / `MultiStartLion`, PyAutoFit#1369/#1374) a **standard,
recommended option for autolens users** with an **MGE source**, and likely also
a **Sersic source**. Tune the settings that control convergence per model
complexity, against a **Nautilus baseline**, so the results can inform
**workspace settings and documentation**.

Use the **full first-class search** (`search.fit`) in `autolens_profiling/searches/`
— NOT `searches_minimal` (that tier is for prototypes that bypass
`NonLinearSearch`; these searches are mature).

## Model cases (increasing complexity)

1. **Sersic lens + Sersic source** (NEW `sersic` model type): `lp_linear.Sersic`
   lens bulge + Isothermal + ExternalShear + `lp_linear.SersicCore` source.
   Mirrors the simulator truth; linear amplitudes keep the comparison about
   model complexity rather than linear-vs-non-linear.
2. **MGE lens + MGE source** (existing `mge` cell, `multi_start_adam/imaging/mge`
   already registered).

Pixelized sources are explicitly **out of scope here** — they are
compile-pathological (see autolens_workspace_developer#100) and are their own
task.

## Settings array (the convergence knobs)

Sweep, per model case:

- `n_starts` — the population size; the core multi-start knob (e.g. 8/16/32/64/128)
- `n_steps` — iteration budget (e.g. 100/300/1000)
- `learning_rate` (e.g. 1e-3/1e-2/1e-1)

**`batch_size` is NOT a tuning knob** — it is numerically inert (proven on the
A100: identical results across {None,1,4,14,100}); it only bounds VRAM and is
set from the vram table.

## Baseline + scoring

- `af.Nautilus` on the identical model per case (JAX rows MUST set
  `force_x1_cpu=True` + `use_jax_vmap=True`, else `nautilus.Sampler` forks and
  corrupts JAX state).
- Score per run: **basin recovery** (`einstein_radius` vs truth **1.6**),
  max log likelihood **vs the Nautilus baseline's**, per-start basin hit rate,
  and wall time (compile vs sample).
- The harness's imaging truth (`simulators/imaging.py`): Isothermal
  einstein_radius=1.6, centre=(0,0), q=0.9/45deg; shear=(0.05,0.05); lens
  `Sersic` n=3 Re=0.6; source `SersicCore` q=0.8/60deg n=1 Re=0.1.

## What the harness lacks (build it)

- **No `sersic` model type** — `_setup.py` dispatches only mge / pixelization /
  delaunay / point-source.
- **No truth / correctness scoring** — the harness profiles *cost*, not whether
  a search found the right answer. A tuning campaign needs a truth constant and
  a basin metric.
- **No search-hyperparameter axis** — `sweep.py` sweeps
  `(sampler, dataset_class, model) x (CPU/GPU x fp64/mp)`. Tuning needs a
  settings-grid axis over `n_starts x n_steps x learning_rate`.
- Priors are already **broad uniform** by design ("the search scripts need the
  sampler to actually search a realistic prior volume so its convergence cost
  reflects production use") — correct for tuning; do not switch to
  truth-centred priors (those are only for FD probes).

## Deliverable

Optimal settings per model complexity (Sersic vs MGE), evidenced against
Nautilus, feeding the workspace defaults + the `searches.py` guide docs
(af.MultiStartAdam is already documented there config-only).

Cheap enough to sweep: the MGE benchmark ran 128 starts in ~50 s warm on an A100.

<!-- intaken 2026-07-15; human: full search not searches_minimal; sweep n_starts x n_steps x lr; Nautilus baseline per case -->
