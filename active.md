# Active Tasks

## complete-archive-highlights
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/368
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/371
- prompt: active/complete_archive_wiki.md
- issued: 2026-08-29
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/mind-workflow
- repos:
  - PyAutoMind: feature/complete-archive-highlights

## session-hook-long-tail
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/369
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/372
- prompt: active/session_hook_reaches_only_four_of_thirty_four_repos.md
- issued: 2026-08-29
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/mind-workflow
- repos:
  - PyAutoMind: feature/session-hook-long-tail

## repos-sync-config-checks
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/370
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/373
- prompt: active/repos-sync-config-stamper.md
- issued: 2026-08-29
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/mind-workflow
- repos:
  - PyAutoMind: feature/repos-sync-config-checks

## nautilus-serial-bound-training
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1547
- prompt: active/nautilus_serial_bound_training.md
- issued: 2026-08-29
- session: claude --resume ede55346-4e08-4851-b2b8-d9a21a49b776
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1548
- worktree: ~/Code/PyAutoLabs-wt/nautilus-serial-bound-training
- classification: library (PyAutoFit only)
- repos:
  - PyAutoFit: feature/nautilus-serial-bound-training

## log-likelihood-ceiling-default-off
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1549
- prompt: active/log_likelihood_ceiling_default_off.md
- issued: 2026-08-29
- status: library-shipped, awaiting-merge
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1550
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/198
- ci: both GREEN — PyAutoFit#1550 docs-build + unittest 3.12 + 3.13 + unittest-nojax all pass; autolens_profiling#198 lint pass
- next-skill: /prm (both PRs green and awaiting the human's merge; Heart YELLOW below is unacknowledged)
- heart-yellow: NOT acknowledged by a human in this session — surfaced verbatim for sign-off before merge. `workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)`; stale: `release validation incomplete: no rehearsal for current source`. Both unrelated to this change; PR-open only, nothing merged.
- worktree: ~/Code/PyAutoLabs-wt/log-likelihood-ceiling-default-off
- classification: library (PyAutoFit) + config-only follow-up (autolens_profiling)
- parallel-claim: PyAutoFit is also claimed by `nautilus-serial-bound-training` (awaiting-merge, PR #1548). File sets are disjoint - that branch touches only `nautilus/search.py` + its test; this one touches `fitness.py`, `nss/search.py`, the two `general.yaml` config files and the ceiling tests. Human-approved parallel worktree, own branch, own index.
- repos:
  - PyAutoFit: feature/log-likelihood-ceiling-default-off
  - autolens_profiling: feature/log-likelihood-ceiling-default-off
