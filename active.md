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

## untrack-fits-test-artifacts
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/494 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/untrack_generated_fits_test_artifacts.md
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/495 (pending-release)
- repos:
  - PyAutoArray: feature/untrack-fits-test-artifacts
- no-worktree: shipped from a web session (no local worktree, no gh; issue and PR
  driven through the GitHub MCP surface). The PyAutoArray clone lives at
  /home/user/pyautoarray on feature/untrack-fits-test-artifacts.
- summary: |
    Convert the six test_autoarray output_test writers to pytest tmp_path, then untrack
    and delete the 13 tracked FITS/dat artifacts. Audit found only 1 of the 13 is a live
    output (structures/arrays/files/array/output_test/array.fits, the file #483 flipped);
    the other 12 are orphans no test references. Also replaces the two file-by-file
    .gitignore lines with test_autoarray/**/output_test/ and drops a dead test_data_path
    fixture in dataset/imaging/test_dataset.py. Verify: clean checkout, suite twice in a
    row, git status clean after each. Siblings (PyAutoGalaxy/PyAutoLens) file separately.
