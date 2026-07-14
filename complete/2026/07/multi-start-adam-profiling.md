## multi-start-adam-profiling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/67 (closed)
- completed: 2026-07-14
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/68 (merged e703d894, squash)
- repos: autolens_profiling
- summary: Registered af.MultiStartAdam (Fit#1369) as a first-class profiling sampler in autolens_profiling/searches/, scoped to imaging/mge (benchmark-proven MAP cell). build_multi_start_adam + SAMPLER_BUILDERS row + multi_start_adam/imaging/mge.py cell + sweep.py CELLS entry; made n_live sampler-aware (null for MAP optimizers) + _sampler_config_dict records n_starts/n_steps. Add+register only (no profiling run — A100 sweep is the profiling agent's job). Also reconciled pre-existing simulators/README.md build_readme drift (gate-required). --auto-style ship, Heart YELLOW acked (set unchanged). Scope was user-chosen imaging/mge-only. Completes the multi-start gradient search promotion's profiling leg. See project_multi_start_gradient_search_promotion.
