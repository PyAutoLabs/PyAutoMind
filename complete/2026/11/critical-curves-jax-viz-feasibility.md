## Outcome

Research for the critical-curves campaign (Pulse task `critical_curves_jax_modeling_viz_feasibility`; human decision 2026-11-06). PR #522 merged 2026-11-09 (6ca73ad0) under the live human's Heart-RED development override and `/prm`.

**Verdict:** keep `marching_squares` as the modeling-run critical-curve default at every scale. No library or default change.

| Family | Zero-contour tangential | MS s/figure | ZC s/figure (production) | ZC warm |
|---|---|---|---|---|
| imaging/hst | 66/66 pass | 0.26–0.30 | 6.2–14.4 | 0.30–0.58 |
| interferometer/sma | duplicate paths (10/16) | 2.1–2.9 | 7.4–14.4 | 0.18–0.37 |
| group/euclid | MGE 22/22; Delaunay/rectangular 35/44 no curve (±3″ seeds) | 3.0–3.7 | 9–21 | 0.84 (MGE) |
| cluster/simple | 0/44 (seeds; path length) | 0.11–0.13 | 16–22 | 0.27–0.38 |

- Zero-contour recompiles every figure, because a fresh `LensCalc` closure captures the tracer. Caching would only help interferometer and group.
- A coarse 0.2″ marching-squares count plus closure check flags 47/47 zero-contour failures (2 false alarms in 150).
- Production cluster figures miss small member-galaxy curves.

**Evidence:**
- RAL 414456: 17 legs, `ral`, exclusive, 8 CPU, fp64, on a private library checkout at the 2026.11.6.1 mains.
- Corpus: `scripts/lens/critical_curves/viz_feasibility_legs.json`.
- Rows and summary: `results/lens/critical_curves/viz_feasibility/`.
- Wiki: `wiki/campaigns/lens/critical_curves/critical_curves.md`.
- Harness: `scripts/lens/critical_curves/modeling_viz_feasibility{,_scales}.py`.

Laptop pilots ran marching squares about 4× slower than RAL; the RAL numbers are the record.

**Follow-ups (drafts):**
- `draft/refactor/autogalaxy/zero_contour_pytree_compile_cache.md`
- `draft/research/autolens_profiling/critical_curve_oracle_find_the_regime_where.md`
- `draft/docs/autogalaxy/plot_utils_critical_curves_default_docstring_drift.md`
- `draft/research/autolens/cluster_figure_critical_curves_miss_member_curves.md`
- `draft/research/autolens_profiling/visualization_run_time_campaign_measure_and_opti.md`

Side fix shipped in the same session: autolens_profiling#523 / PR #524 (lint drift after PyAutoArray#682).

## Original prompt

# Feasibility: JAX zero-contour critical curves/caustics for modeling-run visualization

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- critical-curves
- visualization
- jax
Difficulty: medium
Priority: medium
Consequence: judge
Campaign: critical-curves
Pulse: organs/PyAutoPulse/tasks/critical_curves_jax_modeling_viz_feasibility.md
Filed: 2026-11-06
Issued: 2026-11-06
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/521

Thin Mind record for the dev claim; Pulse owns the intent. The full question,
evidence and phase plan are in the Pulse task above.

Original request (verbatim): "the Pulse task organs/PyAutoPulse/tasks/critical_curves_jax_modeling_viz_feasibility.md — feasibility of the JAX zero-contour engine for critical curves/caustics in modeling-run visualization (critical-curves campaign; human decision 2026-11-06). Research only, no default change. Use the phase-4 posterior draws from completed autolens_inference legs (galaxy/group first; multi_galaxy/datacube legs still running, see autolens_inference#59)."

Human ruling 2026-11-06: run in parallel with gradient-correctness-sweep (#517)
despite its autolens_profiling claim — this task only adds new files under
scripts/lens/critical_curves/ and the critical-curves wiki.
