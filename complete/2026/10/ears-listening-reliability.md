## ears-listening-reliability

- issue: https://github.com/PyAutoLabs/PyAutoEars/issues/4
- completed: 2026-10-03
- library-pr: https://github.com/PyAutoLabs/PyAutoEars/pull/5
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/457

## Shipped

Human `Prm` authorized both merges. Ears#5 merged d28beb9de131d99aeb93c76f1ef3502797fed36e; Brain#457 merged 5598a952d08034803dd505e5e046669d9104d524. Exact heads verified, all five applicable CI jobs successful, both PRs confirmed merged. Issue Ears#4 closed completed.

Discussion comments and each reply connection are paginated with fixed read-only GraphQL queries. Failures, caps, missing/deleted actors and ambiguous ordering preserve unknown coverage. REST fallback cannot erase gaps. Snapshot v1 unchanged; accepted answers establish response settlement only, never delivery. Brain triage now distinguishes bug reproduction, scientific assumptions/data/inference, proposals and broadcasts; bounded reads report their limits.

Validation: Ears 43 tests and snapshot/state smoke passed; independent collector review CLEAN. Brain full run 1123 pass/42 absent-Cortex skips, then all 47 Cortex tests passed with dependency present (1165 unique tests covered). Exact-head CI: Ears run37136522430 browser/Python3.12/3.13; Brain run37136524869 Python3.12/3.13, all success.

Production witness: Ears board run37137496430 succeeded from merge d28beb9. Published snapshot generated 2026-10-03T16:37:04.144623+00:00 contains 13 conversations. All readable source receipts, including the Discussion hub, are complete; only Jammy2211/euclid_assistant remains unavailable (permissions/rate limit/endpoint not further distinguished). Post-merge Ears tests run37137496436 also passed. Restricted tokens/proxies remain explicitly partial. Heart remains RED for release; no release performed. Phases4–6 remain unissued; next is assistant distribution of /feedback.

Source claims released by lifecycle close; dashboard regenerated with this record. Standalone source clones retained; no task worktree to remove. No timer or waiter outlives this turn.

## Original prompt

# Trustworthy listening and category-sensitive triage

Type: feature
Target: PyAutoEars
Difficulty: large
Autonomy: supervised
Priority: high
Consequence: judge
Epic: community-organ-birth
Filed: 2026-10-03
Issued: 2026-10-03
Issue: https://github.com/PyAutoLabs/PyAutoEars/issues/4

Original request: "Continue" after organ integration and live deployment.
Accepted scope: community-organ-birth phase 3; existing whole-task development authorization continues.

@PyAutoEars owns bounded read-only evidence collection. Paginate Discussion comments and replies with the documented GraphQL read connections, retaining REST fallback as explicitly partial when GraphQL is unavailable. Preserve public verification, no raw-body publication and safe rendering. Detect deleted/malformed activity rather than silently interpreting missing actors as no response owed. Preserve oldest unanswered coverage beyond 30 conversations and paginated PR review/reply coverage. Accepted proposals settle response obligation only, never claim delivery.

@PyAutoBrain owns category-sensitive triage: bug reproduction, scientific assumptions/data/inference, proposal use case/outcome. Do not ask all scientific questions for tracebacks. Preserve human approval for outward replies and existing commands. Any truncated/failed triage activity must be explicit.

Validation: multi-page discussion comments/replies; null/deleted actors; cursor failures/budgets; partial GraphQL responses; REST fallback; >30 items/oldest item; PR review replies; multiple maintainers; response age independent of updated_at; accepted proposals/broadcast; empty success vs inaccessible; malicious HTML. Existing Ears and Brain suites, state contract and applicable CI. No new scheduling, billing, source, reply, release or merge authorization. Tier: judge — merge mode: human /prm.

## PR-open handoff

Ears PR#5 (`66260ab874bb08e49ec4ae4c675c3f34479c8919`) and Brain PR#457
(`cd72445267db89d42713786e8dc5a30c285087fd`) are open; neither merged.
Ears 43 tests pass; state/snapshot smoke valid; independent collector review CLEAN.
Brain full run 1123 pass/42 absent-Cortex skips; then 47/47 Cortex tests passed
with dependency fetched (1165 unique tests covered). Focused community 27 pass.
Logs: /tmp/ears-brain-tests.log and /tmp/ears-cortex-tests.log. Source clones:
/tmp/ears-reliability; clean feature commits have identical published Git trees.

Discussion read capability is bounded and honest: GraphQL errors or restricted
tokens/proxies retain partial REST fallback. No production GraphQL witness yet;
existing Pages workflow provides it after merge. Exact-head CI supplies browser
tests. Next action: human /prm with green checks, then phase4 distribution.

Existing whole-programme authorization continued with "Continue". Heart remains
RED for release; exact previously reported reasons:

- release validation FAILED (stage integrate)
- PyAutoHeart/workflows/Release Integrate: failure
- PyAutoArray/Tests: red
- PyAutoArray/Tests: red
- PyAutoFit/Tests: red
- autofit_workspace_test/Smoke Tests: red
- autogalaxy_workspace_test/Smoke Tests: red
- autolens_workspace_test/Smoke Tests: red
- CI wall-clock: 26 gates · slowest PyAutoBrain Nightly Release 83m · 1 slowed · 6 hang events
- Release readiness: release validation FAILED (stage integrate)
- PyAutoCTI/test_autocti/extract/two_d/parallel/test_parallel_fpr.py::test__estimate_capture: red
- PyAutoNerves/test_autonerves/test_fitsable.py::test__output_to_fits: red
- Unit-test timing: 3 test regressions (>3× baseline), 1 slow (>1.5×)
- autolens_test: red
- Release validation: NOT release_ready — v2026.10.3.1.dev79901 profile=release (2026-10-03T07:43:31+00:00)
- validation_report/stages/integrate: fail
- autolens_assistant: red
- autolens_profiling: red
- autolens_workspace_test: red
- Worktree drift: 0 orphan / 0 missing / 4 dirty
- euclid_strong_lens_modeling_pipeline: red
