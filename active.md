# Active Tasks

## wide-sersic-default
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/96
- issued: 2026-09-20
- prompt: active/wide_sersic_default.md
- session: Codex (session ID unavailable)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/wide-sersic-default
- resume: "Pipeline commit a4e6466 made under the live Heart RED development override; formal review CLEAN. Next: push feature/wide-sersic-default and open the pending-release PR. Merge and release remain separately gated."
- heart-red-override: |
    Live user replied "I authorize" on 2026-09-20 to the task-specific Heart RED development override request for euclid_strong_lens_modeling_pipeline#96.
    Authorization and evidence: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/96#issuecomment-5749918493
    Exact current RED reason: release validation FAILED (stage integrate)
    Also YELLOW: manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml
    Passed branch gates: both scripts compile; installed model probe lens 0.5–10.0/source 0.8–5.0; repository invariants 12/12; Euclid smoke 9/9; git diff --check; formal review CLEAN at a4e6466.
    Scope: development commit, push and pending-release PR only; no merge, release or CI bypass.
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/wide-sersic-default

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
