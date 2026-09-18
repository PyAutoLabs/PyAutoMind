# The reusable smoke workflow's relevance gate skips the `unit` / `slow` pytest jobs on every pipeline PR that does not touch `scripts/` — three PRs merged with zero tests run

Type: bug
Target: pyautoheart
Repos:
- PyAutoHeart
- euclid_strong_lens_modeling_pipeline
Themes:
- ci
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: A euclid_strong_lens_modeling_pipeline PR touching only `util.py` or `tests/` shows `unit / smoke` and `slow / smoke` run (not skipped) on both Python legs; every other caller passing `runner:` is audited and listed in the PR; the CI-map doc says a skipped required job on a PR is not green.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-16
Updated: 2026-09-16

## Finding

Found 2026-09-16 while running `/prm` on `euclid_strong_lens_modeling_pipeline` PR #79.

`PyAutoHeart/.github/workflows/smoke-tests.yml` has a `changes` job whose
`no_smoke_relevant_changes` gate (pull_request only) sets true unless a changed path
matches `scripts/*|config/*|smoke_tests.txt|smoke_notebooks.txt|.github/*`; the `smoke`
job is skipped when it is true.

That path list is right for the smoke runner, but the pipeline's
`.github/workflows/tests.yml` reuses the same workflow with
`runner: .github/scripts/run_tests.py` for its `unit` (`pytest -m "not slow"`) and
`slow` (`pytest -m slow`) jobs — and the gate is inherited unchanged. A PR that changes
`util.py`, `tests/`, `catalogue/` or any root `.py` therefore runs NO pytest on the PR:
the `unit / smoke` and `slow / smoke` legs show `skipped`, `mergeStateStatus` is `CLEAN`,
and the PR looks green.

## Evidence

- PRs #71 (ce4cebb), #72 (46b55eb), #73 (56afea0) — all touching `util.py` and/or
  `tests/` — merged with `unit / smoke` and `slow / smoke` skipped on every leg.
- #75 (81f3139) ran only because it also touched `scripts/sersic_lens_model.py`.
- PR #79 (39faca8: `util.py`, `tests/`, `catalogue/README.md`) — same skip.
- The push-to-main run then runs the full matrix: main's Tests run 34677820679 on
  a363f57 (the merge of #73) is a FAILURE — the first time those tests ran was after
  the merge.

## Fix ask

- When the caller passes a non-default `runner` (or a new boolean input such as
  `skip-relevance-gate: true`, or an input `relevant-paths:` glob list), the `changes`
  job must not apply the smoke path filter. Pytest relevance is at least `**/*.py`,
  `tests/**`, `pytest.ini`, `pyproject.toml`, `config/**`, `.github/**`; simplest is to
  run the matrix unconditionally whenever `runner` is set (keep the docs-only skip).
- Update `euclid_strong_lens_modeling_pipeline/.github/workflows/tests.yml` to pass the
  input.
- Audit every other caller of the reusable workflow that passes `runner:` (e.g.
  `autolens_workspace_test` `retime.yml`) for the same inheritance.
- Add the check to the PyAutoHeart CI-map doc / the `ci_status` reading so `skipped` on
  a required workflow on a PR is surfaced rather than reading as green.

## Related

- The `unit`/`slow` split rationale in the pipeline's `tests.yml` header.
- Heart's own comment in the gate explains why pushes to main always run the full
  matrix (readiness reads main's conclusion).

## Folded 2026-09-17

`draft/bug/pyautoheart/smoke_gate_skips_pytest_runners_on_pr.md` (filed 2026-09-10
from pipeline PR #65) was the same defect with less evidence and was removed at
the witness-campaign close-out (PyAutoMind#398). Its witness — a
euclid_strong_lens_modeling_pipeline PR touching only `tests/` shows
`unit / smoke (3.12)` and `unit / smoke (3.13)` run and pass rather than `skipped` —
is this prompt's witness in other words.
