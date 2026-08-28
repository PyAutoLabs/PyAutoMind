## nautilus-test-mode-degenerate-corner
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1541
- completed: 2026-08-28
- library-pr: PyAutoFit#1542 (merged 8ebcbcbc -> main)
- pair: workspace half is `nautilus-plotter-real-search-cap` (autofit_workspace#150, issue autofit_workspace#149) — record `complete/2026/08/nautilus-plotter-real-search-cap.md`. Both tasks were formalised from THIS one prompt file, which is folded below; the workspace record cross-links back here.
- what shipped: `autofit.plot.corner_cornerpy` now skips — through the existing `logger.info` path, no try/except, no silent guard — when the Kish effective sample size `sum(w)**2/sum(w**2)` is <= the number of parameters, alongside the pre-existing row-count check. New private helper `autofit.non_linear.plot.samples_plotters._effective_sample_size(weight_list, sample_count)`. No signature changes; kwargs forwarding unchanged; test-mode sampler behaviour unchanged.
- root cause (the interesting part): the samples were NOT empty. Under `PYAUTO_TEST_MODE=1` Nautilus stops after its initial batch holding 100 unique rows but exactly ONE non-zero weight (ESS = 1). Since `8cdcff3a0` correctly forwards `weights=` and caller kwargs to corner, the script's `range=0.999` became a *weighted* quantile over that single point and collapsed to a sliver that excluded every row — corner then raised `ValueError: ... 'range' is not valid or the sample is empty`. The old guard counted rows, so it saw 100 and passed. **The degeneracy was in the weights, not the sample count** — that is why the ESS test is the right guard and a row count can never be.
- rejected first revision: the first cut also raised the *global* test-mode sampler budget so Nautilus would produce a usable posterior everywhere. The human declined — it would slow every search in every release wave. Reverted; the single failing script opts out instead (workspace half).
- validation: `pytest test_autofit` green; new tests in `test_autofit/non_linear/plot/test_samples_plotters.py` cover the ESS helper, a weight-degenerate 100x3 sample with caller `range=np.ones(3)*0.999` (asserts the logged skip AND that `corner.corner` is never called), and a uniform-weights control (asserts it IS called).
- heart context: corrective PR for the Heart RED reason `release validation FAILED (stage integrate)` — job `integrate / run_scripts (3.12, autofit, plot)`, run 33177898708, failing after 3.1s.
- prompt premise falsified (side-finding, worth its own prompt): the prompt asserted this "did NOT fail under smoke" and reasoned from there that the bug was release-profile specific. It is not — `plot/` scripts are not listed in `autofit_workspace/smoke_tests.txt` at all, so smoke never ran the script. A "passed under smoke" line means nothing until you have checked the script is in the smoke list.

## Original prompt

# nautilus_plotter.py corner_cornerpy raises ValueError "range is not valid or the sample…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-08-28

Found 2026-08-28 by PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33177898708, job
`integrate / run_scripts (3.12, autofit, plot)`, env profile
`profile_release.yaml`. Failed after 3.1s.

`autofit_workspace/scripts/plot/nautilus_plotter.py` fails; the sibling
`emcee_plotter.py` passed (8.3s) in the same job, and `dynesty_plotter.py`,
`get_dist.py`, `zeus_plotter.py` are skipped, so nautilus is the only live
failure in that directory.

## Traceback tail

Preceded by three warnings that are themselves the tell — the sample handed to
corner is degenerate before corner ever rejects it:

    scipy/stats/_kde.py:588: RuntimeWarning: Degrees of freedom <= 0 for slice
      self._data_covariance = atleast_2d(cov(self.dataset, rowvar=1,
    numpy/lib/_function_base_impl.py:2901: RuntimeWarning: divide by zero encountered in divide
      c *= np.true_divide(1, fact)
    corner/core.py:922: UserWarning: Attempting to set identical low and high ylims
      makes transformation singular; automatically expanding.

then:

    Traceback (most recent call last):
      File ".../workspace/scripts/plot/nautilus_plotter.py", line 106, in <module>
        aplt.corner_cornerpy(
      File ".../autofit/non_linear/plot/plot_util.py", line 112, in wrapper
        return func(*args, **kwargs)
      File ".../autofit/non_linear/plot/samples_plotters.py", line 80, in corner_cornerpy
        corner.corner(data=data, **settings)
      File ".../corner/corner.py", line 248, in corner
        return corner_impl(
      File ".../corner/core.py", line 370, in corner_impl
        hist2d(
      File ".../corner/core.py", line 687, in hist2d
        raise ValueError(
    ValueError: It looks like the provided 'range' is not valid or the sample is empty.

## It did NOT fail under smoke

This did not reproduce in the same day's Workspace Smoke run
(https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33179766004). So it may
well be **release-profile specific**: the release profile runs the sampler for
real rather than in the truncated smoke configuration, so the Nautilus samples
object the plotter is handed differs between the two profiles. Establish which
profile produces which sample shape before assuming a plotting bug.

## What to investigate

- Reproduce under `profile_release.yaml` (not smoke) with the workspace CWD.
- Determine what `data` actually is at `samples_plotters.py:80` — empty,
  single-row, or zero-variance in one or more parameters. The `Degrees of
  freedom <= 0` KDE warning points at a sample with <= 1 effective row for at
  least one slice.
- Then decide the locus: is the Nautilus samples -> corner data conversion in
  PyAutoFit dropping or collapsing samples, or is the workspace script asking
  for a corner plot of a search result that legitimately has too few samples
  under this profile?

## Out of scope

Do not fix this by try/excepting the plot call, by skipping the script, or by
adding a silent "if the sample is empty, return" guard. If the sample really is
degenerate, the fix is upstream of the plot.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/682229dd-73ea-488e-8436-f7a3e9ef00e7/scratchpad/bug2.txt -->
