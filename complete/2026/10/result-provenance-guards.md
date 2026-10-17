# result-provenance-guards

Completed: 2026-10-17
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/303
PR: https://github.com/PyAutoLabs/PyAutoHeart/pull/307

Collectors reject foreign result shards with diagnostics; analyze fails closed before aggregation. The reusable smoke workflow rejects tracked validation output. Tests cover traversal, sibling prefixes, symlink escapes, invalid counts, and tracked versus untracked reports.

## Verification and merge

User /prm authorized the merge. GitHub confirmed MERGED; git merge-base --is-ancestor proves the shipped head is in origin/main. Only PyAutoHeart has a claimed implementation branch; no sibling implementation remains. Both Python 3.12 and 3.13 jobs passed on the exact shipped head in https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/39057220045, including the tenant firewall. No skipped test legs. Issue closed as completed.

Published Heart at shipping was STALE because source moved since release rehearsal; this development merge does not assert release readiness. Live weekly cloud sweep remains unverified where applicable.

## Close-out notes

Original task worktrees are absent from this session; no worktree or data was deleted.

Review-log classification remains unconfirmed: the human-action question was unanswered. The merged heads match the shipped heads; no shadow row or human confirmation is invented.

## Original prompt

# release-integrate: analyze-side foreign-path filter and a workspace-repo lint for tracked result files

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: A planted `*__script.json` carrying a foreign path is excluded from the analyze/collector results with a warning naming the shard and the path (test), and a planted tracked `test-results/` file fails the workspace lint (test); both tests live in `PyAutoHeart/tests`.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-11

The remainder of `complete/2026/09/release-integrate-discard-stale-result-files.md`,
which shipped option 1 of the three guards the original prompt offered
(PyAutoHeart#225: every shard now deletes any result file the workspace checkout
carries before the runner starts, and warns per file). Two defence-in-depth
layers were left open and are re-filed here so the dashboard does not offer the
shipped prompt as backlog:

1. **Analyze-side path filter.** In the analyze/collector path
   (`heart/validate.py` rglob over `*.json`; `heart/checks/test_run.py` and
   `script_timing.py` glob `*__script.json`), drop or flag any result entry whose
   `file` path is not under the runner workspace (does not start with
   `$GITHUB_WORKSPACE`, or starts with a home directory such as `/home/<user>`),
   and log a loud warning naming the shard and the foreign path. This catches a
   leak that arrives by any route the pre-run discard does not see (a result
   written under a different name, or a future runner that changes the layout).
2. **Workspace-repo lint.** A Heart required workflow, or a check in the workspace
   CI, that fails when `test-results/` or any `*__script.json` / `smoke_timings.json`
   is tracked in git — so the leak is refused at the workspace PR rather than
   laundered at the release.

Tests in `PyAutoHeart/tests` for each layer, using a fixture that plants a stale
`*__script.json` carrying a foreign path and asserts it is excluded and warned
about (layer 1), and a planted tracked result file that the lint rejects (layer 2).

Background: nightly Release Integrate runs 34323573912 (2026-09-09) and
34449490363 (2026-09-10) failed at Stage 3 on three stale `jax_likelihood`
failures that autolens_workspace_test#311 had committed by accident; awt#313
removed them and the 2026-09-11 nightly went green. See the record above for
the trap that cost a CI round (the tenant firewall reads test modules).

## Reconciliation — 2026-10-01

Keep open — this is deliberately unshipped remainder. GitHub confirms [PR #225](https://github.com/PyAutoLabs/PyAutoHeart/pull/225) merged on 2026-09-11; `complete/2026/09/release-integrate-discard-stale-result-files.md` explicitly says only the pre-run deletion shipped and re-files the two other guards here. Heart origin/main `ff7003f` still reads JSON in `heart/validate.py`, `heart/checks/test_run.py`, and `heart/checks/script_timing.py` without the requested foreign-result-path warning/filter. The earlier record's phrase “Scope shipped vs filed” describes the parent task, not completion of this remainder.

Issued: 2026-10-17
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/303
