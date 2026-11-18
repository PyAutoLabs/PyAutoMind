## Summary

The batch claim gate no longer counts a prompt's `Target:` as a repo when the prompt declares `Repos:`. `declared_repos()` in `agents/conductors/batch/_batch.py` now returns the known repos from `Repos:` alone. It falls back to `Target:` and then to the survey repos only when `Repos:` names no known repo. The trigger was readiness ruling Q8 (2026-11-18): `results_library_p5c_dr1_census` (Repos: PyAutoCortex, Target: autofit) was held on a PyAutoFit claim. That ruling was answered with a coordination line, which can now stay or go.

- PR: https://github.com/PyAutoLabs/PyAutoBrain/pull/676 (merged 2026-11-18, tier notify, auto-merge on green)
- Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/675
- Tests: `tests/test_batch_declared_repos.py` (5); full suite 2370 passed, 1 skipped.
- Witness: held. A Cortex-only prompt is not held by a claim on its Target repo, a prompt naming the claimed repo is held, and a prompt without `Repos:` falls back to Target.
- Lesson: organ test files must not name instance repos (PyAutoFit etc.). The tenant-firewall lint in Brain CI rejects them; use organ names (PyAutoEyes, PyAutoCortex) in fixtures.

## Original prompt

# Batch claim gate counts a prompt's Target: as a repo even when Repos: is declared

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Issued: 2026-11-18
Consequence: notify
Witness: a new test in PyAutoBrain tests/ passes where `declared_repos` on a prompt with `Target: autofit` and a `Repos:` block naming only PyAutoCortex returns `["PyAutoCortex"]` and `_held_for` against an active.md claiming PyAutoFit returns None; a prompt with no `Repos:` still returns its Target; the full batch test suite passes
Review-minutes: 0
Unattended: ready
Lane: any

## Bug

`declared_repos()` (`agents/conductors/batch/_batch.py:119`) builds a prompt's repo
set from its `Repos:` header **and** its `Target:`, always unioned. `Target:` is
often only an epic grouping, not a repo the task edits. Example:
`draft/feature/autofit/results_library_p5c_dr1_census.md` has `Target: autofit`
but `Repos:` lists only PyAutoCortex (the census is read-only on RAL against the
released stack and writes one Cortex ledger line).

The claim gate (`_held_for`, called from `_ready.py:340` and
`_orchestrator.py:1604` / `:1628`) therefore treated the census as a PyAutoFit
task. The readiness pass `ready-2026-11-18` filed ruling Q8: "`results_library_p5c_dr1_census`
cannot start: repo PyAutoFit is claimed by `ep-projected-model-shared-prior`".
The human resolved it on 2026-11-18 by adding a coordination line to that claim
in `active.md`. That is a workaround; the false conflict recurs for any task
whose Target is an epic label.

## Fix

- When a prompt declares a `Repos:` header with at least one known repo, use it
  alone. Fall back to `Target:`, then the survey `repos`, only when `Repos:` is
  absent (or names no known repo).
- Check the other callers of `declared_repos` (batch grading, lanes, premise,
  `_orchestrator.py:1604`) still behave; `_premise.declared_repos` is a separate
  helper, confirm whether it has the same union.
- Regression test: a prompt with `Target: autofit` and `Repos: PyAutoCortex`
  is not held by a PyAutoFit claim; a prompt with no `Repos:` still falls back to
  its Target.
- Optional, once fixed: the Q8 coordination line on
  `ep-projected-model-shared-prior` in `active.md` becomes redundant; leave it
  (it is harmless and the claim clears when that task ships).

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b01cd956-03bd-4fd1-b437-0416381bb071/scratchpad/raw.md -->
