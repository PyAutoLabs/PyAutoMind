# HowToLens stored results phase 2: Chapters 3, 4 and the optional chapter

Type: docs
Target: HowToLens
Repos:
- PyAutoGalaxy
- PyAutoNerves
- HowToFit
- HowToGalaxy
- HowToLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: `python .github/scripts/stored_results.py check`, extended to Chapters 3, 4 and the optional chapter, passes in HowToLens CI against the released libraries: no search in those chapters samples.
Review-minutes: 25
Unattended: needs-slicing
Lane: ral

Phase 2 of the HowTo stored-results epic (phase 1 = HowToLens#130, PR HowToLens#134: Chapter 2, tooling, CI job). Start after #134 merges; the tooling lives there.

## Searches to store (survey 2026-11-06, re-survey at start)
- Chapter 3 Tutorial 6 adaptive reconstruction: `search_1_mge`, `search_2_adaptive_delaunay` (pixelized source; likely the most expensive in the series).
- Chapter 4: tutorial_1_extra_galaxies (noise_scaling, model), tutorial_2_multi_galaxy (reads `result.samples` for a corner plot), tutorial_3_scaling_relation, tutorial_4_group_scale (3 searches incl. NFW halo and scaling relation), tutorial_5_cluster_scale, tutorial_6_weak_lensing.
- Optional chapter: tutorial_searches (Nautilus slow/fast, Prodigy, Zeus, Emcee: several read `result.samples`), tutorial_prior_passing (2 chained searches).

## Lessons from phase 1 (apply up front)
- Run every search for real (test mode off) before storing; the Chapter 2 rewrite had never been, and 3 of its settings failed: n_live=21 crashed Nautilus (LinAlgError), n_live=75 stalled and n_live=200 sometimes reached a poor solution. Nautilus's `n_points_min` default is n_dim + 50.
- Check every stored fit's log evidence against the lesson it must show (a good fit vs a deliberate failure); seed searches (`seed=1`) and confirm with a second seed before storing.
- The search `name` is not in the identifier, so seeded probe runs can be harvested under the tutorial names.
- `harvest` keeps only valid elliptical components (bug filed: draft/bug/autogalaxy/searches_score_elliptical_components_with_magnit.md).
- Set `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` for JAX CPU runs (jaxlib 0.11.2 deadlock, PyAutoNerves#213).
- RAL compute nodes have no rsync or tar; run as a proper `hpc/sync` campaign (scheduler actions logged), not raw sbatch. Laptop for pilots only.
- Extend `stored_results.py` (CHECKED_TUTORIALS, CORNER_PLOT_SAMPLES) and the tutorial prose the same way as Chapter 2; regenerate notebooks.

## Then
Phase 3: HowToFit and HowToGalaxy (their own stored_results tooling + CI job).

<!-- formalised by the Intake (Conception) Agent on 2026-11-11 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5ee98b5f-b187-4b0a-83a9-3ad898ce13b8/scratchpad/howto_phase2.md -->
