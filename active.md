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

## results-schema-comparability-guard
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/177
- issued: 2026-08-26
- session: claude --resume session_017xgYipoxfBkbU9nJ1yS8tt
- status: workspace-dev
- classification-correction: filed as library-dev; corrected 2026-08-26. WORKFLOW.md lists
  autolens_profiling on NEITHER the library nor the workspace repo list — it is a project repo
  of scripts + results with no installable source, so /start_workspace + /ship_workspace
  ("scripts, notebooks and configs only") is the right door. Matches how the sibling #176 was
  classified in the same repo.
- worktree: ~/Code/PyAutoLabs-wt/results-schema-comparability-guard
- prompt: active/results_schema_version_comparison_guard.md
- sole-claimant-since: 2026-08-26 — this task now solely claims autolens_profiling. Both
  siblings from the job-340576 post-mortem have SHIPPED: log-det-multistart-tag (#175) in
  PR #178, submit-wall-per-cell-throughput (#176) in PR #179 (merge b4b30ee0), each recorded
  in complete/2026/08/. The earlier human-approved parallel-worktree arrangement no longer
  applies — nothing else holds a checkout of this repo.
- inherited-gate: #176 added `scripts/misc/wall/check_submits.py --check` to lint.yml. THIS
  task edits scripts/misc/tooling/build_readme.py and regenerates the root README.md, so its
  PR now runs that gate too. It is inert for this task's diff (it reads hpc/ submits only),
  but a red wall-check on this PR would be real, not noise.
- repos:
  - autolens_profiling: feature/results-schema-comparability-guard
- summary: |
    REPRODUCED. performance.likelihood_evals changed MEANING between results-schema v1 and v2
    for MultiStart* searches: v1 = samples.total_samples (storage count), v2 = total_steps *
    n_starts (reject-inclusive). One cell dir in the phase4-stage2-harvest tree,
    results/searches/multi_start_prodigy_autoconv/imaging/mge/hst, holds both arms with
    differing config_name, so nothing dedupes them: positions-OFF v1 reads 257 evals /
    874.58 ms-per-eval, positions-ON v2 reads 247,808 / 2.23 ms. aggregate.py's comparison.json
    + shared log-scale comparison.png and build_readme.py's searches table render them side by
    side, implying a ~390x per-eval speedup that is pure counter semantics.
    TWO FINDINGS shaping the fix: (1) the break is MultiStart-ONLY — a nested sampler's
    total_samples was already reject-inclusive in v1, verified live on main where
    nautilus/imaging/pixelization/hst holds a legitimate v1=58,464 beside v2=55,984, so the
    prompt's literal "refuse when schema_version differs" guard would false-positive there;
    guard keys on eval-counter BASIS from (schema_version, sampler family), missing key = v1.
    (2) v1's likelihood_evals IS v2's stored_samples (both 257) — the bridge that lets a v1
    MultiStart row render honestly instead of as a wrong eval count.
    Also: _metrics.py::load_summary (the v1->v2 normaliser from W4/#161) has ZERO callers —
    built for this job, never wired in. max_log_likelihood / log_evidence / raw wall stay
    comparable and must NOT be suppressed. OPEN: merge order vs PR #174, whose harvest data
    this guard fires on by design.
