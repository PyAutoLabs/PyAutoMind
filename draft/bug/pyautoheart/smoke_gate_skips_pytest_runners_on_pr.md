# PyAutoHeart smoke-tests.yml relevance gate skips the pytest matrix on PRs that touch only tests/

Type: bug
Target: PyAutoHeart
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoHeart
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Witness: a euclid_strong_lens_modeling_pipeline PR touching only `tests/` shows `unit / smoke (3.12)` and `unit / smoke (3.13)` run and pass rather than `skipped`.
Filed: 2026-09-10

PyAutoHeart reusable smoke-tests.yml: the pull_request relevance gate (no_smoke_relevant_changes — only scripts/, config/, .github/, smoke_tests.txt, smoke_notebooks.txt count) also skips the whole matrix when the caller passes a pytest runner. euclid_strong_lens_modeling_pipeline's tests.yml calls smoke-tests.yml@main with runner .github/scripts/run_tests.py for its unit and slow jobs; PR #65 (2026-09-10) changed only catalogue/, workflow/ and tests/, so unit/smoke and slow/smoke were skipped on the PR, no test ran before merge, and both workflows still concluded success with the PR mergeable. PR #61, which touched scripts/ and config/, ran the full matrix. The gate is smoke-shaped but reused for pytest runners: a test-only or tests/-touching change must run the tests. Fix in PyAutoHeart .github/workflows/smoke-tests.yml: when runner is set (a non-smoke runner), widen the relevance set to tests/, pytest.ini and every path the repo's tests import (catalogue/, util.py, workflow/ — or simply everything except the docs-only set), or bypass the relevance gate for non-smoke runners entirely; keep the docs-only skip. Witness: a euclid PR touching only tests/ shows unit/smoke (3.12) and (3.13) run and pass.

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->
