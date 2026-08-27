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
- status: awaiting-merge — PR open, MERGE BLOCKED by Heart RED
- pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/132 (opened 2026-08-27, label pending-release)
- blocked-by: Heart RED `release validation FAILED (stage integrate)`. PR opened under the
  human-authorized corrective-PR exception naming that exact reason (push + PR-open only).
  Merge is NOT authorized under RED — resume with /prm once Heart clears.
- worktree: ~/Code/PyAutoLabs-wt/rectangular-experiments-gut-stash
- repos:
  - autolens_workspace_developer: feature/rectangular-experiments-gut-stash
- note: the prompt's `Repos:` header names PyAutoGut, but PyAutoGut is NOT modified —
  every condemned path is tracked and pushed, so the Gut's storage model calls for a
  pre-delete SHA in the catalog, not an `archive/condemned/*` payload ref. The second
  repo is PyAutoMind (the `condemned.md` entry).
- correction: the prompt's rename target (`RectangularAdapt{Density,Image}`) was deleted
  by PyAutoArray#461 (f9aceea3, 2026-08-21). Renames are date-checked per `git blame`
  against the 2026-07-23 consolidation — pre → `RectangularBilinearAdapt*`, post →
  `RectangularRTUAdapt*` — per the rule commit 08d5d86 wrote into the gradient README.
  `bandwidth=` is still live on the RTU meshes and is NOT dropped.

## numba-cpu-mge-batch-convolve-cache
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/496
- issued: 2026-08-27
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/numba-cpu-mge-batch-convolve-cache
- repos:
  - PyAutoArray: feature/numba-cpu-mge-batch-convolve-cache
  - PyAutoGalaxy: feature/numba-cpu-mge-batch-convolve-cache
- note: epic numba-cpu-likelihood phase 1. Plan on the issue. Item 4 (pair-loop hoist + mirror) approved
  by user 2026-08-27 after the per-pixel-noise-map check; strict bit-identity NOT required (ulp-level BLAS
  ordering in the mirrored half accepted, pins at rtol 1e-6 are the guard).

## pages-dashboard-publish-gap
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/361 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/pages_dashboard_publish_gap.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/pages-dashboard-publish-gap
- repos:
  - PyAutoMind: feature/pages-dashboard-publish-gap
- parallel-claim: PyAutoMind is also claimed by organ-remote-block-and-uv-hook-repair
  (#360). worktree_check_conflict fires at REPO granularity; the human approved an OWN
  worktree on 2026-08-27 because the file sets are disjoint — #360 touches
  policy/remote_sessions.md, policy/session_start_hook.sh, scripts/session_bootstrap.sh
  and the AGENTS.md marker blocks; this task touches
  .github/workflows/dashboard_refresh.yml and nothing else. Separate worktree = separate
  index AND separate branch, so neither task can inherit the other's commits. Deliberate
  override, not a missed guard.
- note: touches `.github/workflows/dashboard_refresh.yml` ONLY. Disjoint from
  rectangular-experiments-gut-stash, which touches PyAutoMind's `condemned.md` —
  no worktree conflict (worktree_check_conflict clean).
- why: the published board can strand indefinitely while `dashboard.html` on main is
  correct; the nightly cron takes the same early-return path, so nothing heals it.

## organ-remote-block-and-uv-hook-repair
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/360 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/session_fixes_reach_only_two_organs.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/organ-remote-block-and-uv-hook-repair
- repos:
  - PyAutoMind: feature/organ-remote-block-and-uv-hook-repair
  - PyAutoBrain: feature/organ-remote-block-and-uv-hook-repair
  - PyAutoHeart: feature/organ-remote-block-and-uv-hook-repair
  - PyAutoHands: feature/organ-remote-block-and-uv-hook-repair
- scope-note: PyAutoBrain is claimed though the prompt omits it — it carries a generated
  hook copy that goes stale the moment policy/session_start_hook.sh changes, and
  firewall_gate.yml checks it out. The prompt's "all four organs" was written from a
  session that could see two.
- deliberately-out-of-scope: the other 30 repos carrying a stale hook copy (no gate sees
  them; firewall_gate.yml checks out four). Filed as
  draft/maintenance/organs/session_hook_reaches_only_four_of_thirty_four_repos.md
- co-claims PyAutoMind with pages-dashboard-publish-gap (#361), registered by a concurrent
  session after this task's worktree_check_conflict ran clean. Disjoint file sets — that
  task touches `.github/workflows/dashboard_refresh.yml` only; this one touches
  `scripts/`, `policy/`, `tests/` and the generated `.claude/hooks/` copies. Separate
  worktrees, no serialisation needed.

