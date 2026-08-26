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

## log-det-multistart-tag
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/175
- issued: 2026-08-26
- session: claude --resume session_01MdmS2jfUPi8BNjtDVBjBYX
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/log-det-multistart-tag
- prompt: active/log_det_method_missing_from_multistart_tag.md
- shares-worktree-with: submit-wall-per-cell-throughput (#176) — folded in 2026-08-26,
  human-approved; disjoint files. COMMIT DISCIPLINE: never `git add -A` in this worktree,
  explicit pathspecs only, or one task's uncommitted work lands in the other's commit.
- repos:
  - autolens_profiling: feature/log-det-multistart-tag
- summary: |
    Reproduced on clean main: multi_start_unique_tag returns an identical tag for
    cholesky and slogdet arms, so the second resumes the first's .completed fit
    (RAL job 340576: 20 delaunay arms -> 10 output dirs). Fix is a PATH SUFFIX in
    autolens_profiling only -- tag on the SEARCHES_LOG_DET_METHOD env override
    only, never on the W8-resolved default, so an unset env keeps today's exact
    tag. No PyAutoFit change, no PyAutoFit worktree. Next: /start_workspace.

## submit-wall-per-cell-throughput
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/176
- issued: 2026-08-26
- prompt: active/submit_wall_estimates_per_cell_throughput.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/log-det-multistart-tag
- repos:
  - autolens_profiling: feature/log-det-multistart-tag
- shares-worktree-with: log-det-multistart-tag (#175) — this task does NOT own a worktree of its
  own. It was blocked by #175's claim on autolens_profiling and folded into it on 2026-08-26 with
  human approval, because the two touch DISJOINT files: #175 edits scripts/misc/searches/_samplers.py
  (+ its README and test); this task adds scripts/misc/wall/ and edits hpc/batch_gpu/submit_search_*,
  hpc/README.md, .github/workflows/lint.yml, scripts/misc/test/test_wall_check_submits.py.
  COMMIT DISCIPLINE: never `git add -A` there — explicit pathspecs only.
- summary: |
    RAL job 340576 lost 35 of 39 arms (an overnight A100 block) because
    submit_phase8b_bijector_a100 justified --time=0:30:00 with an MGE step rate for an array
    whose arms are mostly knn and delaunay_adapt_split. Measured 2026-08-25: mge 0.117 s/step,
    knn 2.23 (19x), delaunay_adapt_split 4.83 (41x) -- "6x headroom" was ~8x short for knn,
    ~16x short for delaunay. Those rates are recorded NOWHERE in the repo and only 11 of 82
    submits state any wall basis. Fix: scripts/misc/wall/rates.py (curated per-cell table
    mirroring vram/config.py; lookup RAISES on an unmeasured cell, no nearest-neighbour
    fallback), a `# WALL-BASIS:` header required on submit_search_*/submit_phase8b_*,
    check_submits.py gating every cell a submit runs against its own row + its --time, wired
    into lint.yml; phase8b --time -> 6:00:00 from its SLOWEST cell.
