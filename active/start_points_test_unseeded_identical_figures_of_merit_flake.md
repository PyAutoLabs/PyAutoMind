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
