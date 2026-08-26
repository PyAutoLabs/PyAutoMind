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

## submit-wall-per-cell-throughput
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/176
- issued: 2026-08-26
- prompt: active/submit_wall_estimates_per_cell_throughput.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/log-det-multistart-tag
- repos:
  - autolens_profiling: feature/log-det-multistart-tag
- sole-owner-since: 2026-08-26 — log-det-multistart-tag (#175) SHIPPED (PR #178, merge commit
  11d06e50) and is recorded in complete/2026/08/. It branched off origin/main as
  feature/log-det-multistart-tag-175 and its files were restored, so this task now solely owns
  BOTH the worktree ~/Code/PyAutoLabs-wt/log-det-multistart-tag and the branch
  feature/log-det-multistart-tag. The shared-index commit discipline no longer applies —
  nothing else is uncommitted there.
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
    into lint.yml; phase8b --time -> 7:00:00 from its SLOWEST cell (6:00:00 was the pre-
    implementation estimate at 1.4x; the gate's floor for a `rates` row is 1.5x, which
    needs 22,185 s -- past six hours).

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
- parallel-claim: autolens_profiling is ALSO claimed by submit-wall-per-cell-throughput (#176).
  log-det-multistart-tag (#175) SHIPPED 2026-08-26 (PR #178) and no longer claims the repo.
  Human-approved 2026-08-26 to run in a SEPARATE worktree rather than fold or serialise — files
  are disjoint: #176 adds scripts/misc/wall/ and edits hpc/batch_gpu/submit_search_*,
  hpc/README.md, .github/workflows/lint.yml, test_wall_check_submits.py; THIS task edits
  scripts/misc/searches/{_metrics,aggregate}.py, scripts/misc/tooling/build_readme.py,
  scripts/misc/test/ and regenerates the root README.md. (#175 edited
  scripts/misc/searches/_samplers.py + README + test_searches_log_det_and_nautilus_seed.py —
  now on main, disjoint from both.) A separate checkout means a separate git index.
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
