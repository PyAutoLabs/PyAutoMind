# Seed start-point tests

- completed: 2026-10-25
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1719
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1723
- merge-commit: 9994c4490a1a4e3387e9824c1a3fa1805b9fa6f4
- authorization: human /prm on 2026-10-25; merged unchanged at the checked head
- validation: every head workflow/job passed (Python 3.12, Python 3.13, no-JAX; applicable docs); combined serial suite 3913 passed, 1 skipped, 1 xfailed; four branches merge cleanly; model identifier parity passed
- limitation: downstream workspace smoke was not run; the gap was disclosed before the human merge command and remains recorded, not reported as a pass
- release: not performed; preserve pending-release until a published release is verified

## Outcome

Seed start-point tests. The implementation and regression tests are in the linked PR. Test-only #1723 was merged first to remove the known random start-point flake. Its three witness tests passed 200 repetitions each (600 passes). The source changes preserve representative output identifiers. Initial parallel unit failures reproduced the existing shared-output collision task; acceptance used serial combined validation and current-head GitHub CI.

## Close-out

All branch heads are ancestors of origin/main. No source changes were made during /prm. Issues closed as completed; prompts moved through lifecycle.py. The three declared glance tasks record stage-1 merged-unchanged shadow rows from the observed head equality; no independent-adversary evidence is claimed.

## Original prompt

# test_start_points.py draws unseeded start points and flakes on IDENTICAL_FIGURES_OF_MERIT (nojax leg, PyAutoFit#1714)

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- ci
- samplers
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: `pytest test_autofit/non_linear/search/test_start_points.py -q -p no:randomly --count 200` (or a 200-iteration shell loop) passes every time; the three tests draw their points from a seeded generator (or a fitness whose figures of merit cannot coincide), and no `InitializerException` can arise from the draw.
Review-minutes: 2
Unattended: ready
Filed: 2026-10-23

## Why

On PyAutoFit PR #1714 (run 39976190947, `unittest-nojax` leg) `test_plot_false_skips_the_plot`
failed with `autofit.exc.InitializerException: The initial samples all have the same figure of
merit` while the 3.12 and 3.13 legs of the same sha passed and main's nojax leg was green an hour
earlier (run 39970496109). The PR touches only the EP evidence readout; the test does not reach it.

`_search_and_fitness` builds `af.Emcee()` with `af.Model(af.ex.Gaussian)` on `data = np.ones(10)`
and calls `search.start_points(model, fitness, n=2)`. `InitializerBall.samples_from_model` draws
from `np.random.default_rng()` when no `rng` is passed (`autofit/non_linear/initializer.py:104`) and
raises when `np.allclose(fom[0], fom[1:])` (`:214`). With `n=2` on flat data two random draws land
on near-identical log likelihoods often enough to flake. Locally the test passed 3/3 under a nojax
emulation on the PR head.

## Ask

- Seed the draws in these tests (pass `rng=np.random.default_rng(0)` through `start_points`, or set
  the search's seed) so the tests are deterministic, or use a fitness whose figures of merit cannot
  coincide for distinct points.
- Check the sibling tests in the file (`test_plots_the_first_point_once`,
  `test_initializer_gets_the_effective_core_count`) for the same unseeded draw.
- Consider whether `IDENTICAL_FIGURES_OF_MERIT` at `n == 2` should use a tolerance tighter than
  `np.allclose` defaults, or require `n >= 3`, in the library itself — report, do not change, unless
  trivially safe.

## Lineage

- PyAutoFit#1714 — the PR whose nojax leg flaked (log excerpt in the issue #1713 comment of 2026-10-23)
- search-extensibility A2 — the `start_points` entry point the test covers

Issued: 2026-10-25
