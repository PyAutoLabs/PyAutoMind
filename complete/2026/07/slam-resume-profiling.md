## slam-resume-profiling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/70 (closed)
- completed: 2026-07-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/75 (MERGED)
- summary: New pipeline_resume/ tier profiles the full 5-stage SLaM chain cold vs resume with per-component decomposition (runtime wrappers, no library edits) + instant cold path via PYAUTO_TEST_MODE=2 PYAUTO_TEST_MODE_SAMPLES=10000 (test-mode epic phase 3 folded in: size parity 10,000x21/8.81MB vs 9.07MB target, README recipe + deltas, reference benchmarks). VERDICT on #70: resume of a complete chain = 148s pure overhead, 85% recomputation (positions_likelihood_from 70s + adapt-image rebuild 55s; samples CSV load 0.5s) — checkpoint system REJECTED; two targeted load-not-recompute fixes filed as draft/feature/autogalaxy/slam_resume_fast_path_load_persisted_adapt.md. Gotchas: Nautilus default n_batch=100 OOMs 16GB (n_batch not an identifier field — tune freely); PyAutoFit test-mode bypass never writes .completed (bug filed draft/bug/autofit/, harness stopgap in place); chain crashed at source_pix[2] without workspace-parity disable_positions_lh_inversion_check (new config/general.yaml); test-mode resume must keep the same env vars (output/test_mode/ namespacing). Shipped through Heart RED on human ack (5 pre-existing reasons). Real-sampling partial outputs preserved locally under output/pipeline_resume/hst_fast.

## Original prompt

# SLaM resume overhead: profile inter-stage costs, judge speed-up vs checkpointing

Type: feature
Target: workspaces
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

It is common for a user to set off a lens model, get so far, and then resume that model. For SLaM pipelines,
this can take time if it has to do tasks between each stage, which makes doing the science slower.

First, can you extend autolens_profiling to have some testing and profiling code for this, its part of the
core run time and thus falls under profiling rather than hygeine (e.g. in the context of agent work).

Then, can you assess if it is slow, whether the best way forward is to try and speed it up or if it would
be feasily to build a checkpoing system, where resuming goes straight to the latest result to
resume? Normally this would be fine, the issue is that stuff like adapt images, which get passed through
the pipeline, would need to be carefully thought about so the resume has their data loaded from the right place.
This may make a full chckpointing system unnecessary complex. You judge.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ce78c7e9-3f34-4983-bb53-8840527c1fb6/scratchpad/intake_raw.md -->
