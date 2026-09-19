# Active Tasks

## notify-slack-community-discussions
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/408
- issued: 2026-09-20
- prompt: active/notify_slack_general_when_a_community_discussion.md
- session: Codex (session ID unavailable)
- status: paused
- worktree: ~/Code/PyAutoLabs-wt/notify-slack-community-discussions
- repos:
  - PyAutoBrain: feature/community-slack-notifications
- resume: "Paused for the night at the human's request on 2026-09-20. Issue #408 is filed and the worktree is ready. `agents/conductors/community/AGENTS.md` has an uncommitted 49-line runbook draft; `git diff --check` passes. Resume from the live Slack audit: connect Slack access or run `/github subscribe list` and `/github subscribe list features` in `#general`, then configure `PyAutoLabs/.github discussions`, test one approved Discussion, record evidence, and ship. Progress comment: https://github.com/PyAutoLabs/PyAutoBrain/issues/408#issuecomment-5746092241"

## sersic-variants
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/74
- issued: 2026-09-12
- prompt: active/sersic_variants_prior_edge.md
- session: claude --resume session_01KTGhZacWuxrxYkXXWXJbBx
- status: paused
- worktree: ~/Code/PyAutoLabs-wt/sersic-variants
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sersic-variants
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/75
- note: "PR #75 was closed unmerged at the maintainer's request on 2026-09-18. The feature branch, issue #74, prompt and worktree are retained for possible later recovery or selective reuse. Its previous overlap with sed-chain-cpu-route is no longer live because PR #70 merged the CPU-route change."
- summary: |
    --variant for the Sersic stage: four variants (baseline, wide_n,
    central_noise, sersic_point) on the same 100 euclid_sersics core lenses, to
    explain the lens-light Sersic index pile-up at the n = 5 prior edge. The
    inline model block in fit_sersic is extracted into a pure sersic_model_from
    helper; variant=None stays byte-for-byte today's behaviour and any other
    variant writes to unique_tag sersic_lens_model_<variant>. util gains a pure
    Gaussian noise-inflation helper (A = 9, sigma = 0.17") plus a keyword-only
    noise_inflation on load_vis_dataset, and parse_fit_args(with_variant=True).
    New hpc/batch_cpu/submit_sersic_variants runs the four variants sequentially
    inside one array task per lens, because all four restore the same vis_lp zip
    and PyAutoFit's restore() deletes it. Science-clone submit and the analysis
    script (PR 2) are follow-ups.

## sersic-variants-analysis
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/76
- issued: 2026-09-12
- prompt: active/sersic_variants_analysis.md
- session: https://claude.ai/code/session_01LfJojDFow4pxPzuwRHqMt2 (web-github resume 2026-09-17; planned 2026-09-12 in session_01KTGhZacWuxrxYkXXWXJbBx)
- status: workspace-dev
- worktree: n/a — web-github session clone (/home/user/euclid_strong_lens_modeling_pipeline); the local ~/Code/PyAutoLabs-wt/sersic-variants-analysis worktree named on 2026-09-12 never pushed feature/sersic-variants-analysis, so the branch of record is the session's
- repos:
  - euclid_strong_lens_modeling_pipeline: claude/sersic-variants-analysis-3iqibr
- resume: "IMPLEMENTED 2026-09-17 (web-github; Fable planned, Opus executed): claude/sersic-variants-analysis-3iqibr pushed at 480c107 — scripts/analysis/{sersic_variants.py,README.md,__init__.py}, tests/test_sersic_variants_analysis.py (8 tests), one config/build/no_run.yaml entry. Verified locally: the new tests + test_repo_invariants + test_compare_catalogues, 26 passed; the rest of the fast suite needs astropy/autolens (absent in the container) — CI runs it. FLAGGED on issue #76 comment 5715176814: the W1-W4 thresholds are transcribed into the module's WITNESSES constant (plan page rev 3 unreachable from the session) and need the human's confirmation. NEXT = /ship_workspace (PR) then /prm; nothing here imports --variant, so PR #75's merge order is not a gate."
- note: "The earlier conflict survey named sed-chain-cpu-route PR #70 and sersic-variants PR #75. PR #70 merged on 2026-09-18 and PR #75 was closed unmerged at the maintainer's request; neither branch's file set intersects this task, which adds only scripts/analysis/**, tests/test_sersic_variants_analysis.py and one config/build/no_run.yaml entry."
- summary: |
    PR 2 of the euclid_sersics variants work: scripts/analysis/sersic_variants.py
    reads the four lens_sersic_<variant>.csv scrapes that PR #75's --variant
    produces and emits the per-variant comparison production needs - N, median n,
    fractions above 4.5/4.9/9.5 (and 5.0 for wide_n), paired dn and dR_eff against
    baseline with 16-84 % bands, June-vs-baseline dn from sample/lens_map.csv, and
    the four witness readings W1-W4 printed as numbers beside their pre-registered
    thresholds, never as a verdict word. Four-panel shared-bin histogram PNG plus a
    markdown report. Pure functions split from the CLI; a synthetic four-CSV
    fixture with a variant missing two tiles pins the inner join and its reporting.

## oneshot-benchmark-harness
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/126
- issued: 2026-09-17
- prompt: active/oneshot_benchmark_harness.md
- session: claude --resume session_01YTzjiXh2fLocc6dNqLQ66d
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/380
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/127
- autonomy: supervised (header; launched on the human's "Go / continue" in-session — plan on the issue, shipped to PR-open 2026-09-17, merge is human; Brain PR first, it is the assistant PR's `Brain-ref:`)
- location: web-github (session clones /home/user/autolens_assistant + /home/user/PyAutoBrain, no task worktree)
- worktree: n/a — web-github session clones
- repos:
- note: "PyAutoBrain PR #380 and autolens_assistant PR #127 merged; issue #126 is closed. Both repo claims are released. The entry remains active only for the first real headless runs noted below; do not fully close it as part of codex-hook-parity."
- summary: |
    One-shot, machine-scored assistant benchmarks: headless `benchmark.py run`
    (harnesses.yaml adapters, private workdir without benchmarks/truth, compute
    shims), computed-score contract (common gates × card metrics → score.json,
    RESULTS.md medians), prompt freeze (prompt_sha256 + VERSIONS.lock), first
    one-shot card `oneshot-smoke`, 2026-07 cards retired to prompts/conversational/,
    Brain clone VALIDATION_PLAN/partition update. Cards
    benchmark_positions_initialised_inference / benchmark_forward_model_consistency
    stay in draft/, Blocked-by this task. Real headless runs need a laptop with
    the agents installed — the human's first step after merge.
