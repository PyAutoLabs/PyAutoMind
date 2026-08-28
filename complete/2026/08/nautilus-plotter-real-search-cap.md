## nautilus-plotter-real-search-cap
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/149
- completed: 2026-08-28
- workspace-pr: autofit_workspace#150 (merged b2550a13 -> main)
- pair: workspace half of `nautilus-test-mode-degenerate-corner` (PyAutoFit#1542, issue PyAutoFit#1541) — record `complete/2026/08/nautilus-test-mode-degenerate-corner.md`. Merged behind the library-first gate: PyAutoFit#1542 read MERGED before this PR was merged. **Both tasks were formalised from ONE prompt file** (`nautilus_plotter_py_corner_cornerpy_raises_value.md`), which `lifecycle.py record` folded into the library record; it is reproduced verbatim below so this record stands alone.
- what shipped: `scripts/plot/nautilus_plotter.py` declares `ENV: real_search` in its `__Env__ (Developer Only)` section — the runner releases `PYAUTO_TEST_MODE` for this one script — and caps the search with an explicit `n_like_max=3000` on `af.Nautilus`, the same lever other workspace examples use. `notebooks/plot/nautilus_plotter.ipynb` regenerated (`generate.py` strips the `__Env__` section).
- why not a library-wide fix: a plot example needs a real posterior. Raising the global test-mode sampler budget in PyAutoFit would have fixed it too, but the human declined — it slows every release-wave search. So the library got the ESS guard (crash -> logged skip) and the one script that genuinely needs samples opts out of test mode.
- calibration (release profile, `output/` wiped between runs — the numbers, not a guess): 300 / 500 / 1000 calls still crash, Nautilus still exploring, `N_eff = 1`; 2000 renders no corner (`N_eff = 3`); 2500 renders but at `N_eff` 13-20; **3000 gives `N_eff` 357-527 in 22-26 s, 3/3 stable** — the chosen value; natural finish is 3500 calls / 35 s.
- validation: exit 0 under `profile_release.yaml` with the corner figure rendered, 3/3 runs. Control: `emcee_plotter.py` still runs under test mode, exit 0. Env resolution checked directly — `PYAUTO_TEST_MODE` absent for this script, still `1` for its siblings, so `real_search` is scoped to the one script and did not leak.
- heart context: corrective PR for the Heart RED reason `release validation FAILED (stage integrate)`, run 33177898708, job `integrate / run_scripts (3.12, autofit, plot)`.

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
