# Active Tasks

## notify-slack-community-discussions
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/408
- issued: 2026-09-20
- prompt: active/notify_slack_general_when_a_community_discussion.md
- session: Codex (session ID unavailable)
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/notify-slack-community-discussions
- repos:
  - PyAutoBrain: feature/community-slack-notifications
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/409
- pending-release: PyAutoBrain@https://github.com/PyAutoLabs/PyAutoBrain/pull/409
- heart-red-override: |
    2026-09-20 live user authorization: "yes override i authorize" for issue #408's documentation branch, permitting commit, push and PR-open only; recorded at https://github.com/PyAutoLabs/PyAutoBrain/issues/408#issuecomment-5750713819.
    Exact RED reason: "release validation FAILED (stage integrate)". Also YELLOW: "manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml".
    Branch gates: live Discussion #21 to Slack #general PASS; discussions-only feature list PASS; diff and generated-agent-surface checks PASS; docs review CLEAN. No runtime tests or downstream smoke apply. Merge, release and bypassing required checks remain unauthorized.
- resume: "GitHub Discussions → Slack #general is live and tested (issue #408). PR #409 is open with pending-release; judge current CI and merge only on a separate human /prm request. Heart RED development override applies to PR-open only."

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
