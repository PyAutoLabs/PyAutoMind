# Parked tasks

Tasks that were started or scoped but are not currently in flight. Listed
here so they remain visible across machines instead of disappearing into
unindexed worktrees or stashes. Move an entry back to `active.md` (or to
`planned.md` if re-scoping is needed) when work resumes; on shipping,
write the dated `complete/<YYYY>/<MM>/<slug>.md` record instead.

## group4-mge-search-benchmark
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/82
- prompt: active/research_profiling_experiment_in_the_autolens_pr.md
- parked: 2026-07-24 — code + first GPU results MERGED (PR #83); worktree/claim RELEASED
- remaining: gradient-family sweep (prodigy/lion/adabelief/prodigy_autoconv) + Nautilus anchor on laptop GPU (~/venv/PyAutoGPU, JAX_PLATFORM_NAME=cuda JAX_PLATFORMS=cuda,cpu XLA_PYTHON_CLIENT_MEM_FRACTION=0.5, --config-name local_gpu_fp64), then recovery/walltime aggregation. Warm output preserved in main checkout output/searches/.
- note: NEW PATHS (scripts/<dataset>/<task>/ restructure LANDED, autolens_profiling#84) — group4 cells now live at scripts/cluster/searches/<sampler>/mge.py (samplers: multi_start_prodigy, multi_start_lion, multi_start_adabelief, multi_start_prodigy_autoconv, nautilus); run them via the sweep driver scripts/misc/searches/sweep.py (e.g. `--only <sampler>/group/mge` — sweep still keys the group cell class internally, mapping it to scripts/cluster/ on disk). If compile still too heavy: dial _GROUP4_MGE_TOTAL_GAUSSIANS 10->6 and/or _MULTI_START_N_STARTS 64->32.

## matplotlib-inline-standalones
- prompt: active/matplotlib_inline_standalones.md
- parked: 2026-08-08 — surfaced by the orphaned-prompt triage; VERIFIED INCOMPLETE, not shipped
- classification: refactor (autolens_workspace + autogalaxy_workspace)
- remaining: the prompt calls for removing five standalone `# %matplotlib inline` comments.
  At least TWO survive on autolens_workspace main —
  `scripts/interferometer/features/advanced/potential_correction/start_here.py:36` and
  `scripts/imaging/features/advanced/potential_correction/start_here.py:56`.
  The autogalaxy_workspace half was not counted; do that first to confirm how many of the
  five are left.
- note: do NOT broaden into the old `pyprojroot` bootstrap sweep — the prompt is explicit
  that the dependent AutoCTI follow-up owns that.

## pyautoreduce-slacs1430-acs-comparison
- prompt: active/pyautoreduce_slacs1430_acs_comparison.md
- parked: 2026-08-08 — surfaced by the orphaned-prompt triage; STATE UNVERIFIED
- classification: test (PyAutoReduce + autolens_assistant)
- why unverified: the comparison targets a collaborator dataset at
  `/mnt/c/Users/Jammy/Science/subhalo/dataset/slacs/slacs1430+4105`, which this session cannot
  see. Confirm from the laptop whether the reduction and parity fits were ever run.
