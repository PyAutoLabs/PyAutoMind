# Active Tasks

## search-ext-a0b-hygiene
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1670
- issued: 2026-10-08
- prompt: active/search_extensibility_a0b_hygiene.md
- epic: search-extensibility (phase A0b)
- session: Claude CLI (Fable 5.1, /start_dev --auto); session ID unavailable
- status: library-shipped, awaiting-merge — PyAutoFit#1672 opened 2026-10-08 under --auto (tier judge → human /prm); A0a(ii) being implemented stacked on this branch
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1672
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1672
- retires-on-merge: draft/bug/autofit/drawer_crashes_under_nullpaths_timer_none.md (Drawer NullPaths fix is in #1672; close it as a record at /prm)
- validation: 3073 passed / 2 skipped / 3 xfailed; nojax emulation 915 passed; afW + afT search smoke all exit 0; review CLEAN; two reviewer items flagged in the PR body (search_dict_for instead of changing search_dict's shape; plot_search=False for the start-point plot)
- autonomy: --auto launch 2026-10-08; effective safe (refactor); Consequence judge → ends at PR-open, human /prm
- worktree: ~/Code/PyAutoLabs-wt/search-ext-a0b-hygiene
- repos:
  - PyAutoFit: feature/search-ext-a0b-hygiene (+ feature/search-ext-a0a2-backend-conformance stacked on it for the A0a(ii) PR)
- tier: judge (human /prm)
- heart-ack: STALE at launch (release validation incomplete: no rehearsal for current source)

## linear-solver-p4a-jacobi-a100-divergence
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/397
- issued: 2026-10-08
- session: Claude Code CLI (Fable 5.1), session 331e5f0e
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/linear-solver-p4a-jacobi-a100-divergence
- repos:
  - autolens_profiling: feature/linear-solver-p4a-jacobi-a100-divergence
