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
