## slam-resume-fastpath
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/502 (closed)
- completed: 2026-07-17
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/504 (MERGED, first), https://github.com/PyAutoLabs/PyAutoLens/pull/619 (MERGED, second — imports _append_to_search_zip from ag)
- summary: SLaM resume fast-path implementing the #70 judgment — cache-aside keyed on the upstream result's own paths: galaxy_name_image_dict_via_result_from memoizes the raw per-galaxy dict to files/galaxy_images_{model,snr}.fits; positions_likelihood_from memoizes solved positions to files/multiple_image_positions[_plane_<z>].json; threshold math stays live; zero public-API/script change; first-arrival computes+writes, staleness guarded by search identifiers, NullPaths always computes. Validated via pipeline_resume instant recipe: inter-stage resume 151s/130s/128s -> 0.3s/0.0s/0.1s (remaining floor = imports + stage-1 check_likelihood_function compile). Suites 985p/387p; six-workspace smoke 44p/0f/5s, zero tracebacks (2026-07-09's 3 known failures did not reproduce). Gotchas: paths.restore() wipes post-completion files/ writes — caches MUST be appended into the search .zip (_append_to_search_zip; future public home in PyAutoFit paths is a candidate); the viz-gated fits_adapt_images artifact was NOT relied on (only written when plots.yaml enables it). Shipped through Heart RED on human ack (5 pre-existing reasons). Mechanical ship + smoke delegated to Sonnet subagents per WORKFLOW.md.

## Original prompt

# SLaM resume fast-path: load persisted adapt images and positions likelihood

Type: feature
Target: autogalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up implementing the judgment of autolens_profiling#70 (measurement + decomposition there,
2026-07-17 comment): resuming a fully-complete 5-stage SLaM chain costs ~148s of pure overhead on a
laptop-scale dataset, of which ~85% is inter-stage recomputation — `positions_likelihood_from` (70s)
and adapt-image reconstruction from the upstream result (55s), each paying a fresh JAX compile +
inversion/point-solve per resume. Samples loading is <1%. A checkpoint system was ruled out; these
two targeted fixes were recommended instead.

1. **Adapt images disk-first.** Every stage already persists the adapt images it consumed into its
   own `files/` (@PyAutoGalaxy `AnalysisDataset.save_attributes`), and
   `autogalaxy/aggregator/agg_util.adapt_images_from` already reconstructs `AdaptImages` from that
   artifact. Add a load-from-disk path so a resumed stage composes its analysis from its own saved
   `files/adapt_images` when present, instead of rebuilding the upstream result's max-LH fit
   (`galaxy_name_image_dict_via_result_from`). Design care: first arrival at an incomplete stage
   must still compute; only re-arrivals (artifact present) take the shortcut. Opt-out knob if the
   upstream result changed (identifier mismatch invalidates the whole downstream chain anyway, so
   staleness is structurally guarded — state this in the docstring).

2. **Persist + reload the positions likelihood.** @PyAutoLens `positions_likelihood_from` re-runs
   the point solver from the upstream tracer on every resume. The resulting object is small and
   serializable — save it into the consuming stage's `files/` at composition time and load it when
   present, same first-arrival semantics as (1).

Validation: the `pipeline_resume` tier in @autolens_profiling (instant recipe:
`PYAUTO_TEST_MODE=2 PYAUTO_TEST_MODE_SAMPLES=10000 python3 pipeline_resume/slam_resume.py`) gives
before/after resume decompositions in ~3 minutes; target is the ~125s recomputation bucket going to
~0 on re-arrival. Workspace follow-through: `slam_start_here.py` should exercise the fast path
unchanged (the loaders slot beneath the existing calls, no API change to the guide script) — confirm
and note in the guide only if a flag surfaces.

<!-- formalised by the Intake (Conception) Agent on 2026-07-17 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ce78c7e9-3f34-4983-bb53-8840527c1fb6/scratchpad/intake_resume_fastpath.md -->
