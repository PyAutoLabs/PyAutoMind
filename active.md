# Active Tasks

## hst-mge-pilot-qualification
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/417
- issued: 2026-10-13
- session: Codex; session ID unavailable
- status: workspace-shipped, awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/418
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/hst-mge-pilot-qualification
- next: Review and merge #418; independently validated witness implementation, coefficient tolerances and production collection remain separate pending work.
- repos:
  - autolens_profiling: feature/hst-mge-pilot-qualification

## search-ext-b5a-wave2
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/8
- issued: 2026-10-14
- prompt: active/search_ext_b5a_freeze_and_scored_wave2.md
- session: Claude Code CLI (Fable 5.1); session 51fca711; launched --auto
- status: merged (compute complete on RAL, unpulled — B5b pending)
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b5a-wave2
- epic: search-extensibility
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/9
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/63
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/29
- compute: RAL `ral` jobs 408244/408245 (references), 408246 (probe), 408346/408347 (reference builds), 408348/408365/408366/408367 (scored arrays, 11,750 runs, %60 throttle); all 1,629 array tasks COMPLETED by 2026-10-15 morning, nothing pulled yet; freeze sha 72d6faaf, PyAutoFit pin df6d218f1 (A4 merge, unreleased) + PyAutoNerves 7f3055b7 in /mnt/ral/jnightin/autofit_inference/.pyauto_pin/ (zeus-mcmc 2.5.4 in .pyauto_pin/site); RAL clone at f0b3eef (f9605cf state.md-only commit not pulled there); dry-run copy /mnt/ral/jnightin/autofit_inference_b5a_dryrun/ can be deleted
- next: B5b: pull all RAL rows, build the JAX blend realisation-1 reference locally (pilot seeds 0+2 plus RAL seed 1), set probe-first timeouts from probe 408246 and submit the remaining 980 runs of those cells, judge under @2, catalogue, export the wave-2 summary, refresh the Insight snapshot and run `cortex done` on the run lines; carried to B5b: re-judging the pilot's @1 JAX blend rows against the new reference is a reassessment needing an explicit decision; LBFGS on blend numpy still returns +inf at the pin; PRs autofit_inference#9 (merge commit 3463aa190, freeze 72d6faaf reachable from main), PyAutoCortex#63, PyAutoInsight#29 merged 2026-10-15
- repos:
  - autofit_inference: feature/search-ext-b5a-wave2
  - PyAutoInsight: feature/search-ext-b5a-wave2
  - PyAutoCortex: feature/search-ext-b5a-wave2
