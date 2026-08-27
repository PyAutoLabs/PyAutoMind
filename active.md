# Active Tasks

## transformed-message-factor-gradient-unpack
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1501 (issued 2026-08-19)
- issued: 2026-08-19
- prompt: active/16_transformed_message_factor_gradient_unpack.md
- status: HOLD — do not start dev. Fix-or-delete hangs off the PyAutoFit#1498 logpdf-contract
  decision (parked #1500 design bundle); dead code (zero production callers), crashes on first
  call if ever exercised.
- external: community PR https://github.com/PyAutoLabs/PyAutoFit/pull/1502 (@trexfr-ops) targets
  this exact unpack — review via /community before any local work; the #1498 adjudication decides
  whether the method should exist at all.
- registered: 2026-08-19 by the wake_up session — the issuing session (claude/autofit-priors-messages-audit-ylvenv)
  filed the prompt + issue but not this entry, tripping Lifecycle Drift on main.
- repos-none-claimed: this entry claims NO repos — one line deliberately, not 2-space bullets.

## xla-cpu-eigen-pool-deadlock
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1530 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/xla_cpu_eigen_pool_deadlock.md
- status: not started — research follow-up to the shipped jax-compile-stall epic
  (record complete/2026/08/jax-vmap-materialisation-hang.md, PyAutoFit#1528)
- repos-none-claimed: no worktree claimed; investigation is CI-driven via retime.yml
- why: #1528 shipped a WORKAROUND. Every JAX script in both test workspaces now runs
  single-threaded Eigen (~15% slower on the heaviest), and that flag is load-bearing —
  removing it silently brings back seven quarantines.
- the recoverable-cost question: if XLA's pool is merely mis-sized against the runner's
  cgroup quota rather than genuinely deadlocked, the fix is sizing it and the 15% comes back.

## rectangular-experiments-gut-stash
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/131 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/rectangular_experiments_gut_stash.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/rectangular-experiments-gut-stash
- repos:
- note: the prompt's `Repos:` header names PyAutoGut, but PyAutoGut is NOT modified —
  every condemned path is tracked and pushed, so the Gut's storage model calls for a
  pre-delete SHA in the catalog, not an `archive/condemned/*` payload ref. The second
  repo is PyAutoMind (the `condemned.md` entry).
- correction: the prompt's rename target (`RectangularAdapt{Density,Image}`) was deleted
  by PyAutoArray#461 (f9aceea3, 2026-08-21). Renames are date-checked per `git blame`
  against the 2026-07-23 consolidation — pre → `RectangularBilinearAdapt*`, post →
  `RectangularRTUAdapt*` — per the rule commit 08d5d86 wrote into the gradient README.
  `bandwidth=` is still live on the RTU meshes and is NOT dropped.
