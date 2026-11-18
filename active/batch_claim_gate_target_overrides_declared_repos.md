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
